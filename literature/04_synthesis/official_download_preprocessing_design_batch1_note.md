# Official Download/Preprocessing Task Design - Batch 1 Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/official_download_preprocessing_design_batch1.csv

## A. Purpose

This note designs the first official download and preprocessing workflow for the
confirmed/partially-confirmed batch-1 sources. It specifies access methods, local
storage layout, expected formats/CRS, planned variables, join keys, preprocessing
sequence, and quality checks. It does NOT execute any download or preprocessing.

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No datasets were downloaded.
- No full data extraction was run.
- No preprocessing or modeling was run.
- Current gap status: under verification.

## C. Download readiness summary

| domain | source/layer | current readiness | main blocker | recommended next action |
| --- | --- | --- | --- | --- |
| e-Stat/ISA population tables | toukei 00250012 (Zairyu Gaikokujin Tokei) | exact_id_pending (survey + categories + license confirmed) | exact municipality-level statsDataId and vintage not fixed | confirm_statsDataId_first |
| Administrative boundaries | NLNI N03 (v3.1, 2023) | ready_for_scripted_download_later | confirm code field matches e-Stat codes; current terms URL | design_download_script_later |
| Railway/stations | NLNI N02 (FY2024) | ready_for_scripted_download_later | station geometry representation (point vs line) | design_download_script_later |
| Flood | NLNI A31 (v4.0, FY2022) | ready_for_scripted_download_later | confirm depth-class attribute schema | design_download_script_later |
| Sediment disaster | NLNI A33 | exact_id_pending (catalogue id/name confirmed) | per-layer format/CRS/vintage not yet opened | inspect_layer_metadata_first |
| Tsunami | NLNI A40 | exact_id_pending (catalogue id/name confirmed) | per-layer detail; mostly coastal relevance | inspect_layer_metadata_first |
| Spatial reference | GSI tiles / Kiban Chizu Joho | ready_for_manual_download_later | GSI TLS in sandbox; Kiban registration; may be basemap-only | inspect_layer_metadata_first |
| Hazard Map Portal | Kasaneru/Wagamachi viewers | hold_pending_manual_check (context only) | viewer-only; no clean GIS export visible | keep_context_only |

## D. Proposed local folder structure

All raw and intermediate official data are LOCAL-ONLY and must NOT be committed to
the public repo. A dedicated local-only root is used (gitignored; or stored outside
the repo as with the round01 snapshots under E:\rsch\laborJapan_local_fulltext\).

```
<local_data_root>/                         (local-only, gitignored / outside repo)
  data_raw_official/
    estat_isa_foreign_residents/
    nlni_n03_boundaries/
    nlni_n02_railway_station/
    nlni_a31_flood/
    nlni_a33_sediment/
    nlni_a40_tsunami/
    gsi_reference/
  data_processed_official/
    boundaries/
    population/
    accessibility/
    hazards/
    metadata/
      official_download_log.csv
      official_source_provenance.csv
```

Raw official datasets and large GIS files are stored under <local_data_root> only.
Only small, reproducible derived summaries may be committed later, and only if
explicitly approved as safe.

## E. Proposed metadata fields (future download log)

official_download_log.csv fields:

- download_id
- source_id
- source_name
- official_url
- download_date
- data_version_or_year
- license_terms
- raw_file_name
- raw_file_hash
- local_storage_path
- processing_script
- processed_output
- notes

A companion official_source_provenance.csv records source_id, layer/table id,
license name, attribution wording, terms URL, and check date for every file BEFORE
any download.

## F. Proposed preprocessing sequence

Conservative order; nothing runs until exact ids/terms are confirmed:

1. Confirm and retrieve exact e-Stat/ISA statsDataId and area/category parameters
   (metadata only).
2. Confirm and later download NLNI N03 administrative boundaries.
3. Confirm and later download NLNI N02 railway/station layer.
4. Confirm and later download NLNI A31/A33/A40 hazard layers.
5. Harmonize CRS (NLNI JGD2011 geographic EPSG:6668; reproject to a metric CRS such
   as EPSG:6677 for distance/area ops) and standardize administrative codes.
6. Build Chinese residents, total foreign residents, and non-Chinese foreign
   residents (non_chinese_foreign = total_foreign - chinese_residents) at the same
   unit and period.
7. Build accessibility indicators (distance-to-nearest-station, station density).
8. Build hazard exposure indicators (flood/sediment/tsunami overlays vs
   municipalities).
9. Run quality checks (section G) before any modeling.

## G. Required quality checks

- row count by prefecture/municipality;
- missing municipality codes;
- duplicate municipality codes;
- Chinese residents <= total foreign residents (per municipality);
- non-Chinese foreign residents >= 0;
- geometry validity (boundaries/hazard polygons);
- CRS consistency across layers;
- station point coverage (no missing/dup stations);
- hazard layer overlap with the study area;
- license/provenance record present for every file before use.

## H. Public repo safety rule

- No raw official datasets are committed to the public repo.
- No large GIS downloads are committed.
- No API keys or credentials are committed (e-Stat application id and GSI account
  stay out of the repo).
- Scripts should expose a --project-root parameter later (no hard-coded absolute
  paths in committed code).
- Outputs committed later must be small, reproducible summaries only, and only if
  explicitly approved.

## I. Next step

Recommended next task: "e-Stat/ISA exact statsDataId and API-parameter discovery
batch".

Rationale (conservative): the spatial layers (N03, N02, A31) are confirmed enough
to scaffold download scripts, but the population module - the analytical core - is
still gated on the exact municipality-level statsDataId and vintage for survey
00250012, and the China/total category codes still need to be resolved from e-Stat
getMetaInfo. Resolving statsDataId first prevents scaffolding download scripts
around an unconfirmed table. This is a metadata-only step (no large download).

If, during that step, the statsDataId and municipality granularity are resolved
quickly, proceed directly to "official download script scaffold batch 1" (N03/N02/
A31 first, A33/A40 after their per-layer datalist pages are opened). Either way: no
large dataset download, no full extraction, no preprocessing/modeling, no
Introduction, no novelty claim; gap status remains under verification.
