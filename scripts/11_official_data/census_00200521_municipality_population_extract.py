#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Census 00200521 BOUNDED municipality population extraction scaffold (Tokyo-China project).

Scope
-----
Extract, for the confirmed 251 municipality-equivalent areas of Tokyo, Saitama,
Chiba, and Kanagawa, the two Census categories needed for the population module:

    chinese_residents   = value for cat02 == 102 (China)   at cdCat01=0, cdTime=2020000000
    total_foreign       = value for cat02 == 1   (foreign)  at cdCat01=0, cdTime=2020000000
    non_chinese_foreign = total_foreign - chinese_residents

Future QC (NOT run here) must verify: chinese_residents <= total_foreign, and
non_chinese_foreign >= 0, at every municipality.

This is a SCAFFOLD. By itself it performs NO value retrieval. --dry-run and
--metadata-only are safe; the value-retrieving mode (--run-bounded-extraction) is
guarded and refuses to run unless explicitly forced, and is NOT exercised here.

Safety
------
* ESTAT_APP_ID is read from the environment ONLY; never printed/written/committed;
  no URL containing it is ever printed.
* --dry-run and --help need no appId and make no API call.
* --metadata-only calls getMetaInfo only (no data values, no raw save by default).
* --run-bounded-extraction refuses unless --force is ALSO given; refuses all-Japan;
  uses only cdArea from the confirmed area-code list; refuses if area count exceeds
  --max-areas; refuses to write raw output unless --allow-write-raw; and never writes
  raw output into a tracked public-repo path by default.
"""
import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request

ENDPOINT = "https://api.e-stat.go.jp/rest/3.0/app/json/"
DEFAULT_AREA_CSV = "literature/02_matrices/census_00200521_municipality_area_code_confirmation.csv"
DEFAULT_OUTDIR = "data_raw_official/census_00200521_2020_municipality"
# local-only / gitignored path prefixes that are acceptable for raw output
LOCAL_ONLY_PREFIXES = ("data_raw_official", "data_raw", "data_processed_official", "data_processed")


def build_parser():
    p = argparse.ArgumentParser(
        prog="census_00200521_municipality_population_extract.py",
        description="Bounded municipality population extraction scaffold for Census 00200521 "
                    "table 0003445244 (scaffold; value retrieval is guarded and deferred).",
    )
    p.add_argument("--project-root", default=".", help="Repo root for resolving relative paths.")
    p.add_argument("--dry-run", action="store_true",
                   help="Read the area-code CSV and report the plan. No API call; no appId needed.")
    p.add_argument("--metadata-only", action="store_true",
                   help="Call getMetaInfo only to verify dimensions/codes. No data values; no raw save.")
    p.add_argument("--run-bounded-extraction", action="store_true",
                   help="GUARDED future mode: bounded value retrieval. Refuses unless --force is also given.")
    p.add_argument("--stats-data-id", default="0003445244")
    p.add_argument("--cd-time", default="2020000000")
    p.add_argument("--cd-cat01", default="0")
    p.add_argument("--cat02-total", default="1")
    p.add_argument("--cat02-china", default="102")
    p.add_argument("--area-code-csv", default=DEFAULT_AREA_CSV,
                   help="Confirmed municipality area-code CSV (default the confirmation file).")
    p.add_argument("--target-prefectures", default="13,11,12,14",
                   help="Comma-separated prefecture codes (default Tokyo,Saitama,Chiba,Kanagawa).")
    p.add_argument("--outdir", default=DEFAULT_OUTDIR,
                   help="Local-only (gitignored) directory for raw output (only if explicitly authorized).")
    p.add_argument("--max-areas", type=int, default=300, help="Safety cap on number of areas (default 300).")
    p.add_argument("--timeout-seconds", type=int, default=60)
    p.add_argument("--allow-write-raw", action="store_true",
                   help="Permit writing raw output (only with --run-bounded-extraction --force).")
    p.add_argument("--force", action="store_true",
                   help="Required (with --run-bounded-extraction) to actually retrieve values.")
    p.add_argument("--run-controlled-value-test", action="store_true",
                   help="Tiny controlled getStatsData test over --test-areas only (max --max-test-areas). "
                        "Sanitized summary only; no raw output saved.")
    p.add_argument("--test-areas", default="",
                   help="Comma-separated area codes for the controlled value test (required for that mode).")
    p.add_argument("--max-test-areas", type=int, default=10,
                   help="Hard cap on controlled-test area count (default 10).")
    return p


def get_app_id():
    return os.environ.get("ESTAT_APP_ID", "").strip()


def _api_get(method, params, timeout):
    """Call an e-Stat API method. appId is added here and is NEVER printed or returned."""
    q = dict(params)
    q["appId"] = get_app_id()
    url = ENDPOINT + method + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": "census-bounded-extract-scaffold"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _safe(d, *keys, default=None):
    for k in keys:
        d = d[k] if isinstance(d, dict) and k in d else None
        if d is None:
            return default
    return d


def load_target_areas(args):
    """Read the confirmed area-code CSV; return included municipality areas for the target prefectures."""
    path = os.path.join(args.project_root, args.area_code_csv)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"area-code CSV not found: {path}")
    target_prefs = [p.strip() for p in args.target_prefectures.split(",") if p.strip()]
    areas = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("included_in_target_scope", "").strip() != "yes":
                continue
            if row.get("prefecture_code", "").strip() not in target_prefs:
                continue
            areas.append({
                "code": str(row.get("municipality_code", "")).strip(),
                "prefecture": row.get("prefecture_name", "").strip(),
                "prefecture_code": row.get("prefecture_code", "").strip(),
                "type": row.get("municipality_type", "").strip(),
            })
    return areas


def _pref_counts(areas):
    from collections import Counter
    return dict(Counter(a["prefecture"] for a in areas))


def cmd_dry_run(args):
    print("=== Census 00200521 bounded extraction scaffold : DRY RUN ===")
    print("mode: dry-run (NO API call; NO appId required; NO appId printed; NO values; NO raw write)")
    print("project-root:", os.path.abspath(args.project_root))
    areas = load_target_areas(args)
    counts = _pref_counts(areas)
    print("area-code source:", args.area_code_csv)
    print("target prefectures:", args.target_prefectures)
    print("TARGET AREA COUNT (included_in_target_scope=yes):", len(areas))
    for pref in ("Tokyo", "Saitama", "Chiba", "Kanagawa"):
        print(f"  {pref}: {counts.get(pref, 0)}")
    print("max-areas cap:", args.max_areas, "| within cap:", len(areas) <= args.max_areas)
    print("parameters:")
    print(f"  statsDataId={args.stats_data_id} cdTime={args.cd_time} cdCat01={args.cd_cat01}")
    print(f"  cat02_total={args.cat02_total} cat02_china={args.cat02_china}")
    print("variable logic: non_chinese_foreign = total_foreign(cat02=%s) - chinese(cat02=%s)"
          % (args.cat02_total, args.cat02_china))
    print("planned output dir (local-only; not written in this mode):", args.outdir)
    print("planned output files (future): chinese_residents.csv, total_foreign.csv, "
          "non_chinese_foreign.csv (local-only)")
    print("ESTAT_APP_ID present:", "yes" if get_app_id() else "no", "(not needed for dry-run)")
    print("=== DRY RUN OK ===")
    return 0


def cmd_metadata_only(args):
    app = get_app_id()
    if not app:
        print("ERROR: ESTAT_APP_ID not set; metadata-only needs it. Use --dry-run for an offline check.")
        return 3
    print("=== Census 00200521 bounded extraction scaffold : METADATA-ONLY ===")
    print("mode: metadata-only (getMetaInfo; NO getStatsData; NO values; NO raw save)")
    try:
        m = _api_get("getMetaInfo", {"statsDataId": args.stats_data_id}, args.timeout_seconds)
    except Exception as e:
        print("getMetaInfo ERROR:", type(e).__name__, str(e)[:200]); return 6
    status = _safe(m, "GET_META_INFO", "RESULT", "STATUS")
    print("getMetaInfo STATUS:", status)
    if str(status) != "0":
        print("non-zero status; safe stop."); return 7
    cobjs = _safe(m, "GET_META_INFO", "METADATA_INF", "CLASS_INF", "CLASS_OBJ", default=[])
    if isinstance(cobjs, dict):
        cobjs = [cobjs]
    cat01, cat02, area, time_ = set(), set(), set(), set()
    for co in cobjs:
        cid = co.get("@id"); cls = co.get("CLASS", [])
        if isinstance(cls, dict):
            cls = [cls]
        codes = {str(c.get("@code")) for c in cls}
        if cid == "cat01": cat01 = codes
        elif cid == "cat02": cat02 = codes
        elif cid == "area": area = codes
        elif cid == "time": time_ = codes
    print("  cat01 sex-total code", args.cd_cat01, "present:", args.cd_cat01 in cat01)
    print("  cat02 China code", args.cat02_china, "present:", args.cat02_china in cat02)
    print("  cat02 foreign-total code", args.cat02_total, "present:", args.cat02_total in cat02)
    print("  time code", args.cd_time, "present:", args.cd_time in time_)
    # cross-check the confirmed target areas against the live area dimension
    try:
        areas = load_target_areas(args)
        present = sum(1 for a in areas if a["code"] in area)
        print(f"  confirmed target areas present in live area dim: {present}/{len(areas)}")
    except Exception as e:
        print("  (could not cross-check area list:", str(e)[:120], ")")
    print("=== METADATA-ONLY DONE (no data values retrieved; no raw output saved) ===")
    return 0


def cmd_bounded_extraction(args):
    """GUARDED future value-retrieval mode. Refuses unless explicitly forced and bounded."""
    if not args.force:
        print("REFUSED: --run-bounded-extraction requires --force (explicit authorization). No values retrieved.")
        return 11
    areas = load_target_areas(args)
    if not areas:
        print("REFUSED: no target areas loaded."); return 12
    # refuse all-Japan / anything not strictly from the confirmed bounded list
    target_prefs = {p.strip() for p in args.target_prefectures.split(",") if p.strip()}
    if target_prefs != {"13", "11", "12", "14"}:
        print("REFUSED: target prefectures are not the confirmed bounded set (13,11,12,14)."); return 13
    if len(areas) > args.max_areas:
        print(f"REFUSED: area count {len(areas)} exceeds --max-areas {args.max_areas} (bulk guard)."); return 14
    out = os.path.normpath(args.outdir).replace("\\", "/")
    if args.allow_write_raw:
        if not any(out == pfx or out.startswith(pfx + "/") for pfx in LOCAL_ONLY_PREFIXES):
            print(f"REFUSED: outdir '{out}' is not a known local-only/gitignored path; refusing to write raw."); return 15
    print("Bounded extraction is authorized by flags but value retrieval is intentionally NOT performed by")
    print("this scaffold task. Implement/enable the getStatsData calls in the controlled value-extraction")
    print("test batch. (chinese=cat02 102, total=cat02 1, cdCat01=0, cdTime per --cd-time, cdArea=confirmed list.)")
    print("raw output saved:", "permitted-but-not-written" if args.allow_write_raw else "NO (allow-write-raw not set)")
    return 0


def cmd_controlled_value_test(args):
    """Tiny controlled getStatsData test over --test-areas ONLY (<= --max-test-areas).
    Retrieves at most (n areas x 2 categories) value rows for QC; prints a sanitized
    summary only; saves NO raw output; never the full 251-area or all-Japan set."""
    app = get_app_id()
    if not app:
        print("ERROR: ESTAT_APP_ID not set; controlled value test needs it. Aborting safely."); return 3
    test_codes = [c.strip() for c in args.test_areas.split(",") if c.strip()]
    if not test_codes:
        print("REFUSED: --run-controlled-value-test requires --test-areas (comma-separated codes)."); return 21
    if len(test_codes) > args.max_test_areas:
        print(f"REFUSED: {len(test_codes)} test areas exceed --max-test-areas {args.max_test_areas}."); return 22
    # every test area MUST be a confirmed, in-scope municipality (blocks all-Japan / arbitrary codes)
    confirmed = {a["code"] for a in load_target_areas(args)}
    if len(confirmed) >= 251 and len(test_codes) >= 200:
        print("REFUSED: this is the controlled small-test mode; it will not run a near-full area set."); return 23
    not_confirmed = [c for c in test_codes if c not in confirmed]
    if not_confirmed:
        print(f"REFUSED: test areas not in confirmed in-scope list: {not_confirmed}"); return 24

    print("=== Census 00200521 controlled value-extraction test ===")
    print("mode: run-controlled-value-test (tiny getStatsData; sanitized summary only; NO raw output saved)")
    print(f"statsDataId={args.stats_data_id} cdTime={args.cd_time} cdCat01={args.cd_cat01} "
          f"cat02={args.cat02_total},{args.cat02_china}")
    print(f"test areas ({len(test_codes)}):", ",".join(test_codes))
    params = {
        "statsDataId": args.stats_data_id,
        "cdCat01": args.cd_cat01,
        "cdCat02": ",".join([args.cat02_total, args.cat02_china]),
        "cdArea": ",".join(test_codes),
        "cdTime": args.cd_time,
        "metaGetFlg": "N", "cntGetFlg": "N", "lang": "J",
    }
    try:
        d = _api_get("getStatsData", params, args.timeout_seconds)
    except Exception as e:
        print("getStatsData ERROR:", type(e).__name__, str(e)[:200]); return 25
    status = _safe(d, "GET_STATS_DATA", "RESULT", "STATUS")
    values = _safe(d, "GET_STATS_DATA", "STATISTICAL_DATA", "DATA_INF", "VALUE", default=[])
    if isinstance(values, dict):
        values = [values]
    # parse into per-area {cat02: int}; do NOT print raw values
    per_area = {}
    cats_seen, areas_seen = set(), set()
    for v in values:
        area = str(v.get("@area")); cat = str(v.get("@cat02")); raw = v.get("$", "")
        areas_seen.add(area); cats_seen.add(cat)
        try:
            num = int(str(raw).replace(",", ""))
        except (ValueError, TypeError):
            num = None
        per_area.setdefault(area, {})[cat] = num
    # QC gates (computed internally; only booleans/counts reported)
    qc_chinese_le_total = True
    qc_nonneg = True
    missing_cat = 0
    for area in test_codes:
        cells = per_area.get(area, {})
        total = cells.get(args.cat02_total)
        china = cells.get(args.cat02_china)
        if total is None or china is None:
            missing_cat += 1
            continue
        if not (china <= total):
            qc_chinese_le_total = False
        if (total - china) < 0:
            qc_nonneg = False
    missing_area = sum(1 for a in test_codes if a not in areas_seen)
    result = {
        "api_reached": True,
        "response_status": str(status),
        "actual_rows": len(values),
        "areas_returned": len(areas_seen),
        "categories_returned": len(cats_seen),
        "qc_chinese_le_total": qc_chinese_le_total,
        "qc_nonneg": qc_nonneg,
        "missing_area_count": missing_area,
        "missing_category_count": missing_cat,
    }
    print("response status:", result["response_status"])
    print("actual value rows retrieved:", result["actual_rows"])
    print("areas returned:", result["areas_returned"], "| categories returned:", result["categories_returned"])
    print("QC chinese <= total_foreign:", result["qc_chinese_le_total"])
    print("QC non_chinese_foreign >= 0:", result["qc_nonneg"])
    print("missing areas:", result["missing_area_count"], "| missing categories:", result["missing_category_count"])
    print("raw output saved: NO | appId exposed: NO | values printed: NO (sanitized booleans/counts only)")
    print("RESULT_JSON:", json.dumps(result, sort_keys=True))
    print("=== CONTROLLED VALUE TEST DONE (no raw output saved) ===")
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    modes = [args.dry_run, args.metadata_only, args.run_bounded_extraction, args.run_controlled_value_test]
    if sum(bool(x) for x in modes) > 1:
        print("ERROR: choose exactly one of --dry-run / --metadata-only / "
              "--run-bounded-extraction / --run-controlled-value-test."); return 2
    if args.run_controlled_value_test:
        return cmd_controlled_value_test(args)
    if args.run_bounded_extraction:
        return cmd_bounded_extraction(args)
    if args.metadata_only:
        return cmd_metadata_only(args)
    # default safe behavior is dry-run
    return cmd_dry_run(args)


if __name__ == "__main__":
    sys.exit(main())
