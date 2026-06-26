# Existing Local Data Inventory and Reuse Audit - Tokyo-China Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (existing local/repo data inventory + reuse audit before acquisition)
Companion table: metadata/existing_local_data_inventory.csv

## A. Purpose

This audit inventories existing local and repository data-related files and
assesses which previously downloaded or processed assets may be reusable for the
new Tokyo-China Chinese-vs-non-Chinese workflow, which need metadata
reconstruction, which must be re-downloaded after approval, and which should
remain outside the public GitHub repository. It is performed BEFORE any new
download or API extraction.

## B. Evidence boundary

- This is an inventory and reuse audit.
- It is NOT data acquisition.
- It is NOT API extraction.
- It is NOT data cleaning.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- No decision was approved.
- The decision log was NOT modified.
- No existing data file was modified, moved, renamed, deleted, or copied.
- Current status remains: gap under verification.

## C. Locations inspected

Repo paths (existence reported, not modified):
- data/ (exists; contains data_sources.md and EMPTY raw/, processed/)
- data_raw/ (exists; ignored; holds the old baseline raw + processed assets)
- data_processed/ (exists; EMPTY; ignored)
- data_interim/ (MISSING), data_external/ (MISSING)
- outputs/ (exists), outputs/maps/ (EMPTY), outputs/tables/ (EMPTY),
  outputs/figures/ (analysis figures), outputs/round_09_extended_ols/ and
  outputs/round_11_target_audit/ (prior analysis/audit outputs),
  outputs/html/ (prior interactive output, ignored)
- outputs/model_outputs/ (MISSING), outputs/diagnostics/ (MISSING)

External local paths:
- E:\rsch\laborJapan_local_data (MISSING) and subfolders (MISSING)
- E:\rsch\laborJapan_local_fulltext (EXISTS; literature page snapshots in
  round02_manual_check; NOT statistical data)
- E:\rsch\laborJapan_local_temp (MISSING)

Missing locations were reported as missing and NOT created.

Also noted: metadata/population_baseline_manual_verification_results_template.csv
is referenced by the task input list but does NOT exist (never created); recorded
as a missing expected control file, not repaired here.

## D. Inventory summary

- total inventory rows: 36
- tracked repo data-related items: 5
- untracked ignored data-related items: 22
- repo untracked but NOT ignored: 1 (outputs/tables, empty)
- external local items (existing): 1 (laborJapan_local_fulltext)
- missing expected locations: 7
- direct_reuse_possible: 0
- reuse_after_metadata_reconstruction: 9
- reuse_for_context_only: 14
- do_not_reuse: 1 (tokyo_simulated_density.geojson - SIMULATED)
- must_re_download_after_approval: 0 (no existing file in this category; see note below)
- keep_local_only (recommended_action): 1; should_remain_local_only = yes: 17
- unknown / manual_review_needed (recommended_action): 14

Note on "must_re_download_after_approval = 0": no EXISTING file is the Chinese-
specific population source. The Chinese resident count (DDL_001) has NO existing
asset and must be acquired after approval - this is captured in section G, not as
an existing-file category.

## E. Reuse assessment by module

### 1. Population baseline
Exists: e-Stat population assets in data_raw/ (000959256.xlsx, 000959264.xlsx,
HDDSWH5339.zip, tblT001141H5339.zip) and processed all-foreign feature tables
(tokyo_pop_with_station_features, tokyo_features_v*). The OLD baseline measured
ALL-foreign-resident ratio, NOT Chinese vs non-Chinese.
Reuse: partial / context only. The xlsx and census archives are candidates for
the total foreign count (DDL_002) and total-population denominator (DDL_010)
ONLY after confirming exact table, year, and category. The Chinese resident
count (DDL_001) is NOT present and must be acquired (likely ISA nationality
table) after approval. Blocks reuse: no nationality (Chinese) breakdown
confirmed; metadata/license/checksum not reconstructed. New DDL approval still
required for DDL_001/002/010.

### 2. Administrative boundary / area denominator
Exists: NLNI N03-20250101 (municipal boundary, 2025-01-01, with KS-META xml) and
processed tokyo_metro_mainland_proj / tokyo_pop_dissolved geometries.
Reuse: yes after metadata reconstruction. N03 is a strong candidate for the area
denominator (DDL_012) and density (DDL_013). Blocks reuse: metadata, checksum,
license, and CRS confirmation needed; processed geometries must be matched to the
new analysis municipality set.

### 3. Railway / accessibility
Exists: NLNI N02-22 railway layer (2022) and processed nearest-station features
(tokyo_pop_with_station_features).
Reuse: layer reusable after metadata reconstruction (supports DDL_005); the
processed distances are on the old all-foreign geography (context only). Blocks
reuse: metadata/checksum/license/CRS; recompute accessibility on the new units.

### 4. Housing / land price
Exists: NLNI L01-24 land-price points for Saitama/Chiba/Tokyo/Kanagawa (prefs
11/12/13/14), 2024 vintage.
Reuse: yes after metadata reconstruction; supports a housing/land-value context
variable. Blocks reuse: no housing DDL row yet; license/metadata reconstruction
needed.

### 5. Hazard / disaster risk
Exists: NONE. No flood/landslide/tsunami/lowland/evacuation files were found.
Reuse: not applicable. These layers still require later source/layer approval
(NLNI hazard / Hazard Map Portal) per the decision log (DDL_006) - to be acquired
after approval, not reused.

### 6. Service / amenity
Exists: NONE. No facility/school/medical/community/OSM/multilingual-support data
files were found.
Reuse: not applicable; planned for later phases only.

### 7. Existing analysis outputs
Exists: OLS (round_09_extended_ols), LISA and MGWR figures (outputs/figures),
prior target/data_raw audit (round_11), interactive HTML (outputs/html).
Reuse: context only. These are OLD all-foreign baseline outputs and must NOT be
treated as results for the Tokyo-China Chinese-vs-non-Chinese workflow.
CAUTION: data_raw/tokyo_simulated_density.geojson is SIMULATED (do_not_reuse).

## F. Critical distinction

Older Tokyo baseline data may support the previous ALL-foreign-resident
settlement analysis, but they do NOT automatically satisfy the new Tokyo-China
Chinese-vs-non-Chinese workflow unless source, year, geography, nationality
category, administrative code, license, and metadata are verified. In particular,
no existing file is confirmed to contain a Chinese-nationality breakdown.

## G. Decision-log implications (decision log NOT changed)

- DDL_001 Chinese resident count: NO existing asset confirmed -> must be
  re-downloaded after approval (likely ISA nationality table). unknown whether
  any xlsx holds a nationality split; verify first.
- DDL_002 Total foreign resident count: possibly reusable from data_raw e-Stat
  xlsx/census archives -> needs exact-table verification + metadata
  reconstruction.
- DDL_010 Total population denominator: possibly reusable from data_raw census
  archive (tblT001141H5339 / HDDSWH5339) -> needs exact-table verification +
  metadata reconstruction.
- DDL_012 Administrative area denominator: likely reusable from N03-20250101 ->
  needs metadata reconstruction (checksum, license, CRS).
- DDL_013 Chinese resident density: depends on DDL_001 (missing) and DDL_012 ->
  cannot be computed yet.
- Derived DDL_003 / DDL_009 / DDL_011: cannot be computed until their source
  inputs are approved, acquired, and metadata-recorded.

The decision log was not edited; these are reuse observations only.

## H. Metadata reconstruction needs

Reusable candidates (e-Stat population archives, N03 boundary, N02 railway, L01
land price, processed boundary) each need, before reuse: source URL; exact
table/layer ID; download/access date; data year/version; license URL and
summary; raw file name; checksum_sha256; file size; encoding; CRS (if spatial);
join key (JIS municipality code); and preprocessing notes. None currently has a
metadata record in metadata/official_data_source_metadata_template.csv (which is
header-only).

## I. Repository safety conclusion

- Raw data should remain local or ignored unless the license explicitly permits
  commit and the user approves; data_raw/ and data_processed/ are correctly
  ignored.
- Public GitHub should generally contain metadata, scripts, documentation,
  checksums, and small derived tables only where permitted.
- Large GIS/raw files (N03 shp/geojson are hundreds of MB; tokyo_metro geojson
  tens of MB) must remain untracked.
- No PDFs or DOCX should be committed; none are tracked.

## J. Recommended next action

Based on the findings, the appropriate next step is a COMBINATION of Option 1 and
Option 2:

- Option 1 (spatial + denominator candidates exist): prepare a metadata
  reconstruction + checksum task for the strong reuse candidates (N03 boundary
  for DDL_012, N02 railway for DDL_005, L01 land price, and the e-Stat census
  archives for DDL_002/DDL_010) BEFORE any approval/download.
- Option 2 (Chinese-specific population is missing/insufficient): continue the
  manual exact-table verification (PBM_001/PBM_002/PBM_003) and plan a narrow
  acquisition for DDL_001 (Chinese count) after user approval.
- Option 3 also applies to spatial layers lacking metadata (N03/N02/L01):
  prepare a spatial-layer metadata reconstruction task.

Do not recommend bulk re-download. Do not recommend writing the final
Introduction yet. Status remains: gap under verification.
