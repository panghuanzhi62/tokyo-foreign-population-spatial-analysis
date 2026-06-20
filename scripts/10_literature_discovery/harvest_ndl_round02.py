#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 02 NDL-only metadata harvester (Tokyo-China opportunity-risk project).

Standard-library only. Queries the NDL Search (National Diet Library) OpenSearch
metadata API to assemble a PRELIMINARY Japanese-language candidate list of
books, reports, theses, institutional records, and official/public materials for
the Tokyo-China opportunity-risk mismatch project. Japanese queries are read
from the Round 02 query file so the source of truth stays in one place.

This script deliberately does NOT:
  - download PDFs or any full text
  - scrape NDL HTML pages
  - scrape Google Scholar
  - use browser automation
  - use paid APIs
  - store, print, or commit any API key or credential
  - assert any final research gap

The NDL Search OpenSearch API is a public metadata API. Only bibliographic
metadata (title, author/creator, publisher, year, identifiers, stable URL) is
parsed and stored. NDL OpenSearch exposes a free-word "any" search field; this
is the closest metadata-supported mode to the CiNii OpenSearch "q" parameter and
is used here. No full text is retrieved. Records that look like official data,
government reports, municipal policy, statistics, hazard maps, or
administrative-service materials are routed to official_source_registry.csv
rather than the academic tracking CSV. Every classification produced here is
PRELIMINARY metadata triage and MUST be verified manually (title/abstract
translation + record check) before any gap claim is made. Current status: gap
under verification.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

USER_AGENT = "TokyoChinaLitDiscovery/Round02 (academic metadata discovery; stdlib urllib)"
HTTP_TIMEOUT = 15  # seconds; short so a blocked network fails fast
# NDL Search OpenSearch metadata endpoints (public). Try the current host first,
# then the legacy host. Metadata only; no HTML scraping.
NDL_OPENSEARCH_ENDPOINTS = [
    "https://ndlsearch.ndl.go.jp/api/opensearch",
    "https://iss.ndl.go.jp/api/opensearch",
]

QUERY_FILE_REL = Path("literature") / "03_notes" / "round02_japanese_search_queries.md"
TRACKING_CSV_REL = Path("literature") / "02_matrices" / "round02_japanese_source_tracking.csv"
REGISTRY_CSV_REL = Path("literature") / "02_matrices" / "official_source_registry.csv"

# Academic tracking CSV schema (must match the existing header exactly).
TRACKING_COLUMNS = [
    "source_id", "query_id", "source_type", "search_platform",
    "original_title", "english_working_title", "author_or_institution",
    "year", "doi", "stable_url", "publisher_or_host", "language",
    "document_type", "study_area", "population_group", "core_topic",
    "method_or_data_type", "verified_status", "overlap_category",
    "matrix_destination", "translation_needed", "manual_check_needed", "notes",
]

# Official-source registry schema (must match the existing header exactly).
REGISTRY_COLUMNS = [
    "source_id", "institution", "source_title", "english_working_title",
    "year", "stable_url", "source_type", "geographic_coverage",
    "data_or_policy_domain", "relevance_to_tokyo_chinese_project",
    "use_in_analysis", "license_or_access_note", "verified_status", "notes",
]

# ---------------------------------------------------------------------------
# Japanese keyword sets for cautious metadata triage (mirror CiNii/J-STAGE).
# UTF-8 with LF.
# ---------------------------------------------------------------------------
KW = {
    "chinese": ["中国人", "中国籍", "中国系",
                "華人", "華僑", "中国"],
    "foreign": ["外国人", "在留外国人",
                "移民", "外国籍", "ニューカマー"],
    "tokyo": ["東京", "首都圏", "区部", "関東"],
    "japan": ["日本", "全国"],
    "housing": ["住宅", "賃貸", "居住", "住まい",
                "不動産", "アパート"],
    "disaster": ["防災", "災害", "避難", "地震",
                 "洪水", "脆弱", "ハザード", "津波"],
    "service": ["多言語", "医療", "教育", "子育て",
                "行政", "生活支援", "サービス",
                "福祉", "支援"],
    "transit": ["交通", "鉄道", "アクセシビリティ",
                "駅", "通勤"],
    "segregation": ["集住", "分布", "居住分離",
                    "集積", "エスニック", "分離"],
    "method": ["GIS", "空間分析", "空間", "地理情報",
               "統計", "メッシュ"],
}

KW_LABEL = {
    "chinese": "chinese", "foreign": "foreign_resident", "tokyo": "tokyo",
    "japan": "japan", "housing": "housing", "disaster": "disaster",
    "service": "service", "transit": "transit", "segregation": "segregation",
    "method": "spatial_method",
}

# Markers that an NDL record is an official / government / municipal material.
# These are intentionally CONSERVATIVE: single characters such as 都/市/区 are
# avoided because they match inside ordinary words (e.g. 首都圏, 都市, 地区).
# Academic / commercial publishers (see ACADEMIC_PUBLISHER) are excluded first,
# so university journals and learned-society articles are NOT treated as
# official sources.
OFFICIAL_MINISTRY = [
    "総務省", "法務省", "外務省", "財務省", "文部科学省", "厚生労働省",
    "農林水産省", "経済産業省", "国土交通省", "環境省", "防衛省", "内閣府",
    "内閣官房", "復興庁", "デジタル庁", "出入国在留管理庁", "消防庁",
    "気象庁", "観光庁", "文化庁", "スポーツ庁", "こども家庭庁", "警察庁",
    "国税庁", "統計局", "国立社会保障",
]
OFFICIAL_MUNICIPAL = [
    "市役所", "区役所", "町役場", "村役場", "県庁", "都庁", "道庁", "府庁",
    "市町村", "地方自治体", "自治体", "教育委員会", "国際交流協会",
    "国際交流センター", "多文化共生センター",
]
# Strong official document-type markers (title level).
OFFICIAL_DOCTYPE = [
    "白書", "ハザードマップ", "国勢調査", "防災計画", "地域防災計画",
    "多文化共生推進", "ガイドライン", "手引き", "手引", "指針",
    "統計表", "統計年鑑", "統計書",
]
# Data-source (vs policy) markers.
DATA_MARKERS = ["統計", "国勢調査", "センサス", "ハザードマップ", "メッシュ"]
# Academic / commercial publisher markers => never an official source.
ACADEMIC_PUBLISHER = [
    "大学", "学会", "研究会", "紀要", "論叢", "論集", "学術", "出版",
    "書房", "書店", "新聞社", "ジャーナル", "研究所", "研究科", "学院",
]
# A publisher string that is just a place name + municipal suffix
# (e.g. 東京都, 新宿区, 川口市) signals a municipal government publisher.
MUNI_SUFFIX_RE = re.compile(r"^[^\s]{1,8}(都|道|府|県|市|区|町|村)$")
MUNI_EXCLUDE = ["大学", "都市", "地区", "市街", "会", "研究"]


def build_arg_parser():
    p = argparse.ArgumentParser(
        description="NDL-only Round 02 metadata harvester (Tokyo-China project).")
    p.add_argument("--project-root", required=True,
                   help="Absolute path to the repository root.")
    p.add_argument("--run-id", default="round02_ndl",
                   help="Run identifier; controls output subfolder.")
    p.add_argument("--max-per-query", type=int, default=20,
                   help="Max records requested per query (first-pass limit).")
    p.add_argument("--sleep-seconds", type=float, default=1.5,
                   help="Polite delay between NDL requests.")
    return p


def parse_queries(query_file):
    """Parse query_id, group, and Japanese query string from the Round 02 md."""
    queries = []
    current_group = ""
    for line in query_file.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+Query group\s+(QG-[A-Z][^:]*)", line)
        if m:
            current_group = m.group(1).strip()
            continue
        if not line.startswith("| R02-Q"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        query_id = cells[0]
        jp_query = cells[1]
        matrix_target = cells[5] if len(cells) > 5 else ""
        if not re.match(r"^R02-Q\d+$", query_id):
            continue
        queries.append({
            "query_id": query_id,
            "group": current_group,
            "jp_query": jp_query,
            "matrix_target": matrix_target,
        })
    return queries


def http_get_text(url):
    """GET a URL. Returns (raw_text, http_reached, error_string)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "application/xml"})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return raw, True, ""
    except urllib.error.HTTPError as e:
        return None, True, "HTTP %s" % e.code
    except urllib.error.URLError as e:
        return None, False, "URLERROR %s" % getattr(e, "reason", e)
    except Exception as e:  # noqa: BLE001 - defensive; never crash the run
        return None, False, "ERROR %s" % e


def _localname(tag):
    if not isinstance(tag, str):
        return ""
    return tag.split("}")[-1]


def _texts_by_local(item, name):
    out = []
    for e in item.iter():
        if _localname(e.tag) == name and (e.text or "").strip():
            out.append(e.text.strip())
    return out


def _first_text(item, *names):
    for nm in names:
        vals = _texts_by_local(item, nm)
        if vals:
            return vals[0]
    return ""


def _all_texts(item, *names):
    out = []
    for nm in names:
        out.extend(_texts_by_local(item, nm))
    return out


def _parse_items(raw_text):
    """Parse NDL OpenSearch RSS and return (item_elements, total_results)."""
    try:
        root = ET.fromstring(raw_text)
    except ET.ParseError:
        return [], None
    items = [e for e in root.iter() if _localname(e.tag) == "item"]
    total = None
    for e in root.iter():
        if _localname(e.tag) == "totalResults":
            try:
                total = int((e.text or "").strip())
            except (TypeError, ValueError):
                total = None
            break
    return items, total


def _extract_year(item):
    for v in _all_texts(item, "issued", "date", "available", "dateAccepted"):
        m = re.search(r"(\d{4})", v)
        if m:
            return m.group(1)
    return ""


def _extract_doi(item):
    for v in _all_texts(item, "identifier", "seeAlso", "link", "guid"):
        m = re.search(r"10\.\d{4,9}/[^\s\"<>]+", v)
        if m:
            return m.group(0).rstrip(".")
    return ""


def _extract_link(item):
    # Prefer an http(s) <link>; then identifier/guid that looks like a permalink.
    for v in _all_texts(item, "link"):
        if v.startswith("http"):
            return v
    for v in _all_texts(item, "guid", "seeAlso", "identifier"):
        if v.startswith("http"):
            return v
    return ""


def _extract_identifiers(item):
    """Collect ISBN / JP / library identifiers (non-URL) for 'library metadata'."""
    ids = []
    for v in _all_texts(item, "identifier"):
        if v.startswith("http"):
            continue
        ids.append(v)
    return ids


def query_ndl(jp_query, count, endpoint):
    """Run one NDL OpenSearch metadata query against a given endpoint.

    NDL OpenSearch has no single AND "q" field equal to CiNii's; the free-word
    "any" parameter is the closest metadata-supported search mode. Metadata only
    (no PDF / full text). Returns (items, total, http_reached, error_string).
    """
    qs = urllib.parse.urlencode({"any": jp_query, "cnt": count, "idx": 1})
    url = "%s?%s" % (endpoint, qs)
    raw, reached, err = http_get_text(url)
    if raw is None:
        return [], None, reached, err
    items, total = _parse_items(raw)
    return items, total, reached, err


def _scan(text, keys):
    text_low = text.lower()
    hits = []
    for k in keys:
        for term in KW[k]:
            if term.isascii():
                matched = term.lower() in text_low
            else:
                matched = term in text
            if matched:
                hits.append(k)
                break
    return hits


def _is_official(title, publisher, doc_type):
    pub = publisher or ""
    title = title or ""
    blob = " ".join([title, pub, doc_type or ""])
    # Academic / commercial publisher disqualifies official routing first.
    if any(t in pub for t in ACADEMIC_PUBLISHER):
        return False
    inst_hit = any(t in pub or t in title for t in OFFICIAL_MINISTRY)
    muni_hit = any(t in pub for t in OFFICIAL_MUNICIPAL)
    muni_name = (bool(MUNI_SUFFIX_RE.match(pub.strip()))
                 and not any(x in pub for x in MUNI_EXCLUDE))
    doc_hit = any(t in blob for t in OFFICIAL_DOCTYPE)
    return inst_hit or muni_hit or muni_name or doc_hit


def classify_academic(flags, matrix_target):
    """Cautious academic triage. Never returns final A_direct_overlap."""
    modules = sum(1 for k in ("housing", "disaster", "service", "transit")
                  if k in flags)
    tokyo = "tokyo" in flags
    japan = "japan" in flags
    chinese = "chinese" in flags
    foreign = "foreign" in flags
    geo = tokyo or japan
    official_leaning = "official_source_registry" in (matrix_target or "").lower()

    if chinese and geo and modules >= 2:
        return "A_direct_overlap_candidate"
    if (chinese or foreign) and geo and modules >= 1:
        return "B_partial_overlap_candidate"
    if "segregation" in flags and (chinese or foreign):
        return "B_partial_overlap_candidate"
    if "method" in flags and (foreign or chinese or geo):
        return "D_method_support_candidate"
    if official_leaning and (foreign or chinese) and modules >= 1:
        return "official_policy_context"
    if foreign or chinese:
        return "E_background_candidate"
    return "hold_for_translation_or_manual_check"


def matrix_destination_for(cat):
    if cat in ("official_data_source", "official_policy_context"):
        return "official_source_registry.csv (pending verification)"
    if cat in ("A_direct_overlap_candidate", "B_partial_overlap_candidate"):
        return "gap_verification_matrix.csv (pending manual verification)"
    if cat in ("C_theoretical_support_candidate", "D_method_support_candidate"):
        return "literature_matrix.csv (pending verification)"
    if cat == "E_background_candidate":
        return "background (pending verification)"
    if cat == "hold_for_translation_or_manual_check":
        return "hold_pending_translation"
    return "none"


def _norm_title(title):
    return re.sub(r"[\s　]+", " ", (title or "")).strip().lower()


def normalize_item(item, q):
    """Map one NDL OpenSearch item to an intermediate record dict."""
    title = _first_text(item, "title")
    creators = "; ".join(dict.fromkeys(_all_texts(item, "creator", "author")))
    publisher = _first_text(item, "publisher")
    doc_type = _first_text(item, "type", "category", "materialType") or "Material"
    year = _extract_year(item)
    doi = _extract_doi(item)
    url = _extract_link(item)
    ids = _extract_identifiers(item)

    blob = " ".join([title, publisher, creators, doc_type])
    flags = sorted(set(_scan(blob, list(KW.keys()))))
    concepts = ";".join(KW_LABEL[f] for f in flags) or "none"

    study_area = "Tokyo/Japan" if "tokyo" in flags else ("Japan" if "japan" in flags else "")
    population = "Chinese residents" if "chinese" in flags else (
        "foreign residents" if "foreign" in flags else "")
    method = ";".join(KW_LABEL[f] for f in flags if f == "method") or "NA"

    official = _is_official(title, publisher, doc_type)
    if official:
        if any(t in (title + " " + publisher + " " + doc_type) for t in DATA_MARKERS):
            cat = "official_data_source"
        else:
            cat = "official_policy_context"
    else:
        cat = classify_academic(set(flags), q.get("matrix_target", ""))

    incomplete = not (year and (creators or publisher))
    verified_status = "partial" if incomplete else "unverified"

    return {
        "query_id": q["query_id"],
        "group": q.get("group", ""),
        "title": title,
        "creators": creators,
        "publisher": publisher,
        "doc_type": doc_type,
        "year": year if year else "NA",
        "doi": doi if doi else "NA",
        "url": url if url else "NA",
        "ids": ids,
        "flags": flags,
        "concepts": concepts,
        "study_area": study_area,
        "population": population,
        "method": method,
        "category": cat,
        "is_official": official,
        "verified_status": verified_status,
        "_norm_title": _norm_title(title),
    }


def to_tracking_row(rec):
    cat = rec["category"]
    return {
        "query_id": rec["query_id"],
        "source_type": "library_metadata",
        "search_platform": "NDL Search OpenSearch (any keyword)",
        "original_title": rec["title"],
        "english_working_title": "",
        "author_or_institution": rec["creators"],
        "year": rec["year"],
        "doi": rec["doi"],
        "stable_url": rec["url"],
        "publisher_or_host": rec["publisher"],
        "language": "ja",
        "document_type": rec["doc_type"],
        "study_area": rec["study_area"],
        "population_group": rec["population"],
        "core_topic": rec["concepts"],
        "method_or_data_type": rec["method"],
        "verified_status": rec["verified_status"],
        "overlap_category": cat,
        "matrix_destination": matrix_destination_for(cat),
        "translation_needed": "yes",
        "manual_check_needed": "yes",
        "notes": "NDL OpenSearch metadata-only triage round02; group=%s; "
                 "concepts=%s; manual verification required"
                 % (rec["group"], rec["concepts"]),
    }


def to_registry_row(rec):
    domain = ";".join(KW_LABEL[f] for f in rec["flags"]
                      if f in ("housing", "disaster", "service", "transit",
                               "segregation", "method")) or "general"
    geo = rec["study_area"] or "Japan (verify)"
    src_type = "official_data_source" if rec["category"] == "official_data_source" \
        else "official_policy_context"
    relevance = ("possible official %s source for the Tokyo-China project; "
                 "concepts=%s; pending manual verification"
                 % (src_type.replace("official_", "").replace("_", " "),
                    rec["concepts"]))
    return {
        "institution": rec["publisher"] or rec["creators"] or "NA",
        "source_title": rec["title"],
        "english_working_title": "",
        "year": rec["year"],
        "stable_url": rec["url"],
        "source_type": src_type,
        "geographic_coverage": geo,
        "data_or_policy_domain": domain,
        "relevance_to_tokyo_chinese_project": relevance,
        "use_in_analysis": "pending manual verification",
        "license_or_access_note": "NDL metadata only; access/license unverified; "
                                  "full text not downloaded",
        "verified_status": rec["verified_status"],
        "notes": "NDL OpenSearch metadata-only triage round02; group=%s; "
                 "official-source candidate; manual verification required"
                 % rec["group"],
        "_norm_title": rec["_norm_title"],
    }


def read_existing_tracking(tracking_csv):
    """Return (ids, title_index, doi_index, max_ndl_n) for cross-run dedup."""
    ids, title_index, doi_index, max_n = set(), {}, {}, 0
    if not tracking_csv.exists():
        return ids, title_index, doi_index, max_n
    with tracking_csv.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid = (row.get("source_id") or "").strip()
            if sid:
                ids.add(sid)
                m = re.match(r"^R02_NDL_(\d+)$", sid)
                if m:
                    max_n = max(max_n, int(m.group(1)))
            nt = _norm_title(row.get("original_title") or "")
            if nt and nt not in title_index:
                title_index[nt] = row
            doi = (row.get("doi") or "").strip().lower()
            if doi and doi not in ("na", "") and doi not in doi_index:
                doi_index[doi] = row
    return ids, title_index, doi_index, max_n


def read_existing_registry(registry_csv):
    """Return (ids, title_set, max_off_n) for the official registry."""
    ids, titles, max_n = set(), set(), 0
    if not registry_csv.exists():
        return ids, titles, max_n
    with registry_csv.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid = (row.get("source_id") or "").strip()
            if sid:
                ids.add(sid)
                m = re.match(r"^R02_NDL_OFF_(\d+)$", sid)
                if m:
                    max_n = max(max_n, int(m.group(1)))
            nt = _norm_title(row.get("source_title") or "")
            if nt:
                titles.add(nt)
    return ids, titles, max_n


def main():
    args = build_arg_parser().parse_args()
    root = Path(args.project_root)
    out_dir = root / "outputs" / "literature_discovery" / args.run_id
    raw_dir = out_dir / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    queries = parse_queries(root / QUERY_FILE_REL)
    groups = sorted({q["group"] for q in queries})

    # Pick a working endpoint with a single probe (first query) -----------
    endpoint_used = None
    probe_err = {}
    if queries:
        for ep in NDL_OPENSEARCH_ENDPOINTS:
            _items, _total, reached, err = query_ndl(queries[0]["jp_query"],
                                                     args.max_per_query, ep)
            probe_err[ep] = err or ("ok (%d items)" % len(_items))
            if reached and not err:
                endpoint_used = ep
                break
        if endpoint_used is None:
            # default to the current host even if the probe failed
            endpoint_used = NDL_OPENSEARCH_ENDPOINTS[0]
        time.sleep(max(0.0, args.sleep_seconds))

    # Harvest -------------------------------------------------------------
    raw_path = raw_dir / "ndl_raw.jsonl"
    normalized = []
    reached_any = False
    per_query_counts = {}
    per_query_total = {}
    errors = {}
    with raw_path.open("w", encoding="utf-8", newline="\n") as raw_h:
        for q in queries:
            items, total, reached, err = query_ndl(
                q["jp_query"], args.max_per_query, endpoint_used)
            if reached:
                reached_any = True
            if err:
                errors[q["query_id"]] = err
            per_query_counts[q["query_id"]] = len(items)
            per_query_total[q["query_id"]] = total
            for it in items:
                rec = normalize_item(it, q)
                raw_h.write(json.dumps(
                    {"query_id": q["query_id"], "group": q["group"],
                     "record": {k: v for k, v in rec.items() if k != "_norm_title"}},
                    ensure_ascii=True) + "\n")
                normalized.append(rec)
            time.sleep(max(0.0, args.sleep_seconds))

    # Dedup within this run by DOI then normalized title ------------------
    seen_doi, seen_title, deduped = set(), set(), []
    for rec in normalized:
        doi = rec["doi"].lower() if rec["doi"] != "NA" else ""
        nt = rec["_norm_title"]
        if doi and doi in seen_doi:
            continue
        if not doi and nt and nt in seen_title:
            continue
        if doi:
            seen_doi.add(doi)
        if nt:
            seen_title.add(nt)
        deduped.append(rec)

    academic = [r for r in deduped if not r["is_official"]]
    official = [r for r in deduped if r["is_official"]]

    # Append academic rows to tracking CSV (cross-source dedup) -----------
    tracking_csv = root / TRACKING_CSV_REL
    existing_ids, title_index, doi_index, max_n = read_existing_tracking(tracking_csv)
    appended, complementary_added, skipped_dup, prior_overlap = [], 0, 0, 0
    n = max_n
    for rec in academic:
        nt = rec["_norm_title"]
        doi = rec["doi"].lower() if rec["doi"] != "NA" else ""
        existing = None
        if doi and doi in doi_index:
            existing = doi_index[doi]
        elif nt and nt in title_index:
            existing = title_index[nt]
        if existing is not None:
            ex_sid = (existing.get("source_id") or "").strip()
            if ex_sid.startswith("R02_CINII") or ex_sid.startswith("R02_JSTAGE"):
                prior_overlap += 1
            ex_doi = (existing.get("doi") or "").strip().upper()
            ex_url = (existing.get("stable_url") or "").strip().upper()
            stronger = ((rec["doi"] != "NA" and ex_doi in ("NA", ""))
                        or (rec["ids"] and ex_url in ("NA", "")))
            if stronger:
                why = "stronger DOI" if rec["doi"] != "NA" else "library identifier"
                rec_row = to_tracking_row(rec)
                rec_row["notes"] += "; complements %s (NDL %s)" % (ex_sid, why)
                complementary_added += 1
                row = rec_row
            else:
                skipped_dup += 1
                continue
        else:
            row = to_tracking_row(rec)

        n += 1
        sid = "R02_NDL_%03d" % n
        while sid in existing_ids:
            n += 1
            sid = "R02_NDL_%03d" % n
        row["source_id"] = sid
        existing_ids.add(sid)
        if nt:
            title_index.setdefault(nt, row)
        if doi:
            doi_index.setdefault(doi, row)
        appended.append(row)

    if appended:
        write_header = not tracking_csv.exists()
        with tracking_csv.open("a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=TRACKING_COLUMNS, extrasaction="ignore")
            if write_header:
                w.writeheader()
            for row in appended:
                w.writerow(row)

    # Append official rows to the registry (dedup by title) ---------------
    registry_csv = root / REGISTRY_CSV_REL
    reg_ids, reg_titles, reg_max = read_existing_registry(registry_csv)
    reg_appended = []
    rn = reg_max
    for rec in official:
        nt = rec["_norm_title"]
        if nt and nt in reg_titles:
            skipped_dup += 1
            continue
        row = to_registry_row(rec)
        rn += 1
        sid = "R02_NDL_OFF_%03d" % rn
        while sid in reg_ids:
            rn += 1
            sid = "R02_NDL_OFF_%03d" % rn
        row["source_id"] = sid
        reg_ids.add(sid)
        if nt:
            reg_titles.add(nt)
        reg_appended.append(row)

    if reg_appended:
        write_header = not registry_csv.exists()
        with registry_csv.open("a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=REGISTRY_COLUMNS, extrasaction="ignore")
            if write_header:
                w.writeheader()
            for row in reg_appended:
                w.writerow(row)

    # Candidate outputs (all retrieved, deduped) --------------------------
    cand_csv = out_dir / "ndl_candidates.csv"
    cand_cols = ["source_id", "is_official", "category"] + TRACKING_COLUMNS[1:]
    with cand_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cand_cols, extrasaction="ignore")
        w.writeheader()
        for rec in deduped:
            base = to_tracking_row(rec)
            base["source_id"] = ""
            base["is_official"] = "yes" if rec["is_official"] else "no"
            base["category"] = rec["category"]
            w.writerow(base)

    with (out_dir / "ndl_candidates.jsonl").open("w", encoding="utf-8",
                                                 newline="\n") as f:
        for rec in deduped:
            row = {k: v for k, v in rec.items() if k != "_norm_title"}
            f.write(json.dumps(row, ensure_ascii=True) + "\n")

    # Category counts -----------------------------------------------------
    cat_counts = {}
    for rec in deduped:
        cat_counts[rec["category"]] = cat_counts.get(rec["category"], 0) + 1
    a_cnt = cat_counts.get("A_direct_overlap_candidate", 0)
    b_cnt = cat_counts.get("B_partial_overlap_candidate", 0)
    hold_cnt = cat_counts.get("hold_for_translation_or_manual_check", 0)
    off_cnt = cat_counts.get("official_data_source", 0) + \
        cat_counts.get("official_policy_context", 0)

    # Coverage summary md -------------------------------------------------
    s = []
    s.append("# NDL Round 02 Source Coverage Summary")
    s.append("")
    s.append("Run id: %s" % args.run_id)
    s.append("Search platform: NDL Search OpenSearch (any free-word; metadata only)")
    s.append("Endpoint used: %s" % (endpoint_used or "none"))
    s.append("Max per query: %d" % args.max_per_query)
    s.append("Query groups attempted: %d" % len(groups))
    s.append("Queries attempted: %d" % len(queries))
    s.append("NDL reached: %s" % ("YES" if reached_any else "NO"))
    s.append("")
    s.append("## Counts")
    s.append("- candidate records retrieved (post-dedup): %d" % len(deduped))
    s.append("- academic rows appended to tracking CSV: %d" % len(appended))
    s.append("- official rows appended to registry: %d" % len(reg_appended))
    s.append("- duplicate/complementary with prior CiNii/J-STAGE: %d" % prior_overlap)
    s.append("- complementary rows added (stronger metadata): %d" % complementary_added)
    s.append("- duplicates dropped (no stronger metadata): %d" % skipped_dup)
    s.append("- A_direct_overlap_candidate: %d" % a_cnt)
    s.append("- B_partial_overlap_candidate: %d" % b_cnt)
    s.append("- hold_for_translation_or_manual_check: %d" % hold_cnt)
    s.append("- official data/policy sources: %d" % off_cnt)
    s.append("")
    s.append("## Per-query retrieved counts (retrieved / total available)")
    for q in queries:
        total = per_query_total.get(q["query_id"])
        total_s = str(total) if total is not None else "NA"
        line = "- %s (%s): %d / %s" % (
            q["query_id"], q["group"], per_query_counts.get(q["query_id"], 0), total_s)
        if q["query_id"] in errors:
            line += " [error: %s]" % errors[q["query_id"]]
        s.append(line)
    s.append("")
    s.append("## Endpoint probe")
    for ep, st in probe_err.items():
        s.append("- %s : %s" % (ep, st))
    s.append("")
    s.append("## Category counts")
    for k in sorted(cat_counts):
        s.append("- %s: %d" % (k, cat_counts[k]))
    s.append("")
    s.append("## Search-mode limitation")
    s.append("NDL OpenSearch has no single space-separated AND field equal to the "
             "CiNii OpenSearch q parameter; the free-word 'any' parameter was used "
             "as the closest metadata-supported mode. No HTML scraping or "
             "full-text download was performed.")
    s.append("")
    s.append("NOTE: Metadata-only triage. Categories are preliminary and require")
    s.append("manual translation/verification. This does NOT confirm the research")
    s.append("gap. Status: gap under verification.")
    (out_dir / "ndl_source_coverage_summary.md").write_text(
        "\n".join(s) + "\n", encoding="utf-8", newline="\n")

    print("RUN COMPLETE")
    print("ndl_reached:", "YES" if reached_any else "NO")
    print("endpoint_used:", endpoint_used)
    print("query_groups_attempted:", len(groups))
    print("queries_attempted:", len(queries))
    print("candidates_retrieved:", len(deduped))
    print("tracking_rows_appended:", len(appended))
    print("registry_rows_appended:", len(reg_appended))
    print("prior_overlap_cinii_jstage:", prior_overlap)
    print("complementary_added:", complementary_added)
    print("skipped_dup:", skipped_dup)
    print("A_direct_overlap_candidate:", a_cnt)
    print("B_partial_overlap_candidate:", b_cnt)
    print("hold_for_translation_or_manual_check:", hold_cnt)
    print("official_data_policy_sources:", off_cnt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
