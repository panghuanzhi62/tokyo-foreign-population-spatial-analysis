# Official Data Variable Blueprint - Tokyo-China Opportunity-Risk Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (official data variable blueprint)
Companion table: literature/02_matrices/official_data_variable_blueprint.csv

## A. Purpose

This note converts the official-source usability evidence (the official data-
usability inventory) into a candidate variable blueprint for the Tokyo-China
opportunity-risk project. It maps each conceptual dimension to candidate
variables, official source IDs, expected geography and time, access route,
preprocessing requirements, and feasibility status.

## B. Evidence boundary

- This is a planning document for variable construction.
- It is NOT data collection.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- Current status remains: gap under verification.

## C. Blueprint summary

- candidate variable rows: 31
- P1_core_variable rows: 7
- P1_core_spatial_layer rows: 5
- P1_core_context rows: 2
- P2 rows (P2_supporting_variable + P2_context): 9
- P3_background rows: 2
- hold or not-ready rows (priority_level = hold): 6

Variables by concept dimension:

- population_baseline: 4
- chinese_vs_non_chinese_baseline: 3
- housing_context: 3
- transit_accessibility: 3
- service_accessibility: 1
- multilingual_administrative_services: 2
- municipal_policy_context: 1
- education_childcare_welfare_health_context: 2
- disaster_risk_exposure: 4
- spatial_reference: 3
- opportunity_risk_composite: 5

Variables by feasibility status:

- high_feasibility: 5
- medium_feasibility: 8
- partial_feasibility_needs_manual_check: 7
- context_only_not_variable_ready: 7
- hold_due_to_access_or_license_uncertainty: 1
- not_ready_for_analysis: 3

Source coverage: all 11 requested priority source_ids were located in the
existing files and used (R02_OFF_TGT_001, 002, 004, 005, 006, 007, 010, 011, 013,
016 and R02_NDL_OFF_002). No requested source_id was missing; no source was
invented. The housing-related literature IDs (R02_NDL_043, R02_CINII_001,
R02_JSTAGE_002) exist only in the synthesis notes and are treated as literature
context support only - they are NOT used as data source_ids in the blueprint.

## D. Variable design by module

| module | candidate variables | main source IDs | current feasibility | manual checks required | risk_or_limitation |
| --- | --- | --- | --- | --- | --- |
| 1. Chinese vs non-Chinese foreign resident baseline | Chinese count; total foreign count; non-Chinese count (derived); Chinese share; foreign share; Chinese density | R02_OFF_TGT_002, R02_OFF_TGT_001 | high (counts/shares); medium (density) | exact tables, municipality granularity, vintage, area denominator | nationality vs origin; small-area instability |
| 2. Housing / public housing context | public/Toei housing policy context; municipal housing-support context; residential land-use proxy layer | R02_OFF_TGT_007, R02_OFF_TGT_005 | context-only (policy); partial (land-use proxy) | whether any public-housing dataset exists; NLNI land-use layer/vintage | proxy not direct supply; mostly interpretive context |
| 3. Transit / accessibility | distance to nearest station; station density; rail line/station layer | R02_OFF_TGT_005 | medium | exact NLNI railway/station layer, vintage, CRS | origin-geometry choice; boundary sensitivity |
| 4. Service accessibility and multilingual administrative infrastructure | distance to nearest public facility; multilingual living-info context (TSUNAGARI); support-infrastructure context (CLAIR) | R02_OFF_TGT_005, R02_OFF_TGT_013, R02_OFF_TGT_016 | partial (facility distance); hold (TSUNAGARI); context-only (CLAIR) | facility-layer existence; TSUNAGARI manual browser check; CLAIR citable items | TSUNAGARI access unstable; service context not quantitative |
| 5. Education / childcare / welfare / health context | foreign-child education support context; welfare/health multilingual support context | R02_OFF_TGT_016, R02_OFF_TGT_013 | context-only | municipal datasets (none in priority set; MEXT/MHLW not requested) | context-only unless specific municipal datasets identified |
| 6. Disaster / risk exposure | flood hazard exposure indicator; hazard zone spatial layer; sediment risk context; disaster-prevention context | R02_OFF_TGT_005, R02_OFF_TGT_011, R02_OFF_TGT_010 | medium (flood via NLNI); partial (portal); context (bousai) | exact hazard layers, scenario, license; portal reachability | portal access intermittent; threshold/scenario choice |
| 7. Spatial reference and GIS support | administrative boundary layer; area denominator; base map / coordinate reference | R02_OFF_TGT_005, R02_OFF_TGT_006 | medium | boundary vintage vs statistics years; projected CRS; GSI registration | code/vintage mismatch; CRS-dependent area |
| 8. Opportunity-risk composite / typology | housing, accessibility, service, disaster components; mismatch typology (planning rows only) | R02_OFF_TGT_005/007/016/011 | partial or not-ready | inputs confirmed first; weighting/typology to define | weighting/typology not defined; not computed |

## E. Core variable candidates

Strongest candidates for later empirical construction:

- Chinese resident count (ODV_001) - R02_OFF_TGT_002; municipality; biannual/
  annual snapshot; preprocessing: select nationality=China, harmonize codes;
  high_feasibility; manual check: yes.
- Total foreign resident count (ODV_002) - R02_OFF_TGT_002; municipality;
  biannual/annual; preprocessing: total row/sum, harmonize codes;
  high_feasibility; manual check: yes.
- Non-Chinese foreign resident count (ODV_003, derived) - R02_OFF_TGT_002;
  municipality; preprocessing: total minus Chinese for matching area-year;
  high_feasibility; manual check: yes (category consistency).
- Chinese share of foreign residents (ODV_004, derived) - R02_OFF_TGT_002;
  municipality; preprocessing: Chinese/total, guard zero denominators;
  high_feasibility; manual check: yes.
- Foreign resident share of total population (ODV_005) - R02_OFF_TGT_001 +
  R02_OFF_TGT_002; municipality; annual/census; preprocessing: join + align
  vintages; high_feasibility; manual check: yes.
- Nearest station / station accessibility proxy (ODV_011) - R02_OFF_TGT_005;
  area centroid/mesh to station points; preprocessing: download station layer,
  compute nearest distance, align CRS; medium_feasibility; manual check: yes.
- Flood hazard exposure proxy (ODV_020) - R02_OFF_TGT_005 (+R02_OFF_TGT_011);
  polygon overlay; preprocessing: overlay flood zones, pick scenario/threshold;
  medium_feasibility; manual check: yes.
- Service / multilingual context indicator (ODV_015/ODV_016) - R02_OFF_TGT_013
  (hold) / R02_OFF_TGT_016 (context-only); metropolitan/municipal; preprocessing:
  manual review; not variable-ready; manual check: yes.
- Public housing / housing policy context indicator (ODV_008) - R02_OFF_TGT_007;
  metropolitan; preprocessing: summarize policy; context-only; manual check: yes.

## F. Variables not yet ready

- Public/Toei housing policy and municipal housing-support context (ODV_008,
  ODV_009) - source is context-only; no official spatial housing dataset
  confirmed.
- Residential land-use proxy (ODV_010), facility-distance (ODV_014), hazard
  layers (ODV_021, ODV_022) - exact NLNI layer/vintage not yet identified.
- Hazard Map Portal items (ODV_022) - downloadable vs view-only unclear; portal
  access was intermittent in the sandbox.
- TSUNAGARI multilingual context (ODV_015) - page access unstable in the
  automated environment; license unconfirmed.
- CLAIR portal / forum and education/welfare/health context (ODV_016, ODV_017,
  ODV_018, ODV_019) - support policy/service context but not quantitative
  variable construction from the priority set.
- Tokyo statistics cross-check (ODV_007) - data geography may overlap/clash with
  national tables; exact table not identified.
- All opportunity-risk composite rows (ODV_027-ODV_031) - planning only; weighting
  and typology not defined.

## G. Data workflow implications

Before any analysis, a later workflow would need to:

1. identify exact tables/layers (e-Stat/ISA tables; NLNI layers; hazard layers);
2. confirm license and terms per item;
3. download outside the repo or into an ignored data folder only after user
   approval;
4. record source metadata (table ID, vintage, URL, retrieval date, license);
5. harmonize geography and year (municipality codes, boundary vintage, CRS);
6. construct Chinese vs non-Chinese foreign-resident measures with consistent
   categories;
7. construct accessibility / service / risk variables (distances, overlays,
   densities);
8. document preprocessing reproducibly (scripts, parameters, definitions).

## H. Caution

- Official-source feasibility does NOT establish an academic gap.
- Variable availability does NOT imply causal interpretation.
- Chinese nationals (by nationality) must be distinguished from Chinese-origin
  residents; the baseline here is nationality-based.
- Non-Chinese foreign residents should be constructed as all foreign residents
  minus Chinese nationals ONLY where official data allow consistent categories
  for the same area and year.
- Opportunity-risk composite construction requires transparent weighting or
  typology logic defined later; the composite rows here are planning placeholders,
  not computed variables.

## I. Recommended next repo task

Recommended next task: prepare a "data acquisition readiness checklist" for the
P1 data sources (e-Stat, ISA, MLIT NLNI, GSI, and the hazard layers) covering
exact table/layer identification, vintage, license confirmation, geography/CRS
harmonization plan, and metadata recording - BEFORE any actual downloads or API
extraction.

Do not recommend actual data download yet. Do not recommend writing the final
Introduction yet. Status remains: gap under verification.
