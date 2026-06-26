# DF_M01 MVP - Remaining Controls Construction (Synthesis Note)

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: area and 2024 population density constructed for all 251; commercial_density still
missing; full models NOT rerun. No downloads beyond existing local files; no proxies; no
causal-mediation claim.

## A. Purpose

Construct the remaining controls required for full 251-municipality DF_M01 MVP modeling:
municipality area, a full-coverage 2024 population density, and commercial_density. Then
decide whether the four primary and four robustness models can be run.

## B. Area construction from N03

Municipality area_km2 was derived for all 251 municipalities from the existing local
boundary layer data_raw/N03-20250101_GML/N03-20250101.shp (no download). Polygons were
filtered to prefectures 11/12/13/14, dissolved by N03_007 (ward-level codes for
designated cities, matching the frame), reprojected to geographic WGS84, and area was
computed geodesically (pyproj Geod, ellipsoidal) so the Izu/Ogasawara islands are handled
correctly without a single-zone projection error. Coverage: 251/251. Validation against
known municipal areas is close: Oshima 90.76 km2, Choshi 84.12, Saitama-Nishi 29.12
(matches v5 area_sqkm 29.10), Chiyoda 11.35. Output is local-only; a compact QC summary
is committed (dfm01_mvp_area_build_qc_summary.csv).

## C. 2024 population density construction

2024 total population (Basic Resident Register, 2024-01-01) from data_raw/000959256.xlsx
is available for all 251 municipalities (dantai code -> JIS5). Joining to the new area
table gives population_density_2024 = population_2024 / area_km2 for 251/251. This is a
full-coverage, 2024-vintage density that improves on the v5 2020 population_density
(218/251). Recommendation: use population_density_2024 as the model's population-density
control (year_class A_direct_2024), with the v5 2020 density retained only as a robustness
cross-check. Outputs are local-only; a compact QC summary is committed
(dfm01_mvp_population_density_2024_qc_summary.csv).

## D. Commercial-density source and construction status

commercial_density could NOT be constructed: there is no official establishment-count
source in the repository (the two xlsx are Basic Resident Register population; isa_estat
is the ISA/MOJ foreign-resident T2 source; tblT001141/MESH is 2020 Census population
mesh; landPrice and N02/N03 are land-price and GIS layers). Official Economic Census
establishment counts are distributed via e-Stat, which is not reproducibly downloadable
in this environment without an API appId, so acquisition was not attempted. No DF_M04
broker, POI, restaurant, or informal substitute was used. See
dfm01_mvp_commercial_density_missing_source_note.md for the exact e-Stat acquisition
route (toukei codes 00200553 / 00200552; commercial_density = total establishments /
area_km2, area already available locally).

## E. Remaining missingness and coverage

- area_km2: 251/251 (constructed).
- population_density_2024: 251/251 (constructed).
- rail_accessibility: 227/251 (24 still missing).
- housing_cost: 218/251 (33 still missing).
- commercial_density: 0/251 (missing).

## F. Model readiness decision

NOT_READY_MISSING_COMMERCIAL_DENSITY. The formal main model requires
rail_accessibility, housing_cost, commercial_density, and population_density at acceptable
coverage. Two of the four blocking gaps are now fully resolved (area-enabled 2024 density
at 251/251), but commercial_density is entirely absent and rail/housing remain at
227/218. Models 3 and 4 specifically require commercial_density and housing_cost.

## G. Whether models were rerun

No. Per instruction, the models are not rerun until commercial_density is available, and
the 218-case reduced model is not run without explicit authorization.

## H. Recommended next task

Acquire official Economic Census municipality establishment counts from e-Stat for the
251 frame (then commercial_density = total establishments / area_km2), and decide whether
to fill the remaining rail (24) and housing (33) gaps or to run a documented complete-case
model. Then rerun the four primary and four robustness DF_M01 MVP models (HC3) with full
diagnostics. Do not claim causal mediation; results will be framed as temporally ordered,
mechanism-consistent associations.
