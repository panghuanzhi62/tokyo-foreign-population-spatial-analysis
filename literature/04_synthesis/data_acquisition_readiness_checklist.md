# Data Acquisition Readiness Checklist - Tokyo-China Opportunity-Risk Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (data acquisition readiness checklist)
Companion table: literature/02_matrices/data_acquisition_readiness_checklist.csv

## A. Purpose

This note translates the official data variable blueprint into a data
acquisition readiness checklist: what must be confirmed for each P1 official
data source before any data download or API extraction (exact table or layer,
year, geography, license, access route, join key, CRS, preprocessing, and
reproducibility metadata).

## B. Evidence boundary

- This is acquisition-readiness planning.
- It is NOT data acquisition.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- Current status remains: gap under verification.

## C. Readiness summary

- readiness checklist rows: 30
- P1_before_download rows: 2
- P1_before_api rows: 4
- P1_before_spatial_analysis rows: 10
- P2_context rows: 7
- P3_background rows: 1
- hold / not-ready rows (priority_level = hold): 6
- rows needing exact table identification: 7
- rows needing exact layer identification: 6
- rows needing license check: 14
- rows needing CRS / spatial check: 11
- rows marked context-only: 6

Source coverage: all requested priority and context source_ids were located in
the existing files and used (R02_OFF_TGT_001, 002, 004, 005, 006, 007, 010, 011,
013, 016 and R02_NDL_OFF_002). No requested source_id was missing; no source was
invented. The housing-related literature IDs (R02_NDL_043, R02_CINII_001,
R02_JSTAGE_002) exist only in synthesis notes and are treated as literature
context support only - not used as data sources here.

## D. Readiness by module

| module | candidate source IDs | main variables or context indicators | current readiness | blocking issue | next check |
| --- | --- | --- | --- | --- | --- |
| 1. Population baseline / Chinese-vs-non-Chinese baseline | R02_OFF_TGT_001, R02_OFF_TGT_002, R02_OFF_TGT_004 | Chinese count; total foreign; non-Chinese (derived); Chinese share; foreign share; total-population denominator; Tokyo cross-check | needs exact table identification | exact table/dataset ID and time series; category consistency | identify e-Stat/ISA tables and confirm WebAPI endpoint |
| 2. Administrative boundaries and spatial reference | R02_OFF_TGT_005, R02_OFF_TGT_006 | admin boundary layer; area denominator; CRS/basemap (GSI) | needs exact layer / CRS check | layer version vs statistics-year codes; CRS; GSI terms | confirm NLNI boundary layer + version; fix projected CRS; GSI terms |
| 3. Transit / accessibility | R02_OFF_TGT_005 | station layer; line layer; nearest-station distance; station density | needs exact layer / CRS check | layer vintage; origin-geometry; CRS alignment | confirm NLNI railway/station layers and CRS |
| 4. Housing / public housing context | R02_OFF_TGT_007, R02_OFF_TGT_005 | public-housing policy/availability/support context; residential land-use proxy | context-only (policy); needs layer ID (land-use) | no official spatial housing dataset confirmed | confirm whether any housing dataset exists; confirm land-use layer |
| 5. Disaster / risk exposure | R02_OFF_TGT_005, R02_OFF_TGT_010, R02_OFF_TGT_011 | flood hazard exposure; sediment risk; portal suitability; disaster-prevention context | needs exact layer / access-route check | scenario/threshold; portal download vs view-only; portal access | confirm NLNI flood/sediment layers and license; re-check portal access |
| 6. Multilingual / service infrastructure | R02_OFF_TGT_013, R02_OFF_TGT_016, R02_NDL_OFF_002 | multilingual service context; foreign-resident support context; internationalization background | hold (TSUNAGARI); context-only (CLAIR) | TSUNAGARI page not reachable in sandbox | manual browser check of TSUNAGARI; select CLAIR resources |
| 7. Opportunity-risk composite | R02_OFF_TGT_005/007/016/011 | housing / accessibility / service / hazard components; mismatch typology (planning only) | not ready | components not finalized; weighting/typology undefined | finalize component variables, normalization, weighting, sensitivity plan |

## E. Before-download checklist

Before ANY data download or API extraction, confirm for each unit:

- exact source page (landing/catalogue URL)
- exact table / layer name (and dataset/layer ID)
- year / version (vintage; reference date)
- geographic unit (municipality / ward / prefecture; mesh if relevant)
- CRS if spatial (e.g. JGD2011 geographic vs a projected CRS for distance/area)
- license / terms (per table or per layer; attribution requirements)
- file / API format (CSV/Excel; Shapefile/GeoJSON/GML; WebAPI JSON/XML)
- administrative code or spatial join key (JIS municipality code; geometry link)
- storage location (ignored data folder or outside-repo working folder)
- source citation (institution, title, URL, retrieval date)
- metadata registry entry (table/layer ID, vintage, license, retrieval date)
- preprocessing script plan (filters, joins, derivations, definitions)
- whether data can be committed or must remain ignored / local (default: ignored)

## F. Repository safety plan

- No raw datasets should be committed to public GitHub unless explicitly
  approved by the user.
- Data downloads should go to an ignored data folder or an outside-repo working
  folder.
- Large files should not be committed.
- Every downloaded file needs source metadata (table/layer ID, vintage, URL,
  retrieval date, license, citation).
- Scripts should expose a project-root variable and avoid hard-coded local paths.
- Credentials are not expected for these official sources (e-Stat WebAPI uses a
  free application ID; GSI Fundamental data may require free registration).

## G. Recommended acquisition order

A cautious order, only after user approval at each step:

1. Confirm exact e-Stat / ISA population tables (Chinese count, total foreign,
   total population).
2. Confirm NLNI administrative boundary and station layers (version + CRS).
3. Confirm NLNI hazard layers and/or Hazard Map Portal suitability.
4. Confirm GSI terms / CRS / basemap role.
5. Confirm housing context source and whether any variable-ready housing data
   exist.
6. Manually check TSUNAGARI and CLAIR service context.
7. Only then design extraction scripts.

## H. What not to do yet

- Do not download data yet.
- Do not build analysis variables yet.
- Do not start modeling.
- Do not write the final Introduction.
- Do not assert novelty.
- Do not treat official-source feasibility as academic gap evidence.

## I. Recommended next repo task

Recommended next task: prepare official_data_source_metadata_template.csv and
data_download_decision_log.csv before any actual data acquisition. The metadata
template standardizes per-file provenance; the decision log records what was
approved, retrieved, and under which terms.

Do not recommend actual download yet. Status remains: gap under verification.
