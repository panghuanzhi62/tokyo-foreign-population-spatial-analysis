# Population-Baseline Decision-Log Update - Tokyo-China Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (decision-log update: missing population-baseline derived variables + denominators)
Companion file: metadata/data_download_decision_log.csv

## A. Purpose

This note documents the explicit, append-only addition of new
pending_user_approval rows to the data download decision log for the
population-baseline derived variables and prerequisites that the acquisition
approval package identified as missing. It closes the recorded mismatch without
editing any existing decision-log row and without approving any decision.

## B. Evidence boundary

- This is decision-log governance.
- It is NOT data acquisition.
- It is NOT API extraction.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- No decision was approved.
- Current status remains: gap under verification.

## C. Existing decision-log rows preserved

The three core population-baseline rows were preserved byte-for-byte (verified:
the change is purely additive, 5 insertions, 0 deletions):

- DDL_001 - Chinese resident count (R02_OFF_TGT_002): decision_status remains
  pending_user_approval; download_completed remains no.
- DDL_002 - Total foreign resident count (R02_OFF_TGT_002): decision_status
  remains pending_user_approval; download_completed remains no.
- DDL_003 - Non-Chinese foreign residents derived (R02_OFF_TGT_002):
  decision_status remains pending_user_approval; download_completed remains no.

(DDL_004..DDL_008 - the spatial/disaster/service rows - were also left
unchanged.)

## D. New decision-log rows added

Five rows appended as DDL_009..DDL_013 (next sequential IDs after the prior
maximum DDL_008):

| decision_id | candidate_variable_or_layer | source_id | reason | decision_status | download_completed | approval_required_before_download |
| --- | --- | --- | --- | --- | --- | --- |
| DDL_009 | Chinese share of foreign residents | R02_OFF_TGT_002 | Derived ratio requiring approved DDL_001 and DDL_002 inputs | pending_user_approval | no | yes |
| DDL_010 | Total population denominator | R02_OFF_TGT_001 | Needed to compute foreign resident share of total population | pending_user_approval | no | yes |
| DDL_011 | Foreign resident share of total population | R02_OFF_TGT_001 + R02_OFF_TGT_002 | Derived share requiring total foreign count and total population denominator | pending_user_approval | no | yes |
| DDL_012 | Administrative area denominator for density | R02_OFF_TGT_005 | Needed only if density / area-normalized measures are constructed | pending_user_approval | no | yes |
| DDL_013 | Chinese resident density | R02_OFF_TGT_002 + R02_OFF_TGT_005 | Optional derived density requiring approved Chinese count and area denominator | pending_user_approval | no | yes |

All five carry: license_checked = no/partial, license_status = not_checked/
unclear, repo_commit_policy = do_not_commit_raw_data, download_completed = no,
blank download_date/location, blank metadata_record_id, post_download_action =
record_metadata;compute_checksum;store_raw_ignored;create_processing_script, and
a note stating no download has occurred.

## E. Why these rows were needed

The population-baseline acquisition approval package
(metadata/population_baseline_acquisition_approval_package.csv, items
PBA_004/005/006) recorded that the decision log lacked rows for:

- Chinese share of foreign residents (PBA_004) -> now DDL_009.
- Foreign-resident share of total population (PBA_005) -> now DDL_011.
- Density / area denominator (PBA_006) -> now DDL_012 (prerequisite) and DDL_013
  (the density measure).
- The e-Stat total-population denominator (R02_OFF_TGT_001), required by the
  foreign-resident share -> now DDL_010.

This update adds those rows explicitly so every planned population-baseline
construct has a governed, pending decision-log entry before any acquisition.

## F. Dependency logic

- Chinese share (DDL_009) depends on DDL_001 and DDL_002.
- Foreign resident share (DDL_011) depends on DDL_002 and the new e-Stat
  total-population denominator (DDL_010).
- Chinese density (DDL_013) depends on DDL_001 and the new area / boundary
  denominator (DDL_012); DDL_012 in turn relates to the existing NLNI boundary
  row DDL_004.
- Derived variables (DDL_009, DDL_011, DDL_013) must NOT be computed until all
  of their source inputs are approved, acquired, and metadata-recorded.

## G. Repository safety rules

- All new rows are pending_user_approval.
- No row is approved.
- download_completed remains no for every row (all 13).
- Raw data should not be committed by default.
- Every future download requires a metadata record and a SHA-256 checksum.
- Exact tables/layers and license must be confirmed before approval.

## H. Recommended next action

- The user manually checks the exact ISA/e-Stat pages for DDL_001/DDL_002 and the
  new e-Stat denominator row (DDL_010).
- The user may then approve only the first two core source rows (DDL_001,
  DDL_002) first; derived and denominator rows follow once their inputs are
  confirmed.
- No bulk download. No final Introduction yet. Status remains: gap under
  verification.
