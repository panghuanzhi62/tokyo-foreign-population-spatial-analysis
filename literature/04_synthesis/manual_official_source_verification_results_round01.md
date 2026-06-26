# Manual Official-Source Verification Results - Batch 1 (P1 official sources)

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (P1 official-source feasibility and license checks, batch 1)
Provisional topic: Chinese Residents and Opportunity-Risk Environments in
Metropolitan Tokyo: A Public-Data Analysis of Housing, Accessibility, Services,
and Disaster Exposure

## A. Purpose

This note records the FIRST batch of P1 official-source feasibility and license
checks for the project: official statistics, spatial data, disaster/risk, and
multilingual service-infrastructure sources that may support variable
construction and policy/service context. Results are recorded in
literature/02_matrices/manual_check_results_template.csv (7 rows appended).

## B. Evidence boundary

- This is official-source feasibility checking, NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- It does NOT prove final data usability (exact tables/layers/licenses still need
  manual confirmation).
- It does NOT involve dataset download.
- Current status: gap under verification.

## C. Access and usability table

| source_id | institution/source | domain | official page/catalogue checked | license/terms status | data/download performed | current usability | remaining manual check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R02_OFF_TGT_001 | Statistics Bureau / e-Stat | population statistics | landing + Terms-of-Use page (HTTP 200) | 政府標準利用規約 / CC BY 4.0 compatible; commercial OK; attribution required | none | usable (variable construction) | exact Chinese-by-municipality tables + vintage; API key |
| R02_OFF_TGT_002 | Immigration Services Agency | foreign-resident statistics by nationality | statistics table page (HTTP 200) | via e-Stat (政府標準利用規約) | none | usable (variable construction) | municipality-level Chinese counts + time series |
| R02_OFF_TGT_005 | MLIT (NLNI) | spatial base data | download-site landing (HTTP 200; 利用約款 referenced) | 国土数値情報 利用約款 (attribution; most layers free) | none | usable (variable construction) | per-layer terms/vintage; CRS/join keys |
| R02_OFF_TGT_006 | GSI | base maps / geocoding / 基盤地図情報 | GSI home page (HTTP 200 via legacy TLS; 利用規約) | 国土地理院 利用規約 (tiles attribution; 基盤地図情報 free with registration) | none | usable (basemap + data) | tiles vs 基盤地図情報 terms; registration |
| R02_OFF_TGT_010 | Tokyo Metropolitan Government | disaster prevention | Tokyo bousai home page (HTTP 200) | TMG site; open-data terms for any dataset to confirm | none | usable (policy/disaster context) | data vs guidance; multilingual scope |
| R02_OFF_TGT_011 | MLIT/GSI | hazard maps | NOT reachable this run (TLS timeout); previously HTTP 200 | underlying data largely via NLNI | none | partially usable (intermittent access) | reachability; downloadable layers + license |
| R02_OFF_TGT_013 | Tokyo Metropolitan Foundation TSUNAGARI | multilingual living information | NOT reachable (SSL UNEXPECTED_EOF) | unconfirmed | none | hold (manual browser check) | live page + stable multilingual-resource pages |

Local page snapshots (OUTSIDE the Git repo, never committed):
E:\rsch\laborJapan_local_fulltext\round02_manual_check\

## D. Findings by official source

- R02_OFF_TGT_001 (e-Stat) - verified_population_data_source. Official, stable;
  landing and Terms-of-Use pages both returned HTTP 200. The Terms-of-Use page
  confirms content is freely usable (including commercially) with attribution
  under the Government Standard Terms of Use (政府標準利用規約), which is CC BY 4.0
  compatible. Supports the POPULATION BASELINE and area-level (municipality/mesh)
  data via download or WebAPI (application ID). Likely usable for variable
  construction. Uncertain: exact tables and vintage to select.

- R02_OFF_TGT_002 (ISA 在留外国人統計) - verified_population_data_source. Official,
  stable (出入国在留管理庁). Foreign-resident statistics by NATIONALITY (incl.
  China) and by prefecture/municipality, biannual, distributed through e-Stat.
  Directly supports the CHINESE-VS-NON-CHINESE foreign-resident baseline.
  Uncertain: municipality-level granularity for Chinese across all years.

- R02_OFF_TGT_005 (MLIT NLNI) - verified_spatial_data_source. Official, stable;
  landing references 利用約款. Provides SPATIAL layers for accessibility/services/
  exposure: administrative boundaries, railways/stations, land use, public
  facilities (medical/welfare/schools), and hazard layers (flood-inundation
  zones, etc.). Likely usable for spatial variable construction. Uncertain:
  per-layer terms, vintages, CRS/join keys. (The guessed terms URL
  /ksj/other/yakkan.html returned 404; use the current terms link on the landing.)

- R02_OFF_TGT_006 (GSI) - verified_spatial_data_source. Official, stable
  (reachable only with the legacy-TLS option); 利用規約 present. Provides basemaps
  (地理院タイル), 基盤地図情報, and geocoding reference. Usable as basemap/geocoding
  and as a fundamental-data source. Uncertain: tile vs 基盤地図情報 terms and
  registration.

- R02_OFF_TGT_010 (Tokyo disaster prevention) - verified_disaster_or_risk_context.
  Official, stable (東京都総合防災部). Mainly POLICY/CONTEXT plus hazard/evacuation
  guidance and multilingual disaster information; not a primary downloadable
  dataset. Supports disaster/risk CONTEXT; quantitative exposure should come from
  NLNI / the Hazard Map Portal. Uncertain: downloadable data vs guidance;
  multilingual scope.

- R02_OFF_TGT_011 (Hazard Map Portal) - partially_verified. Did not respond this
  run (TLS timeout) but was previously verified (HTTP 200). Provides overlay
  hazard maps (flood/sediment/storm-surge/tsunami) and links to municipal maps.
  Useful for the DISASTER/RISK EXPOSURE layer, but for downloads the underlying
  NLNI layers are the more direct source. Uncertain: reachability here;
  downloadable vs view-only; license.

- R02_OFF_TGT_013 (TSUNAGARI) - still_unclear_hold. Not reachable in this
  environment (SSL UNEXPECTED_EOF under strict and legacy TLS). The institution
  (Tokyo Metropolitan Foundation Tsunagari, TMG-affiliated) is known to provide
  multilingual living information and foreign-resident support, but the live page
  and stable sub-pages could not be confirmed here. Requires a manual browser
  check.

## E. Variable construction implications

| dimension | supporting official sources | current feasibility | remaining checks |
| --- | --- | --- | --- |
| Population baseline / Chinese vs non-Chinese foreign residents | R02_OFF_TGT_001 (e-Stat), R02_OFF_TGT_002 (ISA) | high (nationality-by-area data; open license) | exact tables, municipality granularity, vintage, API key |
| Housing / public-housing context | R02_OFF_TGT_005 (land use); registry R02_OFF_TGT_007/008/009 (context) | medium (land use as proxy; policy context) | housing-specific spatial proxies; public-housing locations |
| Transit / accessibility / spatial layers | R02_OFF_TGT_005 (railways/stations/facilities), R02_OFF_TGT_006 (basemap/geocoding) | high (national GIS layers) | per-layer terms, CRS, vintage; accessibility method |
| Disaster / risk exposure | R02_OFF_TGT_011 (hazard portal), R02_OFF_TGT_005 (浸水想定区域), R02_OFF_TGT_010 (context) | medium-high (data via NLNI; portal intermittent) | downloadable hazard layers + license; reachability |
| Multilingual administrative services | R02_OFF_TGT_013 (TSUNAGARI, held); registry R02_OFF_TGT_014/015/016 | low-medium (context; one source held) | reachability + stable pages; content scope |
| Service infrastructure context | R02_OFF_TGT_010, registry CLAIR/TICC/KIF | medium (context only) | which items are citable context vs data |

## F. Official-source caution

- Official sources support FEASIBILITY and empirical construction, plus
  policy/service CONTEXT.
- Official sources do NOT establish an academic literature gap.
- Licensing, exact data tables, geography/granularity, and the API/download
  workflow still need MANUAL confirmation before any analysis.
- No official source should be cited as proof of novelty.

## G. Repository and copyright safety

- No datasets were downloaded.
- No PDFs were staged.
- No screenshots were committed.
- No raw data were committed.
- Only source-check summaries were recorded (in the results template and this
  note). Page snapshots used for verification are stored OUTSIDE the repo.

## H. Next steps

- Prepare an official data-usability inventory table if these sources are to be
  used for empirical construction.
- Inspect exact tables/layers for e-Stat, ISA statistics, NLNI, GSI, and the
  Hazard Map Portal (tables, layers, vintages, license per item).
- Manually open TSUNAGARI in a normal browser (and re-check the Hazard Map Portal)
  if automated access remains unstable.
- Do not write the final manuscript Introduction yet. Do not assert novelty.
  Status remains: gap under verification.
