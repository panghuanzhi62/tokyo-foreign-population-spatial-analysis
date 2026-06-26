# DF_M01 MVP - Commercial-Density Construction and Model Rerun (Synthesis Note)

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: commercial_density constructed (251/251) from official 2021 Economic Census; full
DF_M01 MVP models rerun on complete-case N=218. No proxy/substitution; no causal-mediation
claim; no novelty claim.

## A. Purpose

Acquire/construct the last missing control (commercial_density) from official Economic
Census / e-Stat establishment counts and, once all controls are available, rerun the
DF_M01 MVP X-M-Y models.

## B. Source search and acquisition route

The repository contained no establishment-count file (the two xlsx are Basic Resident
Register population; isa_estat is the ISA/MOJ foreign-resident T2 source; tblT001141/MESH
is 2020 Census population mesh). The project already had a working e-Stat REST API
extraction pattern (used for the 2020 population census), with the application ID read from
the ESTAT_APP_ID environment variable. That same reproducible route was used here.

## C. Economic Census / e-Stat source identity

- Provider: e-Stat / Statistics Bureau of Japan.
- Statistics: 00200553 - Reiwa-3 (2021) Economic Census for Business Activity, establishment
  tabulation (jigyosho ni kansuru shukei, sangyo-odanteki shukei).
- Table: 0004005655 - industry(major) x opening-period x management-organization private
  establishments and employees, national/prefecture/municipality.
- Selection: tab=102-2021 (establishment count), cat01=AR (all industries excluding public
  service), cat02=00 (opening-period total), cat03=0 (management-organization total),
  time=2021000000, area=the 251 frame municipality codes.
- Raw API JSON saved local-only under data_raw_official/economic_census_establishments/
  (gitignored; not committed). appId never printed/written/committed.

## D. Field mapping and municipality-code linkage

The e-Stat area dimension is the 5-digit municipality/ward code (JIS5 = N03_007), matching
the 251 frame directly (designated-city wards included). All 251 frame codes were present;
establishment_count retrieved 251/251.

## E. Commercial-density construction

commercial_density = establishment_count / area_km2, where area_km2 was built locally from
the N03-20250101 boundary (geodesic). Coverage 251/251. Sanity checks: Chiyoda 3170 and
Chuo 3407 establishments/km2 (central business districts); Ogasawara 2.4; median ~99. In
the models it enters as z of log1p(commercial_density) because it is strongly right-skewed
(population density and non-Chinese foreign stock are treated the same way; rail and housing
are already on a log scale).

## F. Coverage and missingness

area_km2 251/251; population_density_2024 251/251; commercial_density 251/251;
rail_accessibility 227/251; housing_cost 218/251. The full-specification complete-case
sample is N=218, limited by housing_cost. The 33 excluded municipalities are systematically
peripheral (Tokyo islands and mountain villages, Chiba Boso/eastern, Saitama Chichibu), so
the estimand is mainland populated Greater Tokyo, not all 251. This is reported, not hidden
(see dfm01_mvp_missingness_summary.csv).

## G. Model readiness decision

READY_FULL_251_WITH_ACCEPTABLE_MISSINGNESS (complete-case N=218, composition reported).

## H. Whether models were rerun

Yes. Four primary and four robustness models were fit with HC3 robust SEs, plus
diagnostics (fit summary, missingness, descriptives, correlation, VIF, influence). Key
primary results:
- Model 1 (M ~ X + controls): z_log_chinese_stock_2023_12 = 0.427, p<0.001 - prior Chinese
  stock is positively associated with registered support-organization infrastructure
  (X -> M link, mechanism-consistent).
- Model 2 (Y growth ~ M + X + controls): z_log_service_2024_12 = 0.013, p=0.17 - service
  infrastructure is NOT associated with subsequent Chinese-stock growth (M -> Y link not
  supported); X coef -0.052, p=0.033 (slight convergence); growth adj R2 ~0.02.
- Model 3 (M ~ X * commercial_density): interaction 0.106, p=0.040 (positive); commercial
  density dominates the service-location model.
- Model 4 (Y ~ M * housing_cost): interaction -0.008, p=0.27 (null).
Caveats: substantial multicollinearity among urban-structure controls (VIF commercial 21.8,
population density 12.0, chinese stock 9.1, housing 8.3); growth is poorly explained.

Interpretation: mechanism-consistent evidence for the X -> M step only; the M -> Y step is
NOT supported. The overall X -> M -> Y chain is therefore weak/unsupported at the M -> Y
stage. These are temporally ordered associations, NOT causal mediation.

## I. Recommended next task

Decide whether to (a) extend rail/housing to the full 251 (resolving the peripheral-
municipality exclusion) for a full-coverage robustness run, (b) reconsider the M
specification (e.g., per-capita or per-foreign-resident service intensity instead of raw
log count), and (c) add spatial diagnostics (residual Moran's I) if an existing
spatial-weights file is available. Do not claim causal mediation.
