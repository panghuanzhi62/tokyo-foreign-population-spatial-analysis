# Data Acquisition Control Files - Tokyo-China Opportunity-Risk Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (data acquisition control files)
Companion files: metadata/official_data_source_metadata_template.csv ;
metadata/data_download_decision_log.csv

## A. Purpose

This note documents the creation of two governance/control files that must exist
before any official data download or API extraction: a per-source metadata
template and a download decision log. Together they define how future official
datasets, API extracts, spatial layers, versions, licenses, storage locations,
and download decisions will be recorded.

## B. Evidence boundary

- This is reproducibility and governance planning.
- It is NOT data acquisition.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- Current status remains: gap under verification.

## C. Created control files

- metadata/official_data_source_metadata_template.csv - a header-only template
  (41 columns, 0 data rows). It will hold one provenance record per future
  downloaded dataset, API extract, or spatial layer. It should be filled at the
  moment each dataset is acquired (after approval), not before.
- metadata/data_download_decision_log.csv - a decision log (27 columns) seeded
  with 8 planned candidate rows (DDL_001..DDL_008), all with
  download_completed = no and decision_status either pending_user_approval (7) or
  hold (1, TSUNAGARI). It records, per acquisition unit, the decision to download
  or not, the licence check, the storage/commit policy, and the risk assessment.
  Rows must be approved by the user before any download.

Source coverage: the decision-log candidate rows use only source_ids already
present in the registry/inventory/blueprint/readiness checklist
(R02_OFF_TGT_002 ISA, R02_OFF_TGT_005 MLIT NLNI, R02_OFF_TGT_006 GSI,
R02_OFF_TGT_013 TSUNAGARI). No new source was invented. The metadata template is
source-agnostic (header-only) and applies to all priority sources.

## D. Metadata requirements

Every future downloaded dataset, API extract, or spatial layer must record at
least:

- source_id
- official source URL
- landing page or catalogue URL
- download / API route
- license or terms (URL + summary)
- data year / version
- geographic coverage
- spatial unit
- CRS if spatial
- file format
- checksum (SHA-256)
- storage location
- preprocessing script
- citation note
- public-repo commit permission

## E. Download decision rules

- No download without an explicit decision-log entry.
- No raw data committed to public GitHub unless explicitly approved AND the
  license allows it.
- All large / raw data should go to ignored data folders or outside-repo storage.
- Every download requires source metadata.
- Every API extraction requires a reproducible script and metadata.
- If the license is unclear, decision_status must remain hold or
  pending_user_approval.
- Official-source feasibility does NOT equal permission to redistribute data.

## F. Recommended first decision-log candidates

Likely first candidates (NOT approved; listed for planning only):

- e-Stat / ISA population baseline (DDL_001, DDL_002; derived non-Chinese
  construction DDL_003)
- MLIT NLNI administrative boundaries (DDL_004)
- MLIT NLNI railway stations (DDL_005)
- MLIT NLNI hazard layers (DDL_006)
- GSI spatial reference / basemap role (DDL_007)
- TSUNAGARI multilingual / service context (DDL_008, hold)
- Tokyo housing policy context (to add when a concrete dataset question arises;
  currently context-only)

## G. Repository safety plan

- Raw data should NOT be committed by default.
- Metadata and scripts may be committed after review.
- Credentials should NEVER be stored (no API keys in these files).
- PDFs, screenshots, downloaded data, and large files should not be staged.
- Data paths should be controlled by a project-root variable or configuration,
  not hard-coded personal paths.
- Checksums (SHA-256) should be recorded for any future downloaded files.

## H. Recommended next repo task

Recommended next task: prepare a .gitignore and local data-folder safety audit
for future data acquisition, including explicit ignored folders for raw downloads
(e.g. data_raw/), local full text, temporary outputs, and credentials, plus a
check that no raw data or secrets can be accidentally committed.

Do not recommend actual download yet. Do not recommend writing the final
Introduction yet. Status remains: gap under verification.
