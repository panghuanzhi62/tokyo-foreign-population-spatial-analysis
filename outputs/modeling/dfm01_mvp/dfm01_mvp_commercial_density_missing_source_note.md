# DF_M01 MVP - commercial_density Missing-Source Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26

## Status

commercial_density remains MISSING (0/251). It was NOT constructed and NOT acquired in
this step. No proxy was substituted.

## Local search result

No official establishment-count source exists in the repository. Files checked:
- data_raw/000959256.xlsx, 000959264.xlsx: Basic Resident Register population (total /
  foreign) as of 2024-01-01 - population, not establishments.
- data_raw/isa_estat/: ISA/MOJ foreign-resident T2 statistics (the X/Y source).
- tblT001141H5339.txt + HDDSWH5339/MESH05339.shp: 2020 Census population mesh
  (table T001141 = population and households) - not establishments.
- data_raw/landPrice/ (L01-24): posted land prices; data_raw/N02-22, N03-20250101:
  rail and boundary GIS. None contain establishment counts.

## Why not acquired in this step

Official Economic Census establishment counts are distributed via e-Stat, whose
reproducible programmatic access requires an application ID (appId) for the statsData
API, or navigation of dynamic, token-based file-download pages. Neither is reproducible
in one shot in this environment, so acquisition was not attempted (to avoid a fragile,
non-reproducible scrape). Per instruction, no DF_M04 broker, POI, restaurant, or
informal-directory substitute was used.

## Shortest official acquisition route (next approved step)

1. Source: e-Stat Economic Census for Business Activity (keizai census katsudo chosa,
   2021) or Economic Census Basic Survey (kiso chosa) - establishment counts (jigyosho-su)
   by municipality (shikuchoson).
   Government statistics codes (toukei code): 00200553 (activity survey) /
   00200552 (basic survey).
2. Acquire municipality-level total establishment counts for prefectures 11/12/13/14
   (or nationwide then filter to the 251 frame on the 5-digit municipality code).
3. Join to the 251 frame; compute commercial_density = total_establishments / area_km2
   (area_km2 is already built locally for all 251).
4. Optional richer definition: commercial/service establishments per km2 if industry
   classes are retained.
5. Save local-only; commit only a compact QC summary.

## Effect on modeling

The formal main DF_M01 MVP model requires commercial_density (and Models 3/4 depend on
it). With commercial_density at 0/251, the full models are NOT run. Decision:
NOT_READY_MISSING_COMMERCIAL_DENSITY.
