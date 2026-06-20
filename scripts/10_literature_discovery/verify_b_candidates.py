#!/usr/bin/env python3
"""Round 01 B-candidate verification pipeline (Tokyo-China project).

Automates FIRST-STAGE bibliographic and overlap-risk verification of the 13
prioritized B_partial_overlap_candidate records listed in section 6 of
literature/04_synthesis/round01_b_candidate_review.md.

Standard-library only. This script does NOT:
  - scrape Google Scholar
  - download PDFs or full text
  - call SciSpace automatically
  - call CiNii unless CINII_APP_ID is present in the environment
  - store, write, or print API keys / credentials
  - assert or confirm the research gap

All overlap classification is PRELIMINARY keyword triage on metadata only and
MUST be followed by SciSpace Deep Review and manual full-text reading before any
final classification or gap claim.
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

UA = "TokyoChinaBVerify/1.0 (academic bibliographic verification; stdlib urllib)"
TIMEOUT = 8  # seconds per request; short so a blocked network fails fast

KW = {
    "chinese": ["chinese", "china", "prc", "mainland china"],
    "foreign_residents": ["foreign resident", "foreigner", "non-japanese",
                          "immigrant", "migrant", "newcomer", "foreign national"],
    "non_chinese": ["vietnamese", "filipino", "brazilian", "korean", "nepalese",
                    "muslim", "multiethnic", "multi-ethnic", "by nationality",
                    "across nationalities", "foreign residents"],
    "tokyo": ["tokyo", "23 wards", "toshima", "metropolitan tokyo", "kanto"],
    "japan": ["japan", "japanese", "yokohama", "gunma"],
    "housing": ["housing", "rental", "residential", "tenant", "landlord", "dwelling"],
    "transit": ["transit", "transport", "accessibility", "commut", "station", "rail"],
    "service": ["service", "healthcare", "health care", "hospital", "education",
                "school", "multilingual", "welfare", "administrative", "shelter"],
    "disaster": ["disaster", "evacuation", "hazard", "earthquake", "flood",
                 "vulnerability", "risk", "preparedness", "fire"],
    "arrival_infra": ["arrival infrastructure", "settlement infrastructure",
                      "settlement", "reception", "newcomer support", "intermediar"],
    "opportunity_risk": ["opportunity", "mismatch", "inequality", "stratification"],
    "spatial_method": ["lisa", "spatial durbin", "spatial econometric", "2sfca",
                       "mgwr", "geographically weighted", "spatial autocorrelation",
                       "typology", "spatial panel", "moran", "gis",
                       "population distribution"],
    "theory": ["segregation", "spatial assimilation", "co-ethnic", "coethnic",
               "enclave", "place stratification", "ethnic stratification"],
}

PREPRINT_DOI_HINTS = ["ssrn", "10.2139", "osf.io", "10.31235", "_v2"]

VERIFICATION_FIELDS = [
    "record_id", "priority_rank", "title_from_review", "doi_from_review",
    "year_from_review", "verification_status", "doi_resolves", "crossref_match",
    "openalex_match", "semantic_scholar_match", "publisher_or_landing_url",
    "title_match_level", "year_match_level", "venue", "authors",
    "abstract_available", "language_hint", "duplicate_of",
    "needs_manual_source_check", "notes",
]

OVERLAP_FIELDS = [
    "record_id", "priority_rank", "covers_chinese_residents",
    "covers_foreign_residents", "covers_tokyo_or_metropolitan_tokyo",
    "covers_japan", "covers_housing", "covers_transit_accessibility",
    "covers_service_accessibility", "covers_disaster_risk",
    "covers_arrival_or_settlement_infrastructure",
    "covers_opportunity_risk_mismatch", "covers_spatial_method",
    "compares_chinese_non_chinese", "direct_overlap_risk_score",
    "recommended_overlap_category", "manual_deep_read_priority",
]


def build_arg_parser():
    p = argparse.ArgumentParser(
        description="Round 01 B-candidate bibliographic + overlap-risk verification.")
    p.add_argument("--project-root", required=True)
    p.add_argument("--input-review",
                   default="literature/04_synthesis/round01_b_candidate_review.md")
    p.add_argument("--run-id", default="round01_b_verify")
    p.add_argument("--max-records", type=int, default=13)
    p.add_argument("--sleep-seconds", type=float, default=1.0)
    p.add_argument("--skip-network", action="store_true")
    return p


# --------------------------------------------------------------------------
# Parsing the review note
# --------------------------------------------------------------------------
def parse_section6(text):
    lines = text.splitlines()
    start = None
    for i, l in enumerate(lines):
        if l.strip().startswith("## 6."):
            start = i
            break
    if start is None:
        return []
    end = len(lines)
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if s.startswith("## 7") or s.startswith("Lower-priority"):
            end = i
            break
    num_re = re.compile(r"^\s*(\d+)\.\s+(round01_api-\d+)\s*-\s*(.*)$")
    items, cur = [], None
    for l in lines[start:end]:
        m = num_re.match(l)
        if m:
            if cur:
                items.append(cur)
            cur = {"priority_rank": int(m.group(1)),
                   "record_id": m.group(2),
                   "reason": m.group(3).strip()}
        elif cur is not None and l.strip() and not l.strip().startswith("#"):
            cur["reason"] += " " + l.strip()
    if cur:
        items.append(cur)
    for it in items:
        it["reason"] = re.sub(r"\s+", " ", it["reason"]).strip()
    return items


def parse_review_table(text):
    rows = {}
    for l in text.splitlines():
        if l.startswith("| round01_api-"):
            cols = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cols) >= 9:
                rows[cols[0]] = {
                    "title": cols[1], "year": cols[2], "venue": cols[3],
                    "doi": cols[4], "source_api": cols[5],
                    "query_group": cols[6], "likely_module": cols[8]}
    return rows


def load_candidates_csv(path):
    out = {}
    if not path.exists():
        return out
    try:
        with path.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                out[r.get("record_id", "")] = r
    except Exception:
        return {}
    return out


# --------------------------------------------------------------------------
# Network helpers
# --------------------------------------------------------------------------
def http_get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8", "replace")), True, ""
    except urllib.error.HTTPError as e:
        return None, True, "HTTP %s" % e.code
    except urllib.error.URLError as e:
        return None, False, "URLERROR %s" % getattr(e, "reason", e)
    except Exception as e:  # noqa: BLE001
        return None, False, "ERROR %s" % e


def resolve_doi(doi):
    if not doi or doi == "NA":
        return False, "", "no doi"
    url = "https://doi.org/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return True, resp.geturl(), ""
    except urllib.error.HTTPError as e:
        return (e.code < 400), getattr(e, "url", url), "HTTP %s" % e.code
    except urllib.error.URLError as e:
        return False, "", "URLERROR %s" % getattr(e, "reason", e)
    except Exception as e:  # noqa: BLE001
        return False, "", "ERROR %s" % e


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def title_match(a, b):
    a, b = _norm(a), _norm(b)
    if not a or not b:
        return "unknown"
    if a == b:
        return "exact"
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return "unknown"
    overlap = len(ta & tb) / max(1, len(ta | tb))
    if a in b or b in a or overlap >= 0.8:
        return "high"
    if overlap >= 0.4:
        return "partial"
    return "none"


def year_match(a, b):
    try:
        a, b = int(str(a)[:4]), int(str(b)[:4])
    except Exception:
        return "unknown"
    if a == b:
        return "exact"
    if abs(a - b) == 1:
        return "off_by_one"
    return "mismatch"


def scan(text, key):
    text = (text or "").lower()
    return any(term in text for term in KW[key])


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    args = build_arg_parser().parse_args()
    root = Path(args.project_root)
    review_path = root / args.input_review
    review_text = review_path.read_text(encoding="utf-8")

    items = parse_section6(review_text)[:args.max_records]
    table = parse_review_table(review_text)
    cands = load_candidates_csv(
        root / "outputs" / "literature_discovery" / "round01_api" / "candidates.csv")

    out_dir = root / "outputs" / "literature_verification" / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    endpoint_up = {"crossref": True, "openalex": True, "semantic_scholar": True,
                   "doi_resolver": True}
    endpoints_attempted = set()
    cinii_appid = os.environ.get("CINII_APP_ID", "").strip()

    verif_rows, overlap_rows, full_records = [], [], []

    for it in items:
        rid = it["record_id"]
        rank = it["priority_rank"]
        rv = table.get(rid, {})
        cv = cands.get(rid, {})
        title = rv.get("title") or cv.get("title", "")
        doi = rv.get("doi") or cv.get("doi", "")
        if doi in ("NA", ""):
            doi = cv.get("doi", "") or ""
        year = rv.get("year") or cv.get("year", "")
        venue = rv.get("venue") or cv.get("venue", "")
        authors = cv.get("authors", "")
        is_preprint = any(h in (doi or "").lower() for h in PREPRINT_DOI_HINTS)

        meta_title = title
        meta_year = year
        meta_lang = cv.get("language", "")
        abstract_available = (cv.get("abstract_or_summary_available", "") == "yes")
        landing = ""
        cr_match = ox_match = ss_match = False
        doi_ok = False
        notes = []

        if not args.skip_network:
            # DOI resolver
            if endpoint_up["doi_resolver"] and doi and doi != "NA":
                endpoints_attempted.add("doi_resolver")
                doi_ok, landing, derr = resolve_doi(doi)
                if derr.startswith("URLERROR"):
                    endpoint_up["doi_resolver"] = False
                    notes.append("doi_resolver_network_down")
            # Crossref by DOI
            if endpoint_up["crossref"] and doi and doi != "NA":
                endpoints_attempted.add("crossref")
                data, reached, err = http_get_json(
                    "https://api.crossref.org/works/" + urllib.parse.quote(doi))
                if not reached:
                    endpoint_up["crossref"] = False
                    notes.append("crossref_network_down")
                elif data and data.get("message"):
                    cr_match = True
                    m = data["message"]
                    meta_title = (m.get("title") or [meta_title])[0]
                    venue = (m.get("container-title") or [venue])[0]
                    dp = (m.get("issued") or {}).get("date-parts") or [[None]]
                    if dp and dp[0] and dp[0][0]:
                        meta_year = dp[0][0]
                    if m.get("author"):
                        authors = authors or "; ".join(
                            " ".join([a.get("given", ""), a.get("family", "")]).strip()
                            for a in m["author"])
                    meta_lang = meta_lang or m.get("language", "")
                    if m.get("abstract"):
                        abstract_available = True
            # OpenAlex by DOI or title
            if endpoint_up["openalex"]:
                endpoints_attempted.add("openalex")
                if doi and doi != "NA":
                    ox_url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)
                else:
                    ox_url = ("https://api.openalex.org/works?search=%s&per-page=1"
                              % urllib.parse.quote(title))
                data, reached, err = http_get_json(ox_url)
                if not reached:
                    endpoint_up["openalex"] = False
                    notes.append("openalex_network_down")
                elif data:
                    w = data
                    if "results" in data:
                        w = (data.get("results") or [None])[0]
                    if w and (w.get("title") or w.get("display_name")):
                        ox_match = True
                        meta_title = meta_title or w.get("title") or w.get("display_name")
                        if w.get("abstract_inverted_index"):
                            abstract_available = True
                        meta_lang = meta_lang or (w.get("language") or "")
            # Semantic Scholar by DOI or title
            if endpoint_up["semantic_scholar"]:
                endpoints_attempted.add("semantic_scholar")
                fields = "title,year,venue,authors,abstract,externalIds"
                if doi and doi != "NA":
                    ss_url = ("https://api.semanticscholar.org/graph/v1/paper/DOI:%s?fields=%s"
                              % (urllib.parse.quote(doi), fields))
                else:
                    ss_url = ("https://api.semanticscholar.org/graph/v1/paper/search?query=%s"
                              "&limit=1&fields=%s" % (urllib.parse.quote(title), fields))
                data, reached, err = http_get_json(ss_url)
                if not reached:
                    endpoint_up["semantic_scholar"] = False
                    notes.append("semantic_scholar_network_down")
                elif data:
                    w = data
                    if isinstance(data.get("data"), list):
                        w = (data.get("data") or [None])[0]
                    if w and w.get("title"):
                        ss_match = True
                        if w.get("abstract"):
                            abstract_available = True
                elif err.startswith("HTTP 429"):
                    notes.append("semantic_scholar_rate_limited")
            time.sleep(max(0.0, args.sleep_seconds))

        # verification_status
        if args.skip_network:
            status = "network_skipped"
        elif is_preprint:
            status = "duplicate_or_preprint"
        elif doi and doi != "NA" and doi_ok and (cr_match or ox_match):
            status = "verified_by_doi_and_metadata"
        elif cr_match or ox_match or ss_match:
            status = "verified_by_metadata_only"
        elif doi_ok:
            status = "partially_verified"
        else:
            status = "not_verified"

        tm = title_match(title, meta_title) if meta_title else "unknown"
        ym = year_match(year, meta_year) if meta_year else "unknown"

        verif_rows.append({
            "record_id": rid, "priority_rank": rank,
            "title_from_review": title, "doi_from_review": doi or "NA",
            "year_from_review": year or "NA", "verification_status": status,
            "doi_resolves": "yes" if doi_ok else ("skipped" if args.skip_network else "no"),
            "crossref_match": "yes" if cr_match else "no",
            "openalex_match": "yes" if ox_match else "no",
            "semantic_scholar_match": "yes" if ss_match else "no",
            "publisher_or_landing_url": landing or "NA",
            "title_match_level": tm, "year_match_level": ym,
            "venue": venue or "NA", "authors": authors or "NA",
            "abstract_available": "yes" if abstract_available else "no",
            "language_hint": meta_lang or "NA", "duplicate_of": "NA",
            "needs_manual_source_check": "yes",
            "notes": "; ".join(notes) if notes else "preliminary; manual check required",
        })

        # overlap-risk coding (keyword triage on metadata + reason)
        blob = " ".join([title, venue, it["reason"], rv.get("likely_module", "")])
        cov = {k: scan(blob, k) for k in (
            "chinese", "foreign_residents", "tokyo", "japan", "housing",
            "transit", "service", "disaster", "arrival_infra",
            "opportunity_risk", "spatial_method")}
        compares = cov["chinese"] and scan(blob, "non_chinese")
        module_count = sum(1 for k in ("housing", "transit", "service",
                                       "disaster", "arrival_infra") if cov[k])
        raw = (3 if cov["chinese"] else 0) + (2 if compares else 0) \
            + (1 if cov["tokyo"] else 0) + (1 if cov["japan"] and not cov["tokyo"] else 0) \
            + module_count + (2 if cov["opportunity_risk"] else 0)
        score10 = min(10, round(raw / 14.0 * 10))

        if is_preprint:
            rec_cat = "duplicate_or_preprint"
        elif cov["chinese"] and (cov["tokyo"] or cov["japan"]) and module_count >= 2 and cov["opportunity_risk"]:
            rec_cat = "A_risk_requires_full_text_check"
        elif status in ("verified_by_doi_and_metadata", "verified_by_metadata_only") \
                and module_count >= 1 and (cov["tokyo"] or cov["chinese"]):
            rec_cat = "B_partial_overlap_verified"
        elif module_count >= 1 and (cov["tokyo"] or cov["chinese"]):
            rec_cat = "B_partial_overlap_needs_check"
        elif cov["spatial_method"] and module_count == 0:
            rec_cat = "D_method_support"
        elif cov["opportunity_risk"] or scan(blob, "theory"):
            rec_cat = "C_theoretical_support"
        elif cov["tokyo"] or cov["japan"] or cov["foreign_residents"]:
            rec_cat = "E_background_only"
        else:
            rec_cat = "false_positive_or_out_of_scope"

        if rec_cat == "A_risk_requires_full_text_check" or score10 >= 7:
            priority = "high"
        elif rec_cat in ("B_partial_overlap_verified", "B_partial_overlap_needs_check"):
            priority = "medium"
        else:
            priority = "low"

        overlap_rows.append({
            "record_id": rid, "priority_rank": rank,
            "covers_chinese_residents": "yes" if cov["chinese"] else "no",
            "covers_foreign_residents": "yes" if cov["foreign_residents"] else "no",
            "covers_tokyo_or_metropolitan_tokyo": "yes" if cov["tokyo"] else "no",
            "covers_japan": "yes" if cov["japan"] or cov["tokyo"] else "no",
            "covers_housing": "yes" if cov["housing"] else "no",
            "covers_transit_accessibility": "yes" if cov["transit"] else "no",
            "covers_service_accessibility": "yes" if cov["service"] else "no",
            "covers_disaster_risk": "yes" if cov["disaster"] else "no",
            "covers_arrival_or_settlement_infrastructure": "yes" if cov["arrival_infra"] else "no",
            "covers_opportunity_risk_mismatch": "yes" if cov["opportunity_risk"] else "no",
            "covers_spatial_method": "yes" if cov["spatial_method"] else "no",
            "compares_chinese_non_chinese": "yes" if compares else "no",
            "direct_overlap_risk_score": score10,
            "recommended_overlap_category": rec_cat,
            "manual_deep_read_priority": priority,
        })

        full_records.append({
            "verification": verif_rows[-1], "overlap": overlap_rows[-1],
            "reason": it["reason"], "likely_module": rv.get("likely_module", ""),
        })

    # ---- write detailed outputs ----
    _write_csv(out_dir / "verified_b_candidates.csv", VERIFICATION_FIELDS, verif_rows)
    with (out_dir / "verified_b_candidates.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for r in full_records:
            f.write(json.dumps(r, ensure_ascii=True) + "\n")
    _write_csv(out_dir / "overlap_risk_scores.csv", OVERLAP_FIELDS, overlap_rows)

    # high-risk set for SciSpace: priority high, with a top-3 fallback by score
    by_score = sorted(range(len(overlap_rows)),
                      key=lambda i: overlap_rows[i]["direct_overlap_risk_score"],
                      reverse=True)
    high_idx = [i for i in range(len(overlap_rows))
                if overlap_rows[i]["manual_deep_read_priority"] == "high"]
    if len(high_idx) < 3:
        for i in by_score:
            if i not in high_idx:
                high_idx.append(i)
            if len(high_idx) >= 3:
                break
    high_idx = sorted(high_idx, key=lambda i: overlap_rows[i]["priority_rank"])

    _write_scispace_prompts(out_dir / "scispace_deep_review_prompts.md",
                            [full_records[i] for i in high_idx])
    _write_manual_checklist(out_dir / "manual_fulltext_checklist.md",
                            [full_records[i] for i in high_idx])

    status_counts = {}
    for r in verif_rows:
        status_counts[r["verification_status"]] = status_counts.get(
            r["verification_status"], 0) + 1

    manifest = {
        "run_id": args.run_id,
        "input_review": args.input_review,
        "candidates_processed": len(items),
        "skip_network": bool(args.skip_network),
        "endpoints_attempted": sorted(endpoints_attempted),
        "cinii_enabled": bool(cinii_appid),
        "status_counts": status_counts,
        "high_risk_record_ids": [overlap_rows[i]["record_id"] for i in high_idx],
    }
    (out_dir / "verification_run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2), encoding="utf-8", newline="\n")

    # ---- public synthesis ----
    _write_public_synthesis(
        root / "literature" / "04_synthesis" / "round01_b_candidate_verification_status.md",
        args, items, verif_rows, overlap_rows, full_records, high_idx,
        status_counts, sorted(endpoints_attempted), bool(cinii_appid))

    print("RUN COMPLETE")
    print("candidates_processed:", len(items))
    print("verified_by_doi_and_metadata:", status_counts.get("verified_by_doi_and_metadata", 0))
    print("verified_by_metadata_only:", status_counts.get("verified_by_metadata_only", 0))
    print("partially_verified:", status_counts.get("partially_verified", 0))
    print("not_verified:", status_counts.get("not_verified", 0))
    print("duplicate_or_preprint:", status_counts.get("duplicate_or_preprint", 0))
    print("network_skipped:", status_counts.get("network_skipped", 0))
    print("high_risk_for_scispace:", len(high_idx))
    print("output_dir:", out_dir)


def _write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _short(title, n=70):
    t = re.sub(r"\s+", " ", title or "").strip()
    return (t[:n] + "...") if len(t) > n else t


def _write_scispace_prompts(path, records):
    lines = ["# SciSpace Deep Review Prompts (High-Risk B Candidates)", "",
             "One compact prompt per high-risk candidate. These are PRELIMINARY",
             "verification prompts; run each in SciSpace Deep Review against the",
             "full text. Nothing here confirms the research gap.", ""]
    for r in records:
        v = r["verification"]
        lines.append("## %s (priority rank %s)" % (v["record_id"], v["priority_rank"]))
        lines.append("")
        lines.append("Title (from review): %s" % v["title_from_review"])
        lines.append("DOI: %s" % v["doi_from_review"])
        lines.append("")
        lines.append("Prompt:")
        lines.append("Verify this paper and report precisely: (1) the exact research")
        lines.append("question; (2) the study area; (3) the population group studied;")
        lines.append("(4) the data source; (5) the spatial unit of analysis; (6) the")
        lines.append("method. Then state yes/no with evidence for each: (a) are Chinese")
        lines.append("residents analyzed; (b) are non-Chinese foreign residents compared;")
        lines.append("(c) is housing included; (d) is transit/accessibility included;")
        lines.append("(e) are services included; (f) is disaster/risk exposure included;")
        lines.append("(g) is an opportunity-risk mismatch or typology included. Finally,")
        lines.append("explain how this paper overlaps with the provisional topic")
        lines.append("'Chinese Residents and Opportunity-Risk Mismatch in Metropolitan")
        lines.append("Tokyo', and state whether it WEAKENS, SUPPORTS, or only PARTIALLY")
        lines.append("overlaps with that provisional topic.")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _write_manual_checklist(path, records):
    lines = ["# Manual Full-Text Checklist (High-Risk B Candidates)", "",
             "Use this checklist when reading each high-risk item in full text.",
             "Mark each box [ ] -> [x] as completed. Final category is assigned",
             "only AFTER full-text reading.", ""]
    for r in records:
        v = r["verification"]
        lines.append("## %s (priority rank %s)" % (v["record_id"], v["priority_rank"]))
        lines.append("Title: %s" % v["title_from_review"])
        lines.append("DOI: %s" % v["doi_from_review"])
        lines.append("")
        for box in [
            "bibliographic verification (DOI resolves, publisher page matches)",
            "study area confirmed",
            "population confirmed (Chinese / foreign residents / other)",
            "variables confirmed (housing / accessibility / services / disaster)",
            "method confirmed",
            "key findings noted",
            "overlap with Sun 2026 assessed",
            "overlap with opportunity-risk mismatch assessed",
            "decision: enter into literature_matrix.csv (yes/no)",
            "decision: enter into gap_verification_matrix.csv (yes/no)",
            "final category after full-text reading (A/B/C/D/E/false_positive/duplicate)",
        ]:
            lines.append("- [ ] %s" % box)
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _write_public_synthesis(path, args, items, verif_rows, overlap_rows,
                            full_records, high_idx, status_counts,
                            endpoints, cinii_enabled):
    by_id_overlap = {o["record_id"]: o for o in overlap_rows}
    by_id_full = {fr["verification"]["record_id"]: fr for fr in full_records}
    L = []
    L.append("# Round 01 B-Candidate Verification Status")
    L.append("")
    L.append("Project: Tokyo-China opportunity-risk mismatch (provisional working title)")
    L.append("Repo: E:\\rsch\\laborJapan")
    L.append("Run id: %s" % args.run_id)
    L.append("")
    L.append("## A. Purpose")
    L.append("")
    L.append("This note summarizes automated bibliographic and overlap-risk")
    L.append("verification of the 13 prioritized B_partial_overlap_candidate records")
    L.append("from literature/04_synthesis/round01_b_candidate_review.md.")
    L.append("")
    L.append("## B. Evidence status")
    L.append("")
    L.append("- This is automated metadata verification.")
    L.append("- It is NOT final deep reading.")
    L.append("- It does NOT confirm the research gap.")
    L.append("- It does NOT prove absence of direct-overlap literature.")
    L.append("- It must be followed by SciSpace and manual full-text verification.")
    L.append("")
    L.append("## C. Verification coverage")
    L.append("")
    L.append("- Candidates processed: %d" % len(items))
    L.append("- Endpoints attempted: %s" % (", ".join(endpoints) if endpoints else "none (network skipped)"))
    L.append("- CiNii used: %s" % ("yes" if cinii_enabled else "no (no CINII_APP_ID)"))
    L.append("- Verified by DOI and metadata: %d" % status_counts.get("verified_by_doi_and_metadata", 0))
    L.append("- Verified by metadata only: %d" % status_counts.get("verified_by_metadata_only", 0))
    L.append("- Partially verified: %d" % status_counts.get("partially_verified", 0))
    L.append("- Not verified: %d" % status_counts.get("not_verified", 0))
    L.append("- Duplicates or preprints: %d" % status_counts.get("duplicate_or_preprint", 0))
    L.append("- Network skipped: %d" % status_counts.get("network_skipped", 0))
    L.append("")
    L.append("Note: 0 preliminary A_direct_overlap_candidate items in Round 01 does")
    L.append("NOT confirm the research gap and does NOT prove that no direct-overlap")
    L.append("literature exists.")
    L.append("")
    L.append("## D. Candidate verification table")
    L.append("")
    L.append("| priority_rank | record_id | short_title | doi | verification_status | likely_module | recommended_overlap_category | direct_overlap_risk_score | manual_deep_read_priority | next_action |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for v in sorted(verif_rows, key=lambda r: r["priority_rank"]):
        rid = v["record_id"]
        o = by_id_overlap[rid]
        fr = by_id_full[rid]
        na = "SciSpace deep review" if o["manual_deep_read_priority"] == "high" \
            else ("manual publisher/abstract check" if o["manual_deep_read_priority"] == "medium"
                  else "low-priority manual check")
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            v["priority_rank"], rid, _short(v["title_from_review"], 60),
            v["doi_from_review"], v["verification_status"],
            fr["likely_module"] or "NA", o["recommended_overlap_category"],
            o["direct_overlap_risk_score"], o["manual_deep_read_priority"], na))
    L.append("")
    L.append("## E. High-risk items for SciSpace Deep Review")
    L.append("")
    if not high_idx:
        L.append("- (none flagged)")
    for i in high_idx:
        o = overlap_rows[i]
        v = by_id_full[o["record_id"]]["verification"]
        L.append("- %s (rank %s, risk %s): %s" % (
            o["record_id"], o["priority_rank"], o["direct_overlap_risk_score"],
            _short(v["title_from_review"], 80)))
    L.append("")
    L.append("Compact SciSpace prompts for these items are generated locally in")
    L.append("outputs/literature_verification/%s/scispace_deep_review_prompts.md" % args.run_id)
    L.append("(not committed).")
    L.append("")
    L.append("## F. Direct-overlap caution")
    L.append("")
    a_items = [o for o in overlap_rows
               if o["recommended_overlap_category"] == "A_risk_requires_full_text_check"]
    if a_items:
        L.append("Automated triage flagged %d item(s) whose metadata MAY approach the" % len(a_items))
        L.append("full provisional-topic combination. This is a risk signal only, not")
        L.append("a finding, and requires full-text checking:")
        for o in a_items:
            L.append("- %s" % o["record_id"])
    else:
        L.append("No B candidate appears, on metadata alone, to approach the full")
        L.append("provisional-topic combination (Chinese residents in Metropolitan")
        L.append("Tokyo, plus Chinese vs non-Chinese comparison, plus housing, plus")
        L.append("transit/accessibility, plus services, plus disaster/risk exposure,")
        L.append("plus opportunity-risk typology or mismatch). The verified items")
        L.append("cluster on single modules (housing OR disaster OR services).")
    L.append("")
    L.append("Stated cautiously: this does not prove that no such literature exists.")
    L.append("Manual deep review and additional databases are still required.")
    L.append("")
    L.append("## G. Next steps")
    L.append("")
    L.append("- Use SciSpace Deep Review on the highest-risk items.")
    L.append("- Manually check publisher pages and abstracts.")
    L.append("- Update literature_matrix.csv and gap_verification_matrix.csv only")
    L.append("  after verification.")
    L.append("- Do not write the introduction yet.")
    path.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sys.exit(main())
