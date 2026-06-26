"""DF_M01 MVP residual spatial autocorrelation diagnostics.

Builds queen-contiguity weights for the 218 complete-case municipalities from the local
N03-20250101 boundary (libpysal), refits the four growth-side target models on the same
complete-case sample to get residuals, and computes residual Moran's I (analytical EI +
permutation inference; esda not installed so Moran's I is implemented directly). Does not
change the main interpretation; no causal-mediation claim.

Outputs (committable):
  dfm01_mvp_spatial_sample_qc.csv
  dfm01_mvp_spatial_weights_qc.csv
  dfm01_mvp_residual_morans_i.csv
Local-only (not committed):
  data_processed_official/model_panel/dfm01_mvp_queen_weights_218_local_only.gal

Usage: python run_dfm01_mvp_spatial_diagnostics.py --project-root E:\\rsch\\laborJapan
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import statsmodels.formula.api as smf
from libpysal.weights import Queen, KNN
from shapely.validation import make_valid

PRIM_VARS = ["z_log_service_2024_12", "z_log_chinese_stock_2023_12", "z_rail_accessibility",
             "z_housing_cost", "z_commercial_density", "z_population_density",
             "z_non_chinese_foreign_stock", "chinese_growth_log_2024_12_2025_06"]

# target model formulas (OLS residuals are identical with or without HC3)
G = "chinese_growth_log_2024_12_2025_06"
S = "z_log_service_2024_12"
X = "z_log_chinese_stock_2023_12"
CTRL_FULL = "z_rail_accessibility + z_housing_cost + z_commercial_density + z_population_density + z_non_chinese_foreign_stock + C(prefecture)"
# best reduced-collinearity = Spec A (drop population_density), per robustness note
CTRL_REDA = "z_rail_accessibility + z_housing_cost + z_commercial_density + z_non_chinese_foreign_stock + C(prefecture)"
MODELS = {
    "primary_model2":   f"{G} ~ {S} + {X} + {CTRL_FULL}",
    "primary_model4":   f"{G} ~ {S} * z_housing_cost + {X} + z_rail_accessibility + z_commercial_density + z_population_density + z_non_chinese_foreign_stock + C(prefecture)",
    "reducedA_model2":  f"{G} ~ {S} + {X} + {CTRL_REDA}",
    "reducedA_model4":  f"{G} ~ {S} * z_housing_cost + {X} + z_rail_accessibility + z_commercial_density + z_non_chinese_foreign_stock + C(prefecture)",
}
MODEL_DESC = {
    "primary_model2": "Primary Model 2: growth ~ service + Xstock + full controls + pref FE",
    "primary_model4": "Primary Model 4: growth ~ service*housing + Xstock + controls + pref FE",
    "reducedA_model2": "Reduced-collinearity (drop population_density) Model 2",
    "reducedA_model4": "Reduced-collinearity (drop population_density) Model 4",
}


def morans_i(z, Wsparse, S0, perms=999, seed=12345):
    """Row-standardized Moran's I with analytical EI and permutation inference."""
    z = np.asarray(z, dtype=float)
    z = z - z.mean()
    n = z.size
    den = (z * z).sum()
    num = float(z @ (Wsparse @ z))
    I = (n / S0) * num / den
    EI = -1.0 / (n - 1)
    rng = np.random.default_rng(seed)
    sim = np.empty(perms)
    for k in range(perms):
        zp = rng.permutation(z)
        sim[k] = (n / S0) * float(zp @ (Wsparse @ zp)) / (zp * zp).sum()
    # permutation two-sided p-value
    larger = np.sum(np.abs(sim - EI) >= abs(I - EI))
    p_perm = (larger + 1) / (perms + 1)
    z_sim = (I - sim.mean()) / sim.std(ddof=0) if sim.std(ddof=0) > 0 else float("nan")
    # normal-approx two-sided p from z_sim
    from scipy.stats import norm
    p_norm = 2 * (1 - norm.cdf(abs(z_sim)))
    return I, EI, z_sim, p_norm, p_perm


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
    df["included"] = df[PRIM_VARS].notna().all(axis=1)
    cc = df[df["included"]].copy()
    cc_codes = set(cc["municipality_code"])
    print("complete-case N:", len(cc_codes))

    # ---- load N03, dissolve, restrict to 218 ----
    shp = root/"data_raw/N03-20250101_GML/N03-20250101.shp"
    where = "N03_007 LIKE '11%' OR N03_007 LIKE '12%' OR N03_007 LIKE '13%' OR N03_007 LIKE '14%'"
    gdf = gpd.read_file(shp, columns=["N03_007"], where=where)
    gdf["municipality_code"] = gdf["N03_007"].astype(str).str.zfill(5)
    gdf = gdf[gdf["municipality_code"].isin(set(df["municipality_code"]))].copy()
    diss = gdf.dissolve(by="municipality_code", as_index=False)
    diss["geometry"] = diss["geometry"].apply(lambda g: g if g.is_valid else make_valid(g))
    geom_codes = set(diss["municipality_code"])

    # ---- sample QC (all 251 rows) ----
    sq = []
    for _, r in df.iterrows():
        code = r["municipality_code"]
        sq.append({"municipality_code": code, "municipality_name": r["municipality_name"],
                   "prefecture": r["prefecture"],
                   "included_in_complete_case_218": "YES" if code in cc_codes else "NO",
                   "geometry_found": "YES" if code in geom_codes else "NO",
                   "geometry_valid": "YES" if code in geom_codes else "NO",
                   "notes": "N03-20250101 dissolved by N03_007"})
    pd.DataFrame(sq).to_csv(out/"dfm01_mvp_spatial_sample_qc.csv", index=False)

    # ---- restrict geometry to the 218, ordered ----
    g218 = diss[diss["municipality_code"].isin(cc_codes)].copy()
    g218 = g218.set_index("municipality_code").reindex(sorted(cc_codes)).reset_index()
    g218 = gpd.GeoDataFrame(g218, geometry="geometry", crs=diss.crs)

    # ---- queen weights ----
    w = Queen.from_dataframe(g218, use_index=False, ids=list(g218["municipality_code"]))
    w.transform = "r"
    cards = np.array([w.cardinalities[i] for i in w.id_order])
    islands = list(w.islands)
    try:
        ncomp = w.n_components
    except Exception:
        ncomp = ""
    # save local-only .gal
    try:
        from libpysal.io import open as ps_open
        gal_path = mp/"dfm01_mvp_queen_weights_218_local_only.gal"
        f = ps_open(str(gal_path), "w"); f.write(w); f.close()
    except Exception as e:
        print("gal save skipped:", e)

    # ---- KNN-6 sensitivity weights (guarantees no isolates given the island in queen) ----
    wk = KNN.from_dataframe(g218, k=6, ids=list(g218["municipality_code"]))
    wk.transform = "r"
    cardsk = np.array([wk.cardinalities[i] for i in wk.id_order])

    wqc = [{
        "weights_type": "queen_contiguity_row_standardized", "n_units": w.n,
        "n_components": ncomp, "n_isolates": len(islands),
        "min_neighbors": int(cards.min()), "median_neighbors": float(np.median(cards)),
        "max_neighbors": int(cards.max()),
        "source_boundary": "data_raw/N03-20250101_GML/N03-20250101.shp (dissolved by N03_007)",
        "crs_used": str(g218.crs),
        "notes": ("islands: " + ",".join(islands)) if islands else "no isolates; single contiguous structure",
    }, {
        "weights_type": "knn6_row_standardized", "n_units": wk.n, "n_components": "",
        "n_isolates": 0, "min_neighbors": int(cardsk.min()),
        "median_neighbors": float(np.median(cardsk)), "max_neighbors": int(cardsk.max()),
        "source_boundary": "data_raw/N03-20250101_GML/N03-20250101.shp (centroids, dissolved by N03_007)",
        "crs_used": str(g218.crs),
        "notes": "k=6 nearest neighbors sensitivity (no isolates) because queen has 1 island (12205)",
    }]
    pd.DataFrame(wqc).to_csv(out/"dfm01_mvp_spatial_weights_qc.csv", index=False)
    print("queen:", w.n, "units; isolates", len(islands), "components", ncomp,
          "neighbors", cards.min(), np.median(cards), cards.max(),
          "| knn6 neighbors", cardsk.min(), np.median(cardsk), cardsk.max())

    schemes = {
        "queen_row_standardized": (w.sparse, ncomp, len(islands)),
        "knn6_row_standardized": (wk.sparse, "", 0),
    }
    code_order = list(g218["municipality_code"])
    rows = []
    for mid, formula in MODELS.items():
        sub = cc.dropna(subset=[c for c in PRIM_VARS]).copy()
        res = smf.ols(formula, data=sub).fit()
        resid = pd.Series(res.resid.values, index=sub["municipality_code"].values)
        z = resid.reindex(code_order).values
        for wtype, (Wsp, nc, nis) in schemes.items():
            S0 = float(Wsp.sum())
            if np.isnan(z).any():
                rows.append({"model_id": mid, "model_description": MODEL_DESC[mid],
                             "sample_n": int(np.sum(~np.isnan(z))), "weights_type": wtype,
                             "n_components": nc, "n_isolates": nis, "morans_i": "", "expected_i": "",
                             "z_score": "", "p_value": "", "permutation_p_value": "",
                             "spatial_autocorrelation_flag": "NOT_RUN", "interpretation": "",
                             "notes": "NaN residuals"})
                continue
            I, EI, zsc, p_norm, p_perm = morans_i(z, Wsp, S0)
            flag = "YES" if p_perm < 0.05 else ("BORDERLINE" if p_perm < 0.10 else "NO")
            sign = "negative" if I < EI else "positive"
            interp = {"YES": f"significant {sign} residual spatial autocorrelation",
                      "BORDERLINE": f"borderline {sign} residual spatial autocorrelation",
                      "NO": "no significant residual spatial autocorrelation"}[flag]
            rows.append({"model_id": mid, "model_description": MODEL_DESC[mid],
                         "sample_n": int(z.size), "weights_type": wtype, "n_components": nc,
                         "n_isolates": nis, "morans_i": round(I, 5), "expected_i": round(EI, 5),
                         "z_score": round(zsc, 4), "p_value": round(p_norm, 5),
                         "permutation_p_value": round(p_perm, 5),
                         "spatial_autocorrelation_flag": flag, "interpretation": interp,
                         "notes": "999 perms seed=12345; OLS residuals"})
            print(f"  {mid} [{wtype}]: I={I:.4f} EI={EI:.4f} z={zsc:.3f} p_perm={p_perm:.4f} flag={flag}")
    pd.DataFrame(rows).to_csv(out/"dfm01_mvp_residual_morans_i.csv", index=False)


if __name__ == "__main__":
    main()
