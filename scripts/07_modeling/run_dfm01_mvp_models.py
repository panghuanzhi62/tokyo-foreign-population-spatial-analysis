"""Run the DF_M01-only MVP X-M-Y models (primary + robustness) with HC3 robust SEs,
plus full diagnostics. Complete-case modeling; complete-case N and the excluded
municipality composition are reported (never silently dropped).

Design (temporally ordered associations; NOT causal mediation):
  M1: z_log_service_2024_12 ~ z_log_chinese_stock_2023_12 + controls + C(prefecture)
  M2: chinese_growth_log_2024_12_2025_06 ~ z_log_service_2024_12 + z_log_chinese_stock_2023_12
      + controls + C(prefecture)
  M3: z_log_service_2024_12 ~ z_log_chinese_stock_2023_12 * z_commercial_density + controls + C(pref)
  M4: chinese_growth_log_2024_12_2025_06 ~ z_log_service_2024_12 * z_housing_cost
      + z_log_chinese_stock_2023_12 + controls + C(pref)
Robustness block: M = z_log_service_2024_06, Y = chinese_growth_log_2024_06_2025_06.
Controls: z_rail_accessibility, z_housing_cost, z_commercial_density, z_population_density,
z_non_chinese_foreign_stock (commercial/population/non-Chinese are z of log1p), C(prefecture).

Usage:
    python run_dfm01_mvp_models.py --project-root E:\\rsch\\laborJapan
"""
import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
import statsmodels.api as sm

CONTROLS = ("z_rail_accessibility + z_housing_cost + z_commercial_density + "
            "z_population_density + z_non_chinese_foreign_stock + C(prefecture)")
PREDICTORS = ["z_log_chinese_stock_2023_12", "z_rail_accessibility", "z_housing_cost",
              "z_commercial_density", "z_population_density", "z_non_chinese_foreign_stock"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--panel", default=None)
    args = ap.parse_args()
    root = Path(args.project_root)
    panel = Path(args.panel) if args.panel else (
        root/"data_processed_official/model_panel/tokyo_china_dfm01_mvp_model_panel_local_only.csv")
    out = root/"outputs/modeling/dfm01_mvp"
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(panel, dtype={"municipality_code": str, "prefecture": str})

    blocks = {
        "primary": dict(service="z_log_service_2024_12", growth="chinese_growth_log_2024_12_2025_06"),
        "robustness": dict(service="z_log_service_2024_06", growth="chinese_growth_log_2024_06_2025_06"),
    }

    def formulas(service, growth):
        return {
            "model1": f"{service} ~ z_log_chinese_stock_2023_12 + {CONTROLS}",
            "model2": f"{growth} ~ {service} + z_log_chinese_stock_2023_12 + {CONTROLS}",
            "model3": (f"{service} ~ z_log_chinese_stock_2023_12 * z_commercial_density + "
                       f"z_rail_accessibility + z_housing_cost + z_population_density + "
                       f"z_non_chinese_foreign_stock + C(prefecture)"),
            "model4": (f"{growth} ~ {service} * z_housing_cost + z_log_chinese_stock_2023_12 + "
                       f"z_rail_accessibility + z_commercial_density + z_population_density + "
                       f"z_non_chinese_foreign_stock + C(prefecture)"),
        }

    coeff_rows = {"primary": [], "robustness": []}
    fit_rows = []
    fits = {}
    for blk, sp in blocks.items():
        for mname, f in formulas(sp["service"], sp["growth"]).items():
            res = smf.ols(f, data=df).fit(cov_type="HC3")
            fits[(blk, mname)] = res
            for term in res.params.index:
                coeff_rows[blk].append({
                    "model": mname, "term": term, "coef": round(res.params[term], 6),
                    "std_err_hc3": round(res.bse[term], 6), "t": round(res.tvalues[term], 4),
                    "p_value": round(res.pvalues[term], 6), "n": int(res.nobs)})
            fit_rows.append({
                "block": blk, "model": mname, "n": int(res.nobs),
                "df_model": int(res.df_model), "df_resid": int(res.df_resid),
                "rsquared": round(res.rsquared, 5), "rsquared_adj": round(res.rsquared_adj, 5),
                "f_pvalue": ("" if res.f_pvalue is None else round(float(res.f_pvalue), 6)),
                "cov_type": "HC3", "formula": f})

    pd.DataFrame(coeff_rows["primary"]).to_csv(out/"dfm01_mvp_model_coefficients_primary.csv", index=False)
    pd.DataFrame(coeff_rows["robustness"]).to_csv(out/"dfm01_mvp_model_coefficients_robustness.csv", index=False)
    pd.DataFrame(fit_rows).to_csv(out/"dfm01_mvp_model_fit_summary.csv", index=False)

    # ---- missingness summary + excluded composition ----
    model_vars = ["z_log_service_2024_12", "z_log_service_2024_06", "z_log_chinese_stock_2023_12",
                  "z_rail_accessibility", "z_housing_cost", "z_commercial_density",
                  "z_population_density", "z_non_chinese_foreign_stock",
                  "chinese_growth_log_2024_12_2025_06", "chinese_growth_log_2024_06_2025_06"]
    miss_rows = []
    for v in model_vars:
        present = int(df[v].notna().sum())
        miss_rows.append({"variable": v, "n_present": present, "n_missing": int(len(df) - present),
                          "coverage": f"{present}/{len(df)}"})
    # complete-case per block + excluded composition (primary)
    prim_vars = [blocks["primary"]["service"], blocks["primary"]["growth"]] + PREDICTORS
    cc_primary = df.dropna(subset=prim_vars)
    rob_vars = [blocks["robustness"]["service"], blocks["robustness"]["growth"]] + PREDICTORS
    cc_rob = df.dropna(subset=rob_vars)
    miss_rows.append({"variable": "COMPLETE_CASE_primary", "n_present": int(len(cc_primary)),
                      "n_missing": int(len(df) - len(cc_primary)), "coverage": f"{len(cc_primary)}/{len(df)}"})
    miss_rows.append({"variable": "COMPLETE_CASE_robustness", "n_present": int(len(cc_rob)),
                      "n_missing": int(len(df) - len(cc_rob)), "coverage": f"{len(cc_rob)}/{len(df)}"})
    excluded = df[~df["municipality_code"].isin(cc_primary["municipality_code"])]
    for pref, g in excluded.groupby("prefecture"):
        miss_rows.append({"variable": f"excluded_primary_prefecture_{pref}", "n_present": int(len(g)),
                          "n_missing": "", "coverage": ""})
    pd.DataFrame(miss_rows).to_csv(out/"dfm01_mvp_missingness_summary.csv", index=False)

    # ---- descriptive statistics (raw + key z over full panel) ----
    desc_vars = ["chinese_stock_2023_12", "chinese_stock_2024_12", "chinese_stock_2025_06",
                 "df_m01_support_count_2024_12", "df_m01_support_count_2024_06",
                 "rail_accessibility", "housing_cost", "commercial_density", "population_density",
                 "non_chinese_foreign_stock", "chinese_growth_log_2024_12_2025_06",
                 "z_log_service_2024_12", "z_log_chinese_stock_2023_12"]
    drows = []
    for v in desc_vars:
        s = pd.to_numeric(df[v], errors="coerce").dropna()
        drows.append({"variable": v, "n": int(s.size), "mean": round(s.mean(), 4),
                      "std": round(s.std(), 4), "min": round(s.min(), 4),
                      "median": round(s.median(), 4), "max": round(s.max(), 4)})
    pd.DataFrame(drows).to_csv(out/"dfm01_mvp_descriptive_statistics.csv", index=False)

    # ---- correlation matrix (primary complete-case) ----
    corr_vars = ["z_log_service_2024_12", "z_log_chinese_stock_2023_12", "z_rail_accessibility",
                 "z_housing_cost", "z_commercial_density", "z_population_density",
                 "z_non_chinese_foreign_stock", "chinese_growth_log_2024_12_2025_06"]
    corr = cc_primary[corr_vars].astype(float).corr(method="pearson").round(4)
    corr.to_csv(out/"dfm01_mvp_correlation_matrix.csv")

    # ---- VIF (predictors in Model 2, primary complete-case) ----
    X = cc_primary[PREDICTORS].astype(float).copy()
    X = sm.add_constant(X)
    vif_rows = []
    for i, col in enumerate(X.columns):
        if col == "const":
            continue
        vif_rows.append({"predictor": col, "vif": round(variance_inflation_factor(X.values, i), 4)})
    pd.DataFrame(vif_rows).to_csv(out/"dfm01_mvp_vif_summary.csv", index=False)

    # ---- influence (Model 2 and Model 4, primary; top 10 by |studentized resid| / Cook's D) ----
    infl_rows = []
    for mname, sp_service, sp_growth in [("model2", "z_log_service_2024_12", "chinese_growth_log_2024_12_2025_06"),
                                         ("model4", "z_log_service_2024_12", "chinese_growth_log_2024_12_2025_06")]:
        f = formulas(blocks["primary"]["service"], blocks["primary"]["growth"])[mname]
        sub = df.dropna(subset=prim_vars).reset_index(drop=True)
        res_ols = smf.ols(f, data=sub).fit()  # non-robust for influence measures
        infl = OLSInfluence(res_ols)
        stud = infl.resid_studentized_external
        cooks = infl.cooks_distance[0]
        order = np.argsort(-np.abs(stud))[:10]
        for rank, idx in enumerate(order, 1):
            infl_rows.append({"model": mname, "rank": rank,
                              "municipality_code": sub.loc[idx, "municipality_code"],
                              "municipality_name": sub.loc[idx, "municipality_name"],
                              "prefecture": sub.loc[idx, "prefecture"],
                              "studentized_resid": round(float(stud[idx]), 4),
                              "cooks_distance": round(float(cooks[idx]), 6)})
    pd.DataFrame(infl_rows).to_csv(out/"dfm01_mvp_influence_cases.csv", index=False)

    # ---- run note ----
    m2 = fits[("primary", "model2")]
    note = out/"dfm01_mvp_model_run_note.md"
    lines = [
        "# DF_M01 MVP Model Run Note", "",
        f"Panel: {panel.name} ; complete-case N (primary) = {int(len(cc_primary))}/251 ; "
        f"robustness = {int(len(cc_rob))}/251.",
        "OLS with HC3 robust standard errors. NOT causal mediation; temporally ordered,",
        "mechanism-consistent associations only.", "",
        "Controls: rail accessibility, housing cost (log land price), commercial density",
        "(z of log1p 2021 Economic Census establishments/area), population density (z of log1p",
        "2024 BRR pop/area), non-Chinese foreign stock (z of log1p), prefecture fixed effects.", "",
        "Complete-case excludes 33 peripheral municipalities (Tokyo islands/mountain, Chiba Boso,",
        "Saitama Chichibu) that lack v5 rail/housing; see missingness summary. Estimand is",
        "therefore mainland populated Greater Tokyo, not all 251.", "",
        f"Model 2 (Y growth ~ service + X + controls): service coef "
        f"{round(m2.params.get('z_log_service_2024_12', float('nan')), 4)} "
        f"(p={round(m2.pvalues.get('z_log_service_2024_12', float('nan')), 4)}), "
        f"adj R2 {round(m2.rsquared_adj, 4)}, n {int(m2.nobs)}.",
    ]
    note.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("models fitted; primary complete-case N =", int(len(cc_primary)))
    for (blk, mname), res in fits.items():
        print(f"  {blk}/{mname}: n={int(res.nobs)} adjR2={round(res.rsquared_adj,4)}")


if __name__ == "__main__":
    main()
