"""DF_M01 MVP robustness & diagnostics (HC3). Reads the local-only model panel and the
2024 population-density table; writes compact committable diagnostics. No model is
presented as a new main model; this is robustness only. No causal-mediation claim.

Outputs (committable):
  dfm01_mvp_complete_case_exclusion_audit.csv
  dfm01_mvp_collinearity_robustness_coefficients.csv
  dfm01_mvp_collinearity_robustness_fit_summary.csv
  dfm01_mvp_alternative_m_scaling_coefficients.csv
  dfm01_mvp_residual_spatial_check.csv

Usage: python run_dfm01_mvp_robustness.py --project-root E:\\rsch\\laborJapan
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

PRIM_VARS = ["z_log_service_2024_12", "z_log_chinese_stock_2023_12", "z_rail_accessibility",
             "z_housing_cost", "z_commercial_density", "z_population_density",
             "z_non_chinese_foreign_stock", "chinese_growth_log_2024_12_2025_06"]


def zser(s):
    s = pd.to_numeric(s, errors="coerce")
    sd = s.std(ddof=0)
    return (s - s.mean()) / sd if sd and sd > 0 else s * 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    args = ap.parse_args()
    root = Path(args.project_root)
    mp = root/"data_processed_official/model_panel"
    out = root/"outputs/modeling/dfm01_mvp"
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(mp/"tokyo_china_dfm01_mvp_model_panel_local_only.csv",
                     dtype={"municipality_code": str, "prefecture": str})
    pop = pd.read_csv(mp/"tokyo_china_population_density_2024_251_local_only.csv",
                      dtype={"municipality_code": str})[["municipality_code", "population_2024", "area_km2"]]
    df = df.merge(pop, on="municipality_code", how="left")

    df["included"] = df[PRIM_VARS].notna().all(axis=1)
    inc = df[df["included"]]
    exc = df[~df["included"]]

    # ---- (1) complete-case exclusion audit ----
    audit_vars = ["chinese_stock_2023_12", "chinese_growth_log_2024_12_2025_06",
                  "df_m01_support_count_2024_12", "population_2024", "area_km2",
                  "commercial_density", "population_density", "non_chinese_foreign_stock"]
    arows = []
    for v in audit_vars:
        iv = pd.to_numeric(inc[v], errors="coerce"); ev = pd.to_numeric(exc[v], errors="coerce")
        arows.append({"variable": v, "included_n": int(iv.notna().sum()), "excluded_n": int(ev.notna().sum()),
                      "included_mean": round(iv.mean(), 4), "excluded_mean": round(ev.mean(), 4),
                      "included_median": round(iv.median(), 4), "excluded_median": round(ev.median(), 4)})
    # prefecture composition
    for pref in sorted(df["prefecture"].unique()):
        arows.append({"variable": f"prefecture_{pref}_count",
                      "included_n": int((inc["prefecture"] == pref).sum()),
                      "excluded_n": int((exc["prefecture"] == pref).sum()),
                      "included_mean": "", "excluded_mean": "", "included_median": "", "excluded_median": ""})
    # missing-reason breakdown among excluded
    rail_miss = exc["z_rail_accessibility"].isna()
    house_miss = exc["z_housing_cost"].isna()
    arows.append({"variable": "excluded_missing_housing_only", "included_n": "", "excluded_n": int((house_miss & ~rail_miss).sum()),
                  "included_mean": "", "excluded_mean": "", "included_median": "", "excluded_median": ""})
    arows.append({"variable": "excluded_missing_rail_only", "included_n": "", "excluded_n": int((rail_miss & ~house_miss).sum()),
                  "included_mean": "", "excluded_mean": "", "included_median": "", "excluded_median": ""})
    arows.append({"variable": "excluded_missing_both_rail_housing", "included_n": "", "excluded_n": int((rail_miss & house_miss).sum()),
                  "included_mean": "", "excluded_mean": "", "included_median": "", "excluded_median": ""})
    pd.DataFrame(arows).to_csv(out/"dfm01_mvp_complete_case_exclusion_audit.csv", index=False)

    # ---- (4) collinearity robustness ----
    # residualized commercial density (Spec C): log_commercial_density ~ z_population_density + C(pref)
    base = df.dropna(subset=["log_commercial_density", "z_population_density"]).copy()
    res_c = smf.ols("log_commercial_density ~ z_population_density + C(prefecture)", data=base).fit()
    df.loc[base.index, "commercial_resid"] = res_c.resid
    df["z_commercial_resid"] = zser(df["commercial_resid"])
    # winsorized commercial (Spec D): winsorize log_commercial at 1/99 pct then z
    lc = pd.to_numeric(df["log_commercial_density"], errors="coerce")
    lo, hi = np.nanpercentile(lc, 1), np.nanpercentile(lc, 99)
    df["z_commercial_winsor"] = zser(lc.clip(lo, hi))

    S, G = "z_log_service_2024_12", "chinese_growth_log_2024_12_2025_06"
    X = "z_log_chinese_stock_2023_12"
    C_full = "z_rail_accessibility + z_housing_cost + z_commercial_density + z_population_density + z_non_chinese_foreign_stock + C(prefecture)"

    def specs(commercial="z_commercial_density", drop_pop=False, drop_comm_nonfocal=False):
        ctrl = ["z_rail_accessibility", "z_housing_cost", "z_population_density", "z_non_chinese_foreign_stock"]
        if not drop_pop:
            pass
        else:
            ctrl = [c for c in ctrl if c != "z_population_density"]
        comm_in_controls = commercial if not drop_comm_nonfocal else None
        ctrl_124 = ctrl + ([comm_in_controls] if comm_in_controls else [])
        c124 = " + ".join(ctrl_124 + ["C(prefecture)"])
        # model3 always keeps commercial as focal moderator
        ctrl3 = ctrl + ["z_non_chinese_foreign_stock"] if False else ctrl
        c3 = " + ".join([c for c in ctrl if c != "z_population_density" or not drop_pop] + ["C(prefecture)"])
        return {
            "model1": f"{S} ~ {X} + {c124}",
            "model2": f"{G} ~ {S} + {X} + {c124}",
            "model3": f"{S} ~ {X} * {commercial} + " + " + ".join(ctrl + ["C(prefecture)"]),
            "model4": f"{G} ~ {S} * z_housing_cost + {X} + " + " + ".join([c for c in ctrl if c != 'z_housing_cost'] + ([comm_in_controls] if comm_in_controls else []) + ["C(prefecture)"]),
        }

    spec_defs = {
        "baseline": specs("z_commercial_density"),
        "A_drop_population_density": specs("z_commercial_density", drop_pop=True),
        "B_drop_commercial_except_M3": specs("z_commercial_density", drop_comm_nonfocal=True),
        "C_residualized_commercial": specs("z_commercial_resid"),
        "D_winsorized_commercial": specs("z_commercial_winsor"),
    }
    focal = {"model1": X, "model2": S, "model3": None, "model4": None}  # None => interaction
    crows, frows = [], []
    for sname, fset in spec_defs.items():
        for m, f in fset.items():
            res = smf.ols(f, data=df).fit(cov_type="HC3")
            # focal term
            if focal[m] is not None:
                term = focal[m]
            else:
                term = next((t for t in res.params.index if ":" in t), None)
            if term is not None and term in res.params.index:
                crows.append({"spec": sname, "model": m, "focal_term": term,
                              "coef": round(res.params[term], 6), "std_err_hc3": round(res.bse[term], 6),
                              "p_value": round(res.pvalues[term], 6), "n": int(res.nobs)})
            frows.append({"spec": sname, "model": m, "n": int(res.nobs),
                          "rsquared_adj": round(res.rsquared_adj, 5)})
    pd.DataFrame(crows).to_csv(out/"dfm01_mvp_collinearity_robustness_coefficients.csv", index=False)
    pd.DataFrame(frows).to_csv(out/"dfm01_mvp_collinearity_robustness_fit_summary.csv", index=False)

    # ---- (5) alternative M scaling diagnostics (Model 2 variants) ----
    df["total_foreign_est"] = (pd.to_numeric(df["chinese_stock_2023_12"], errors="coerce")
                               + pd.to_numeric(df["non_chinese_foreign_stock"], errors="coerce"))
    df["service_count_raw"] = pd.to_numeric(df["df_m01_support_count_2024_12"], errors="coerce")
    df["service_per_10000_foreigners"] = df["service_count_raw"] / df["total_foreign_est"].replace(0, np.nan) * 10000
    df["service_per_10000_total_pop"] = df["service_count_raw"] / pd.to_numeric(df["population_2024"], errors="coerce").replace(0, np.nan) * 10000
    alt_specs = {
        "service_count_raw": zser(df["service_count_raw"]),
        "log1p_service_count": df["z_log_service_2024_12"],  # already z of log1p
        "service_per_10000_foreigners": zser(df["service_per_10000_foreigners"]),
        "service_per_10000_total_population": zser(df["service_per_10000_total_pop"]),
    }
    arows2 = []
    for name, zvals in alt_specs.items():
        df["z_alt_service"] = zvals
        f = f"{G} ~ z_alt_service + {X} + {C_full}"
        res = smf.ols(f, data=df).fit(cov_type="HC3")
        arows2.append({"m_variant": name, "term": "z_alt_service",
                       "coef": round(res.params.get("z_alt_service", float('nan')), 6),
                       "std_err_hc3": round(res.bse.get("z_alt_service", float('nan')), 6),
                       "p_value": round(res.pvalues.get("z_alt_service", float('nan')), 6),
                       "n": int(res.nobs), "rsquared_adj": round(res.rsquared_adj, 5)})
    pd.DataFrame(arows2).to_csv(out/"dfm01_mvp_alternative_m_scaling_coefficients.csv", index=False)

    # ---- (7) residual spatial check: SKIPPED (no compatible existing weights) ----
    pd.DataFrame([{
        "check": "residual_morans_I", "status": "SKIPPED",
        "reason": "no compatible existing 251/218 spatial-weights file (.gal/.gwt/.npz/.pkl) found; "
                  "src/tokyo_foreigners/spatial_diagnostics.py + notebook exist but target the old "
                  "Tokyo-only N03 frame; creating new weights is out of scope this task",
        "models_intended": "primary M2, primary M4, best reduced-collinearity M2/M4",
    }]).to_csv(out/"dfm01_mvp_residual_spatial_check.csv", index=False)

    # console summary
    print("included N:", int(inc.shape[0]), "excluded N:", int(exc.shape[0]))
    print("log_commercial skew:", round(float(pd.to_numeric(df['log_commercial_density'], errors='coerce').skew()), 3),
          "| raw commercial skew:", round(float(pd.to_numeric(df['commercial_density'], errors='coerce').skew()), 3))
    print(pd.DataFrame(crows).to_string(index=False))
    print(pd.DataFrame(arows2).to_string(index=False))


if __name__ == "__main__":
    main()
