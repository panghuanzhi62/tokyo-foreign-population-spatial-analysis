# DF_M01 Registered Support Organizations - Municipality-Level Count Build Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-25

## A. Purpose

This note documents the LOCAL-ONLY construction test for DF_M01 municipality-level counts:
turning the official ISA/MOJ registered-support-organization registry into per-municipality
counts on the project 251 Greater Tokyo frame, and verifying linkability. No modeling, no
ISA/MOJ normalization, no approval package. Raw, address-level, and geocoded records are NOT
written or committed; only the parser, this note, the commit-safe QC summary, and reports are
committed. The final municipality-count dataset is local-only and NOT committed.

## B. Source status

- Official source: ISA/MOJ registered support organizations registry (toroku shien kikan
  torokubo), edition as of 2026-06-18; 11,439 organizations nationally.
- Time validity: B_observable_by_2024_or_2025.
- Registration date available: YES (every record carries a Date of Registration).
- Address available: YES (organization address and a separate support-office address).
- No cancellation/deletion date in the current snapshot: confirmed (right-censoring).
- Raw files remain local-only under data_raw_official; not committed.

## C. Count-construction logic

- Parser: scripts/06_service_infrastructure/build_df_m01_registered_support_counts.py
  (openpyxl; no network). Records detected by registration-number pattern (NN-style with the
  toroku marker), so continuation/merged rows and phone-number cells are not miscounted
  (raw record count equals the official 11,439 exactly).
- Date filters (registered-by snapshot filters, NOT active-stock): registered_by_2024_06_30,
  registered_by_2024_12_31, registered_by_2025_06_30, current_snapshot.
- Greater Tokyo filter: address prefecture in Tokyo, Saitama, Chiba, Kanagawa.
- Municipality parse: city/ward/town/village token extracted from the Japanese address;
  suffix search starts after the first character so names beginning with the suffix char
  (Ichikawa, Ichihara) are handled; small/large "ke" (Chigasaki) is normalized.
- Address role: support_office (primary; the service point) with org address as a comparison
  variant via --address-role.
- JIS code linking: parsed municipality matched to the local 251-frame ISA panel
  (isa_moj_chinese_stock_t2_2023_12_2025_06.csv); designated cities (Saitama, Chiba, Yokohama,
  Kawasaki, Sagamihara) are linked at WARD level, matching the frame.
- 251-frame zero filling: every frame municipality is emitted; municipalities with no
  organization receive an explicit zero (true zeros, not missing).

## D. QC results (primary role = support_office)

- National raw count: 11,439 (= unique registration numbers = official edition count).
- Date parse success: 11,439 of 11,439.
- Greater Tokyo records: 3,751.
- Municipality parse success (Greater Tokyo): 3,751 of 3,751.
- Municipality-code link success (Greater Tokyo): 3,749 of 3,751 (99.95 percent); the 2
  unlinked are a stray-character Tokyo address and a Kawasaki address missing its ward.
- Registered by 2024-06-30 (Greater Tokyo): 2,488; national 8040.
- Registered by 2024-12-31 (Greater Tokyo): 2,924; national 9157.
- Registered by 2025-06-30 (Greater Tokyo): 3,139; national 9748.
- Municipalities with positive count: 196 (by 2024-06-30), 200 (by 2024-12-31), 201 (by
  2025-06-30), 207 (current) of 251.
- Org-address role gives a near-identical picture (Greater Tokyo 3,741; link 3,735).
- Can construct municipality counts: YES.

## E. Interpretation

The DF_M01 count is a dated INSTITUTIONAL migrant-support subcomponent (Specified Skilled
Worker support organizations), not the full migrant-oriented service infrastructure variable.
It is cleanly constructible at the 251-municipality level with near-complete linkage.

## F. Limitation

- Not China-specific (serves all Specified Skilled Worker nationalities).
- Current file right-censors cancelled/deleted organizations (no deletion date), so
  registered-by counts are snapshot existence, not true 2024 active stock.
- Institutional/employment-support bias; omits informal Chinese-oriented services.
- Address may represent the organization HQ or the support office; both roles are provided.
- Should be combined with other A-class M sources (Japanese-language institutions, employment
  placement, real-estate brokers) to form a defensible composite M.

## G. Decision

DF_M01_COUNTS_CONSTRUCTED_LOCAL_ONLY.

## H. Next step

Proceed to the second A-class source acquisition/sample (preferably designated Japanese-language
institutions or licensed employment-placement offices), then build a composite M; keep DF_M01
as one dated subcomponent and, in parallel, pursue an archived ~2024 registry snapshot to
upgrade DF_M01 toward A_2024_stock.

## I. Gap status

Gap status: under verification. No novelty asserted; no causal mediation claimed.
