# Population-Baseline Acquisition Approval Package - Tokyo-China Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (first P1 acquisition approval package: ISA / e-Stat population baseline)
Companion table: metadata/population_baseline_acquisition_approval_package.csv

## A. Purpose

This note prepares the FIRST P1 data acquisition approval package, for the
ISA / e-Stat population-baseline sources. It specifies what the user must
confirm and approve BEFORE any data download or API extraction begins. It maps
planned population-baseline variables to existing decision-log rows, lists the
exact manual checks required, and records (without editing the decision log)
where decision-log rows are missing.

## B. Evidence boundary

- This is a pre-download approval package.
- It is NOT data acquisition.
- It is NOT API extraction.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- Current status remains: gap under verification.

## C. Source scope

- R02_OFF_TGT_001 e-Stat - portal of official statistics; route to the total-
  population denominator and an alternate route to foreign-resident tables.
- R02_OFF_TGT_002 ISA resident foreigner statistics (Zairyu Gaikokujin Tokei) -
  foreign-resident counts by nationality and area; primary source for Chinese
  and total foreign counts.
- R02_OFF_TGT_004 Tokyo statistics - supplementary context only (Tokyo-level
  cross-check); not required for the core baseline and not included as an
  approval item here.

Category clarification (important):

- "Chinese residents" at this dataset-planning stage means Chinese NATIONALS, or
  Chinese residents BY NATIONALITY, depending on the official data category.
- This is NOT equivalent to Chinese-ORIGIN residents unless the official source
  explicitly defines it that way.
- Non-Chinese foreign residents should only be computed as all foreign residents
  minus Chinese nationals when category, year, and geography are consistent
  across both inputs.

## D. Approval package summary

- approval items: 6
- linked decision-log rows: 3 (DDL_001, DDL_002, DDL_003)
- items recommended approve_after_manual_table_check: 2 (PBA_001, PBA_002)
- items held for exact table check: 1 (PBA_005)
- items held for license check: 0
- items held for geography/category consistency: 3 (PBA_003, PBA_004, PBA_006)
- items with download_completed = no: 6 (all)
- approved downloads: 0
- completed downloads: 0

## E. Approval table

| approval_item_id | candidate variable or construct | source_id | decision_id | manual check required | approval condition | recommended user decision | risk level |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PBA_001 | Chinese resident count | R02_OFF_TGT_002 | DDL_001 | exact table/endpoint + license | approve after table/license confirmed | approve_after_manual_table_check | low |
| PBA_002 | Total foreign resident count | R02_OFF_TGT_002 | DDL_002 | table consistent with PBA_001 | approve after definition matched | approve_after_manual_table_check | low |
| PBA_003 | Non-Chinese foreign residents (derived) | R02_OFF_TGT_002 | DDL_003 | category/year/geography consistency | approve after PBA_001/002 approved | hold_until_geography_confirmed | low |
| PBA_004 | Chinese share of foreign residents (derived) | R02_OFF_TGT_002 | none (recommend new DDL) | denominator + year/geography match | approve after inputs + add DDL row | hold_until_geography_confirmed | low |
| PBA_005 | Foreign resident share of total population (derived) | R02_OFF_TGT_001 (+ISA) | none (recommend new DDL) | identify e-Stat population table | approve after table identified + add DDL row(s) | hold_until_exact_table_confirmed | medium |
| PBA_006 | Chinese resident density (area-based, optional) | R02_OFF_TGT_002 (+R02_OFF_TGT_005 boundary) | none (recommend new DDL) | boundary source + CRS | do not approve until boundary (DDL_004) approved | hold_until_geography_confirmed | medium |

## F. Required manual checks before approval

- exact official source page (ISA statistics page; e-Stat dataset listing)
- exact table / API endpoint (dataset ID; WebAPI endpoint and application ID)
- data year or period (biannual Jun/Dec; chosen vintage)
- geographic unit (municipality / prefecture)
- administrative code or join key (JIS municipality code; vintage across years)
- nationality category definition (Chinese nationals by nationality; total all-
  foreign definition)
- total foreign resident definition (total row vs sum over nationalities)
- total population denominator if needed (e-Stat table; whether it includes
  foreign residents)
- license or terms (Government Standard Terms applies to the exact table)
- planned storage location (data_raw/ gitignored or outside-repo working folder)
- metadata record fields (see section H)
- whether raw data may be committed (default: do NOT commit; keep local/ignored)
- construction logic for non-Chinese foreign residents (total minus Chinese)
- construction logic for share variables (ratios; zero-denominator handling)
- quality-control plan (totals reconcile; ranges valid; small-count flags)

## G. Decision-log linkage

Current decision-log rows relevant to the population baseline (unchanged; read
only):

| decision_id | source_id | candidate variable/layer | current decision_status | download_completed |
| --- | --- | --- | --- | --- |
| DDL_001 | R02_OFF_TGT_002 | Chinese resident count | pending_user_approval | no |
| DDL_002 | R02_OFF_TGT_002 | Total foreign resident count | pending_user_approval | no |
| DDL_003 | R02_OFF_TGT_002 | Non-Chinese foreign residents (derived) | pending_user_approval | no |

No decision has been approved and no download has been completed.

Recorded mismatches (NOT silently repaired; recommended FUTURE decision-log
updates only):

1. No DDL row for Chinese share of foreign residents (PBA_004).
2. No DDL row for foreign-resident share of total population (PBA_005).
3. No DDL row for density / area-based denominator (PBA_006).
4. No DDL row for the e-Stat total-population denominator (R02_OFF_TGT_001),
   which PBA_005 requires.

These should be added to metadata/data_download_decision_log.csv as new
pending_user_approval rows in a later, explicit update task. This package does
NOT edit the decision log.

## H. Metadata fields to fill after approval

From metadata/official_data_source_metadata_template.csv, fill when data are
actually acquired (after approval):

- metadata_record_id
- source_id
- dataset_or_layer_name
- source_url
- catalogue_or_landing_page_url
- download_or_api_url
- access_method
- data_type
- geographic_coverage
- spatial_unit
- temporal_coverage
- data_year_or_version
- download_or_access_date
- license_or_terms_url
- license_or_terms_summary
- storage_location_actual
- raw_file_name
- checksum_sha256
- file_size_bytes
- encoding
- language
- join_key
- preprocessing_required
- citation_note
- metadata_verified_status

## I. Repository safety rules for this source group

- No raw ISA / e-Stat files should be committed by default.
- Raw data should be stored outside the repo or in an ignored data_raw/ only
  after approval.
- Metadata and scripts may be committed after review.
- Every raw file needs a SHA-256 checksum recorded.
- Every API extraction must be reproducible (script + parameters + metadata).
- No credentials are expected for these sources.
- If an API key is ever required (e.g. e-Stat WebAPI application ID), it must be
  stored only in environment variables and NEVER committed.

## J. Recommended next action

- The user manually opens the official ISA and e-Stat pages and confirms the
  exact tables/endpoints, year, geography, category definitions, and license.
- The user decides which approval items to approve (candidates: PBA_001 and
  PBA_002 first; PBA_003 follows once inputs are consistent; PBA_004/005/006
  require new decision-log rows first).
- Only AFTER approval, prepare a narrow acquisition script or manual acquisition
  note for the approved items, and record metadata + checksums.

Do not recommend bulk download. Do not recommend writing the final Introduction
yet. Status remains: gap under verification.
