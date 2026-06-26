# DF_M01 MVP - Robustness & Diagnostics Interpretation (Synthesis Note)

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
No causal-mediation claim. No novelty claim. Robustness/diagnostics only; main model
unchanged. All HC3; complete-case N=218.

## A. Purpose

Determine whether the DF_M01 MVP findings are stable: (1) X -> M robustness; (2) M -> Y
null stability; (3) whether the Model 3 interaction survives reduced-collinearity
specifications; (4) whether the N=218 complete case creates geographic exclusion bias;
(5) residual spatial autocorrelation (if existing weights available).

## B. Baseline model recap

Primary (HC3, N=218): M1 X->M z_log_chinese_stock_2023_12 = 0.427 (p<0.001); M2 M->Y
z_log_service_2024_12 = 0.013 (p=0.17, null); M3 X*commercial interaction = 0.106 (p=0.040);
M4 M*housing interaction = -0.008 (p=0.27, null). Baseline VIFs high (commercial 21.8,
population_density 12.0).

## C. Complete-case exclusion audit

The 33 excluded municipalities are systematically peripheral (Chiba Boso/eastern 20, Tokyo
islands+mountain 11, Saitama Chichibu 2; Kanagawa 0). They are tiny and rural (median Chinese
stock 10 vs 808; population 6,968 vs 131,321; commercial_density 9 vs 127; DF_M01 count 0 vs
5). Binding constraint is housing_cost (all 33 lack housing; 24 also lack rail). The N=218
sample represents mainland populated Greater Tokyo with complete housing/rail controls;
complete-case modeling is defensible, but the exclusion is non-random, so the estimand should
be stated as "mainland/populated Greater Tokyo municipalities (N=218)".

## D. Collinearity diagnostics and reduced-collinearity results

Across baseline + 4 reduced-collinearity specs (drop population_density; drop commercial
except M3; residualized commercial; winsorized commercial):
- X -> M: positive in 4/5 (0.40-0.43, p<=0.002), attenuates to marginal (0.254, p=0.077)
  only when population_density is dropped -> robust but partly entangled with population
  density.
- M -> Y: stably null in all 5 specs (p 0.11-0.76).
- Model 3 X*commercial interaction: positive in all 5, significant in baseline/A/B/C and
  STRENGTHENS under reduced collinearity (A 0.329 p<0.001; C residualized 0.145 p=0.006);
  only marginal under winsorization (D 0.098 p=0.071) -> survives reduced collinearity.
- Model 4 M*housing interaction: stably null.

## E. Alternative M scaling diagnostics

Diagnostic Model 2 with service as raw count, log1p count, per-10k foreigners, and per-10k
population all give null M -> Y (p 0.17-0.96). The null is invariant to scaling. Per-capita
scalings are diagnostics only (denominator endogeneity).

## F. Timing robustness

X -> M stable across windows (0.427 -> 0.441, both p<0.001); M -> Y stably null (0.013 p=0.17
-> 0.007 p=0.51); Model 3 interaction stable positive (0.106 -> 0.124, p<=0.04); Model 4
stable null.

## G. Residual spatial autocorrelation check

NOT RUN - no compatible existing 251/218 spatial-weights file found; new weights are out of
scope this task. The null M -> Y therefore carries an unverified-spatial-autocorrelation
caveat (residual Moran's I deferred to a separate approved step).

## H. Substantive interpretation

WEAK_PARTIAL_MECHANISM_EVIDENCE.

The temporally ordered evidence supports the X -> M step only: prior Chinese stock is robustly
associated with the location of registered support-organization infrastructure, and that
association is amplified where commercial density is high (Model 3 interaction survives
reduced-collinearity). The M -> Y step is robustly null across every collinearity
specification, every service scaling, and both timing windows: support-organization
infrastructure in 2024 is not associated with subsequent 2024-2025 Chinese-stock growth.
Therefore the service-driven-growth mechanism is not supported; the data are consistent with
service infrastructure FOLLOWING existing population (X -> M) rather than DRIVING its growth
(M -> Y). These are associations, NOT causal mediation.

## I. Recommended next step

Single next step: build queen-contiguity spatial weights for the 218 complete-case
municipalities from the local N03-20250101 boundary and compute residual Moran's I for
Models 2 and 4 (primary and reduced-collinearity) to close the last robustness gap before any
manuscript framing. Do not claim causal mediation.
