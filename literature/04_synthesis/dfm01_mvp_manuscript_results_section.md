# DF_M01 MVP - Manuscript-Facing Results Section (Draft)

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Draft for possible manuscript use. Cautious, association-only language. No causal-mediation
claim. No novelty claim. M = institutional migrant-support service infrastructure (registered
support organizations), NOT a complete migrant-service ecosystem.

## 4.1 Analytical sample and control coverage

The study frame is the 251 municipality-equivalent units of Greater Tokyo (Tokyo, Saitama,
Chiba, and Kanagawa; designated-city wards treated as units). The exposure X is the Chinese
registered-resident stock as of December 2023; the mediator-position variable M is the
municipality count of registered support organizations (DF_M01, toroku shien kikan) observable
by 2024 (primary: registered-by 2024-12; robustness: 2024-06); the outcome Y is the change in
Chinese registered stock from December 2024 to June 2025. Controls are rail accessibility,
housing cost (posted land price), commercial density (2021 Economic Census establishments per
square kilometre), 2024 population density, non-Chinese foreign stock, and prefecture fixed
effects. Commercial density, municipality area, and 2024 population density are available for
all 251 units; rail accessibility (227/251) and housing cost (218/251) are available for the
mainland populated core.

The full-specification complete-case sample is N=218. The 33 excluded municipalities are
systematically peripheral and small (Tokyo islands and mountain villages, the Chiba
Boso/eastern fringe, and two Saitama Chichibu-area towns/villages; Kanagawa is fully retained),
with much lower Chinese stock, population, and service counts than the included core. The
estimand is therefore best described as the mainland populated Greater Tokyo municipalities
with complete rail and housing controls (N=218); because the exclusion is non-random, results
should not be generalized to the smallest peripheral units.

## 4.2 Baseline X-M-Y models

All models use OLS with HC3 robust standard errors; continuous predictors are standardized
(commercial density, population density, and non-Chinese foreign stock as standardized
log1p values). See dfm01_mvp_manuscript_table_baseline_results.csv.

- Model 1 (M on X). Prior Chinese stock is positively and significantly associated with the
  count of registered support organizations (standardized coefficient 0.427, p < 0.001; adj
  R-squared 0.842). Institutional support infrastructure is spatially aligned with prior
  Chinese population concentration.
- Model 2 (Y on M). The support-organization count is not associated with subsequent short-term
  Chinese registered-stock growth (standardized coefficient 0.013, p = 0.168; adj R-squared
  0.019). The model does not provide robust evidence that institutional support infrastructure
  is followed by faster registered-stock growth.
- Model 3 (M on X, moderated by commercial density). The alignment between prior Chinese stock
  and support-organization formation is stronger in commercially denser municipalities
  (interaction 0.106, p = 0.040). This conditioning is partially robust (see 4.3).
- Model 4 (Y on M, moderated by housing cost). There is no robust evidence that any
  service-to-growth association is moderated by housing cost (interaction -0.008, p = 0.267).

## 4.3 Robustness checks

See dfm01_mvp_manuscript_table_robustness_summary.csv.

- Collinearity (5 specifications: baseline, drop population density, drop commercial except as
  the Model 3 moderator, residualized commercial, winsorized commercial). The X-M association
  remains positive (attenuating to marginal only when population density is dropped); the M-Y
  association remains null throughout; the Model 3 interaction survives reduced-collinearity
  specifications (strengthening when population density is dropped and when commercial density is
  residualized) and is marginal only under winsorization; the Model 4 interaction remains null.
- Alternative M scaling (raw count, log1p count, support organizations per 10,000 foreign
  residents, per 10,000 total population). The M-Y null is invariant to scaling (p 0.17-0.96);
  per-capita scalings are reported as diagnostics only because of denominator endogeneity.
- Timing (primary 2024-12 window vs robustness 2024-06 window). The X-M association is stable
  (0.427 vs 0.441) and the M-Y null is stable (0.013, p 0.17 vs 0.007, p 0.51).
- Residual spatial autocorrelation. Before spatial modelling, the growth-side residuals show
  statistically significant negative spatial autocorrelation (queen Moran's I about -0.10;
  KNN-6 about -0.08), indicating spatial dispersion rather than clustering.
- Explicit spatial robustness (4.4).

## 4.4 Spatial robustness interpretation

Because the growth-side residual Moran's I was significantly negative, we fit spatially explicit
robustness models on the same 218 complete-case sample using queen and KNN-6 weights: SLX
(spatially lagged covariates), a spatial-error model (GM_Error), and a spatial-lag model
(ML_Lag). The negative residual Moran's I indicates dispersion or competitive differentiation
between neighbouring municipalities, not omitted clustering; consistent with this, the estimated
spatial parameters are negative (spatial-lag rho about -0.37 to -0.39, p < 0.005; spatial-error
lambda about -0.33 to -0.41). Across all specifications and both weighting schemes, the
service coefficient remains non-significant (p about 0.18-0.33) and the service-by-housing
interaction remains non-significant (p about 0.17-0.44). The spatial-lag model resolves the
residual autocorrelation (post-model Moran's I about 0, p about 0.88). The growth-side null is
thus robust to explicit spatial-dependence modelling.

## 4.5 Substantive interpretation

Institutional migrant-support services are strongly aligned with prior Chinese population
concentration, especially in commercially dense municipalities. However, these services do not
robustly predict short-term subsequent Chinese registered-resident growth once urban
opportunity controls, alternative service scaling, timing choices, and spatial dependence are
considered.

## 4.6 What the results do and do not support

Supported:
- a population-to-service alignment (prior Chinese stock is associated with institutional
  support infrastructure);
- a commercial-density conditioning of service formation (the alignment is stronger where
  commercial density is high);
- the absence of a robust short-term service-to-growth relationship.

Not supported:
- causal mediation of any kind;
- institutional support infrastructure as a short-term driver of Chinese population growth;
- claims about a full migrant-service ecosystem (M is one institutional, non-China-specific
  dimension only).

These are temporally ordered associations on public official data; they are not causal effects.
