# DF_M04 Real-Estate Broker Registry (takken) - Acquisition Plan (Conditional)

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Status: CONDITIONAL - execute only if a reproducible official takken list is confirmed AND a
control/robustness use is decided. DF_M04 is a control/robustness candidate, NOT main M.

## 0. Trigger condition

Do NOT execute this plan now. The authoritative source (MLIT search system) is search-only with
no confirmed bulk download/API, and the registry is not migrant-oriented. Execute only if:
(a) a reproducible official downloadable list (CSV/Excel, or an official periodic file) for the
    four prefectures is later confirmed; and
(b) the analysis decides a housing-service control/robustness variable is wanted.

## 1. Exact local-only raw folder (never committed)

    data_raw_official/service_infrastructure/DF_M04_real_estate_broker_registry/

This folder lives under data_raw_official/ which is untracked/local-only. Raw broker records,
address-level records, and any geocoded output MUST remain here and MUST NOT be staged.

## 2. Retrieval steps

1. Confirm a reproducible official source: a downloadable list from MLIT or a prefectural
   government open-data portal, or a stable official periodic file. Record provider, URL,
   access date, format, license/terms.
2. If only the MLIT search system is available, do NOT bulk-scrape the congested dynamic site;
   instead seek an official export or published list. Heavy scraping is out of scope.
3. Acquire per prefecture: Tokyo, Saitama, Chiba, Kanagawa. Save each raw file under the folder
   in step 1 with provider and access date in the filename.

## 3. Parser requirements

- Read raw records; extract: license number (menkyo bango), trade name, head-office address
  (honten shozaichi), license date (menkyo nengappi), license validity end (yuko kikan
  manryobi), active/cancelled status if present, license type (MLIT vs prefecture from number
  prefix).
- Normalize head-office address to municipality; build a name-to-JIS crosswalk join (reuse the
  DF_M01 / 251-frame crosswalk:
  data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv).
- Designated cities resolved at ward level to match the 251 frame.

## 4. Expected fields

menkyo_bango, shogo, honten_shozaichi, prefecture, municipality, municipality_jis,
menkyo_nengappi, yuko_kikan_manryobi, active_status, license_type.

## 5. 2024 active-stock / current-stock filter logic

- Registered-by-2024: keep records with menkyo_nengappi <= 2024-12-31.
- Active-2024 (approximate): registered-by-2024 AND validity end >= 2024 reference date AND not
  cancelled. Flag as APPROXIMATE because the published list right-censors closed operators.
- If only a current list with no dates is acquired, treat as current capacity only
  (C_current_only); do not assert 2024 stock.

## 6. Municipality-linking approach

- First validate municipality-NAME parsing against the 251 frame (do NOT geocode first).
- Geocode only the residual addresses that name-parsing fails to link.
- Output local-only municipality-level COUNTS (one count per 251-frame municipality).

## 7. QC gates

- Link rate to 251 frame reported; investigate if < 99 percent.
- Duplicate license-number check.
- Date-field completeness reported.
- Active vs registered counts both reported with explicit definitions.
- Collinearity check vs existing commercial-density / population controls before any modeling use.

## 8. Files that must remain UNCOMMITTED (local-only)

- All raw broker files under data_raw_official/service_infrastructure/DF_M04_real_estate_broker_registry/
- Any address-level records.
- Any geocoded records.
- Any final or intermediate M dataset.

## 9. Compact outputs allowed for commit (only if explicitly approved later)

- A municipality-level COUNT table (no addresses) if the analysis approves it.
- Updated source-profile / QC-summary CSVs and feasibility note.

No modeling, no novelty claim, no causal-mediation claim. Gap status stays under verification.
