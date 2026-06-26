#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Acquire 2021 Economic Census municipality establishment counts (e-Stat) and build
commercial_density for the 251 Greater Tokyo frame.

Source: e-Stat statistics 00200553 (Reiwa-3 / 2021 Economic Census for Business Activity,
establishment tabulation), table 0004005655 "industry(major), opening-period, management-
organization by private establishments and employees - national/prefecture/municipality".
Selection for a clean municipality establishment total:
    tab    = 102-2021  (jigyosho-su / establishment count)
    cat01  = AR        (all industries excl. public service)
    cat02  = 00        (opening period: total)
    cat03  = 0         (management organization: total)
    time   = 2021000000
    area   = the 251 frame municipality codes (JIS5 = N03_007)

commercial_density = establishment_count / area_km2 (area built locally from N03).

Safety: ESTAT_APP_ID is read from the environment ONLY; never printed/written/committed.
Raw API JSON is written local-only under data_raw_official/ (gitignored). Only compact
QC is committed by the caller.

Usage:
    python economic_census_establishments_extract.py --project-root E:\\rsch\\laborJapan
"""
import argparse
import csv
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.e-stat.go.jp/rest/3.0/app/json/"
STATS_DATA_ID = "0004005655"
TAB = "102-2021"   # establishment count
CAT01 = "AR"       # all industries excl public service
CAT02 = "00"       # opening period total
CAT03 = "0"        # management organization total
CD_TIME = "2021000000"


def app_id():
    return os.environ.get("ESTAT_APP_ID", "").strip()


def api(method, params, timeout=90):
    q = dict(params); q["appId"] = app_id()
    url = ENDPOINT + method + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": "econ-census-establishments"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--query-date", required=True, help="YYYY-MM-DD stamp for raw filename")
    args = ap.parse_args()
    root = Path(args.project_root)
    if not app_id():
        raise SystemExit("ERROR: ESTAT_APP_ID not set in environment; cannot acquire.")

    # frame + area
    isa = list(csv.DictReader(open(
        root/"data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv",
        encoding="utf-8")))
    frame = {r["municipality_code"]: (r["prefecture_code"], r["municipality_name"]) for r in isa}
    codes = sorted(frame)
    area = {}
    for r in csv.DictReader(open(
            root/"data_processed_official/model_panel/tokyo_china_municipality_area_251_local_only.csv",
            encoding="utf-8")):
        v = r["area_km2"]; area[r["municipality_code"]] = float(v) if v not in ("", None) else None

    # retrieve establishment counts (chunked cdArea)
    raw_payloads = []
    est = {}
    for chunk in chunks(codes, 100):
        params = {
            "statsDataId": STATS_DATA_ID, "cdTab": TAB, "cdCat01": CAT01,
            "cdCat02": CAT02, "cdCat03": CAT03, "cdTime": CD_TIME,
            "cdArea": ",".join(chunk), "metaGetFlg": "N", "cntGetFlg": "N", "lang": "J",
        }
        d = api("getStatsData", params)
        raw_payloads.append(d)
        status = d.get("GET_STATS_DATA", {}).get("RESULT", {}).get("STATUS")
        if str(status) != "0":
            raise SystemExit(f"getStatsData non-zero status {status}: "
                             f"{d.get('GET_STATS_DATA',{}).get('RESULT',{}).get('ERROR_MSG','')}")
        vals = d.get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {}).get("DATA_INF", {}).get("VALUE", [])
        if isinstance(vals, dict):
            vals = [vals]
        for v in vals:
            a = str(v.get("@area")); raw = str(v.get("$", "")).replace(",", "")
            try:
                est[a] = int(raw)
            except ValueError:
                est[a] = None

    # save raw local-only (gitignored)
    raw_dir = root/"data_raw_official/economic_census_establishments"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir/f"raw_getStatsData_{STATS_DATA_ID}_2021_{args.query_date}.json"
    raw_path.write_text(json.dumps(raw_payloads, ensure_ascii=False), encoding="utf-8")
    print(f"[local-only] raw saved: {raw_path}")

    # build processed local-only table + QC
    panel_dir = root/"data_processed_official/model_panel"
    panel_dir.mkdir(parents=True, exist_ok=True)
    proc_path = panel_dir/"tokyo_china_commercial_density_251_local_only.csv"
    out_dir = root/"outputs/modeling/dfm01_mvp"
    out_dir.mkdir(parents=True, exist_ok=True)
    qc_path = out_dir/"dfm01_mvp_commercial_density_build_qc_summary.csv"

    proc_rows, qc_rows = [], []
    n_est = n_dens = 0
    for c in codes:
        pref, name = frame[c]
        e = est.get(c); a = area.get(c)
        dens = (e / a) if (e is not None and a not in (None, 0)) else None
        if e is not None: n_est += 1
        if dens is not None: n_dens += 1
        proc_rows.append({
            "municipality_code": c, "municipality_name": name, "prefecture": pref,
            "establishment_count": "" if e is None else e,
            "area_km2": "" if a is None else round(a, 6),
            "commercial_density": "" if dens is None else round(dens, 6),
            "economic_census_year": "2021",
            "source_table_id": STATS_DATA_ID,
            "source_provider": "e-Stat / Statistics Bureau (Reiwa-3 Economic Census for Business Activity)",
            "notes": "tab=102-2021 jigyosho-su; cat01=AR all-industries-excl-public-service; cat02/03 totals",
        })
        qc_rows.append({
            "municipality_code": c, "municipality_name": name, "prefecture": pref,
            "establishment_count_available": "YES" if e is not None else "NO",
            "area_km2_available": "YES" if a is not None else "NO",
            "commercial_density_available": "YES" if dens is not None else "NO",
            "establishment_count": "" if e is None else e,
            "commercial_density": "" if dens is None else round(dens, 2),
            "source_table_id": STATS_DATA_ID, "economic_census_year": "2021",
            "notes": "establishments/area_km2" if dens is not None else "missing establishment or area",
        })

    with open(proc_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(proc_rows[0].keys())); w.writeheader(); w.writerows(proc_rows)
    with open(qc_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(qc_rows[0].keys())); w.writeheader(); w.writerows(qc_rows)
    print(f"[local-only] commercial density table: {proc_path}")
    print(f"[committable] commercial density QC: {qc_path}")
    print(f"establishment_count: {n_est}/{len(codes)} ; commercial_density: {n_dens}/{len(codes)}")


if __name__ == "__main__":
    main()
