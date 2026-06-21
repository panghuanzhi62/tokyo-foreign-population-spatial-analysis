# Official Data-Usability Inventory - Tokyo-China Opportunity-Risk Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (official data-usability inventory)
Companion table: literature/02_matrices/official_data_usability_inventory.csv

## A. Purpose

This note converts the completed P1 official-source feasibility and license
checks into a structured official data-usability inventory for the Tokyo-China
opportunity-risk project. It clarifies which official sources can support later
variable construction, spatial analysis, policy context, or service-
infrastructure interpretation. It is a planning artifact for empirical
construction, not an analysis and not a literature review.

## B. Evidence boundary

- This is data-usability planning, NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- It does NOT prove final data usability (exact tables, layers, licenses,
  spatial granularity, and temporal coverage still require manual confirmation).
- No datasets or PDFs were downloaded.
- Current status remains: gap under verification.

## C. Inventory summary

- inventory rows: 11
- P1_data_construction sources: 3 (e-Stat, ISA, MLIT NLNI)
- P1_context_construction sources: 2 (GSI, Tokyo disaster prevention)
- P2_context sources: 4 (Tokyo statistics, Tokyo housing policy, Hazard Map
  Portal, CLAIR portal)
- P3_background sources: 1 (CLAIR periodical)
- hold or partially usable sources: 3 (Tokyo statistics - partial; Hazard Map
  Portal - partial; TSUNAGARI - hold)
- sources suitable for population baseline: 3 (e-Stat, ISA, Tokyo statistics)
- sources suitable for spatial variable construction: 2 (MLIT NLNI, GSI)
- sources suitable for housing context: 1 (Tokyo housing policy)
- sources suitable for disaster/risk context: 2 (Tokyo disaster prevention,
  Hazard Map Portal)
- sources suitable for multilingual/service context: 2 (TSUNAGARI, CLAIR portal)

Source-id coverage: all 11 priority source_ids were located in the existing
files and are included (R02_OFF_TGT_001, 002, 004, 005, 006, 007, 010, 011, 013,
016 and R02_NDL_OFF_002). No requested source_id was missing; no source was
invented.

## D. Data construction feasibility by module

| module | candidate official sources | current usability | manual checks required | risk_or_limitation |
| --- | --- | --- | --- | --- |
| 1. Chinese vs non-Chinese foreign resident population baseline | e-Stat (R02_OFF_TGT_001), ISA (R02_OFF_TGT_002); Tokyo statistics (R02_OFF_TGT_004) cross-check | usable after manual download/API (e-Stat, ISA); partial (Tokyo stats) | exact tables, municipality granularity for Chinese, vintage, API key | municipality-level Chinese counts across all years not confirmed |
| 2. Administrative and spatial boundary construction | MLIT NLNI (R02_OFF_TGT_005), GSI (R02_OFF_TGT_006) | usable after manual download/API | per-layer terms/vintage, CRS/join keys, GSI registration | per-layer terms vary; CRS/join keys to verify |
| 3. Transit/accessibility variables | MLIT NLNI (R02_OFF_TGT_005, railways/stations/facilities); GSI (R02_OFF_TGT_006) basemap/geocoding | usable after manual download/API | select rail/station/facility layers; accessibility method; CRS | per-layer vintage and terms; method choice pending |
| 4. Housing/public housing context | Tokyo housing policy (R02_OFF_TGT_007); MLIT NLNI land use (R02_OFF_TGT_005) as proxy | usable for context only (housing); usable for data (land-use proxy) | whether public-housing locations exist as a dataset | mostly interpretive context, not direct gap evidence |
| 5. Disaster/risk exposure | Hazard Map Portal (R02_OFF_TGT_011), MLIT NLNI flood zones (R02_OFF_TGT_005); Tokyo disaster prevention (R02_OFF_TGT_010) context | partial (portal); usable for data (NLNI); context (Tokyo bosai) | downloadable hazard layers + license; portal reachability | portal access intermittent in sandbox; exposure data better via NLNI |
| 6. Multilingual administrative and service infrastructure | TSUNAGARI (R02_OFF_TGT_013, hold); CLAIR portal (R02_OFF_TGT_016) | hold (TSUNAGARI); usable for context only (CLAIR) | TSUNAGARI manual browser check; specific CLAIR resources | one source held due to access; context-only |
| 7. Health/welfare/education context | (none among the 11 priority sources; registry holds R02_OFF_TGT_017 MEXT CLARINET, R02_OFF_TGT_018 MHLW) | not inventoried here | future inventory pass if needed | not covered by this priority set |
| 8. Municipal/prefectural policy context | CLAIR portal (R02_OFF_TGT_016), CLAIR periodical (R02_NDL_OFF_002) | usable for context only; background only | identify specific citable resources/issues | policy/background context, not variable construction |

Note on module 7: the requested priority set does not include a
health/welfare/education source, so this module has no candidate inventory row.
The official source registry separately holds MEXT CLARINET (R02_OFF_TGT_017) and
MHLW (R02_OFF_TGT_018) for a future inventory pass; they are not added here to
avoid inventing scope beyond the requested priority sources.

## E. Source-by-source notes

- R02_OFF_TGT_001 e-Stat (ODU_001) - variable-ready. Primary portal for census
  and Basic Resident Register statistics incl. foreign residents by nationality
  and municipality. License confirmed open (Government Standard Terms of Use, CC
  BY 4.0 compatible, attribution required). Remaining manual check: select exact
  Chinese-by-municipality tables and vintage; obtain API key. Do not yet claim a
  specific table is available.

- R02_OFF_TGT_002 ISA foreign-resident statistics (ODU_002) - variable-ready.
  Foreign-resident counts by nationality (incl. China) and area, biannual,
  distributed via e-Stat. Directly supports the Chinese-vs-non-Chinese baseline.
  Remaining manual check: municipality-level Chinese counts and full time series.
  Do not yet claim exact geography/time coverage.

- R02_OFF_TGT_004 Tokyo statistics (ODU_003) - partially usable / context. Tokyo
  ward/municipality population incl. foreign residents; a Tokyo-level cross-check
  and demographic context that overlaps e-Stat. Remaining manual check: identify
  specific variable-ready tables. Treat as secondary to e-Stat/ISA for now.

- R02_OFF_TGT_005 MLIT NLNI (ODU_004) - variable-ready (spatial). Vector layers
  for boundaries, railways/stations, land use, public facilities, and flood-
  inundation zones; core spatial input for accessibility and exposure modules.
  Remaining manual check: select exact layers, per-layer terms/vintage, CRS/join
  keys. Do not yet claim a specific layer or license without per-layer review.

- R02_OFF_TGT_006 GSI (ODU_005) - context/spatial reference. Base maps (GSI
  tiles), Fundamental Geospatial Data, and geocoding/spatial reference. Usable as
  basemap and reference; derived use needs per-product terms and registration.
  Remaining manual check: tiles vs Fundamental Geospatial Data terms and
  registration. Reachable only via legacy-TLS option in the sandbox.

- R02_OFF_TGT_007 Tokyo housing policy (ODU_006) - context only. Tokyo housing
  and public (Toei) housing policy and consultation context for the housing-
  constraint module; supports interpretation, not direct gap evidence. Remaining
  manual check: whether any housing dataset (e.g. public-housing locations)
  exists. Do not yet claim a housing dataset is available.

- R02_OFF_TGT_010 Tokyo disaster prevention (ODU_007) - context. Disaster-
  prevention policy, evacuation guidance, and multilingual disaster information;
  context rather than a primary downloadable dataset. Remaining manual check:
  distinguish data vs guidance and multilingual scope. Quantitative exposure
  should come from NLNI / the Hazard Map Portal.

- R02_OFF_TGT_011 Hazard Map Portal (ODU_008) - partially usable. Flood,
  sediment, storm-surge, and tsunami hazard overlays; useful for the disaster-
  exposure layer, but underlying data is more directly obtained via NLNI. Access
  was intermittent in the sandbox (HTTP 200 on 2026-06-21; a prior run timed out
  on TLS). Remaining manual check: reachability outside the sandbox, downloadable
  vs view-only layers, and license.

- R02_OFF_TGT_013 TSUNAGARI (ODU_009) - hold. Tokyo Metropolitan quasi-official
  foundation providing multilingual living information and foreign-resident
  support; core multilingual service-infrastructure context. The live page was
  not reachable in the sandbox (SSL UNEXPECTED_EOF under strict and legacy TLS).
  Identity and relevance are sound, but content is unconfirmed. Remaining manual
  check: open in a normal browser and confirm live page, multilingual resources,
  and license. Do not yet claim its content or resource structure.

- R02_OFF_TGT_016 CLAIR portal (ODU_010) - context only. CLAIR's official portal
  of municipal multicultural-coexistence and multilingual resources; service and
  policy context. Remaining manual check: identify specific citable resources.
  Not direct variable construction unless a specific dataset is identified.

- R02_NDL_OFF_002 CLAIR periodical (ODU_011) - background only. CLAIR's Local
  Government and International Relations Forum periodical (NDL metadata only);
  municipal-internationalization background, not Tokyo-China specific and not
  data-ready. Remaining manual check (optional): specific issues. Use only as
  background context.

## F. Official-source caution

- Official sources can support empirical construction and policy/service context.
- Official sources CANNOT establish academic novelty.
- They must NOT be cited as proof that no prior study exists.
- Licensing, exact tables/layers, spatial granularity, and temporal coverage must
  be confirmed before analysis.

## G. Recommended data workflow next steps

Recommended future task: prepare official_data_variable_blueprint.csv that maps:

- concept dimension
- candidate variable
- source_id
- expected geography
- expected time
- download/API route
- preprocessing requirement
- feasibility status

Do not recommend final analysis yet. Do not recommend writing the final
Introduction yet. Status remains: gap under verification.
