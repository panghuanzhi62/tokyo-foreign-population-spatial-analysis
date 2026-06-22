# Official Exact-Table and Exact-Layer Confirmation - Batch 1 Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/official_exact_table_layer_confirmation_batch1.csv

## A. Purpose

This note records batch 1 of exact-table and exact-layer confirmation for the
Tokyo-China project, before any data download. It pins down exact official table
IDs, exact catalogue/layer names and identifiers, access routes, key fields,
geography, time period, CRS/geometry where visible, and license/terms status for
the highest-priority population and spatial layers identified in the official
table/layer-level inspection plan.

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No datasets were downloaded.
- No full data extraction, preprocessing, or modeling was run.
- Confirmation is limited to official catalogue pages, official metadata, e-Stat
  survey metadata, NLNI datalist pages, and terms pages. Only small metadata
  queries were used to identify IDs, names, fields, and terms.
- Current gap status: under verification.

Official identifiers are reproduced exactly (e.g. e-Stat toukei 00250012; NLNI
layer codes N03/N02/A31/A33/A40). Japanese table/layer names are given in
romanized (Hepburn) transliteration for ASCII-safe portability rather than in
kanji; the exact code identifiers, not the romaji, are the authoritative keys.

## C. Confirmation summary table

| domain | source_id | exact table/layer confirmed? | ID confirmed? | geography confirmed? | time/update confirmed? | download required later? | remaining blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| resident_foreigner_statistics (e-Stat) | R02_OFF_TGT_001 | yes (survey: Zairyu Gaikokujin Tokei) | partial (toukei 00250012; statsDataId pending) | yes (national; prefecture; municipality per table) | yes (1959-2025; biannual) | yes | exact municipality-level statsDataId and vintage |
| resident_foreigner_statistics (e-Stat WebAPI) | R02_OFF_TGT_001 | route confirmed | pending (statsDataId via getStatsList) | yes | yes | metadata now / extraction later | app id; statsDataId + category codes |
| resident_foreigner_statistics (ISA) | R02_OFF_TGT_002 | yes (same survey) | partial (00250012; local table 24-12-t2; China=01_023 observed) | yes (prefecture; municipality per year) | yes (Jun/Dec) | yes | municipality-level Chinese counts vary by year |
| administrative_boundary_layer | R02_OFF_TGT_005 | yes (N03 Gyosei Kuiki) | yes (N03 v3.1) | yes (national incl. 4 prefectures) | yes (2023-01-01) | yes | code-to-population join key; vintage match |
| rail_station_accessibility_layer | R02_OFF_TGT_005 | yes (N02 Tetsudo, lines+stations) | yes (N02 FY2024) | yes (national incl. Tokyo region) | yes (2024-12-31) | yes | station geometry representation (point vs line) |
| disaster_or_hazard_layer (flood) | R02_OFF_TGT_005 | yes (A31 Kozui Shinsui Sotei Kuiki) | yes (A31 v4.0) | yes (national incl. Tokyo region) | yes (FY2022) | yes | depth-class attribute schema |
| disaster_or_hazard_layer (sediment/tsunami) | R02_OFF_TGT_005 | partial (A33 sediment; A40 tsunami names confirmed) | yes (A33, A40 catalogue ids) | yes | per-layer (pending) | yes | per-layer format/CRS/vintage not yet opened |
| basemap_or_reference_layer (GSI) | R02_OFF_TGT_006 | partial (tiles + Kiban Chizu Joho) | n/a (multiple products) | yes | continuous | maybe | GSI TLS in sandbox; Kiban Chizu Joho registration |
| web_map_export_check (Hazard Portal) | R02_OFF_TGT_011 | viewer confirmed | n/a (no layer ids exposed) | yes (by municipality) | terms updated 2024-12-09 | no (use NLNI) | no clean GIS export visible; manual browser check |
| terms_or_license_check (e-Stat/ISA) | R02_OFF_TGT_001 | yes (Seifu Hyojun Riyo Kiyaku) | n/a | n/a | current | no | per-dataset applicability at selection |
| terms_or_license_check (NLNI) | R02_OFF_TGT_005 | yes (Riyo Yakkan) | n/a | n/a | current | no | current terms URL (old link 404); per-layer terms |
| terms_or_license_check (GSI) | R02_OFF_TGT_006 | yes (Riyo Kiyaku) | n/a | n/a | current | no | tile vs Kiban Chizu Joho terms; registration |

## D. Population construction assessment

Conservative reading of the confirmed e-Stat / ISA metadata:

- Chinese resident baseline: FEASIBLE. The survey Zairyu Gaikokujin Tokei
  (government statistics code 00250012) records foreign residents by nationality,
  and China (Chugoku) is a discrete nationality category (nationality code
  01_023 observed locally in the ISA table family 24-12-t2).
- All foreign residents (total): FEASIBLE. A total (sosu) figure for all foreign
  residents is available in the same survey at the same area unit.
- Non-Chinese foreign residents: FEASIBLE as a construct. It can be built as
  non_Chinese_foreign = total_foreign(sosu) - Chinese(Chugoku) at the same area
  and reference period. This avoids the error of contrasting Chinese residents
  with all foreigners (which would double-count Chinese in the comparator).
- What remains uncertain before download: the exact municipality-level table
  (statsDataId) and vintage; whether municipality (shikuchoson) granularity for
  Chinese counts is available consistently across the chosen years for Tokyo,
  Saitama, Chiba, and Kanagawa (the e-Stat survey metadata foregrounds prefecture
  units; municipality detail is in specific tables and must be confirmed per
  table/year); and the WebAPI category codes for China and total.

Overall: population construction is PARTIAL-to-feasible (survey, categories, and
license confirmed; exact municipality table/statsDataId and vintage still pending);
the non-Chinese foreign construct is feasible in principle at the confirmed unit.

## E. Spatial layer assessment

- Administrative boundary layer: CONFIRMED. NLNI N03 (Gyosei Kuiki), Shapefile and
  GML (JPGIS2014), polygon, JGD2011 geographic (B,L), attributes include
  prefecture/municipality names and the administrative area code; vintage
  2023-01-01 (v3.1); national coverage including the four target prefectures.
- Railway/station layer: CONFIRMED. NLNI N02 (Tetsudo) contains railway lines and
  stations (eki), Shapefile/GeoJSON/GML, JGD2011; fields include line name,
  operating company, and station name; vintage FY2024 (2024-12-31).
  Distance-to-station / transit accessibility is plausibly constructible; confirm
  station geometry representation before computation.
- Disaster/hazard layers: A31 (Kozui Shinsui Sotei Kuiki, flood) fully confirmed
  (Shapefile/GeoJSON/GML, polygon, JGD2011, FY2022 v4.0). A33 (Dosha Saigai
  Keikai Kuiki, sediment) and A40 (Tsunami Shinsui Sotei, tsunami) confirmed by
  identifier and name from the NLNI catalogue; per-layer format/CRS/vintage to be
  opened next.
- GSI reference role: REFERENCE/BASEMAP. GSI tiles (Chiriin tiles) and Kiban Chizu
  Joho (Fundamental Geospatial Data) provide basemap, geocoding, and an alternative
  boundary/building reference; terms verified in round01; GSI pages were
  TLS-restricted in this sandbox this run.
- Hazard Map Portal export uncertainty: the portal is primarily a web-map viewer
  (Kasaneru Hazard Map / Wagamachi Hazard Map) with no clean GIS export visible on
  the landing page; its terms page exists (updated 2024-12-09) and a data-source
  attribution page is referenced. Downloadable hazard exposure should come from the
  NLNI layers (A31/A33/A40), not from the portal.

## F. Blocking issues

- Exact e-Stat per-table statsDataId not yet confirmed (survey-level code 00250012
  confirmed).
- Exact ISA municipality-level table and the China/total category codes not yet
  fixed for the chosen years.
- Geographic-unit uncertainty: municipality-level nationality detail availability
  across all target prefectures/years must be confirmed.
- Time-period alignment: population reference year(s) must be matched to the
  boundary-layer vintage and to the hazard-layer vintages.
- CRS/geometry: NLNI layers are JGD2011 geographic; A33/A40 per-layer
  geometry/CRS/attributes not yet individually opened; station geometry
  representation to verify.
- License/terms: e-Stat/ISA (Government Standard Terms of Use) and NLNI (Riyo
  Yakkan) confirmed at the source level, but per-dataset/per-layer applicability
  and the current NLNI terms URL still need confirmation; GSI terms confirmed but
  Kiban Chizu Joho registration applies.
- Hazard portal export uncertainty: viewer-only; manual browser check required;
  NLNI is the download path.
- Analytical caution: do NOT use Chinese-residents-vs-all-foreigners as the main
  contrast; the comparator must be non-Chinese foreign residents (all minus
  Chinese) at the same unit and period.

## G. Recommended next step

Recommended next task: "official download/preprocessing task design batch 1".

Rationale: the highest-priority population source (Zairyu Gaikokujin Tokei /
e-Stat, code 00250012) and the key spatial layers (NLNI N03 boundaries, N02
railway/stations, A31 flood, with A33/A40 catalogue-confirmed) are confirmed at the
exact-name/exact-layer level with formats, CRS, vintages, and source-level licenses
established, and the population construction logic (including the non-Chinese
comparator) is feasible. The remaining items are bounded selection/verification
steps (exact e-Stat statsDataId and vintage; A33/A40 per-layer detail; per-layer
license confirmation; Hazard Portal export decided in favour of NLNI) that are
better resolved while designing a conservative, no-bulk-download task plan rather
than in a separate confirmation batch 2.

If, when designing that task, the exact e-Stat statsDataId or municipality-level
granularity cannot be pinned down, fall back to "official exact-table and
exact-layer confirmation batch 2" focused on e-Stat statsDataId/municipality
granularity and the A33/A40 hazard-layer detail. Either way: no large dataset
download, no Introduction, no novelty claim; gap status remains under verification.
