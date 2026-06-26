"""DF_M01 MVP growth-side spatial robustness models.

On the same 218 complete-case sample and the same queen / KNN-6 weights as the residual
diagnostics, fit:
  - OLS baseline (HC3) Model 2 / Model 4 (reference);
  - SLX (OLS + spatially lagged covariates, HC3) under queen and KNN-6;
  - Spatial error (ML, spreg) under queen and KNN-6;
  - Spatial lag (ML, spreg) under queen and KNN-6.
Then recompute residual Moran's I for each fitted model. The objective is robustness
checking of the M->Y null and the M*housing null; NOT a diffusion theory. No causal
mediation claim. Queen has 1 island (12205) which ML cannot invert, so queen SEM/SAR drop
that single unit (N=217, documented); SLX keeps it with zero spatial lags (N=218).

Outputs (committable):
  dfm01_mvp_spatial_robustness_coefficients.csv
  dfm01_mvp_spatial_robustness_fit_summary.csv
  dfm01_mvp_spatial_robustness_residual_morans_i.csv

Usage: python run_dfm01_mvp_spatial_robustness.py --project-root E:\\rsch\\laborJapan
"""
import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import statsmodels.formula.api as smf
from libpysal.weights import Queen, KNN
from shapely.validation import make_valid
import spreg

warnings.filterwarnings("ignore")

PRIM_VARS = ["z_log_service_2024_12", "z_log_chinese_stock_2023_12", "z_rail_accessibility",
             "z_housing_cost", "z_commercial_density", "z_population_density",
             "z_non_chinese_foreign_stock", "chinese_growth_log_2024_12_2025_06"]
Y = "chinese_growth_log_2024_12_2025_06"
SVC = "z_log_service_2024_12"
HOUS = "z_housing_cost"
BASE_CTRL = ["z_log_chinese_stock_2023_12", "z_rail_accessibility", "z_housing_cost",
             "z_commercial_density", "z_population_density", "z_non_chinese_foreign_stock"]
LAG_COVARS = ["z_log_service_2024_12", "z_log_chinese_stock_2023_12", "z_commercial_density",
              "z_population_density", "z_rail_accessibility", "z_housing_cost"]


def morans_i(u, Wsp, perms=999, seed=12345):
    u = np.asarray(u, dtype=float); u = u - u.mean()
    n = u.size; S0 = float(Wsp.sum())
    den = (u * u).sum()
    I = (n / S0) * float(u @ (Wsp @ u)) / den
    EI = -1.0 / (n - 1)
    rng = np.random.default_rng(seed)
    sim = np.empty(perms)
    for k in range(perms):
        up = rng.permutation(u)
        sim[k] = (n / S0) * float(up @ (Wsp @ up)) / (up * up).sum()
    p_perm = (np.sum(np.abs(sim - EI) >= abs(I - EI)) + 1) / (perms + 1)
    return I, EI, p_perm


def prefecture_dummies(d):
    du = pd.get_dummies(d["prefecture"].astype(str), prefix="pref", drop_first=True).astype(float)
    return du


def design(d, model):
    """Return (X_df) base design (no constant; spreg adds it) for model 2 or 4."""
    cols = {}
    for c in BASE_CTRL:
        cols[c] = pd.to_numeric(d[c], errors="coerce").values
    cols[SVC] = pd.to_numeric(d[SVC], errors="coerce").values
    if model == 4:
        cols["svc_x_hous"] = pd.to_numeric(d[SVC], errors="coerce").values * pd.to_numeric(d[HOUS], errors="coerce").values
    X = pd.DataFrame(cols, index=d.index)
    X = pd.concat([X, prefecture_dummies(d)], axis=1)
    return X


def slx_cols(d, Wsp, order_codes):
    """spatial lags of LAG_COVARS aligned to order_codes."""
    out = {}
    base = d.set_index("municipality_code")
    for c in LAG_COVARS:
        v = pd.to_numeric(base.loc[order_codes, c], errors="coerce").values
        out["W_" + c] = Wsp @ v
    return pd.DataFrame(out, index=[order_codes.index(x) if False else i for i, x in enumerate(order_codes)])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--project-root", required=True)
    args = ap.parse_args(); root = Path(args.project_root)
    mp = root/"data_processed_official/model_panel"; out = root/"outputs/modeling/dfm01_mvp"

    df = pd.read_csv(mp/"tokyo_china_dfm01_mvp_model_panel_local_only.csv",
                     dtype={"municipality_code": str, "prefecture": str})
    cc = df[df[PRIM_VARS].notna().all(axis=1)].copy()
    cc = cc.sort_values("municipality_code").reset_index(drop=True)
    codes = list(cc["municipality_code"])
    print("complete-case N:", len(codes))

    # geometry + weights aligned to sorted codes
    shp = root/"data_raw/N03-20250101_GML/N03-20250101.shp"
    where = "N03_007 LIKE '11%' OR N03_007 LIKE '12%' OR N03_007 LIKE '13%' OR N03_007 LIKE '14%'"
    gdf = gpd.read_file(shp, columns=["N03_007"], where=where)
    gdf["municipality_code"] = gdf["N03_007"].astype(str).str.zfill(5)
    gdf = gdf[gdf["municipality_code"].isin(set(codes))]
    diss = gdf.dissolve(by="municipality_code", as_index=False)
    diss["geometry"] = diss["geometry"].apply(lambda g: g if g.is_valid else make_valid(g))
    g = diss.set_index("municipality_code").reindex(codes).reset_index()
    g = gpd.GeoDataFrame(g, geometry="geometry", crs=diss.crs)

    wq = Queen.from_dataframe(g, use_index=False, ids=codes); wq.transform = "r"
    wk = KNN.from_dataframe(g, k=6, ids=codes); wk.transform = "r"
    islands = list(wq.islands)
    print("queen islands:", islands)

    coef_rows, fit_rows, mi_rows = [], [], []

    def record(model_id, family, wtype, n, svc_c, svc_p, int_c, int_p, sp_name, sp_est, sp_p,
               r2, ll, aic, resid, Wsp_for_resid):
        m_concl = ("null_supported" if (svc_p is not None and svc_p >= 0.05)
                   else ("positive_supported" if (svc_c is not None and svc_c > 0)
                         else "negative_supported")) if svc_p is not None else "not_applicable"
        if model_id.startswith("model4"):
            i_concl = ("null_supported" if (int_p is not None and int_p >= 0.05) else "supported") if int_p is not None else "not_applicable"
        else:
            i_concl = "not_applicable"
        coef_rows.append({"model_id": model_id, "model_family": family, "weights_type": wtype,
                          "sample_n": n,
                          "focal_service_coefficient": "" if svc_c is None else round(svc_c, 6),
                          "focal_service_p_value": "" if svc_p is None else round(svc_p, 5),
                          "focal_interaction_coefficient": "" if int_c is None else round(int_c, 6),
                          "focal_interaction_p_value": "" if int_p is None else round(int_p, 5),
                          "spatial_parameter_name": sp_name or "",
                          "spatial_parameter_estimate": "" if sp_est is None else round(sp_est, 6),
                          "spatial_parameter_p_value": "" if sp_p is None else round(sp_p, 5),
                          "conclusion_for_M_to_Y": m_concl,
                          "conclusion_for_M_housing_interaction": i_concl,
                          "notes": ""})
        fit_rows.append({"model_id": model_id, "model_family": family, "weights_type": wtype,
                         "sample_n": n, "adj_or_pseudo_r2": "" if r2 is None else round(r2, 5),
                         "logLik": "" if ll is None else round(ll, 3),
                         "aic": "" if aic is None else round(aic, 3)})
        if resid is not None and Wsp_for_resid is not None:
            I, EI, p = morans_i(resid, Wsp_for_resid)
            status = ("STILL_SIGNIFICANT" if p < 0.05 else ("REDUCED_BUT_PRESENT" if p < 0.10 else "RESOLVED"))
            mi_rows.append({"model_id": model_id, "model_family": family, "weights_type": wtype,
                            "sample_n": n, "residual_morans_i": round(I, 5), "expected_i": round(EI, 5),
                            "permutation_p_value": round(p, 5), "spatial_residual_status": status,
                            "notes": "999 perms seed=12345"})
            return m_concl, status
        return m_concl, "NOT_COMPUTED"

    # ---------- OLS baselines (reference) ----------
    f2 = f"{Y} ~ {SVC} + " + " + ".join(BASE_CTRL[1:]) + " + z_log_chinese_stock_2023_12 + C(prefecture)"
    f2 = f"{Y} ~ {SVC} + " + " + ".join(BASE_CTRL) + " + C(prefecture)"
    f4 = f"{Y} ~ {SVC} * {HOUS} + " + " + ".join([c for c in BASE_CTRL if c != HOUS]) + " + C(prefecture)"
    for mid, f, model in [("model2", f2, 2), ("model4", f4, 4)]:
        r = smf.ols(f, data=cc).fit(cov_type="HC3")
        svc_c, svc_p = r.params[SVC], r.pvalues[SVC]
        it = next((t for t in r.params.index if ":" in t), None)
        ic, ip = (r.params[it], r.pvalues[it]) if it else (None, None)
        record(mid + "_OLS", "OLS_baseline", "none", int(r.nobs), svc_c, svc_p, ic, ip,
               None, None, None, r.rsquared_adj, None, None, r.resid.values, wq.sparse)

    # ---------- SLX (OLS + HC3) queen & knn6 ----------
    for wtype, w in [("queen", wq), ("knn6", wk)]:
        Wsp = w.sparse
        lags = {}
        base_idx = cc.set_index("municipality_code")
        for c in LAG_COVARS:
            lags["W_" + c] = Wsp @ pd.to_numeric(base_idx.loc[codes, c], errors="coerce").values
        slx = cc.copy().reset_index(drop=True)
        for k, v in lags.items():
            slx[k] = v
        for mid, model in [("model2", 2), ("model4", 4)]:
            lagterms = " + ".join(["W_" + c for c in LAG_COVARS])
            if model == 2:
                f = f"{Y} ~ {SVC} + " + " + ".join(BASE_CTRL) + f" + {lagterms} + C(prefecture)"
            else:
                f = f"{Y} ~ {SVC} * {HOUS} + " + " + ".join([c for c in BASE_CTRL if c != HOUS]) + f" + {lagterms} + C(prefecture)"
            r = smf.ols(f, data=slx).fit(cov_type="HC3")
            svc_c, svc_p = r.params[SVC], r.pvalues[SVC]
            it = next((t for t in r.params.index if ":" in t and "W_" not in t), None)
            ic, ip = (r.params[it], r.pvalues[it]) if it else (None, None)
            record(f"{mid}_SLX_{wtype}", "SLX", wtype, int(r.nobs), svc_c, svc_p, ic, ip,
                   None, None, None, r.rsquared_adj, None, None, r.resid.values, Wsp)

    # ---------- Spatial error & lag (spreg ML) ----------
    for wtype, w, drop_island in [("queen", wq, True), ("knn6", wk, False)]:
        if drop_island and islands:
            keep = [c for c in codes if c not in islands]
            sub = cc[cc["municipality_code"].isin(keep)].sort_values("municipality_code").reset_index(drop=True)
            sub_codes = list(sub["municipality_code"])
            gg = g[g["municipality_code"].isin(keep)].set_index("municipality_code").reindex(sub_codes).reset_index()
            gg = gpd.GeoDataFrame(gg, geometry="geometry", crs=g.crs)
            ww = Queen.from_dataframe(gg, use_index=False, ids=sub_codes); ww.transform = "r"
        else:
            sub = cc.sort_values("municipality_code").reset_index(drop=True); ww = w
        ydat = pd.to_numeric(sub[Y], errors="coerce").values.reshape(-1, 1)
        Wsp_sub = ww.sparse
        for mid, model in [("model2", 2), ("model4", 4)]:
            Xdf = design(sub, model)
            Xarr = Xdf.values.astype(float)
            xnames = list(Xdf.columns)
            # spatial error (GM/GMM; ML_Error has a spreg 1.8.5 / numpy2 summary bug)
            try:
                me = spreg.GM_Error(ydat, Xarr, w=ww, name_x=xnames)
                bn = ["CONSTANT"] + xnames + ["lambda"]
                bser = pd.Series(me.betas.flatten(), index=bn)
                # GM_Error z_stat covers CONSTANT + betas only (not lambda)
                pser = pd.Series([z[1] for z in me.z_stat], index=["CONSTANT"] + xnames)
                ic = bser.get("svc_x_hous"); ip = pser.get("svc_x_hous")
                record(f"{mid}_SEM_{wtype}", "spatial_error", wtype, int(me.n),
                       bser.get(SVC), pser.get(SVC), ic, ip, "lambda", bser.get("lambda"),
                       None, getattr(me, "pr2", None), None, None, me.u.flatten(), Wsp_sub)
            except Exception as e:
                print(f"SEM {wtype} {mid} failed:", e)
            # spatial lag (ML)
            try:
                ml = spreg.ML_Lag(ydat, Xarr, w=ww, name_x=xnames)
                bn = ["CONSTANT"] + xnames + ["rho"]
                bser = pd.Series(ml.betas.flatten(), index=bn)
                pser = pd.Series([z[1] for z in ml.z_stat], index=bn)
                ic = bser.get("svc_x_hous"); ip = pser.get("svc_x_hous")
                record(f"{mid}_SLAG_{wtype}", "spatial_lag", wtype, int(ml.n),
                       bser.get(SVC), pser.get(SVC), ic, ip, "rho", bser.get("rho"),
                       pser.get("rho"), ml.pr2, ml.logll, ml.aic, ml.u.flatten(), Wsp_sub)
            except Exception as e:
                print(f"SLAG {wtype} {mid} failed:", e)

    pd.DataFrame(coef_rows).to_csv(out/"dfm01_mvp_spatial_robustness_coefficients.csv", index=False)
    pd.DataFrame(fit_rows).to_csv(out/"dfm01_mvp_spatial_robustness_fit_summary.csv", index=False)
    pd.DataFrame(mi_rows).to_csv(out/"dfm01_mvp_spatial_robustness_residual_morans_i.csv", index=False)
    print("\nCOEFFICIENTS:")
    print(pd.DataFrame(coef_rows)[["model_id","model_family","weights_type","sample_n",
          "focal_service_coefficient","focal_service_p_value","focal_interaction_coefficient",
          "focal_interaction_p_value","spatial_parameter_name","spatial_parameter_estimate",
          "spatial_parameter_p_value"]].to_string(index=False))
    print("\nRESIDUAL MORAN'S I:")
    print(pd.DataFrame(mi_rows).to_string(index=False))


if __name__ == "__main__":
    main()
