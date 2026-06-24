# DF_M01 Registered Support Organizations - Acquisition Plan

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\rsch\laborJapan   Branch: agentic-upgrade   Date: 2026-06-25
Status: planning only. No modeling. No final M dataset committed.

## 1. Exact local-only raw folder

data_raw_official/service_infrastructure/DF_M01_registered_support_organizations/
- registered_support_organizations_JP_2026-06-18.xlsx  (current, local-only, NOT committed)
- registered_support_organizations_EN_2026-06-18.xlsx  (current, local-only, NOT committed)
- (to acquire) archived snapshot near 2024-12 for A_2024_stock upgrade, local-only, NOT committed.

## 2. Retrieval steps

- Source page: https://www.moj.go.jp/isa/applications/ssw/nyuukokukanri07_00205.html
- Download the Japanese registry Excel (authoritative addresses) and English Excel (ASCII
  headers) to the local-only folder above. Record the as-of date and SHA256 in metadata only.
- For the A-class upgrade, obtain a dated archived edition near 2024-12 (agency periodic
  edition or an independently mirrored dated edition) into the same local-only folder.

## 3. Parser requirements

- Header is on the third row; data begins below it. Use the 10-column schema (registration
  number, date of registration, name, address block, representative, support office, support
  detail, date of starting support, languages, note).
- Treat a row as a new organization when the registration-number cell is non-empty (merged
  cells leave continuation rows blank).
- Address block: column index 3 = postal code, 4 = org address (prefecture-prefixed),
  5 = phone; column index 9 = support-office address. Parse prefecture + municipality
  (ku/shi/cho/son) from columns 4 and 9 separately.

## 4. Expected fields (parsed output, local-only)

registration_number, registration_date, name, org_prefecture, org_municipality_name,
org_municipality_code, office_prefecture, office_municipality_name, office_municipality_code,
supported_languages, has_chinese_language_flag, source_as_of_date.

## 5. 2024 active-stock filter logic

- observable_by_2024_12 = registration_date <= 2024-12-31 (primary post-M-window predictor).
- observable_by_2024_06 = registration_date <= 2024-06-30 (alternative ordering).
- true_active_2024_12 = present in the archived ~2024-12 snapshot (A-class upgrade; resolves
  right-censoring from cancellations).
- Report both the current-file observable-by-2024 count and the archived-snapshot active count;
  document the difference as a measurement-sensitivity check.

## 6. Municipality-linking approach

- Normalize address text; extract prefecture + municipality token.
- Crosswalk municipality name to JIS code using the project name-to-JIS-code crosswalk on the
  251 Greater Tokyo frame. Fill non-matching municipalities in the 251 frame with zero.
- Decide HQ (col 4) vs service point (col 9) as the assignment address; default to support
  office for service-point interpretation, with HQ as a robustness variant.

## 7. QC gates

- organization count equals official as-of count for the file edition.
- every Greater Tokyo organization maps to exactly one municipality in the 251 frame.
- registration dates parse for at least 99 percent of records; log the residual.
- municipality counts sum to the Greater Tokyo organization total.
- zero-count municipalities are explicitly present (true zeros, not missing).

## 8. Files that must remain uncommitted

- all raw Excel files (current and archived snapshots).
- any address-level or organization-level parsed records.
- any geocoded records.
- the final municipality-count M dataset (local-only).

## 9. Compact outputs allowed for commit

- this acquisition plan and the feasibility note.
- the source profile CSV and sample QC summary CSV (aggregate metadata only, no address-level
  records).
- provenance/metadata rows (URL, as-of date, checksum, counts) if added later.
- the three fixed reports.
