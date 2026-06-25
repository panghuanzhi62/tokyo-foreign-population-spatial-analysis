# DF_M01-Only MVP X-M-Y Model - Interpretation Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: PARTIAL - panel assembly and readiness check completed; models NOT fitted
(missing-input gate). No causal mediation claimed. No novelty asserted.

## 1. Why DF_M01 is the MVP M source

Among DF_M01-DF_M04, DF_M01 (registered support organizations / toroku shien kikan)
is the only currently usable main-M source: it is municipality-linkable, carries
registration dates, supports constructible municipality-level counts, and is
classified time_validity_class B_observable_by_2024_or_2025. Municipality counts for
registered_by_2024_06 and registered_by_2024_12 are already built for the full 251
Greater Tokyo frame (251/251 municipalities).

M is defined CAUTIOUSLY as institutional migrant-support service infrastructure
(registered institutional support organizations). It is NOT described as a complete
migrant-service ecosystem.

## 2. Why DF_M02, DF_M03, DF_M04 are excluded from the main M

- DF_M02 (Japanese-language education institutions): robustness/descriptive only;
  official list is prefecture-level and not directly municipality-linkable; no
  per-record 2024 validity.
- DF_M03 (licensed employment placement offices): conceptually useful but the
  authoritative source is search-only with no confirmed reproducible bulk source;
  HOLD_PENDING_SOURCE_VALIDATION.
- DF_M04 (real-estate broker registry): generic housing-market service registry, not
  migrant-oriented; control_candidate / robustness only.

Therefore the MVP main M uses DF_M01 only.

## 3. Temporal ordering (exact)

X (Chinese registered stock, 2023-12)
-> M (DF_M01 registered support-organization count; primary registered_by_2024_12,
   robustness registered_by_2024_06)
-> Y (Chinese registered stock growth; primary 2024-12 -> 2025-06, robustness
   2024-06 -> 2025-06).

X precedes M precedes Y. This ordering supports temporally ordered associations only.

## 4. Variable definitions

- X: chinese_stock_2023_12 ; z_log_chinese_stock_2023_12 = z(log1p(stock)).
- M primary: df_m01_support_count_2024_12 ; z_log_service_2024_12 = z(log1p(count)).
- M robustness: df_m01_support_count_2024_06 ; z_log_service_2024_06.
- Y primary: chinese_growth_log_2024_12_2025_06 = log1p(stock_2025_06) -
  log1p(stock_2024_12).
- Y robustness: chinese_growth_log_2024_06_2025_06 = log1p(stock_2025_06) -
  log1p(stock_2024_06).
- Controls: rail accessibility, housing cost / land price, commercial density,
  population density, non-Chinese foreign stock (z-standardized), and prefecture
  fixed effects C(prefecture).

## 5. Model formulas

- Model 1: z_log_service_2024_12 ~ z_log_chinese_stock_2023_12 + controls + C(prefecture)
- Model 2: chinese_growth_log_2024_12_2025_06 ~ z_log_service_2024_12 +
  z_log_chinese_stock_2023_12 + controls + C(prefecture)
- Model 3: z_log_service_2024_12 ~ z_log_chinese_stock_2023_12 * z_commercial_density +
  controls + C(prefecture)
- Model 4: chinese_growth_log_2024_12_2025_06 ~ z_log_service_2024_12 * z_housing_cost +
  z_log_chinese_stock_2023_12 + controls + C(prefecture)
Robustness block: same four models with M = z_log_service_2024_06 and
Y = chinese_growth_log_2024_06_2025_06. OLS, HC3 robust standard errors.

## 6. Current input status and why models were not fitted

Available at the official, processed, municipality level for the 251 frame:
- 251 frame, X (2023-12), Y (2024-06 / 2024-12 / 2025-06), M (DF_M01 2024-06 and
  2024-12), non-Chinese foreign stock (2020 census), prefecture fixed effects.

Missing (no processed municipality-level field for the 251 frame; see
model_readiness_inventory.csv):
- rail_accessibility - raw station shapefile only (data_raw/N02-22_GML/...).
- housing_cost / land price - raw land-price posting points only
  (data_raw/landPrice/L01-24_{11,12,13,14}_GML/*.shp).
- population_density - the processed population file holds only foreign counts (no
  total population); area exists only in the N03 boundary shapefile.
- commercial_density - NO source file anywhere in the repository.

Building rail accessibility, land price, and population density would require GIS
spatial operations (geocoding / spatial joins), which are not permitted in this task.
Commercial density has no source at all and would require new economic-census
acquisition. Per the design, proxies must not be invented. Therefore the runner
applied a missing-input gate and fitted NO models (Models 3 and 4 cannot even be
specified without commercial_density and housing_cost). See
outputs/modeling/dfm01_mvp/dfm01_mvp_model_run_note.md.

## 7. Limitations

- M is registered-by-snapshot, not active stock; one institutional service dimension
  only (not a full migrant-service ecosystem).
- non-Chinese foreign stock control is 2020 census vintage.
- The four missing controls block the specified adjusted models; an unadjusted or
  partially adjusted run was NOT performed because it would silently drop required
  controls and is outside the approved specification.

## 8. Non-causal interpretation language

These models are designed to test temporally ordered associations and
mechanism-consistent evidence. They do NOT identify causal mediation. Any future
results will be described as associations consistent (or inconsistent) with the
hypothesized mechanism, not as mediation or causal effects.

## 9. Does the current state support mechanism-consistent evidence?

Inconclusive at present: the assembled X-M-Y panel is temporally well ordered and
ready, but the specified adjusted models were not fitted because required controls
are missing. No association is reported yet.

## 10. Next step after MVP

Single next step: in a separate approved step, build a local-only processed
municipality-level controls table for the 251 frame (population_density from total
population + municipality area; housing_cost from L01 land-price layers;
rail_accessibility from N02 station layers; commercial_density via economic-census
acquisition), then re-run build + run scripts to fit the four primary and four
robustness models. Do not geocode or acquire controls inside this task.
