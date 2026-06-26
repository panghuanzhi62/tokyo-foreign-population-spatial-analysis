# DF_M01 MVP - Remaining Controls Build Note (compact)

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: area + 2024 population density CONSTRUCTED (251/251); commercial_density MISSING;
models NOT rerun. No downloads, no proxies, no causal-mediation claim.

## Built this step
- area_km2: 251/251 from N03-20250101 boundary (geodesic WGS84, dissolved by N03_007).
  Validated vs known areas (Oshima 90.76, Choshi 84.12, Saitama-Nishi 29.12, Chiyoda 11.35).
- population_density_2024: 251/251 = Basic Resident Register 2024-01-01 total population
  (000959256.xlsx) / area_km2. Stronger 2024 vintage than the v5 2020 density (218/251);
  recommended to replace v5 2020 density in the model.

## Reused (partial)
- rail_accessibility: 227/251 (v5 log_dist_to_station_m + 9 pop_with_station backfills).
- housing_cost: 218/251 (v5 log_median_land_price_jpy, L01-24 2024).

## Still missing
- commercial_density: 0/251. No local establishment source; not acquired (see
  dfm01_mvp_commercial_density_missing_source_note.md for the e-Stat route).

## Readiness decision
NOT_READY_MISSING_COMMERCIAL_DENSITY. Models NOT rerun.

## Coverage table
control | coverage | ready
area_km2 | 251/251 | YES
population_density_2024 | 251/251 | YES
rail_accessibility | 227/251 | PARTIAL
housing_cost | 218/251 | PARTIAL
commercial_density | 0/251 | NO
