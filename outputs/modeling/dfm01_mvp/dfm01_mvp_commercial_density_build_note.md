# DF_M01 MVP - commercial_density Build Note (compact)

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: commercial_density CONSTRUCTED 251/251 from official 2021 Economic Census; full
DF_M01 MVP models rerun on complete-case N=218. No proxy/substitution. No causal mediation.

## Source
e-Stat statistics 00200553 (2021 Economic Census for Business Activity, establishment
tabulation), table 0004005655. Selection: tab=102-2021 (jigyosho-su / establishment
count), cat01=AR (all industries excl. public service), cat02=00 and cat03=0 (totals),
time=2021. Acquired via the e-Stat REST API (appId from ESTAT_APP_ID env; never committed).
Raw JSON saved local-only under data_raw_official/economic_census_establishments/.

## Construction
commercial_density = establishment_count / area_km2 (area_km2 built locally from N03).
Coverage 251/251. Sanity: Chiyoda 3170, Chuo 3407 estab/km2 (CBDs); Ogasawara 2.4;
median ~99. Modeled as z of log1p(commercial_density) (right-skewed).

## Coverage of all controls (251 frame)
area_km2 251/251 ; population_density_2024 251/251 ; commercial_density 251/251 ;
rail_accessibility 227/251 ; housing_cost 218/251.

## Readiness + models
READY_FULL_251_WITH_ACCEPTABLE_MISSINGNESS. Complete-case N=218 (limited by housing_cost;
33 excluded = Tokyo islands/mountain, Chiba Boso, Saitama Chichibu). Models rerun (HC3):
- M1 (M~X): z_log_chinese_stock_2023_12 = 0.427, p<0.001 (X->M positive).
- M2 (Y~M+X): z_log_service_2024_12 = 0.013, p=0.17 (M->Y null); X coef -0.052, p=0.033.
- M3 (M~X*commercial): interaction 0.106, p=0.040 (sig).
- M4 (Y~M*housing): interaction -0.008, p=0.27 (null).
VIF: commercial 21.8, population_density 12.0, chinese_stock 9.1, housing 8.3 (multicollinear).

## Interpretation
Mechanism-consistent for X->M only; M->Y is not supported (null, growth adj R2 ~0.02).
Associations only; NOT causal mediation.
