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


def main(argv=None):
    args = build_parser().parse_args(argv)
    modes = [args.dry_run, args.metadata_only, args.run_bounded_extraction]
    if sum(bool(x) for x in modes) > 1:
        print("ERROR: choose exactly one of --dry-run / --metadata-only / --run-bounded-extraction."); return 2
    if args.run_bounded_extraction:
        return cmd_bounded_extraction(args)
    if args.metadata_only:
        return cmd_metadata_only(args)
    # default safe behavior is dry-run
    return cmd_dry_run(args)


if __name__ == "__main__":
    sys.exit(main())
