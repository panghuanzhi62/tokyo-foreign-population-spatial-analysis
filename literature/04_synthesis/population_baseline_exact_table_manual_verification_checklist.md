# Population-Baseline Exact-Table Manual Verification Checklist - Tokyo-China Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (manual exact-table verification before any approval/download)
Companion table: metadata/population_baseline_exact_table_manual_verification_checklist.csv

## A. Purpose

This note prepares the manual exact-table verification checklist for the
ISA / e-Stat population-baseline data, to be completed by the user on the
official source pages BEFORE any approval, download, or API extraction. It tells
the user exactly what to confirm (table/endpoint, year, geography, category,
admin code, license, format) for each priority decision-log row.

## B. Evidence boundary

- This is manual-verification planning.
- It is NOT data acquisition.
- It is NOT API extraction.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- No decision was approved.
- Current status remains: gap under verification.

## C. Priority rows for manual check

Three decision-log rows must be manually checked FIRST because they are the
source inputs on which every derived population-baseline variable depends:

- DDL_001 - Chinese resident count (R02_OFF_TGT_002, ISA). The numerator for the
  Chinese-vs-non-Chinese contrast and the Chinese share.
- DDL_002 - Total foreign resident count (R02_OFF_TGT_002, ISA). The denominator
  for the Chinese share and the basis for the non-Chinese construction.
- DDL_010 - Total population denominator (R02_OFF_TGT_001, e-Stat). Required for
  the foreign-resident share of total population; introduces a second source
  whose vintage must align with the ISA foreign-resident tables.

All three are currently pending_user_approval with download_completed = no.

## D. Manual verification table

| manual_check_id | decision_id | candidate variable | source_id | exact item to confirm | approval condition | if not confirmed action |
| --- | --- | --- | --- | --- | --- | --- |
| PBM_001 | DDL_001 | Chinese resident count | R02_OFF_TGT_002 | ISA/e-Stat nationality-by-area table + dataset ID; year; municipality; Chinese-nationality category; JIS code; license | approve only if table, year, geography, category, license confirmed | keep DDL_001 pending; record unmet item |
| PBM_002 | DDL_002 | Total foreign resident count | R02_OFF_TGT_002 | total-foreign table in same family; same year/geography as PBM_001; total definition; license | approve only if denominator definition consistent with DDL_001 | keep DDL_002 pending; record unmet item |
| PBM_003 | DDL_010 | Total population denominator | R02_OFF_TGT_001 | e-Stat total-population table + dataset ID; year matched to DDL_002; geography; includes-foreign-residents?; license | approve only if same geography and compatible year matched to DDL_002 | keep DDL_010 pending; record unmet item |
| PBM_004 | DDL_003/009/011/012/013 | derived/dependent (summary) | ISA/e-Stat/NLNI | confirm input rows first; no new page; DDL_012 boundary is a separate NLNI check | do not approve/compute until inputs approved, acquired, metadata-recorded | keep all dependent rows pending; do not compute |

## E. Category and denominator cautions

- Chinese residents should be treated as Chinese NATIONALS or nationality-based
  residents if that is how the official table defines the category.
- Do NOT treat nationality-based Chinese residents as Chinese-ORIGIN residents.
- Non-Chinese foreign residents can only be computed as total foreign residents
  minus Chinese nationals if source, year, geography, and categories are
  consistent.
- Foreign-resident share requires a compatible total-population denominator
  (DDL_010), with aligned vintage and matching geography.
- Derived variables (DDL_003, DDL_009, DDL_011, DDL_013) cannot be computed
  before their source inputs are approved and metadata-recorded.

## F. Metadata fields to prepare after approval

From metadata/official_data_source_metadata_template.csv, complete after any
future acquisition:

- metadata_record_id
- source_id
- dataset_or_layer_name
- source_url
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

## G. Recommended approval sequence

1. Manually verify DDL_001 and DDL_002 first (PBM_001, PBM_002).
2. If both are confirmed, the user may approve ONLY DDL_001 and DDL_002 first.
3. Verify DDL_010 (PBM_003) before approving the foreign-resident share.
4. Do NOT approve derived rows (DDL_003, DDL_009, DDL_011, DDL_013) until input
   rows are confirmed and acquired.
5. Do NOT approve density (DDL_013) until the area/boundary source (DDL_012) is
   separately verified.

## H. What not to do yet

- Do not download data yet.
- Do not call APIs yet.
- Do not approve in the decision log yet.
- Do not compute variables yet.
- Do not write the final Introduction.
- Do not assert novelty.

## I. Recommended next action

- The user opens the official ISA and e-Stat pages in a browser and fills this
  manual checklist (table IDs, years, geography, category, license, format).
- After manual confirmation, prepare a narrow approval update for DDL_001 and
  DDL_002 only.

Status remains: gap under verification.
