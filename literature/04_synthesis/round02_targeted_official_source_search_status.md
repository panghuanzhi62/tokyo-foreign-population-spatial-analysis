# Round 02 Targeted Official-Source Search Status

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (targeted official-source discovery and registry building)

## A. Purpose

This note summarizes a targeted official-source discovery pass for the
Tokyo-China opportunity-risk mismatch project. It focuses on official and
quasi-official data, policy, and service-infrastructure sources across the
project's domains (population/nationality statistics, housing, disaster/risk,
multilingual administrative services, health/welfare/education, and open/spatial
data) and geographies (Tokyo Metropolis first, then Saitama, Chiba, Kanagawa,
and key metropolitan municipalities). It populates and improves
official_source_registry.csv only; it does not add academic literature to
literature_matrix.csv or gap_verification_matrix.csv.

## B. Evidence status

- This is official-source discovery and source-registry building.
- It is NOT an academic literature review.
- It is NOT a full-text review (no PDFs or datasets were downloaded).
- It does NOT confirm the research gap.
- It does NOT prove novelty.
- Official-source suitability, licensing, and data usability still require manual
  checking. Current status: gap under verification.

## C. Search coverage

Approach: because official Japanese government and quasi-official sites generally
lack a uniform search API, a conservative semi-automated approach was used: a
curated list of KNOWN, stable official/quasi-official landing or catalogue pages
was verified with a single lightweight reachability check (HTTP status only; no
crawling, no PDF/dataset download, no browser automation).

- Official institutions / sources checked: 21
- Candidate official sources identified: 21
- Rows appended to official_source_registry.csv: 21 (R02_OFF_TGT_001 ..
  R02_OFF_TGT_021)
- Rows updated in official_source_registry.csv: 1 (R02_NDL_OFF_002, CLAIR notes
  clarified and cross-referenced to the live CLAIR portal R02_OFF_TGT_016)

Sources by domain group (mutually exclusive grouping):
- population / nationality statistics: 4
- open / spatial data catalogues: 2
- housing: 3
- disaster / risk: 3
- multilingual administrative services: 4
- health / welfare / education: 2
- prefectural / municipal (Saitama, Chiba, Kanagawa): 3

By verification status:
- verified_by_official_catalogue: 5
- verified_by_official_page: 13
- hold_for_manual_check (auto-reachability not confirmed): 3

## D. Important official sources

- R02_OFF_TGT_001 | 総務省統計局 / e-Stat | 政府統計の総合窓口 (e-Stat) | NA |
  population statistics; open data | Japan (incl. Tokyo) |
  use: official_population_data
  Why it matters: primary portal for census and Basic Resident Register
  statistics, including foreign-resident population by nationality and
  municipality; baseline for the Tokyo-region population layer.

- R02_OFF_TGT_002 | 出入国在留管理庁 (ISA) | 在留外国人統計 | NA |
  foreign-resident population by nationality | Japan (by prefecture/municipality) |
  use: official_population_data
  Why it matters: official foreign-resident counts by nationality (incl. Chinese)
  and area; supports the Chinese-resident population baseline for Tokyo and
  surrounding prefectures.

- R02_OFF_TGT_004 | 東京都総務局統計部 | 東京都の統計 / 東京都の人口（推計） | NA |
  Tokyo population statistics | Tokyo Metropolis | use: official_population_data
  Why it matters: Tokyo Metropolitan Government statistics including
  ward/municipality population and foreign-resident figures; core Tokyo
  population layer.

- R02_OFF_TGT_005 | 国土交通省 (MLIT) | 国土数値情報ダウンロードサイト | NA |
  spatial base data | Japan (incl. Tokyo region) | use: official_spatial_data
  Why it matters: national GIS layers (boundaries, railways/stations, land use,
  facilities, hazard) for the accessibility and exposure layers.

- R02_OFF_TGT_011 | MLIT / 国土地理院 | ハザードマップポータルサイト | NA |
  hazard maps; risk exposure | Japan (by municipality) | use: disaster_or_risk_context
  Why it matters: national hazard-map portal for constructing the
  disaster-exposure layer across Tokyo-region municipalities. (Auto-reachability
  not confirmed this run; held for manual check.)

- R02_OFF_TGT_007 | 東京都住宅政策本部 | 東京都住宅政策本部 | NA |
  housing policy; public (Toei) housing | Tokyo Metropolis | use: housing_policy_context
  Why it matters: Tokyo housing policy and public-housing context for the
  housing-constraint module.

- R02_OFF_TGT_013 | 東京都つながり創成財団 (Tsunagari) | 東京都多言語生活情報 | NA |
  multilingual living information | Tokyo Metropolis |
  use: multilingual_administrative_context
  Why it matters: Tokyo Metropolitan quasi-official foundation for multilingual
  foreign-resident support; core multilingual service infrastructure for Tokyo.
  (Auto-reachability not confirmed this run; held for manual check.)

- R02_OFF_TGT_010 | 東京都 | 東京都防災ホームページ | NA |
  disaster prevention; multilingual disaster info | Tokyo Metropolis |
  use: disaster_or_risk_context
  Why it matters: Tokyo disaster-prevention portal incl. evacuation and
  multilingual disaster information; disaster-exposure and risk-communication
  context.

## E. Weak or held sources

Held for manual check (the single automated reachability check did not return a
success status this run; these are well-known official sites and the failures
are most likely network/blocking artifacts, not dead links):

- R02_OFF_TGT_006 | 国土地理院 (GSI Maps) | https://www.gsi.go.jp/ — base maps;
  re-check the landing page manually.
- R02_OFF_TGT_011 | ハザードマップポータルサイト | https://disaportal.gsi.go.jp/ —
  hazard-map portal; re-check manually (high value for the exposure layer).
- R02_OFF_TGT_013 | 東京都つながり創成財団 | https://www.tsunagari-tokyo.jp/ —
  Tokyo multilingual support; re-check manually (high value for the service
  module).

Weak relevance (carried from the prior NDL pass, unchanged here):
- R02_NDL_OFF_001 | 法務省民事局 directive (adoption registration) —
  weak_background_only; off-topic for the opportunity-risk modules.

## F. Methodological relevance

The registered official sources may support later empirical construction:

- Foreign-resident population baseline: e-Stat (R02_OFF_TGT_001), ISA 在留外国人統計
  (R02_OFF_TGT_002), MIC Basic Resident Register (R02_OFF_TGT_003), Tokyo
  statistics (R02_OFF_TGT_004) — Chinese and total foreign-resident counts by
  ward/municipality.
- Spatial layers: MLIT National Land Numerical Information (R02_OFF_TGT_005) and
  GSI (R02_OFF_TGT_006) — boundaries, transit/stations, land use for accessibility.
- Housing context: Tokyo Bureau of Housing Policy (R02_OFF_TGT_007), UR
  (R02_OFF_TGT_008), JKK Tokyo (R02_OFF_TGT_009) — public/affordable housing.
- Disaster/risk exposure: Tokyo disaster portal (R02_OFF_TGT_010), Hazard Map
  Portal (R02_OFF_TGT_011), Cabinet Office (R02_OFF_TGT_012).
- Multilingual administrative-service context: Tsunagari (R02_OFF_TGT_013), TICC
  (R02_OFF_TGT_014), ISA support portal (R02_OFF_TGT_015), CLAIR portal
  (R02_OFF_TGT_016), KIF (R02_OFF_TGT_021).
- Health/welfare/education: MEXT CLARINET (R02_OFF_TGT_017), MHLW
  (R02_OFF_TGT_018).
- Open-data inventory: e-Stat, MLIT NLNI, and the Hazard Map Portal are the main
  catalogue entry points for later (manual) data acquisition.

These are context and potential data-construction sources; none is treated as
academic evidence and none bears on the gap claim.

## G. Limitations

- No PDFs or datasets were downloaded; only landing/catalogue pages were recorded.
- Official pages may change; URLs and resources require manual re-verification.
- Source licensing and data usability require manual checking before any dataset
  is used.
- Some prefectural/municipal entries point to portal roots; the specific
  multicultural/foreign-resident sub-pages must be confirmed manually.
- Three high-value sources were held when the single automated reachability check
  did not succeed; they require a manual re-check.
- This official-source pass does not replace academic literature verification.

## H. Next steps

- Manually verify the highest-value official sources, starting with the held
  items (Hazard Map Portal, GSI, Tsunagari) and the population/spatial-data
  catalogues.
- Decide which official sources support variable construction (population,
  spatial, hazard) versus policy/context interpretation (multilingual, housing,
  welfare/education).
- Then prepare a Round 02 synthesis across all Japanese-source searches (CiNii,
  J-STAGE, NDL, official sources).
- Do not write the Introduction yet.
- Do not assert novelty yet. Status remains: gap under verification.
