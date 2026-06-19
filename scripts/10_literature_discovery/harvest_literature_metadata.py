#!/usr/bin/env python3
"""Tokyo-China literature discovery: API-first metadata harvester.

Standard-library only. Queries open scholarly-metadata APIs (OpenAlex,
Crossref, Semantic Scholar, and optionally CiNii) to assemble a PRELIMINARY
candidate list for the Tokyo-China opportunity-risk mismatch project.

This script deliberately does NOT:
  - scrape Google Scholar (prohibited by its terms; use SciSpace later)
  - download PDFs or any full text
  - store, write, or print API keys / credentials
  - assert any final research gap

Every classification produced here is PRELIMINARY keyword-based triage and MUST
be verified manually (DOI + publisher page + deep reading) before any gap claim
is made. See literature/03_notes/automated_literature_discovery_protocol.md.
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

USER_AGENT = "TokyoChinaLitDiscovery/1.0 (academic literature discovery; stdlib urllib)"
HTTP_TIMEOUT = 8  # seconds; kept short so a blocked network fails fast

# ---------------------------------------------------------------------------
# Query groups. Each entry: stable group key + a human query string.
# English terms are used for the API query; romanized Japanese hints are kept
# in comments / labels so the file stays ASCII-safe.
# ---------------------------------------------------------------------------
QUERY_GROUPS = [
    ("chinese_migration_japan", "Chinese migration to Japan"),
    ("chinese_residents_tokyo", "Chinese residents Tokyo"),
    ("chinese_immigrants_settlement", "Chinese immigrants Japan settlement"),
    ("foreign_residents_segregation", "foreign residents Japan residential segregation"),
    ("tokyo_settlement_assimilation", "Tokyo immigrant settlement spatial assimilation"),
    ("coethnic_location_choice", "co-ethnic networks Tokyo immigrant location choice"),
    ("arrival_infrastructure", "arrival infrastructure migrant settlement infrastructure"),
    ("housing_discrimination", "foreigners Tokyo rental housing discrimination"),
    ("service_accessibility_gis", "immigrant service accessibility GIS"),
    ("disaster_vulnerability", "foreign residents Tokyo disaster vulnerability evacuation"),
    ("opportunity_risk_mismatch", "opportunity-risk mismatch immigrant settlement"),
    ("urban_opportunity_structure", "urban opportunity structure immigrant housing services risk"),
    ("spatial_methods", "LISA spatial econometrics 2SFCA MGWR spatial typology immigrants"),
]

# ---------------------------------------------------------------------------
# Keyword sets for preliminary overlap flagging (lowercase matching).
# ---------------------------------------------------------------------------
KW = {
    "chinese": ["chinese", "china", "prc", "mainland china"],
    "non_chinese_comparison": [
        "vietnamese", "filipino", "brazilian", "korean", "nepalese",
        "multi-group", "multiple groups", "across nationalities",
        "by nationality", "foreign residents",
    ],
    "housing": ["housing", "rental", "residential", "tenant", "landlord", "dwelling"],
    "transit": ["transit", "transport", "accessibility", "commut", "station", "rail"],
    "service": ["service", "healthcare", "health care", "hospital", "education",
                "school", "multilingual", "welfare", "childcare"],
    "disaster": ["disaster", "evacuation", "hazard", "earthquake", "flood",
                 "vulnerability", "risk exposure", "shelter"],
    "arrival_infra": ["arrival infrastructure", "settlement infrastructure",
                      "intermediar", "broker", "reception", "newcomer support"],
    "opportunity_risk": ["opportunity", "opportunity structure", "mismatch",
                         "opportunity-risk", "risk", "inequality"],
    "tokyo_japan": ["tokyo", "japan", "japanese", "kanto", "metropolitan tokyo"],
    "method": ["lisa", "spatial durbin", "spatial econometric", "2sfca",
               "mgwr", "geographically weighted", "spatial autocorrelation",
               "typology", "spatial panel", "moran"],
    "theory": ["spatial assimilation", "co-ethnic", "coethnic", "enclave",
               "segregation", "place stratification"],
}


def build_arg_parser():
    p = argparse.ArgumentParser(
        description="API-first literature metadata harvester (Tokyo-China project).")
    p.add_argument("--project-root", required=True,
                   help="Absolute path to the repository root.")
    p.add_argument("--run-id", default="round01_api",
                   help="Run identifier; controls output subfolder.")
    p.add_argument("--max-per-query", type=int, default=25,
                   help="Max records requested per API per query group.")
    return p


def http_get_json(url):
    """GET a URL and parse JSON. Returns (data, http_reached, error_string)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw), True, ""
    except urllib.error.HTTPError as e:
        # Server was reached but returned an error status (e.g. 429/400).
        return None, True, "HTTP %s" % e.code
    except urllib.error.URLError as e:
        # Network/DNS failure: server not reached.
        return None, False, "URLERROR %s" % getattr(e, "reason", e)
    except Exception as e:  # noqa: BLE001 - defensive; never crash the run
        return None, False, "ERROR %s" % e


def _norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def _scan(text, keys):
    text = (text or "").lower()
    hits = []
    for k in keys:
        for term in KW[k]:
            if term in text:
                hits.append(k)
                break
    return hits


def classify(rec):
    """Preliminary, keyword-only overlap triage. NOT final evidence."""
    blob = " ".join(str(rec.get(f, "")) for f in
                    ("title", "venue", "country_or_region_hint",
                     "population_group_hint", "core_concept_hint", "method_hint"))
    flags = set(_scan(blob, list(KW.keys())))
    modules = sum(1 for k in ("housing", "transit", "service", "disaster",
                              "arrival_infra") if k in flags)
    tokyo = "tokyo_japan" in flags
    chinese = "chinese" in flags

    if chinese and "opportunity_risk" in flags and modules >= 2 and tokyo:
        cat = "A_direct_overlap_candidate"
    elif (chinese or tokyo) and modules >= 1:
        cat = "B_partial_overlap_candidate"
    elif "theory" in flags or "opportunity_risk" in flags:
        cat = "C_theoretical_support_candidate"
    elif "method" in flags:
        cat = "D_method_support_candidate"
    elif tokyo or chinese or "non_chinese_comparison" in flags:
        cat = "E_background_candidate"
    else:
        cat = "uncertain"
    return sorted(flags), cat


# ---------------------------------------------------------------------------
# Per-source query + normalization. Each returns (raw_items, normalized_items,
# http_reached_bool, error_string).
# ---------------------------------------------------------------------------
def query_openalex(group, query, n):
    url = ("https://api.openalex.org/works?search=%s&per-page=%d"
           % (urllib.parse.quote(query), n))
    data, reached, err = http_get_json(url)
    raw, norm = [], []
    if data and isinstance(data.get("results"), list):
        for w in data["results"]:
            raw.append({"query_group": group, "query": query, "record": w})
            inv = w.get("abstract_inverted_index")
            authors = [a.get("author", {}).get("display_name", "")
                       for a in (w.get("authorships") or [])]
            doi = (w.get("doi") or "").replace("https://doi.org/", "")
            venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
            norm.append(_normalize(
                source="openalex", group=group, query=query,
                title=w.get("title") or w.get("display_name") or "",
                authors=authors, year=w.get("publication_year"),
                venue=venue, doi=doi, url=w.get("id") or "",
                abstract_avail=bool(inv), language=w.get("language") or ""))
    return raw, norm, reached, err


def query_crossref(group, query, n):
    url = ("https://api.crossref.org/works?query=%s&rows=%d"
           % (urllib.parse.quote(query), n))
    data, reached, err = http_get_json(url)
    raw, norm = [], []
    items = (((data or {}).get("message") or {}).get("items")) or []
    for w in items:
        raw.append({"query_group": group, "query": query, "record": w})
        authors = [" ".join([a.get("given", ""), a.get("family", "")]).strip()
                   for a in (w.get("author") or [])]
        title = (w.get("title") or [""])[0]
        venue = (w.get("container-title") or [""])[0]
        year = None
        dp = (w.get("issued") or {}).get("date-parts") or [[None]]
        if dp and dp[0]:
            year = dp[0][0]
        norm.append(_normalize(
            source="crossref", group=group, query=query, title=title,
            authors=authors, year=year, venue=venue, doi=w.get("DOI") or "",
            url=w.get("URL") or "", abstract_avail=bool(w.get("abstract")),
            language=w.get("language") or ""))
    return raw, norm, reached, err


def query_semantic_scholar(group, query, n):
    fields = "title,year,authors,venue,externalIds,abstract,publicationTypes"
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?query=%s"
           "&limit=%d&fields=%s"
           % (urllib.parse.quote(query), min(n, 100), fields))
    data, reached, err = http_get_json(url)
    raw, norm = [], []
    for w in ((data or {}).get("data") or []):
        raw.append({"query_group": group, "query": query, "record": w})
        authors = [a.get("name", "") for a in (w.get("authors") or [])]
        doi = (w.get("externalIds") or {}).get("DOI", "") or ""
        norm.append(_normalize(
            source="semantic_scholar", group=group, query=query,
            title=w.get("title") or "", authors=authors, year=w.get("year"),
            venue=w.get("venue") or "", doi=doi,
            url=("https://doi.org/" + doi) if doi else (w.get("url") or ""),
            abstract_avail=bool(w.get("abstract")), language=""))
    return raw, norm, reached, err


def query_cinii(group, query, n, appid):
    url = ("https://cir.nii.ac.jp/opensearch/all?q=%s&count=%d&format=json&appid=%s"
           % (urllib.parse.quote(query), n, urllib.parse.quote(appid)))
    data, reached, err = http_get_json(url)
    raw, norm = [], []
    for w in ((data or {}).get("items") or []):
        raw.append({"query_group": group, "query": query, "record": w})
        title = w.get("title") or ""
        doi = ""
        norm.append(_normalize(
            source="cinii", group=group, query=query, title=title,
            authors=[], year=None, venue=w.get("dc:publisher", ""), doi=doi,
            url=w.get("link", {}).get("@id", "") if isinstance(w.get("link"), dict) else "",
            abstract_avail=False, language="ja"))
    return raw, norm, reached, err


def _normalize(source, group, query, title, authors, year, venue, doi, url,
               abstract_avail, language):
    title = (title or "").strip()
    venue = (venue or "").strip()
    blob = " ".join([title, venue])
    country = "Japan" if any(t in blob.lower() for t in KW["tokyo_japan"]) else ""
    city = "Tokyo" if "tokyo" in blob.lower() else ""
    pop = ""
    if any(t in blob.lower() for t in KW["chinese"]):
        pop = "Chinese"
    elif any(t in blob.lower() for t in KW["non_chinese_comparison"]):
        pop = "foreign residents"
    concept = ";".join(_scan(blob, ["opportunity_risk", "theory", "housing",
                                     "service", "disaster", "transit",
                                     "arrival_infra"]))
    method = ";".join(_scan(blob, ["method"]))
    return {
        "source_api": source,
        "query_group": group,
        "query_string": query,
        "title": title,
        "authors": "; ".join([a for a in authors if a]),
        "year": year if year is not None else "",
        "venue": venue,
        "doi": (doi or "").strip(),
        "url": (url or "").strip(),
        "abstract_or_summary_available": "yes" if abstract_avail else "no",
        "language": language or "",
        "country_or_region_hint": country,
        "city_or_study_area_hint": city,
        "population_group_hint": pop,
        "core_concept_hint": concept,
        "method_hint": method,
    }


SCHEMA_COLUMNS = [
    "record_id", "source_api", "query_group", "query_string", "title",
    "authors", "year", "venue", "doi", "url",
    "abstract_or_summary_available", "language", "country_or_region_hint",
    "city_or_study_area_hint", "population_group_hint", "core_concept_hint",
    "method_hint", "overlap_flags", "preliminary_overlap_category",
    "verification_status", "notes",
]


def main():
    args = build_arg_parser().parse_args()
    root = Path(args.project_root)
    out_dir = root / "outputs" / "literature_discovery" / args.run_id
    raw_dir = out_dir / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    cinii_appid = os.environ.get("CINII_APP_ID", "").strip()

    # Source registry. CiNii only if an app id is present in the environment.
    sources = [
        ("openalex", query_openalex, {}),
        ("crossref", query_crossref, {}),
        ("semantic_scholar", query_semantic_scholar, {}),
    ]
    if cinii_appid:
        sources.append(("cinii", lambda g, q, n: query_cinii(g, q, n, cinii_appid), {}))

    available = {name: True for name, _, _ in sources}
    reached = {name: False for name, _, _ in sources}
    counts = {name: 0 for name, _, _ in sources}
    errors = {name: "" for name, _, _ in sources}

    raw_handles = {name: (raw_dir / ("%s.jsonl" % name)).open("w", encoding="utf-8",
                                                              newline="\n")
                   for name, _, _ in sources}

    normalized_all = []
    try:
        for group, query in QUERY_GROUPS:
            for name, fn, _ in sources:
                if not available[name]:
                    continue
                raw_items, norm_items, http_reached, err = fn(group, query, args.max_per_query)
                if http_reached:
                    reached[name] = True
                else:
                    # Network failure: stop hammering this source for the rest.
                    available[name] = False
                    errors[name] = err
                if err and not errors[name]:
                    errors[name] = err
                for r in raw_items:
                    raw_handles[name].write(json.dumps(r, ensure_ascii=True) + "\n")
                counts[name] += len(norm_items)
                normalized_all.extend(norm_items)
                time.sleep(0.5)  # be polite to public APIs
    finally:
        for h in raw_handles.values():
            h.close()

    # Deduplicate: DOI first, then normalized title.
    seen_doi, seen_title, deduped = {}, {}, []
    for rec in normalized_all:
        doi = rec.get("doi", "").lower().strip()
        nt = _norm_title(rec.get("title", ""))
        if doi and doi in seen_doi:
            continue
        if not doi and nt and nt in seen_title:
            continue
        if doi:
            seen_doi[doi] = True
        if nt:
            seen_title[nt] = True
        deduped.append(rec)

    # Assign ids + preliminary classification.
    for i, rec in enumerate(deduped, start=1):
        rec["record_id"] = "%s-%04d" % (args.run_id, i)
        flags, cat = classify(rec)
        rec["overlap_flags"] = ";".join(flags)
        rec["preliminary_overlap_category"] = cat
        rec["verification_status"] = "unverified_auto"
        rec["notes"] = "preliminary keyword triage; manual verification required"

    # candidates.csv
    cand_csv = out_dir / "candidates.csv"
    with cand_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for rec in deduped:
            w.writerow(rec)

    # candidates.jsonl
    with (out_dir / "candidates.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for rec in deduped:
            f.write(json.dumps(rec, ensure_ascii=True) + "\n")

    # direct-overlap candidate report
    a_list = [r for r in deduped if r["preliminary_overlap_category"] == "A_direct_overlap_candidate"]
    b_list = [r for r in deduped if r["preliminary_overlap_category"] == "B_partial_overlap_candidate"]
    lines = []
    lines.append("# Direct-Overlap Candidate Report (PRELIMINARY)")
    lines.append("")
    lines.append("Run id: %s" % args.run_id)
    lines.append("")
    lines.append("WARNING: This is automated keyword triage only. It is NOT")
    lines.append("evidence of a real overlap and does NOT confirm or deny the")
    lines.append("research gap. Every item below must be verified manually via")
    lines.append("DOI and publisher page, then deep-read in SciSpace.")
    lines.append("")
    lines.append("## A_direct_overlap_candidate (%d)" % len(a_list))
    lines.append("")
    if not a_list:
        lines.append("(none flagged in this run)")
    for r in a_list:
        lines.append("- %s | %s (%s) | DOI: %s | flags: %s"
                     % (r["record_id"], r["title"][:120], r["year"],
                        r["doi"] or "none", r["overlap_flags"]))
    lines.append("")
    lines.append("## B_partial_overlap_candidate (%d)" % len(b_list))
    lines.append("")
    if not b_list:
        lines.append("(none flagged in this run)")
    for r in b_list:
        lines.append("- %s | %s (%s) | DOI: %s | flags: %s"
                     % (r["record_id"], r["title"][:120], r["year"],
                        r["doi"] or "none", r["overlap_flags"]))
    lines.append("")
    (out_dir / "direct_overlap_candidates.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    # source coverage summary
    cat_counts = {}
    for r in deduped:
        cat_counts[r["preliminary_overlap_category"]] = cat_counts.get(
            r["preliminary_overlap_category"], 0) + 1
    s = []
    s.append("# Source Coverage Summary")
    s.append("")
    s.append("Run id: %s" % args.run_id)
    s.append("Max per query: %d" % args.max_per_query)
    s.append("Query groups: %d" % len(QUERY_GROUPS))
    s.append("")
    s.append("## APIs")
    for name, _, _ in sources:
        s.append("- %s: reached=%s, normalized_records=%d%s"
                 % (name, "YES" if reached[name] else "NO", counts[name],
                    ("" if not errors[name] else ", last_error=" + errors[name])))
    if not cinii_appid:
        s.append("- cinii: SKIPPED (no CINII_APP_ID in environment)")
    s.append("")
    s.append("## After dedup")
    s.append("- total normalized (pre-dedup): %d" % len(normalized_all))
    s.append("- unique candidates (post-dedup): %d" % len(deduped))
    s.append("")
    s.append("## Preliminary category counts")
    for k in ("A_direct_overlap_candidate", "B_partial_overlap_candidate",
              "C_theoretical_support_candidate", "D_method_support_candidate",
              "E_background_candidate", "uncertain"):
        s.append("- %s: %d" % (k, cat_counts.get(k, 0)))
    s.append("")
    s.append("NOTE: Categories are preliminary keyword triage and require")
    s.append("manual verification before any gap claim.")
    (out_dir / "source_coverage_summary.md").write_text(
        "\n".join(s) + "\n", encoding="utf-8", newline="\n")

    # run manifest (machine-readable, no credentials)
    manifest = {
        "run_id": args.run_id,
        "max_per_query": args.max_per_query,
        "query_groups": [g for g, _ in QUERY_GROUPS],
        "apis_reached": [name for name in reached if reached[name]],
        "apis_configured": [name for name, _, _ in sources],
        "cinii_enabled": bool(cinii_appid),
        "counts_per_api": counts,
        "total_pre_dedup": len(normalized_all),
        "unique_post_dedup": len(deduped),
        "category_counts": cat_counts,
    }
    (out_dir / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2), encoding="utf-8",
        newline="\n")

    print("RUN COMPLETE")
    print("output_dir:", out_dir)
    print("apis_reached:", ", ".join([n for n in reached if reached[n]]) or "none")
    print("unique_candidates:", len(deduped))
    for k in ("A_direct_overlap_candidate", "B_partial_overlap_candidate"):
        print("%s: %d" % (k, cat_counts.get(k, 0)))


if __name__ == "__main__":
    sys.exit(main())
