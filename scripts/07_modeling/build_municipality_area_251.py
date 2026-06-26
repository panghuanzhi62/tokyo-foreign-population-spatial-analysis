"""Derive municipality area_km2 for the 251 Greater Tokyo frame from the existing
local N03-20250101 boundary layer (no download). Geodesic area is used (ellipsoidal,
zone-independent) so the Tokyo islands (Izu/Ogasawara) are handled correctly.

LOCAL-ONLY output:
  data_processed_official/model_panel/tokyo_china_municipality_area_251_local_only.csv
COMMITTABLE QC:
  outputs/modeling/dfm01_mvp/dfm01_mvp_area_build_qc_summary.csv

Usage:
    python build_municipality_area_251.py --project-root E:\\rsch\\laborJapan
"""
import argparse
import csv
from pathlib import Path

import geopandas as gpd
from pyproj import Geod
from shapely.validation import make_valid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    args = ap.parse_args()
    root = Path(args.project_root)

    # 251 frame
    isa = list(csv.DictReader(open(
        root/"data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv",
        encoding="utf-8")))
    frame = {}
    for r in isa:
        frame[r["municipality_code"]] = (r["prefecture_code"], r["municipality_name"])
    codes = sorted(frame)

    shp = root/"data_raw/N03-20250101_GML/N03-20250101.shp"
    where = "N03_007 LIKE '11%' OR N03_007 LIKE '12%' OR N03_007 LIKE '13%' OR N03_007 LIKE '14%'"
    print("reading N03 (filtered to prefectures 11-14)...")
    try:
        gdf = gpd.read_file(shp, columns=["N03_007"], where=where)
    except Exception as e:  # fallback: read all then filter
        print("where-filter read failed, reading full layer:", e)
        gdf = gpd.read_file(shp, columns=["N03_007"])
        gdf = gdf[gdf["N03_007"].astype(str).str.slice(0, 2).isin(["11","12","13","14"])]
    print("rows read:", len(gdf), "crs:", gdf.crs)

    gdf["code"] = gdf["N03_007"].astype(str).str.zfill(5)
    gdf = gdf[gdf["code"].isin(set(codes))].copy()
    print("rows in 251 frame:", len(gdf), "distinct codes:", gdf["code"].nunique())

    # dissolve multipart / ward polygons by municipality code
    diss = gdf.dissolve(by="code", as_index=False)
    # ensure geographic CRS for geodesic area
    diss = diss.to_crs(4326)

    geod = Geod(ellps="WGS84")
    area_km2 = {}
    valid_flag = {}
    for _, row in diss.iterrows():
        geom = row.geometry
        ok = "YES"
        if geom is None:
            area_km2[row["code"]] = None; valid_flag[row["code"]] = "NO"; continue
        if not geom.is_valid:
            geom = make_valid(geom); ok = "repaired"
        a, _p = geod.geometry_area_perimeter(geom)
        area_km2[row["code"]] = abs(a)/1e6
        valid_flag[row["code"]] = ok

    # write local-only area table + QC
    panel_dir = root/"data_processed_official/model_panel"
    panel_dir.mkdir(parents=True, exist_ok=True)
    local_path = panel_dir/"tokyo_china_municipality_area_251_local_only.csv"
    out_dir = root/"outputs/modeling/dfm01_mvp"
    out_dir.mkdir(parents=True, exist_ok=True)
    qc_path = out_dir/"dfm01_mvp_area_build_qc_summary.csv"

    local_rows, qc_rows = [], []
    n_avail = 0
    for code in codes:
        pref, name = frame[code]
        a = area_km2.get(code)
        avail = "YES" if a is not None else "NO"
        if a is not None:
            n_avail += 1
        local_rows.append({"municipality_code": code, "municipality_name": name,
                           "prefecture": pref, "area_km2": "" if a is None else round(a, 6)})
        qc_rows.append({
            "municipality_code": code, "municipality_name": name, "prefecture": pref,
            "area_km2_available": avail, "area_km2": "" if a is None else round(a, 4),
            "source_layer": "data_raw/N03-20250101_GML/N03-20250101.shp",
            "crs_used": "geodesic WGS84 (Geod ellps=WGS84) after to_crs(4326)",
            "geometry_valid": valid_flag.get(code, "NO"),
            "notes": "dissolved by N03_007; ward-level codes for designated cities" if a is not None
                     else "code not found in N03 layer"})

    with open(local_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(local_rows[0].keys())); w.writeheader(); w.writerows(local_rows)
    with open(qc_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(qc_rows[0].keys())); w.writeheader(); w.writerows(qc_rows)
    print(f"[local-only] area table: {local_path}")
    print(f"[committable] area QC: {qc_path}")
    print(f"AREA available: {n_avail}/{len(codes)}")


if __name__ == "__main__":
    main()
