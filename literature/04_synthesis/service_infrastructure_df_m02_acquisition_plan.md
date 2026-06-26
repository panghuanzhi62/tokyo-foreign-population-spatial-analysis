# DF_M02 Japanese-Language Education Institutions - Acquisition Plan

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-25
Status: planning only. No modeling. No final M dataset committed.

## 1. Local-only raw folder

data_raw_official/service_infrastructure/DF_M02_japanese_language_education_institutions/
- moj_kokuji_japanese_language_institutions_2026-05-12.pdf  (acquired, local-only, NOT committed)
- (to acquire) MEXT nintei certified-institution round PDFs and cumulative list, local-only.

## 2. Retrieval steps

- kokuji list: https://www.moj.go.jp/isa/applications/resources/nyuukokukanri07_00217.html
  download the "kokuji sareta nihongo kyoiku kikan to" PDF via the moj.go.jp/isa/content host
  (the isa.go.jp host returned an HTML page; use moj.go.jp). Record URL, as-of date, SHA256.
- nintei list: https://www.mext.go.jp/a_menu/nihongo_kyoiku/1420729_00022.htm and the portal
  nihongokyouiku.mext.go.jp; download each certification-round result PDF and any cumulative
  list; record round dates.

## 3. Parser requirements

- The kokuji PDF is vertical-text; use a PDF table extractor (pdfplumber/camelot) with layout
  awareness, not naive text extraction. Expect columns name (meisho) and location (shozaichi =
  prefecture only).
- Because municipality is absent, a GEOCODING step is mandatory: resolve each institution by
  name + prefecture (and branch-campus markers in the name) to a municipality, then to a JIS
  code on the 251 frame. Consider matching against a public school directory or gBizINFO for
  full addresses.

## 4. Expected fields (parsed output, local-only)

institution_name, prefecture, (geocoded) municipality_name, (derived) municipality_code,
source_list (kokuji|nintei), certification_round (nintei only), certification_date (nintei only).

## 5. 2024 stock filter logic

- kokuji: existence by snapshot only (no per-record date) -> observable-by-2026 with most
  institutions plausibly pre-2024; cannot filter precisely by 2024.
- nintei: certified_in_FY2024_rounds -> a date-anchored observable-by-2024/2025 subset.
- Report both; do not claim a precise 2024 active stock from the kokuji list.

## 6. Municipality-linking approach

- Geocode institution name+prefecture to municipality; crosswalk municipality name to JIS code
  on the 251 frame (same crosswalk used for DF_M01). Zero-fill the frame.
- Flag low-confidence geocodes for manual review; report geocoding success rate as a QC gate.

## 7. QC gates

- institution count vs the official list size (per list edition).
- geocoding success rate (target high; report residual).
- every linked Greater Tokyo institution maps to exactly one 251-frame municipality.
- municipality counts sum to the Greater Tokyo institution total; zeros explicit.

## 8. Files that must remain uncommitted

- all raw PDFs (kokuji and nintei).
- any institution-level or address-level parsed/geocoded records.
- the final municipality-count M dataset (local-only).

## 9. Compact outputs allowed for commit

- this acquisition plan and the feasibility note.
- the source profile CSV and sample QC summary CSV (aggregate metadata only).
- provenance/metadata rows (URL, as-of date, checksum, counts) if added later.
- the three fixed reports.
