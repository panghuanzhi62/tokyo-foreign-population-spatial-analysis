"""Build the DF_M01-only MVP X-M-Y model panel for the 251 Greater Tokyo frame.

This is the MVP panel builder for the temporally ordered design:
    X  = Chinese registered stock 2023-12
    M  = DF_M01 registered institutional support-organization count by municipality
         (registered_by_2024_12 primary; registered_by_2024_06 robustness)
    Y  = Chinese registered stock growth (2024-12 -> 2025-06 primary;
         2024-06 -> 2025-06 robustness)

M is defined CAUTIOUSLY as "institutional migrant-support service infrastructure
(registered institutional support organizations)" - NOT a complete migrant-service
ecosystem. DF_M02/DF_M03/DF_M04 are excluded from the main M by design.

The builder ASSEMBLES the inputs that exist at the official, processed,
municipality level for the 251 frame, and writes a machine-readable readiness
inventory. It DOES NOT invent proxies for missing controls and it does not
geocode. If required controls are absent, the readiness inventory records them as
MISSING and the downstream runner (run_dfm01_mvp_models.py) refuses to fit.

Outputs:
  LOCAL-ONLY (never committed):
    data_processed_official/model_panel/tokyo_china_dfm01_mvp_model_panel_local_only.csv
  COMMITTABLE:
    outputs/modeling/dfm01_mvp/model_readiness_inventory.csv

Usage:
    python build_dfm01_mvp_model_panel.py --project-root E:\\rsch\\laborJapan
"""
import argparse
import csv
import math
import statistics
from pathlib import Path

# Required model controls (must be processed, municipality-level, 251-frame).
REQUIRED_CONTROLS = [
    "rail_accessibility",
    "housing_cost",
    "commercial_density",
    "population_density",
    "non_chinese_foreign_stock",
]


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def zscore(values):
    """Population-style z standardization over non-missing values."""
    present = [v for v in values if v is not None]
    if len(present) < 2:
        return [None for _ in values]
    mu = statistics.fmean(present)
    sd = statistics.pstdev(present)
    if sd == 0:
        return [0.0 if v is not None else None for v in values]
    return [(v - mu) / sd if v is not None else None for v in values]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    args = ap.parse_args()
    root = Path(args.project_root)

    isa_path = root / "data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv"
    m01_06_path = root / "data_processed_official/service_infrastructure/DF_M01_registered_support_organizations/df_m01_counts_by_municipality_2024_06_30.csv"
    m01_12_path = root / "data_processed_official/service_infrastructure/DF_M01_registered_support_organizations/df_m01_counts_by_municipality_2024_12_31.csv"
    census_path = root / "data_processed_official/population/census_00200521_2020_municipality_population.csv"

    # ---- X / Y : ISA-MOJ Chinese registered stock panel (long -> wide) ----
    isa = load_csv(isa_path)
    stock = {}      # code -> {survey_time -> value}
    name = {}       # code -> municipality_name
    pref = {}       # code -> prefecture_code
    for r in isa:
        code = r["municipality_code"]
        stock.setdefault(code, {})[r["survey_time"]] = to_float(r["chinese_registered"])
        name[code] = r["municipality_name"]
        pref[code] = r["prefecture_code"]
    frame = sorted(stock.keys())

    # ---- M : DF_M01 support-organization counts ----
    m06 = {r["municipality_code"]: to_float(r["df_m01_count"]) for r in load_csv(m01_06_path)}
    m12 = {r["municipality_code"]: to_float(r["df_m01_count"]) for r in load_csv(m01_12_path)}

    # ---- Control that IS available: non-Chinese foreign stock (2020 census) ----
    ncf = {r["municipality_code"]: to_float(r["non_chinese_foreign"]) for r in load_csv(census_path)}

    # ---- Assemble per-municipality rows ----
    rows = []
    for code in frame:
        s = stock[code]
        x2023 = s.get("2023-12")
        y2406 = s.get("2024-06")
        y2412 = s.get("2024-12")
        y2506 = s.get("2025-06")
        row = {
            "municipality_code": code,
            "municipality_name": name.get(code, ""),
            "prefecture": pref.get(code, ""),
            "chinese_stock_2023_12": x2023,
            "chinese_stock_2024_06": y2406,
            "chinese_stock_2024_12": y2412,
            "chinese_stock_2025_06": y2506,
            "df_m01_support_count_2024_06": m06.get(code),
            "df_m01_support_count_2024_12": m12.get(code),
            # Required controls: only non_chinese_foreign_stock is available.
            "rail_accessibility": None,
            "housing_cost": None,
            "commercial_density": None,
            "population_density": None,
            "non_chinese_foreign_stock": ncf.get(code),
            "prefecture_fe": pref.get(code, ""),
        }
        # Derived
        row["log_chinese_stock_2023_12"] = math.log1p(x2023) if x2023 is not None else None
        row["log_service_2024_12"] = math.log1p(m12.get(code)) if m12.get(code) is not None else None
        row["log_service_2024_06"] = math.log1p(m06.get(code)) if m06.get(code) is not None else None
        if y2506 is not None and y2412 is not None:
            row["chinese_growth_log_2024_12_2025_06"] = math.log1p(y2506) - math.log1p(y2412)
            row["chinese_growth_abs_2024_12_2025_06"] = y2506 - y2412
        else:
            row["chinese_growth_log_2024_12_2025_06"] = None
            row["chinese_growth_abs_2024_12_2025_06"] = None
        if y2506 is not None and y2406 is not None:
            row["chinese_growth_log_2024_06_2025_06"] = math.log1p(y2506) - math.log1p(y2406)
            row["chinese_growth_abs_2024_06_2025_06"] = y2506 - y2406
        else:
            row["chinese_growth_log_2024_06_2025_06"] = None
            row["chinese_growth_abs_2024_06_2025_06"] = None
        rows.append(row)

    # ---- Z-standardize continuous predictors that exist ----
    z_specs = {
        "z_log_chinese_stock_2023_12": "log_chinese_stock_2023_12",
        "z_log_service_2024_12": "log_service_2024_12",
        "z_log_service_2024_06": "log_service_2024_06",
        "z_rail_accessibility": "rail_accessibility",
        "z_housing_cost": "housing_cost",
        "z_commercial_density": "commercial_density",
        "z_population_density": "population_density",
        "z_non_chinese_foreign_stock": "non_chinese_foreign_stock",
    }
    for zcol, src in z_specs.items():
        zs = zscore([r[src] for r in rows])
        for r, zv in zip(rows, zs):
            r[zcol] = zv

    # ---- Write LOCAL-ONLY panel ----
    panel_dir = root / "data_processed_official/model_panel"
    panel_dir.mkdir(parents=True, exist_ok=True)
    panel_path = panel_dir / "tokyo_china_dfm01_mvp_model_panel_local_only.csv"
    cols = list(rows[0].keys())
    with open(panel_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print(f"[local-only] wrote model panel: {panel_path} ({len(rows)} rows)")

    # ---- Readiness inventory (COMMITTABLE) ----
    def coverage(colname):
        present = sum(1 for r in rows if r.get(colname) is not None)
        return present

    inv = []
    inv.append({"input_role": "municipality_frame", "input_name": "251_greater_tokyo_frame",
                "status": "AVAILABLE", "n_present": len(rows), "n_expected": 251,
                "source_path": "data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv",
                "note": "251 municipalities, prefectures 11/12/13/14"})
    inv.append({"input_role": "X", "input_name": "chinese_stock_2023_12",
                "status": "AVAILABLE", "n_present": coverage("chinese_stock_2023_12"), "n_expected": 251,
                "source_path": "data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv",
                "note": "ISA-MOJ T2 panel"})
    for t in ["2024_06", "2024_12", "2025_06"]:
        inv.append({"input_role": "Y", "input_name": f"chinese_stock_{t}",
                    "status": "AVAILABLE", "n_present": coverage(f"chinese_stock_{t}"), "n_expected": 251,
                    "source_path": "data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv",
                    "note": "ISA-MOJ T2 panel"})
    inv.append({"input_role": "M_primary", "input_name": "df_m01_support_count_2024_12",
                "status": "AVAILABLE", "n_present": coverage("df_m01_support_count_2024_12"), "n_expected": 251,
                "source_path": "data_processed_official/service_infrastructure/DF_M01_registered_support_organizations/df_m01_counts_by_municipality_2024_12_31.csv",
                "note": "registered_by_2024_12 snapshot; not active stock"})
    inv.append({"input_role": "M_robustness", "input_name": "df_m01_support_count_2024_06",
                "status": "AVAILABLE", "n_present": coverage("df_m01_support_count_2024_06"), "n_expected": 251,
                "source_path": "data_processed_official/service_infrastructure/DF_M01_registered_support_organizations/df_m01_counts_by_municipality_2024_06_30.csv",
                "note": "registered_by_2024_06 snapshot"})
    inv.append({"input_role": "control", "input_name": "non_chinese_foreign_stock",
                "status": "AVAILABLE", "n_present": coverage("non_chinese_foreign_stock"), "n_expected": 251,
                "source_path": "data_processed_official/population/census_00200521_2020_municipality_population.csv",
                "note": "2020 census foreign residents (non-Chinese); vintage caveat"})
    inv.append({"input_role": "control", "input_name": "prefecture_fe",
                "status": "AVAILABLE", "n_present": len(rows), "n_expected": 251,
                "source_path": "derived from municipality_code prefix",
                "note": "categorical fixed effects 11/12/13/14"})
    # MISSING controls
    inv.append({"input_role": "control", "input_name": "rail_accessibility",
                "status": "MISSING", "n_present": 0, "n_expected": 251,
                "source_path": "raw only: data_raw/N02-22_GML/.../N02-22_Station.shp",
                "note": "no processed municipality-level field for 251 frame; raw station shapefile needs GIS/geocoding (forbidden this task)"})
    inv.append({"input_role": "control", "input_name": "housing_cost",
                "status": "MISSING", "n_present": 0, "n_expected": 251,
                "source_path": "raw only: data_raw/landPrice/L01-24_{11,12,13,14}_GML/*.shp",
                "note": "official land-price posting points for all 4 prefectures; needs GIS aggregation to municipality (forbidden this task); no processed 251-frame field"})
    inv.append({"input_role": "control", "input_name": "commercial_density",
                "status": "MISSING", "n_present": 0, "n_expected": 251,
                "source_path": "none in repo",
                "note": "no source file anywhere; would require new economic-census acquisition"})
    inv.append({"input_role": "control", "input_name": "population_density",
                "status": "MISSING", "n_present": 0, "n_expected": 251,
                "source_path": "raw only: total pop + N03 area shapefile",
                "note": "processed population file holds only foreign counts (no total population); area only in N03 boundary shapefile; needs GIS (forbidden this task)"})

    out_dir = root / "outputs/modeling/dfm01_mvp"
    out_dir.mkdir(parents=True, exist_ok=True)
    inv_path = out_dir / "model_readiness_inventory.csv"
    inv_cols = ["input_role", "input_name", "status", "n_present", "n_expected", "source_path", "note"]
    with open(inv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=inv_cols)
        w.writeheader()
        for r in inv:
            w.writerow(r)
    print(f"[committable] wrote readiness inventory: {inv_path}")

    missing = [r["input_name"] for r in inv if r["status"] == "MISSING"]
    print("MISSING required controls:", missing)
    print("MODEL_READY:", len(missing) == 0)


if __name__ == "__main__":
    main()
