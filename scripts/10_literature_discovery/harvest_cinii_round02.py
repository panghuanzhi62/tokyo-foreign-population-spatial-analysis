#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 02 CiNii-only metadata harvester (Tokyo-China opportunity-risk project).

Standard-library only. Queries the CiNii Research OpenSearch metadata API to
assemble a PRELIMINARY Japanese-language candidate list for the Tokyo-China
opportunity-risk mismatch project. Japanese queries are read from the Round 02
query file so the source of truth stays in one place.

This script deliberately does NOT:
  - download PDFs or any full text
  - scrape Google Scholar
  - use browser automation
  - use paid APIs
  - print, write, or commit the CiNii application id (CINII_APP_ID)
  - assert any final research gap

The CiNii application id is read ONLY from the CINII_APP_ID environment
variable. It is never echoed to stdout, written to any output file, or stored
in any manifest. Every classification produced here is PRELIMINARY metadata
triage and MUST be verified manually (title/abstract translation + record
check) before any gap claim is made. Current status: gap under verification.
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
from pathlib import Path

USER_AGENT = "TokyoChinaLitDiscovery/Round02 (academic metadata discovery; stdlib urllib)"
HTTP_TIMEOUT = 12  # seconds; short so a blocked network fails fast
CINII_OPENSEARCH = "https://cir.nii.ac.jp/opensearch/all"

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
# Japanese keyword sets for cautious metadata triage. These are necessary
# because CiNii titles are Japanese; the file is UTF-8 with LF.
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
        description="CiNii-only Round 02 metadata harvester (Tokyo-China project).")
    p.add_argument("--project-root", required=True,
                   help="Absolute path to the repository root.")
    p.add_argument("--run-id", default="round02_cinii",
                   help="Run identifier; controls output subfolder.")
    p.add_argument("--max-per-query", type=int, default=20,
                   help="Max records requested per query (first-pass limit).")
    p.add_argument("--sleep-seconds", type=float, default=1.5,
                   help="Polite delay between CiNii requests.")
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


def http_get_json(url):
    """GET a URL and parse JSON. Returns (data, http_reached, error_string)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw), True, ""
    except urllib.error.HTTPError as e:
        return None, True, "HTTP %s" % e.code
    except urllib.error.URLError as e:
        return None, False, "URLERROR %s" % getattr(e, "reason", e)
    except json.JSONDecodeError as e:
        return None, True, "JSON_DECODE %s" % e
    except Exception as e:  # noqa: BLE001 - defensive; never crash the run
        return None, False, "ERROR %s" % e


def _as_text(value):
    """CiNii JSON-LD fields may be str, dict, or list of either."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for k in ("@value", "@id", "name", "title"):
            if value.get(k):
                return str(value[k]).strip()
        return ""
    if isinstance(value, list):
        parts = [_as_text(v) for v in value]
        return "; ".join([p for p in parts if p])
    return str(value).strip()


def _first(rec, *keys):
    for k in keys:
        if k in rec and rec[k]:
            return rec[k]
    return None


def _extract_items(data):
    """Return the list of result items from a CiNii OpenSearch JSON payload."""
    if not isinstance(data, dict):
        return []
    if isinstance(data.get("items"), list):
        return data["items"]
    graph = data.get("@graph")
    if isinstance(graph, list):
        for node in graph:
            if isinstance(node, dict) and isinstance(node.get("items"), list):
                return node["items"]
    return []


def _extract_year(rec):
    for k in ("prism:publicationDate", "dc:date", "datePublished",
              "prism:coverDate", "dc:issued"):
        text = _as_text(rec.get(k))
        m = re.search(r"(\d{4})", text)
        if m:
            return m.group(1)
    return ""


def _extract_doi(rec):
    for k in ("prism:doi", "dc:identifier", "doi", "@id"):
        text = _as_text(rec.get(k))
        m = re.search(r"10\.\d{4,9}/[^\s\"<>]+", text)
        if m:
            return m.group(0).rstrip(".")
    return ""


def query_cinii(jp_query, count, appid):
    """Run one CiNii OpenSearch metadata query. appid is never logged."""
    qs = urllib.parse.urlencode({
        "q": jp_query, "count": count, "format": "json", "appid": appid,
    })
    url = "%s?%s" % (CINII_OPENSEARCH, qs)
    data, reached, err = http_get_json(url)
    return _extract_items(data), reached, err


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


def matrix_destination_for(cat, matrix_target):
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


def normalize_record(rec, q, appid_unused=None):
    """Map one CiNii item to the tracking-CSV field shape."""
    title = _as_text(_first(rec, "title", "dc:title", "@title"))
    creators = _as_text(_first(rec, "dc:creator", "creator", "author",
                               "foaf:maker"))
    publisher = _as_text(_first(rec, "dc:publisher", "prism:publicationName",
                                "publisher"))
    doc_type = _as_text(_first(rec, "dc:type", "@type", "type")) or "article"
    year = _extract_year(rec)
    doi = _extract_doi(rec)
    url = _as_text(_first(rec, "@id", "link", "url", "rdfs:seeAlso"))
    lang = _as_text(_first(rec, "dc:language", "inLanguage")) or "ja"

    blob = " ".join([title, publisher, creators])
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

    incomplete = not (doi and year and creators)
    verified_status = "partial" if incomplete else "unverified"

    return {
        "query_id": q["query_id"],
        "source_type": "academic_metadata",
        "search_platform": "CiNii Research OpenSearch",
        "original_title": title,
        "english_working_title": "",
        "author_or_institution": creators,
        "year": year if year else "NA",
        "doi": doi if doi else "NA",
        "stable_url": url if url else "NA",
        "publisher_or_host": publisher,
        "language": lang,
        "document_type": doc_type,
        "study_area": study_area,
        "population_group": population,
        "core_topic": concepts,
        "method_or_data_type": method,
        "verified_status": verified_status,
        "overlap_category": cat,
        "matrix_destination": matrix_destination_for(cat, q.get("matrix_target", "")),
        "translation_needed": "yes" if title else "yes",
        "manual_check_needed": "yes",
        "notes": "CiNii metadata-only triage round02; group=%s; concepts=%s; "
                 "manual verification required" % (q.get("group", ""), concepts),
        "_norm_title": re.sub(r"\s+", " ",
                              re.sub(r"[\s　]+", " ", title)).strip().lower(),
    }


def read_existing_tracking(tracking_csv):
    """Return (existing source_ids, existing normalized titles, max R02_CINII n)."""
    ids, titles, max_n = set(), set(), 0
    if not tracking_csv.exists():
        return ids, titles, max_n
    with tracking_csv.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid = (row.get("source_id") or "").strip()
            if sid:
                ids.add(sid)
                m = re.match(r"^R02_CINII_(\d+)$", sid)
                if m:
                    max_n = max(max_n, int(m.group(1)))
            t = (row.get("original_title") or "").strip().lower()
            if t:
                titles.add(re.sub(r"[\s　]+", " ", t))
    return ids, titles, max_n


def main():
    args = build_arg_parser().parse_args()
    root = Path(args.project_root)
    out_dir = root / "outputs" / "literature_discovery" / args.run_id
    raw_dir = out_dir / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    appid = os.environ.get("CINII_APP_ID", "").strip()
    if not appid:
        print("CINII_APP_ID missing: CiNii search SKIPPED.")
        return 0

    query_file = root / QUERY_FILE_REL
    queries = parse_queries(query_file)
    groups = sorted({q["group"] for q in queries})

    # Harvest -------------------------------------------------------------
    raw_path = raw_dir / "cinii_raw.jsonl"
    normalized = []
    reached_any = False
    per_query_counts = {}
    errors = {}
    with raw_path.open("w", encoding="utf-8", newline="\n") as raw_h:
        for q in queries:
            items, reached, err = query_cinii(q["jp_query"], args.max_per_query, appid)
            if reached:
                reached_any = True
            if err:
                errors[q["query_id"]] = err
            per_query_counts[q["query_id"]] = len(items)
            for it in items:
                raw_h.write(json.dumps(
                    {"query_id": q["query_id"], "group": q["group"], "record": it},
                    ensure_ascii=True) + "\n")
                normalized.append(normalize_record(it, q))
            time.sleep(max(0.0, args.sleep_seconds))

    # Dedup within this run by normalized title (and DOI when present) ----
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

    # Append to tracking CSV with cross-run dedup -------------------------
    tracking_csv = root / TRACKING_CSV_REL
    existing_ids, existing_titles, max_n = read_existing_tracking(tracking_csv)
    appended = []
    n = max_n
    for rec in deduped:
        nt = rec["_norm_title"]
        if nt and nt in existing_titles:
            continue
        n += 1
        sid = "R02_CINII_%03d" % n
        while sid in existing_ids:
            n += 1
            sid = "R02_CINII_%03d" % n
        rec["source_id"] = sid
        existing_ids.add(sid)
        if nt:
            existing_titles.add(nt)
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
    cand_csv = out_dir / "cinii_candidates.csv"
    with cand_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source_id"] + TRACKING_COLUMNS[1:],
                           extrasaction="ignore")
        w.writeheader()
        for rec in deduped:
            row = dict(rec)
            row.setdefault("source_id", "")
            w.writerow(row)

    with (out_dir / "cinii_candidates.jsonl").open("w", encoding="utf-8",
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
    s.append("# CiNii Round 02 Source Coverage Summary")
    s.append("")
    s.append("Run id: %s" % args.run_id)
    s.append("Max per query: %d" % args.max_per_query)
    s.append("Query groups attempted: %d" % len(groups))
    s.append("Queries attempted: %d" % len(queries))
    s.append("CiNii reached: %s" % ("YES" if reached_any else "NO"))
    s.append("")
    s.append("## Counts")
    s.append("- candidate records retrieved (post-dedup): %d" % len(deduped))
    s.append("- rows appended to tracking CSV: %d" % len(appended))
    s.append("- A_direct_overlap_candidate: %d" % a_cnt)
    s.append("- B_partial_overlap_candidate: %d" % b_cnt)
    s.append("- hold_for_translation_or_manual_check: %d" % hold_cnt)
    s.append("")
    s.append("## Per-query retrieved counts")
    for q in queries:
        line = "- %s (%s): %d" % (q["query_id"], q["group"],
                                  per_query_counts.get(q["query_id"], 0))
        if q["query_id"] in errors:
            line += " [error: %s]" % errors[q["query_id"]]
        s.append(line)
    s.append("")
    s.append("## Category counts")
    for k in sorted(cat_counts):
        s.append("- %s: %d" % (k, cat_counts[k]))
    s.append("")
    s.append("NOTE: Metadata-only triage. Categories are preliminary and")
    s.append("require manual translation/verification. This does NOT confirm")
    s.append("the research gap. Status: gap under verification.")
    (out_dir / "cinii_source_coverage_summary.md").write_text(
        "\n".join(s) + "\n", encoding="utf-8", newline="\n")

    print("RUN COMPLETE")
    print("cinii_reached:", "YES" if reached_any else "NO")
    print("query_groups_attempted:", len(groups))
    print("queries_attempted:", len(queries))
    print("candidates_retrieved:", len(deduped))
    print("rows_appended:", len(appended))
    print("A_direct_overlap_candidate:", a_cnt)
    print("B_partial_overlap_candidate:", b_cnt)
    print("hold_for_translation_or_manual_check:", hold_cnt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
