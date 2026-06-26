#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Census 00200521 small metadata/count test scaffold (Tokyo-China project).

Purpose
-------
Verify, with the SMALLEST possible official e-Stat API touch, that the confirmed
2020 Population Census table can support the population module:

    chinese_residents   = cat02 == 102 (China)
    total_foreign       = cat02 == 1   (foreign total)
    non_chinese_foreign = total_foreign - chinese_residents

This is a METADATA / COUNT test only. It NEVER performs a full extraction, never
retrieves all municipalities or all categories, and never saves raw API output.

Confirmed parameters (from the exact-table confirmation batch):
    statistics code : 00200521
    tstat           : 000001136464  (2020 Basic Complete Tabulation)
    statsDataId     : 0003445244    ("Foreigners: population by sex and nationality
                                      - national, prefecture, municipality")
    time            : 2020000000    (2020)
    sex total       : cat01 = 0
    foreign total   : cat02 = 1
    China           : cat02 = 102
    sample areas    : 13101 (Chiyoda-ku), 11201 (Kawagoe-shi),
                      12101 (Chiba-shi Chuo-ku), 14101 (Yokohama-shi Tsurumi-ku)

Safety
------
* ESTAT_APP_ID is read from the environment ONLY.
* The appId is NEVER printed, written to a file, or included in any printed URL.
* --dry-run makes NO API call and needs NO appId.
* --run-count-test issues only a tiny controlled request:
    - getMetaInfo (dimension/category metadata), and
    - getStatsData with cntGetFlg=Y (returns ONLY a record COUNT, no data values).
  No data values are retrieved; no raw response is saved.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

ENDPOINT = "https://api.e-stat.go.jp/rest/3.0/app/json/"
MAX_TEST_AREAS = 20  # hard cap: refuse anything that looks like a bulk pull


def build_parser():
    p = argparse.ArgumentParser(
        prog="census_00200521_small_metadata_test.py",
        description="Tiny metadata/count test for Census 00200521 table 0003445244 "
                    "(metadata only; no full extraction; no raw output saved).",
    )
    p.add_argument("--project-root", default=".",
                   help="Repo root (used only to anchor/validate paths; no data is written by default).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the planned parameters only. No API call. No appId needed or printed.")
    p.add_argument("--run-count-test", action="store_true",
                   help="Run the tiny metadata + count test (getMetaInfo + getStatsData cntGetFlg=Y).")
    p.add_argument("--stats-data-id", default="0003445244", help="Census statsDataId (default 0003445244).")
    p.add_argument("--cd-time", default="2020000000", help="Time code (default 2020000000 = 2020).")
    p.add_argument("--cd-cat01", default="0", help="Sex category code (default 0 = total).")
    p.add_argument("--china-cat02", default="102", help="China nationality code (default 102).")
    p.add_argument("--foreign-total-cat02", default="1", help="Foreign-total nationality code (default 1).")
    p.add_argument("--test-areas", default="13101,11201,12101,14101",
                   help="Comma-separated sample area codes (default 4 Tokyo-metro municipalities).")
    p.add_argument("--timeout-seconds", type=int, default=60, help="HTTP timeout per call (default 60).")
    return p


def get_app_id():
    return os.environ.get("ESTAT_APP_ID", "").strip()


def _api_get(method, params, timeout):
    """Call an e-Stat API method. appId is added here and NEVER printed or returned."""
    q = dict(params)
    q["appId"] = get_app_id()
    url = ENDPOINT + method + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": "census-small-metadata-test"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _safe(d, *keys, default=None):
    for k in keys:
        d = d[k] if isinstance(d, dict) and k in d else None
        if d is None:
            return default
    return d


def _planned_params(args):
    return {
        "statistics_code": "00200521",
        "tstat": "000001136464",
        "statsDataId": args.stats_data_id,
        "cdTime": args.cd_time,
        "cdCat01_sex_total": args.cd_cat01,
        "cdCat02_china": args.china_cat02,
        "cdCat02_foreign_total": args.foreign_total_cat02,
        "test_areas": args.test_areas,
        "timeout_seconds": args.timeout_seconds,
        "variable_logic": "non_chinese_foreign = total_foreign(cat02=%s) - chinese(cat02=%s)"
                          % (args.foreign_total_cat02, args.china_cat02),
    }


def cmd_dry_run(args):
    print("=== Census 00200521 small metadata/count test : DRY RUN ===")
    print("mode: dry-run (NO API call; NO appId required; NO appId printed)")
    print("project-root:", os.path.abspath(args.project_root),
          "(exists)" if os.path.isdir(args.project_root) else "(MISSING)")
    print("ESTAT_APP_ID present in env:", "yes" if get_app_id() else "no")
    print("planned API methods (when --run-count-test): getMetaInfo, getStatsData(cntGetFlg=Y)")
    print("planned parameters:")
    for k, v in _planned_params(args).items():
        print(f"  {k} = {v}")
    areas = [a for a in args.test_areas.split(",") if a.strip()]
    print(f"test area count: {len(areas)} (cap {MAX_TEST_AREAS})")
    print("NOTE: count test retrieves NO data values (cntGetFlg=Y) and saves NO raw output.")
    print("=== DRY RUN OK ===")
    return 0


def cmd_count_test(args):
    app = get_app_id()
    if not app:
        print("ERROR: ESTAT_APP_ID is not set in the environment. Cannot run the count test.")
        print("Set ESTAT_APP_ID (environment only) and retry, or use --dry-run.")
        return 3
    areas = [a.strip() for a in args.test_areas.split(",") if a.strip()]
    if not areas:
        print("ERROR: no test areas provided."); return 4
    if len(areas) > MAX_TEST_AREAS:
        print(f"ERROR: {len(areas)} test areas exceeds safety cap {MAX_TEST_AREAS}; refusing (looks like bulk).")
        return 5

    print("=== Census 00200521 small metadata/count test : RUN ===")
    print("mode: run-count-test (metadata + cntGetFlg=Y; NO data values; NO raw output saved)")
    print("statsDataId:", args.stats_data_id, "| cdTime:", args.cd_time, "| areas:", len(areas))

    # ---- 1. getMetaInfo: verify category/area/time codes exist ----
    try:
        m = _api_get("getMetaInfo", {"statsDataId": args.stats_data_id}, args.timeout_seconds)
    except Exception as e:
        print("getMetaInfo ERROR:", type(e).__name__, str(e)[:200]); return 6
    mstatus = _safe(m, "GET_META_INFO", "RESULT", "STATUS")
    print("getMetaInfo STATUS:", mstatus)
    if str(mstatus) != "0":
        print("getMetaInfo non-zero status; aborting safely."); return 7

    cobjs = _safe(m, "GET_META_INFO", "METADATA_INF", "CLASS_INF", "CLASS_OBJ", default=[])
    if isinstance(cobjs, dict):
        cobjs = [cobjs]
    cat02_codes, area_codes, time_codes = set(), set(), set()
    for co in cobjs:
        cid = co.get("@id")
        cls = co.get("CLASS", [])
        if isinstance(cls, dict):
            cls = [cls]
        codes = {str(c.get("@code")) for c in cls}
        if cid == "cat02":
            cat02_codes = codes
        elif cid == "area":
            area_codes = codes
        elif cid == "time":
            time_codes = codes

    china_ok = args.china_cat02 in cat02_codes
    total_ok = args.foreign_total_cat02 in cat02_codes
    time_ok = args.cd_time in time_codes
    areas_present = [a for a in areas if a in area_codes]
    print(f"  China code {args.china_cat02} present in cat02: {china_ok}")
    print(f"  Foreign-total code {args.foreign_total_cat02} present in cat02: {total_ok}")
    print(f"  Time code {args.cd_time} present: {time_ok}")
    print(f"  Test areas present in area dim: {len(areas_present)}/{len(areas)}")

    if not (china_ok and total_ok and time_ok and areas_present):
        print("Metadata check incomplete; not issuing count request. (Safe stop.)")
        return 8

    # ---- 2. getStatsData with cntGetFlg=Y : COUNT ONLY (no data values) ----
    params = {
        "statsDataId": args.stats_data_id,
        "cdCat01": args.cd_cat01,
        "cdCat02": ",".join([args.foreign_total_cat02, args.china_cat02]),
        "cdArea": ",".join(areas_present),
        "cdTime": args.cd_time,
        "cntGetFlg": "Y",     # <-- returns COUNT only; NO data values
        "metaGetFlg": "N",
        "lang": "J",
    }
    try:
        d = _api_get("getStatsData", params, args.timeout_seconds)
    except Exception as e:
        print("getStatsData(count) ERROR:", type(e).__name__, str(e)[:200]); return 9
    dstatus = _safe(d, "GET_STATS_DATA", "RESULT", "STATUS")
    total_number = _safe(d, "GET_STATS_DATA", "STATISTICAL_DATA", "RESULT_INF", "TOTAL_NUMBER")
    print("getStatsData(cntGetFlg=Y) STATUS:", dstatus)
    print("matching cell COUNT (no values retrieved):", total_number)
    expected = len(areas_present) * 2  # 2 categories x 1 sex x 1 time
    print(f"expected approx (areas x 2 categories): {expected}")
    ok = (str(dstatus) == "0") and (total_number is not None) and int(total_number) > 0
    print("COUNT TEST RESULT:", "PASS" if ok else "INCONCLUSIVE")
    print("construction feasibility (china & total codes present, count>0):",
          "YES" if (china_ok and total_ok and ok) else "PENDING")
    print("=== RUN DONE (no data values retrieved; no raw output saved) ===")
    return 0 if ok else 10


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.dry_run and args.run_count_test:
        print("ERROR: choose either --dry-run or --run-count-test, not both."); return 2
    if args.run_count_test:
        return cmd_count_test(args)
    # default to dry-run behavior (safe) when neither or only --dry-run is given
    return cmd_dry_run(args)


if __name__ == "__main__":
    sys.exit(main())
