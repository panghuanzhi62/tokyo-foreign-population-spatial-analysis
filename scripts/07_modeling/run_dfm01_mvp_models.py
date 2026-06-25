"""Run the DF_M01-only MVP X-M-Y models (primary + robustness).

Design (temporally ordered associations; NOT causal mediation):
  Model 1: z_log_service_2024_12 ~ z_log_chinese_stock_2023_12 + controls + C(prefecture)
  Model 2: chinese_growth_log_2024_12_2025_06 ~ z_log_service_2024_12
           + z_log_chinese_stock_2023_12 + controls + C(prefecture)
  Model 3: z_log_service_2024_12 ~ z_log_chinese_stock_2023_12 * z_commercial_density
           + controls + C(prefecture)
  Model 4: chinese_growth_log_2024_12_2025_06 ~ z_log_service_2024_12 * z_housing_cost
           + z_log_chinese_stock_2023_12 + controls + C(prefecture)
Robustness: M = z_log_service_2024_06 ; Y = chinese_growth_log_2024_06_2025_06.

OLS with HC3 robust standard errors.

This runner is GUARDED: it requires the full control set (rail_accessibility,
housing_cost, commercial_density, population_density, non_chinese_foreign_stock)
to be present in the panel. If any required control is missing it does NOT fit any
model and instead writes a missing-input determination, because the design
explicitly forbids inventing proxies for missing controls. Models 3 and 4 in
particular require commercial_density and housing_cost respectively.

Usage:
    python run_dfm01_mvp_models.py --project-root E:\\rsch\\laborJapan
    python run_dfm01_mvp_models.py --project-root . --panel <panel.csv>
"""
import argparse
import csv
from pathlib import Path

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


def control_present(rows, col):
    return any(r.get(col) not in (None, "") for r in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--panel", default=None,
                    help="path to model panel CSV (defaults to the local-only panel)")
    args = ap.parse_args()
    root = Path(args.project_root)

    panel_path = Path(args.panel) if args.panel else (
        root / "data_processed_official/model_panel/tokyo_china_dfm01_mvp_model_panel_local_only.csv")
    out_dir = root / "outputs/modeling/dfm01_mvp"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not panel_path.exists():
        raise SystemExit(f"panel not found: {panel_path} (run build_dfm01_mvp_model_panel.py first)")

    rows = load_csv(panel_path)
    missing = [c for c in REQUIRED_CONTROLS if not control_present(rows, c)]

    if missing:
        # Missing-input gate: do not invent proxies, do not fit.
        note = out_dir / "dfm01_mvp_model_run_note.md"
        lines = [
            "# DF_M01 MVP Model Run Note - MISSING-INPUT STOP",
            "",
            f"Panel: {panel_path.name} ({len(rows)} municipality rows)",
            "",
            "Status: MODELS NOT FITTED.",
            "",
            "Reason: the MVP design requires a fixed control set, and the following",
            "required controls are not available as processed, municipality-level fields",
            "for the 251 Greater Tokyo frame. Per the task design, proxies must NOT be",
            "invented and geocoding is not permitted in this task, so no model is fitted.",
            "",
            "Missing required controls:",
        ]
        for c in missing:
            lines.append(f"- {c}")
        lines += [
            "",
            "Models 3 and 4 additionally depend on commercial_density and housing_cost",
            "respectively, so the interaction models cannot be specified at all.",
            "",
            "Available inputs (X, Y, M=DF_M01, non_chinese_foreign_stock, prefecture FE)",
            "are assembled in the local-only panel and itemized in",
            "outputs/modeling/dfm01_mvp/model_readiness_inventory.csv.",
            "",
            "Shortest next action: build a local-only, processed, municipality-level",
            "controls table for the 251 frame (population_density, housing_cost/land_price,",
            "rail_accessibility from the existing GIS layers, plus commercial_density via",
            "economic-census acquisition) in a separate approved step, then re-run.",
        ]
        note.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print("MISSING required controls:", missing)
        print("Models NOT fitted; wrote missing-input determination:", note)
        return

    # ---- Full control set present: fit models (statsmodels) ----
    import numpy as np  # noqa: F401
    import pandas as pd
    import statsmodels.formula.api as smf

    df = pd.read_csv(panel_path)

    def fit(formula):
        return smf.ols(formula, data=df).fit(cov_type="HC3")

    controls = ("z_rail_accessibility + z_housing_cost + z_commercial_density + "
                "z_population_density + z_non_chinese_foreign_stock + C(prefecture)")

    def run_block(service, growth):
        return {
            "model1": fit(f"{service} ~ z_log_chinese_stock_2023_12 + {controls}"),
            "model2": fit(f"{growth} ~ {service} + z_log_chinese_stock_2023_12 + {controls}"),
            "model3": fit(f"{service} ~ z_log_chinese_stock_2023_12 * z_commercial_density + "
                          f"z_rail_accessibility + z_housing_cost + z_population_density + "
                          f"z_non_chinese_foreign_stock + C(prefecture)"),
            "model4": fit(f"{growth} ~ {service} * z_housing_cost + z_log_chinese_stock_2023_12 + "
                          f"z_rail_accessibility + z_commercial_density + z_population_density + "
                          f"z_non_chinese_foreign_stock + C(prefecture)"),
        }

    primary = run_block("z_log_service_2024_12", "chinese_growth_log_2024_12_2025_06")
    robustness = run_block("z_log_service_2024_06", "chinese_growth_log_2024_06_2025_06")

    def write_coeffs(blocks, path):
        recs = []
        for mname, res in blocks.items():
            for term in res.params.index:
                recs.append({
                    "model": mname, "term": term,
                    "coef": res.params[term], "std_err": res.bse[term],
                    "p_value": res.pvalues[term], "n": int(res.nobs),
                    "rsquared": res.rsquared, "rsquared_adj": res.rsquared_adj,
                })
        pd.DataFrame(recs).to_csv(path, index=False)

    write_coeffs(primary, out_dir / "dfm01_mvp_model_coefficients_primary.csv")
    write_coeffs(robustness, out_dir / "dfm01_mvp_model_coefficients_robustness.csv")
    print("Models fitted; coefficient tables written.")


if __name__ == "__main__":
    main()
