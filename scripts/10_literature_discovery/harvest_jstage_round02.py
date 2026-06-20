#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 02 J-STAGE-only metadata harvester (Tokyo-China opportunity-risk project).

Standard-library only. Queries the J-STAGE WebAPI article-search service
(service=3) metadata endpoint to assemble a PRELIMINARY Japanese-language
candidate list for the Tokyo-China opportunity-risk mismatch project. Japanese
queries are read from the Round 02 query file so the source of truth stays in
one place.

This script deliberately does NOT:
  - download PDFs or any full text
  - scrape J-STAGE HTML pages
  - scrape Google Scholar
  - use browser automation
  - use paid APIs
  - store, print, or commit any API key or credential
  - assert any final research gap

The J-STAGE WebAPI is a public metadata API. Only bibliographic metadata
(article title, authors, journal/material, volume/issue, year, DOI, stable URL)
is parsed and stored. The article-search service exposes a free-text search
field; J-STAGE has no single space-separated AND field equivalent to the CiNii
OpenSearch "q" parameter, so the closest metadata-supported mode (the WebAPI
"text" search parameter) is used and the limitation is recorded. No full text is
retrieved. Every classification produced here is PRELIMINARY metadata triage and
MUST be verified manually (title/abstract translation + record check) before any
gap claim is made. Current status: gap under verification.
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
HTTP_TIMEOUT = 12  # seconds; short so a blocked network fails fast
# J-STAGE WebAPI article-search service (service=3). Public metadata endpoint.
JSTAGE_WEBAPI = "https://api.jstage.jst.go.jp/searchapi/do"

# Relative path (from project root) to the Round 02 Japanese query file.
QUERY_FILE_REL = Path("literature") / "03_notes" / "round02_japanese_search_queries.md"
TRACKING_CSV_REL = Path("literature") / "02_matrices" / "round02_japanese_source_tracking.csv"

# Tracking CSV schema (must match the existing header exactly).
TRACKING_COLUMNS = [
    "source_id", "query_id", "source_type", "search_platform",
    "original_title", "english_working_title", "author_or_institution",
    "year", "doi", "stable_url", "publisher_or_host", "language",
    "document_type", "study_area", "population_group", "core_topic",
    "method_or_data_type", "verified_status", "overlap_category",
    "matrix_destination", "translation_needed", "manual_check_needed", "notes",
]

# ---------------------------------------------------------------------------
# Japanese keyword sets for cautious metadata triage. These mirror the CiNii
# harvester so coding stays consistent across platforms. UTF-8 with LF.
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

# Romanized labels for ASCII-safe output of detected concepts.
KW_LABEL = {
    "chinese": "chinese", "foreign": "foreign_resident", "tokyo": "tokyo",
    "japan": "japan", "housing": "housing", "disaster": "disaster",
    "service": "service", "transit": "transit", "segregation": "segregation",
    "method": "spatial_method",
}


def build_arg_parser():
    p = argparse.ArgumentParser(
        description="J-STAGE-only Round 02 metadata harvester (Tokyo-China project).")
    p.add_argument("--project-root", required=True,
                   help="Absolute path to the repository root.")
    p.add_argument("--run-id", default="round02_jstage",
                   help="Run identifier; controls output subfolder.")
    p.add_argument("--max-per-query", type=int, default=20,
                   help="Max records requested per query (first-pass limit).")
    p.add_argument("--sleep-seconds", type=float, default=1.5,
                   help="Polite delay between J-STAGE requests.")
    return p


def parse_queries(query_file):
    """Parse query_id, group, and Japanese query string from the Round 02 md.

    Returns a list of dicts: {query_id, group, jp_query, matrix_target}.
    Keeps the markdown file as the single source of truth so the script body
    stays free of hard-coded Japanese query strings.
    """
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


def http_get_bytes(url):
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
    """Strip the XML namespace from an element tag."""
    if not isinstance(tag, str):
        return ""
    return tag.split("}")[-1]


def _child_by_local(elem, name):
    if elem is None:
        return None
    for c in list(elem):
        if _localname(c.tag) == name:
            return c
    return None


def _entry_iter_local(entry, name):
    """All descendants of `entry` whose local tag matches `name`."""
    return [e for e in entry.iter() if _localname(e.tag) == name]


def _ja_en(elem):
    """Element may carry <ja>/<en> children; return (ja_text, en_text)."""
    if elem is None:
        return "", ""
    ja_el = _child_by_local(elem, "ja")
    en_el = _child_by_local(elem, "en")
    ja_t = (ja_el.text or "").strip() if ja_el is not None else ""
    en_t = (en_el.text or "").strip() if en_el is not None else ""
    if not ja_t and not en_t and (elem.text or "").strip():
        ja_t = elem.text.strip()
    return ja_t, en_t


def _author_name(author_elem):
    """Pull a display name from a J-STAGE <author> element (ja preferred)."""
    for lang in ("ja", "en"):
        lang_el = _child_by_local(author_elem, lang)
        if lang_el is not None:
            nm = _child_by_local(lang_el, "name")
            if nm is not None and (nm.text or "").strip():
                return nm.text.strip()
            if (lang_el.text or "").strip():
                return lang_el.text.strip()
    nm = _child_by_local(author_elem, "name")
    if nm is not None and (nm.text or "").strip():
        return nm.text.strip()
    if (author_elem.text or "").strip():
        return author_elem.text.strip()
    return ""


def _extract_entries(raw_text):
    """Parse J-STAGE Atom XML and return (entry_elements, total_results)."""
    try:
        root = ET.fromstring(raw_text)
    except ET.ParseError:
        return [], None
    entries = [e for e in root.iter() if _localname(e.tag) == "entry"]
    total = None
    for e in root.iter():
        if _localname(e.tag) == "totalResults":
            try:
                total = int((e.text or "").strip())
            except (TypeError, ValueError):
                total = None
            break
    return entries, total


def _extract_year(entry):
    for name in ("pubyear", "publicationDate", "date", "issued", "coverDate"):
        for el in _entry_iter_local(entry, name):
            m = re.search(r"(\d{4})", (el.text or ""))
            if m:
                return m.group(1)
    return ""


def _extract_doi(entry):
    for name in ("doi", "identifier", "id"):
        for el in _entry_iter_local(entry, name):
            m = re.search(r"10\.\d{4,9}/[^\s\"<>]+", (el.text or ""))
            if m:
                return m.group(0).rstrip(".")
    return ""


def _extract_link(entry):
    link_el = None
    for el in _entry_iter_local(entry, "article_link"):
        link_el = el
        break
    if link_el is not None:
        ja, en = _ja_en(link_el)
        if ja:
            return ja
        if en:
            return en
    # Fall back to prism:url / id text.
    for name in ("url", "id"):
        for el in _entry_iter_local(entry, name):
            txt = (el.text or "").strip()
            if txt.startswith("http"):
                return txt
    return ""


def query_jstage(jp_query, count):
    """Run one J-STAGE WebAPI article-search metadata query.

    J-STAGE has no single space-separated AND "q" field; the WebAPI "text"
    parameter is the closest metadata-supported search mode. This searches the
    indexed metadata/content but retrieves METADATA ONLY (no PDF/full text is
    downloaded). Returns (entries, total_results, http_reached, error_string).
    """
    qs = urllib.parse.urlencode({
        "service": 3,            # article-search service
        "text": jp_query,        # closest free-text metadata search field
        "count": count,          # first-pass limit
        "start": 1,
    })
    url = "%s?%s" % (JSTAGE_WEBAPI, qs)
    raw, reached, err = http_get_bytes(url)
    if raw is None:
        return [], None, reached, err
    entries, total = _extract_entries(raw)
    return entries, total, reached, err


def _scan(text, keys):
    """Substring scan. ASCII terms (e.g. GIS) match case-insensitively;
    Japanese terms match as-is."""
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


def classify(blob, matrix_target):
    """Cautious metadata triage. Never returns final A_direct_overlap."""
    flags = set(_scan(blob, list(KW.keys())))
    modules = sum(1 for k in ("housing", "disaster", "service", "transit")
                  if k in flags)
    tokyo = "tokyo" in flags
    japan = "japan" in flags
    chinese = "chinese" in flags
    foreign = "foreign" in flags
    geo = tokyo or japan

    target = (matrix_target or "").lower()
    official_leaning = "official_source_registry" in target

    if chinese and geo and modules >= 2:
        cat = "A_direct_overlap_candidate"
    elif (chinese or foreign) and geo and modules >= 1:
        cat = "B_partial_overlap_candidate"
    elif "segregation" in flags and (chinese or foreign):
        cat = "B_partial_overlap_candidate"
    elif "method" in flags and (foreign or chinese or geo):
        cat = "D_method_support_candidate"
    elif official_leaning and (foreign or chinese) and modules >= 1:
        cat = "official_policy_context"
    elif foreign or chinese:
        cat = "E_background_candidate"
    else:
        cat = "hold_for_translation_or_manual_check"
    return sorted(flags), cat


def matrix_destination_for(cat):
    if cat in ("official_data_source", "official_policy_context"):
        return "official_source_registry.csv (pending verification)"
    if cat == "A_direct_overlap_candidate":
        return "gap_verification_matrix.csv (pending manual verification)"
    if cat == "B_partial_overlap_candidate":
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


def normalize_record(entry, q):
    """Map one J-STAGE article entry to the tracking-CSV field shape."""
    title_el = None
    for el in _entry_iter_local(entry, "article_title"):
        title_el = el
        break
    title_ja, title_en = _ja_en(title_el)
    title = title_ja or title_en

    mat_el = None
    for el in _entry_iter_local(entry, "material_title"):
        mat_el = el
        break
    mat_ja, mat_en = _ja_en(mat_el)
    publisher = mat_ja or mat_en

    authors = "; ".join(
        n for n in (_author_name(a) for a in _entry_iter_local(entry, "author")) if n)

    year = _extract_year(entry)
    doi = _extract_doi(entry)
    url = _extract_link(entry)

    blob = " ".join([title_ja, title_en, publisher, authors])
    flags, cat = classify(blob, q.get("matrix_target", ""))
    concepts = ";".join(KW_LABEL[f] for f in flags) or "none"

    study_area = ""
    if "tokyo" in flags:
        study_area = "Tokyo/Japan"
    elif "japan" in flags:
        study_area = "Japan"

    population = ""
    if "chinese" in flags:
        population = "Chinese residents"
    elif "foreign" in flags:
        population = "foreign residents"

    method = ";".join(KW_LABEL[f] for f in flags if f == "method") or "NA"

    incomplete = not (doi and year and authors)
    verified_status = "partial" if incomplete else "unverified"

    return {
        "query_id": q["query_id"],
        "source_type": "academic_metadata",
        "search_platform": "J-STAGE WebAPI (service=3, text search)",
        "original_title": title,
        "english_working_title": title_en,
        "author_or_institution": authors,
        "year": year if year else "NA",
        "doi": doi if doi else "NA",
        "stable_url": url if url else "NA",
        "publisher_or_host": publisher,
        "language": "ja" if title_ja else ("en" if title_en else "ja"),
        "document_type": "Article",
        "study_area": study_area,
        "population_group": population,
        "core_topic": concepts,
        "method_or_data_type": method,
        "verified_status": verified_status,
        "overlap_category": cat,
        "matrix_destination": matrix_destination_for(cat),
        # Official J-STAGE English title (when present) is not a working
        # translation; otherwise Japanese title needs later human translation.
        "translation_needed": "no" if title_en else "yes",
        "manual_check_needed": "yes",
        "notes": "J-STAGE WebAPI metadata-only triage round02; group=%s; "
                 "concepts=%s; manual verification required"
                 % (q.get("group", ""), concepts),
        "_norm_title": _norm_title(title),
    }


def read_existing_tracking(tracking_csv):
    """Inspect the existing tracking CSV for cross-run dedup.

    Returns (existing_ids, title_index, doi_index, max_jstage_n) where
    title_index maps normalized_title -> row dict and doi_index maps
    lowercased DOI -> row dict (for matching against earlier CiNii records).
    """
    ids = set()
    title_index = {}
    doi_index = {}
    max_n = 0
    if not tracking_csv.exists():
        return ids, title_index, doi_index, max_n
    with tracking_csv.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid = (row.get("source_id") or "").strip()
            if sid:
                ids.add(sid)
                m = re.match(r"^R02_JSTAGE_(\d+)$", sid)
                if m:
                    max_n = max(max_n, int(m.group(1)))
            nt = _norm_title(row.get("original_title") or "")
            if nt and nt not in title_index:
                title_index[nt] = row
            doi = (row.get("doi") or "").strip().lower()
            if doi and doi not in ("na", "") and doi not in doi_index:
                doi_index[doi] = row
    return ids, title_index, doi_index, max_n


def main():
    args = build_arg_parser().parse_args()
    root = Path(args.project_root)
    out_dir = root / "outputs" / "literature_discovery" / args.run_id
    raw_dir = out_dir / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    query_file = root / QUERY_FILE_REL
    queries = parse_queries(query_file)
    groups = sorted({q["group"] for q in queries})

    # Harvest -------------------------------------------------------------
    raw_path = raw_dir / "jstage_raw.jsonl"
    normalized = []
    reached_any = False
    per_query_counts = {}
    per_query_total = {}
    errors = {}
    with raw_path.open("w", encoding="utf-8", newline="\n") as raw_h:
        for q in queries:
            entries, total, reached, err = query_jstage(
                q["jp_query"], args.max_per_query)
            if reached:
                reached_any = True
            if err:
                errors[q["query_id"]] = err
            per_query_counts[q["query_id"]] = len(entries)
            per_query_total[q["query_id"]] = total
            for ent in entries:
                rec = normalize_record(ent, q)
                # Raw metadata snapshot (ASCII-safe JSON; metadata only).
                raw_h.write(json.dumps(
                    {"query_id": q["query_id"], "group": q["group"],
                     "record": {k: v for k, v in rec.items()
                                if k != "_norm_title"}},
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

    # Append to tracking CSV with cross-run dedup (incl. CiNii overlap) ---
    tracking_csv = root / TRACKING_CSV_REL
    existing_ids, title_index, doi_index, max_n = read_existing_tracking(tracking_csv)
    appended = []
    cinii_overlap = 0          # J-STAGE candidates matching a prior CiNii record
    skipped_dup = 0            # duplicates dropped (no stronger metadata)
    complementary_added = 0    # duplicates added because metadata is stronger
    n = max_n
    for rec in deduped:
        nt = rec["_norm_title"]
        doi = rec["doi"].lower() if rec["doi"] != "NA" else ""

        existing = None
        if doi and doi in doi_index:
            existing = doi_index[doi]
        elif nt and nt in title_index:
            existing = title_index[nt]

        if existing is not None:
            ex_sid = (existing.get("source_id") or "").strip()
            is_cinii = ex_sid.startswith("R02_CINII")
            if is_cinii:
                cinii_overlap += 1
            ex_doi = (existing.get("doi") or "").strip().upper()
            ex_pub = (existing.get("publisher_or_host") or "").strip()
            stronger_doi = (rec["doi"] != "NA") and (ex_doi in ("NA", ""))
            stronger_pub = bool(rec["publisher_or_host"]) and not ex_pub
            if stronger_doi or stronger_pub:
                reason = []
                if stronger_doi:
                    reason.append("stronger DOI")
                if stronger_pub:
                    reason.append("stronger publisher")
                rec["notes"] += ("; complements %s (%s)"
                                 % (ex_sid, ", ".join(reason)))
                complementary_added += 1
                # fall through to append
            else:
                skipped_dup += 1
                continue

        n += 1
        sid = "R02_JSTAGE_%03d" % n
        while sid in existing_ids:
            n += 1
            sid = "R02_JSTAGE_%03d" % n
        rec["source_id"] = sid
        existing_ids.add(sid)
        if nt:
            title_index.setdefault(nt, rec)
        if doi:
            doi_index.setdefault(doi, rec)
        appended.append(rec)

    if appended:
        write_header = not tracking_csv.exists()
        with tracking_csv.open("a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=TRACKING_COLUMNS, extrasaction="ignore")
            if write_header:
                w.writeheader()
            for rec in appended:
                w.writerow(rec)

    # Candidate outputs (all retrieved, deduped) --------------------------
    cand_csv = out_dir / "jstage_candidates.csv"
    with cand_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source_id"] + TRACKING_COLUMNS[1:],
                           extrasaction="ignore")
        w.writeheader()
        for rec in deduped:
            row = dict(rec)
            row.setdefault("source_id", "")
            w.writerow(row)

    with (out_dir / "jstage_candidates.jsonl").open("w", encoding="utf-8",
                                                    newline="\n") as f:
        for rec in deduped:
            row = {k: v for k, v in rec.items() if k != "_norm_title"}
            f.write(json.dumps(row, ensure_ascii=True) + "\n")

    # Category counts -----------------------------------------------------
    cat_counts = {}
    for rec in deduped:
        cat_counts[rec["overlap_category"]] = cat_counts.get(
            rec["overlap_category"], 0) + 1
    a_cnt = cat_counts.get("A_direct_overlap_candidate", 0)
    b_cnt = cat_counts.get("B_partial_overlap_candidate", 0)
    hold_cnt = cat_counts.get("hold_for_translation_or_manual_check", 0)

    # Coverage summary md -------------------------------------------------
    s = []
    s.append("# J-STAGE Round 02 Source Coverage Summary")
    s.append("")
    s.append("Run id: %s" % args.run_id)
    s.append("Search platform: J-STAGE WebAPI (service=3 article search, "
             "text parameter; metadata only)")
    s.append("Max per query: %d" % args.max_per_query)
    s.append("Query groups attempted: %d" % len(groups))
    s.append("Queries attempted: %d" % len(queries))
    s.append("J-STAGE reached: %s" % ("YES" if reached_any else "NO"))
    s.append("")
    s.append("## Counts")
    s.append("- candidate records retrieved (post-dedup): %d" % len(deduped))
    s.append("- rows appended to tracking CSV: %d" % len(appended))
    s.append("- duplicate/complementary with prior CiNii records: %d" % cinii_overlap)
    s.append("- duplicates dropped (no stronger metadata): %d" % skipped_dup)
    s.append("- complementary rows added (stronger metadata): %d" % complementary_added)
    s.append("- A_direct_overlap_candidate: %d" % a_cnt)
    s.append("- B_partial_overlap_candidate: %d" % b_cnt)
    s.append("- hold_for_translation_or_manual_check: %d" % hold_cnt)
    s.append("")
    s.append("## Per-query retrieved counts (retrieved / total available)")
    for q in queries:
        total = per_query_total.get(q["query_id"])
        total_s = str(total) if total is not None else "NA"
        line = "- %s (%s): %d / %s" % (
            q["query_id"], q["group"],
            per_query_counts.get(q["query_id"], 0), total_s)
        if q["query_id"] in errors:
            line += " [error: %s]" % errors[q["query_id"]]
        s.append(line)
    s.append("")
    s.append("## Category counts")
    for k in sorted(cat_counts):
        s.append("- %s: %d" % (k, cat_counts[k]))
    s.append("")
    s.append("## Search-mode limitation")
    s.append("J-STAGE WebAPI has no single space-separated AND field equal to "
             "the CiNii OpenSearch q parameter. The closest metadata-supported "
             "mode (the WebAPI text search parameter) was used. Recall may "
             "differ from CiNii. No HTML scraping or full-text download was "
             "performed.")
    s.append("")
    s.append("NOTE: Metadata-only triage. Categories are preliminary and")
    s.append("require manual translation/verification. This does NOT confirm")
    s.append("the research gap. Status: gap under verification.")
    (out_dir / "jstage_source_coverage_summary.md").write_text(
        "\n".join(s) + "\n", encoding="utf-8", newline="\n")

    print("RUN COMPLETE")
    print("jstage_reached:", "YES" if reached_any else "NO")
    print("query_groups_attempted:", len(groups))
    print("queries_attempted:", len(queries))
    print("candidates_retrieved:", len(deduped))
    print("rows_appended:", len(appended))
    print("cinii_overlap:", cinii_overlap)
    print("complementary_added:", complementary_added)
    print("skipped_dup:", skipped_dup)
    print("A_direct_overlap_candidate:", a_cnt)
    print("B_partial_overlap_candidate:", b_cnt)
    print("hold_for_translation_or_manual_check:", hold_cnt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
