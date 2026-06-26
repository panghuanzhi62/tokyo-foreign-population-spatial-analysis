# DF_M01 MVP - Residual Spatial Autocorrelation Diagnostics Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
No causal-mediation claim. Main interpretation unchanged.

## A. Purpose

Test whether the growth-side OLS residuals (Models 2 and 4) exhibit residual spatial
autocorrelation, which would violate the OLS independence assumption underlying the HC3
inference for the M -> Y null and the M*housing interaction.

## B. Sample and boundary source

Complete-case N=218 (the same sample as the MVP rerun and robustness diagnostics).
Boundary: data_raw/N03-20250101_GML/N03-20250101.shp, dissolved by N03_007 to municipality/
ward units and restricted to the 218 complete-case codes. See dfm01_mvp_spatial_sample_qc.csv.

## C. Spatial weights construction

- Queen contiguity, row-standardized: 218 units, neighbors min/median/max = 0/5/11, but the
  graph is NOT fully connected: 2 components and 1 ISLAND (12205 Katsuura-shi), whose
  Boso-peninsula land neighbors (e.g. Otaki 12441, Onjuku 12443) are in the excluded 33.
- Because an island exists, a k-nearest-neighbor (k=6) sensitivity weighting was also built
  (no isolates, every unit has 6 neighbors). See dfm01_mvp_spatial_weights_qc.csv.
- Moran's I implemented directly (esda not installed): observed I, analytical E[I]=-1/(n-1),
  permutation inference (999 permutations, seed=12345), permutation two-sided p.

## D. Residual Moran's I results

All four target models show SIGNIFICANT NEGATIVE residual spatial autocorrelation under both
weighting schemes (see dfm01_mvp_residual_morans_i.csv):

Queen (row-standardized):
- Primary Model 2: I=-0.102, E[I]=-0.005, z=-2.68, p_perm=0.015 -> YES
- Primary Model 4: I=-0.104, z=-2.72, p_perm=0.015 -> YES
- Reduced-collinearity (drop population_density) Model 2: I=-0.094, z=-2.45, p_perm=0.020 -> YES
- Reduced-collinearity Model 4: I=-0.104, z=-2.72, p_perm=0.015 -> YES

KNN-6 sensitivity (row-standardized; no isolates):
- Primary Model 2: I=-0.079, z=-2.38, p_perm=0.019 -> YES
- Primary Model 4: I=-0.078, z=-2.33, p_perm=0.022 -> YES
- Reduced-collinearity Model 2: I=-0.077, z=-2.33, p_perm=0.024 -> YES
- Reduced-collinearity Model 4: I=-0.078, z=-2.33, p_perm=0.023 -> YES

The negative sign and significance are stable across queen vs KNN-6, so they are NOT an
artifact of the single queen island.

## E. Implications for Model 2 M->Y null result

The M -> Y null is robust to this finding. The residual autocorrelation is NEGATIVE
(neighboring municipalities have DISSIMILAR growth residuals - a dispersion/competition
pattern, not clustering). Negative autocorrelation does not manufacture a null result; and
the null was already stable across all collinearity specs, all service scalings, and both
timing windows. So the M -> Y null is not an artifact of spatial structure. However, because
residual autocorrelation is statistically significant, the OLS independence assumption is
violated, so a spatial-error / spatial-lag robustness model would strengthen the inference
before any strong claim.

## F. Implications for Model 4 M*housing null result

Same conclusion: the M*housing interaction null stands, but a spatial model robustness check
is warranted given the significant negative residual autocorrelation.

## G. Limitations

- Queen graph is not fully connected (1 island, 2 components) because the excluded 33
  peripheral municipalities sever some Boso-peninsula adjacencies; KNN-6 was used as a
  sensitivity to address this and confirms the result.
- Moran's I was implemented directly (esda unavailable); inference is permutation-based
  (999 perms) and uses the analytical E[I]; a full esda cross-check is deferred.
- This is a residual-diagnostic only; no spatial-error/spatial-lag model was fit here.

## H. Recommended next task

Fit spatial-error and/or spatial-lag (SLX) robustness versions of Models 2 and 4 on the 218
complete-case sample (spreg or statsmodels) using these weights, to confirm the M -> Y null
and the interactions under explicit spatial dependence. Do not claim causal mediation.
