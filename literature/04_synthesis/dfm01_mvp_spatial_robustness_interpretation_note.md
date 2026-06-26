# DF_M01 MVP - Spatial Robustness (Synthesis / Manuscript-Facing Note)

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Cautious, manuscript-facing. No causal-mediation claim. No novelty claim. Main
interpretation unchanged.

## What was tested

The baseline growth-side null result (DF_M01 support-organization infrastructure in 2024 is
not associated with subsequent 2024-2025 Chinese-population growth) was tested against
explicit spatial dependence. On the same 218 complete-case municipalities (mainland populated
Greater Tokyo) and the same queen and KNN-6 weights used in the residual diagnostics, we fit
SLX (spatially lagged covariates), spatial-error (GM_Error), and spatial-lag (ML_Lag) models
for Model 2 and Model 4, and recomputed residual Moran's I.

## The residual spatial pattern was negative

Residual Moran's I was significantly NEGATIVE (queen about -0.10, KNN-6 about -0.08). This
indicates spatial DISPERSION or competitive differentiation between neighbouring
municipalities, not an omitted clustering process. Consistent with this, the estimated spatial
parameters are negative (spatial-lag rho about -0.37 to -0.39, p < 0.005; spatial-error lambda
about -0.33 to -0.41).

## The growth-side null is robust

Across OLS, SLX, spatial-error, and spatial-lag specifications, under both weighting schemes,
the service coefficient remains non-significant (p about 0.18-0.33), and the service x housing
interaction remains non-significant (p about 0.17-0.44). The spatial-lag model fully absorbs
the residual spatial autocorrelation (post-model Moran's I about 0, p about 0.88) without the
service coefficient becoming significant.

Therefore the absence of a short-term service-to-growth relationship is ROBUST to
spatial-dependence diagnostics. The interpretation does not need revision: the evidence is
consistent with migrant support-organization infrastructure FOLLOWING existing Chinese
population (the robust positive X -> M association) rather than DRIVING its subsequent growth
(the robust M -> Y null). The service-side X -> M association and the Model 3
commercial-density interaction are unaffected by these growth-side spatial checks.

Final interpretation: GROWTH_SIDE_NULL_SURVIVES_SPATIAL_ROBUSTNESS. Overall MVP reading
remains WEAK_PARTIAL_MECHANISM_EVIDENCE. These are temporally ordered associations, NOT causal
mediation.

## Caveats

- Estimand is mainland populated Greater Tokyo (N=218); 33 peripheral municipalities are
  excluded by missing rail/housing controls (one Boso unit, Katsuura, is additionally a queen
  island and is dropped from the ML spatial models, N=217).
- spreg ML_Error has a version-specific summary bug here, so the spatial-error model uses the
  GMM estimator (GM_Error); the decisive autocorrelation resolution comes from the spatial-lag
  model.
- Short outcome window (2024-12 to 2025-06); a null may also reflect the brevity of the window.

## Recommended next step

Consolidate baseline + collinearity + scaling + timing + spatial robustness into one
manuscript-facing results section. Do not claim causal mediation.
