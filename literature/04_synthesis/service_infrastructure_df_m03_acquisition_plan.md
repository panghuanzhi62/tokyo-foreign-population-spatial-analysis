# DF_M03 Licensed Employment Placement Offices - Acquisition / Validation Plan

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-25
Status: CONDITIONAL plan (source on HOLD). No modeling. No final M dataset. No heavy scraping.

## 0. Precondition (must pass before any acquisition)

Confirm a REPRODUCIBLE acquisition path. Acceptable paths, in priority order:
1. A CSV/Excel export within the Jinzai Service site search results (verify on the results
   screen, not the homepage/help).
2. A prefectural Labour Bureau published list (PDF/Excel) of licensed offices for Tokyo,
   Saitama, Chiba, Kanagawa.
3. A periodic official file (e.g., an MHLW open-data release).
If none exists, DO NOT scrape the dynamic site heavily; keep DF_M03 excluded from the main M.

## 1. Local-only raw folder

data_raw_official/service_infrastructure/DF_M03_licensed_employment_placement_offices/
- SOURCE_METADATA_local_only.txt  (already saved; reproducibility note; NOT committed)
- (only if a reproducible file is found) the downloaded list, local-only, NOT committed.

## 2. Retrieval steps (only if precondition passes)

- Portal: https://jinzai.hellowork.mhlw.go.jp/JinzaiWeb/ ; employment-placement search.
- Filter by prefecture (Tokyo/Saitama/Chiba/Kanagawa). Capture permit number, office name,
  address, permit date, expiration. Record URL and access date; respect terms and rate limits.

## 3. Parser requirements

- Parse office address to prefecture + municipality (reuse the DF_M01 municipality parser and
  the 251-frame name-to-JIS crosswalk). Use permit-number prefix to cross-check issuing
  prefecture.

## 4. Expected fields (parsed output, local-only)

permit_number, office_name, prefecture, municipality_name, municipality_code, permit_date,
expiration_date, business_type.

## 5. 2024 stock filter logic

- registered_by_2024_12_31 = permit_date <= 2024-12-31 (and not expired before the window).
- active_2024 approximation = permit valid (not expired) across 2024; flag right-censoring.

## 6. Municipality-linking approach

- Municipality parse + name-to-JIS crosswalk on the 251 frame; zero-fill; report link rate.

## 7. QC gates

- record count vs the source list size; municipality link rate; Greater Tokyo offices map to
  exactly one 251-frame municipality; counts sum; zeros explicit.

## 8. Files that must remain uncommitted

- any downloaded list, address-level/permit-level records, geocoded records, final M dataset.

## 9. Compact outputs allowed for commit

- this plan and the feasibility note; the source profile and sample QC CSVs (aggregate only);
  provenance rows; the three fixed reports.
