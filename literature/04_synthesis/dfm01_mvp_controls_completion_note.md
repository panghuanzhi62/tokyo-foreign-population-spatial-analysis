# DF_M01 MVP - Controls Completion / Coverage-Gap Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: controls join + gap assessment only. No downloads, no GIS, no models rerun, no
commercial-density proxy invented.

## A. Which controls are now joinable

Three controls were joined from data_raw/tokyo_features_v5_extended_with_density.csv to
the 251 frame on N03_007 -> municipality_code (no aggregation, no GIS):
- rail_accessibility = log_dist_to_station_m
- housing_cost = log_median_land_price_jpy
- population_density = population_density (2020)

Supplementary additions:
- population_2024 = 2024-01-01 Basic Resident Register total population
  (data_raw/000959256.xlsx), available for ALL 251.
- population_density_2024 = population_2024 / area_sqkm, computed only where area exists.
- rail_accessibility backfilled for municipalities present in the 227-row
  data_raw/tokyo_pop_with_station_features.csv but absent from v5 (log of
  dist_to_station_m), flagged rail_backfilled=YES.

commercial_density: NOT joinable - no local source.

## B. Exact coverage by control (out of 251)

- rail_accessibility: 227/251 (218 from v5 + 9 backfilled from pop_with_station).
- housing_cost: 218/251.
- population_density (2020): 218/251.
- population_density_2024: 218/251 (limited by area, not by population).
- population_2024 (total population only): 251/251.
- commercial_density: 0/251.
- v5 feature coverage: 218/251.

## C. Exact 33 municipalities missing from v5

Tokyo (13) islands (9): 13361, 13362, 13363, 13364, 13381, 13382, 13401, 13402, 13421.
Tokyo (13) mountain village/town (2): 13307, 13308.
Chiba (12) Boso/eastern cities + towns/villages (20): 12202, 12215, 12234, 12235, 12236,
12237, 12342, 12347, 12349, 12403, 12409, 12410, 12421, 12422, 12423, 12424, 12426,
12441, 12443, 12463 (includes real cities, e.g. 12202, 12215, 12234, 12235, 12236, 12237).
Saitama (11) Chichibu-area towns/villages (2): 11363, 11369.

Exact municipality names for all 251 (incl these 33) are in
outputs/modeling/dfm01_mvp/dfm01_mvp_controls_coverage_gap.csv. Of the 33, 9 received a
rail backfill from the 227-row table; 24 still lack rail, and all 33 lack housing and
v5-area-based density.

## D. Can 2024 population density be built from 000959256.xlsx plus area?

Partially. 2024 total population is available for all 251 from 000959256.xlsx, but
municipality AREA is available for only 218/251 (area_sqkm in v5). Therefore
population_density_2024 was computed for 218/251 only. Building it for the remaining 33
requires municipality area, which exists only in the N03-20250101 boundary shapefile and
would require GIS polygon-area computation (deferred; not run in this task). Missing
field for the 33: area_km2. Shortest next action: derive municipality area for the 33
(or all 251) from the N03 boundary layer in a separate approved GIS step, then complete
population_density_2024 at 251/251.

## E. Does commercial_density exist locally?

No. No establishment / business / commercial-density field exists in any local file.
data_raw/000959256.xlsx and 000959264.xlsx are Basic Resident Register population
(total and foreign); data_raw/isa_estat/ holds only ISA/MOJ foreign-resident T2
statistics (the X/Y source). No Economic Census / e-Stat establishment counts are
present. commercial_density must be constructed from an official establishment-count
source. Do NOT substitute DF_M04 real-estate brokers or restaurant/service POIs.

## F. Can the full models be run?

No. The formal main design requires rail_accessibility, housing_cost,
commercial_density, and population_density at acceptable (preferably 251/251) coverage.
commercial_density is 0/251 and the other controls reach only 218-227/251. Models 3 and
4 specifically require commercial_density and housing_cost. Therefore the full DF_M01 MVP
models are NOT run.

## G. Model readiness decision

NOT_READY_MISSING_COMMERCIAL_AND_COVERAGE_GAPS.

## H. Recommended next task

Single next step: acquire/construct commercial_density from an official municipality-level
establishment-count source (Economic Census / e-Stat) for the 251 frame, and derive
municipality area for the 33 missing municipalities from the N03 boundary layer to close
rail/housing/density coverage to 251/251 (both in separate approved steps). Then rerun the
four primary and four robustness DF_M01 MVP models (HC3) with full diagnostics. If the
user explicitly authorizes it, a clearly labeled EXPLORATORY reduced model (218 complete
cases, three controls, no commercial_density) could be prepared, but it must not be
presented as the main design and is not run here.
