# DF_M01 MVP - Existing Controls Inventory / Mapping Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: inventory/mapping only. No controls built, no GIS processing, no downloads, no
models rerun. No proxies invented.

## A. Purpose

The DF_M01-only MVP model previously stopped at a missing-input gate for four controls
(rail_accessibility, housing_cost, commercial_density, population_density). This note
checks whether those controls ALREADY EXIST in the local Tokyo project files under
data_raw, before building or downloading anything new.

## B. Search scope

Files inspected (column names, row counts, keys, candidate fields):
- data_raw/tokyo_features_v5_extended_with_density.csv (218 rows)
- data_raw/tokyo_mgwr_ready.csv (218)
- data_raw/tokyo_features_v4_extended_prep.csv (218)
- data_raw/tokyo_features_v3_ols.csv (218)
- data_raw/tokyo_features_v2.csv (218)
- data_raw/tokyo_features_v1.csv (227)
- data_raw/tokyo_pop_with_station_features.csv (227)
- data_raw/tokyo_pop_dissolved.csv (227)
- data_raw/000959256.xlsx, data_raw/000959264.xlsx (Basic Resident Register, 2024-01-01)
- folders noted (not processed): data_raw/landPrice/ (L01-24 GML, 4 prefectures),
  data_raw/N02-22_GML/ (stations), data_raw/N03-20250101_GML/ (boundaries),
  data_raw/isa_estat/ (ISA/MOJ foreign-resident T2 stats = the X/Y source).
Keywords: station, rail, dist_to_station, land_price, median_land_price, commercial,
establishment, business, jigyosho, keizai census, population, total_pop, area, density.

Key/coverage facts: the feature tables key on N03_007 (JIS 5-digit municipality/ward
code) and join cleanly to the 251 frame, but cover only 218/251 (v5 family) or 227/251
(v1/pop family). The 33 missing from v5 are mostly Chiba and Tokyo towns/villages
(e.g. 12xxx gun, Tokyo island/mountain villages). The xlsx use dantai_code (6-digit =
JIS5 + check digit) and cover all municipalities nationwide.

## C. Findings by control

### rail_accessibility - FOUND (partial coverage)
- Best candidate: data_raw/tokyo_features_v5_extended_with_density.csv, field
  log_dist_to_station_m (raw metres available in tokyo_features_v2.csv as
  dist_to_station_m; station names in v1/pop_with_station).
- Apparent year: N02-22 station network (2022). year_class B_baseline_structural.
- Usable for main model: YES as a structural baseline, but only 218/251 directly;
  tokyo_pop_with_station_features.csv (227) can backfill some rows.
- Join to 251 frame: DIRECT on N03_007 -> municipality_code (no aggregation, no GIS).
- Limitation: 33-municipality coverage gap; distance-to-nearest-station is an inverse
  accessibility proxy.

### housing_cost / land price - FOUND (partial coverage)
- Best candidate: tokyo_features_v5, field log_median_land_price_jpy (raw JPY in
  tokyo_features_v2 as median_land_price_jpy).
- Apparent year: L01-24 official posted land prices (2024). year_class A_direct_2024.
- Usable for main model: YES (strongest temporal match; 2024). Coverage 218/251.
- Join to 251 frame: DIRECT on N03_007 (already aggregated to municipality; no GIS).
- Limitation: 33-municipality coverage gap.

### population_density - FOUND (partial coverage)
- Best candidate: tokyo_features_v5, field population_density (also
  log_population_density, plus components total_pop and area_sqkm).
- Apparent year: total population ~2020 census; area from N03 boundary.
  year_class B_baseline_structural.
- Supplementary: 000959256.xlsx gives Basic Resident Register TOTAL POPULATION as of
  2024-01-01 for ALL 251 municipalities (incl the 33 missing from v5), but converting to
  density still needs municipality area (N03 GIS, deferred this task).
- Usable for main model: YES as 2020 baseline density (218/251); full-coverage 2024
  density would require deferred GIS area work.
- Join to 251 frame: DIRECT on N03_007 for v5; xlsx needs check-digit strip.
- Limitation: 33-municipality coverage gap for the precomputed density.

### commercial_density - NOT FOUND
- No establishment / business / commercial-density field exists in any local file.
- isa_estat holds only ISA/MOJ foreign-resident T2 statistics (the X/Y source); the two
  numeric xlsx are Basic Resident Register population (not Economic Census).
- year_class D_unusable (no source). recommended_action: construct_new_source
  (Economic Census / keizai census establishment counts) in a separate approved step.

## D. Decision

PARTIAL_CONTROLS_FOUND.

Three of four controls (rail_accessibility, housing_cost, population_density) already
exist as precomputed, municipality-level fields that join directly to the 251 frame on
N03_007 - but only for 218/251 municipalities. The fourth (commercial_density) has no
local source. Therefore not ALL_CONTROLS_FOUND_READY_TO_JOIN.

## E. Recommended next task

Single next step: in a separate approved step, JOIN the three found controls
(log_dist_to_station_m, log_median_land_price_jpy, population_density) from
tokyo_features_v5 to the DF_M01 MVP model panel on N03_007 -> municipality_code, then
decide how to handle (a) the 33-municipality coverage gap (backfill from the 227-row
tables and/or the 2024 Basic Resident Register population + deferred N03 area) and
(b) the still-missing commercial_density (construct from Economic Census, or run a
reduced model that omits/limits commercial_density with that limitation stated). Do not
build, aggregate, geocode, download, or rerun models in this task.
