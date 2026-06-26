# DF_M01 MVP - Growth-Side Spatial Robustness Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
No causal-mediation claim. Robustness checking only; not a diffusion theory.

## A. Purpose

Test whether the growth-side DF_M01 MVP results - the M -> Y null (Model 2) and the
M*housing null interaction (Model 4) - survive explicit modeling of spatial dependence.

## B. Why spatial robustness was needed

Residual Moran's I for the growth-side OLS models was significantly NEGATIVE (queen about
-0.10, KNN-6 about -0.08, permutation p about 0.015-0.024). Negative residual autocorrelation
indicates spatial DISPERSION / competitive differentiation among neighbours, not omitted
clustering. The OLS independence assumption is nonetheless violated, so spatial-dependence
robustness models are warranted.

## C. Model set

Packages: libpysal 4.14.1, spreg 1.8.5, geopandas 1.1.2, statsmodels 0.14.6 (esda NOT
installed - Moran's I implemented directly). Same 218 complete-case sample and same queen /
KNN-6 weights as the residual diagnostics. Queen has 1 island (12205 Katsuura-shi), which ML
inversion cannot handle, so the spatial-error/lag models drop that single unit (N=217); SLX
keeps it (zero spatial lags, N=218).
- OLS baseline (HC3) - reference.
- SLX: OLS + spatially lagged covariates (W_service, W_chinese_stock, W_commercial,
  W_population_density, W_rail, W_housing), HC3; queen and KNN-6.
- Spatial error (spreg GM_Error; ML_Error has a spreg 1.8.5 / numpy-2 summary bug): queen
  and KNN-6.
- Spatial lag (spreg ML_Lag): queen and KNN-6.

## D. Queen-weight results

Focal service coefficient (M -> Y), all NULL:
- SLX queen: 0.010, p=0.331 ; SEM queen: 0.013, p=0.256 ; SAR queen: 0.011, p=0.328.
- Model 4 interaction (M*housing): SLX -0.006 p=0.441 ; SEM -0.007 p=0.184 ; SAR -0.008 p=0.172
  (all null).
Spatial parameters NEGATIVE: SAR rho=-0.373 (p=0.0006); SEM lambda=-0.412 (GMM, no z-p).

## E. KNN-6 results

Focal service coefficient (M -> Y), all NULL:
- SLX knn6: 0.013, p=0.181 ; SEM knn6: 0.013, p=0.285 ; SAR knn6: 0.013, p=0.246.
- Model 4 interaction: SLX -0.009 p=0.315 ; SEM -0.007 p=0.193 ; SAR -0.008 p=0.190 (all null).
Spatial parameters NEGATIVE: SAR rho=-0.388 (p=0.004); SEM lambda=-0.327 (GMM).

## F. Whether M->Y null survives spatial robustness

YES. The service coefficient is non-significant in every specification (OLS, SLX, SEM, SAR;
queen and KNN-6; p ranges 0.18-0.33). No spatially explicit model produces a significant
service-to-growth relationship.

## G. Whether M*housing null survives spatial robustness

YES. The interaction is non-significant in every specification (p 0.17-0.44).

## H. Whether residual spatial autocorrelation is reduced or resolved

- Spatial LAG (SAR) RESOLVES it: post-model residual Moran's I about 0 (queen -0.0002 p=0.89;
  knn6 -0.0005 p=0.88). The negative rho captures the dispersion structure.
- SLX does NOT resolve it (lagged-X only): residuals remain significant (about -0.09 to -0.10).
- Spatial ERROR (GM_Error) RAW residuals remain significant (about -0.09 to -0.11); note this
  uses the raw residual u, not the spatially filtered residual, so it understates the error
  model's correction - a minor diagnostic caveat. The SAR result is the decisive one.

## I. Substantive interpretation

GROWTH_SIDE_NULL_SURVIVES_SPATIAL_ROBUSTNESS.

The absence of a short-term (2024 -> 2024-2025) relationship between DF_M01 support-
organization infrastructure and subsequent Chinese-population growth is robust to explicit
spatial-dependence modeling (SLX, spatial-error, spatial-lag, under two weighting schemes).
The spatial dependence that exists is NEGATIVE (rho, lambda < 0), consistent with local
dispersion / competitive differentiation rather than diffusion; it is fully absorbed by the
spatial-lag model without making the service coefficient significant. The main MVP
interpretation (WEAK_PARTIAL_MECHANISM_EVIDENCE: X -> M supported, M -> Y null) is UNCHANGED.
These are associations, NOT causal mediation.

## J. Recommended next task

Consolidate the DF_M01 MVP results (baseline + collinearity + scaling + timing + spatial
robustness) into a single manuscript-facing results section, with the estimand stated as
mainland populated Greater Tokyo (N=218). Optionally revisit a longer Y window when later ISA
stock waves are available. Do not claim causal mediation.
