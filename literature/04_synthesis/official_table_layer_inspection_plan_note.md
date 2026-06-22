# Official Table/Layer-Level Inspection Plan Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/official_table_layer_inspection_plan.csv

## A. Purpose

This note translates the completed official data-usability inventory
(literature/02_matrices/official_data_usability_inventory.csv) into a concrete
pre-download table/layer inspection plan. It identifies the exact official tables,
candidate GIS layer families, catalogue pages, API endpoints, terms pages, and
manual checks that must be confirmed before any dataset is downloaded or any
preprocessing is run. It does not download data and does not begin analysis.

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No datasets were downloaded.
- No preprocessing or modeling was run.
- The plan only identifies what must be checked before empirical data acquisition.
- Current gap status: under verification.

The official sources establish data feasibility only. They are not evidence that
no prior academic study exists. Academic novelty and the research gap must still
come from audited literature records and later full-text verification.

## C. Inspection priorities

Priority values: P1_blocking_before_download; P2_needed_before_modeling;
P3_context_only.

| priority | inspection target | reason | blocking issue | next action |
| --- | --- | --- | --- | --- |
| P1 | e-Stat foreign-resident table (ITL_001) and ISA Zairyu Gaikokujin Tokei table (ITL_003) | population baseline and Chinese vs non-Chinese comparator depend on these exact tables | nationality is registration-based not ethnicity; municipality-level nationality detail may be limited | inspect_exact_table |
| P1 | NLNI administrative boundary candidate layer (ITL_006) | all spatial joins/mapping require a consistent municipality geometry | exact layer/year not opened; code field and CRS must match the population join key | inspect_exact_layer |
| P1 | e-Stat / ISA terms (ITL_020, ITL_021) | reuse/redistribution must be cleared before any download | per-table applicability of the Government Standard Terms of Use unconfirmed | inspect_license_before_download |
| P1 | Hazard Map Portal layers and terms (ITL_014, ITL_024) | high-value hazard exposure but clean GIS export uncertain | viewer-only access could block clean downloadable GIS layers; export/license unclear | manual_browser_check / inspect_license_before_download |
| P1 | NLNI terms (ITL_022) | per-layer terms cover boundaries, rail/station, land use, facilities, hazard | per-layer conditions vary and are unconfirmed | inspect_license_before_download |
| P2 | NLNI railway/station candidate layer (ITL_008) | station/accessibility measures depend on this layer family | exact layer, currency, and completeness not yet verified | inspect_exact_layer |
| P2 | NLNI hazard/disaster candidate layer (ITL_013) | fallback hazard exposure overlay if portal export is blocked | hazard types present in the catalogue must be confirmed | inspect_exact_layer |
| P2 | GSI basemap/reference and terms (ITL_007, ITL_023) | basemap, geocoding, CRS reference | Fundamental Geospatial Data may require registration | inspect_exact_layer / inspect_license_before_download |
| P2 | e-Stat WebAPI parameters (ITL_002) | programmatic pull of the confirmed population table | statsDataId and area/category codes must match ITL_001 | inspect_API_parameters |
| P3 | Housing/land-use context (ITL_009, ITL_010, ITL_011, ITL_012) | context for the housing/built-environment module | likely policy text or context, not structured spatial data | inspect_exact_layer / keep_as_context_only |
| P3 | Multilingual/service context pages (ITL_015, ITL_016, ITL_017, ITL_018, ITL_019) | service-access context for foreign residents | likely context-only; TSUNAGARI unreachable in sandbox | manual_browser_check / keep_as_context_only |
| P3 | Service-page terms (ITL_025) | web-content terms before any reuse | TSUNAGARI/service-page terms need manual confirmation | inspect_license_before_download |

## D. Proposed sequence before data download

Conservative order. Each step is completed before the next, and no large dataset
is downloaded until all table/layer checks are finished.

1. Confirm e-Stat / ISA population tables and exact fields (ITL_001, ITL_002,
   ITL_003), with MIC Basic Resident Register (ITL_004) and Tokyo statistics
   (ITL_005) as denominator cross-checks.
2. Confirm the spatial boundary layer and CRS (ITL_006) and GSI reference/basemap
   (ITL_007).
3. Confirm railway/station layer feasibility (ITL_008).
4. Confirm hazard/risk layer availability and download terms (ITL_013, ITL_014),
   with Tokyo disaster prevention (ITL_015) as context.
5. Confirm service/context sources and whether they contain analyzable locations
   (ITL_009, ITL_010, ITL_011, ITL_012, ITL_016, ITL_017, ITL_018, ITL_019).
6. Only after all table/layer checks are complete, create separate
   download/preprocessing tasks.

License/terms checks (ITL_020 through ITL_025) run alongside the matching data
step and must clear before any download of the corresponding source.

## E. Blocking issues

- Nationality vs ethnicity/origin mismatch: official counts are by registered
  nationality, not ethnicity or origin; the operational definition must be stated
  explicitly and ethnicity claims avoided.
- Chinese vs all-foreigners comparison problem: comparing Chinese residents to all
  foreign residents double-counts Chinese in the comparator.
- Non-Chinese foreign residents must be constructed as all foreign residents minus
  Chinese residents at the same spatial unit and reference period.
- Municipality versus smaller-area spatial availability: nationality detail may
  exist only at municipality level, not sub-municipal; the analysis unit must be
  set to the finest confirmed unit.
- Licensing uncertainty before download: reuse/redistribution terms for e-Stat,
  ISA-via-e-Stat, NLNI, GSI, and the Hazard Map Portal are unconfirmed per
  table/layer and must be cleared first.
- Hazard web-map interfaces may not provide clean GIS layers: the Hazard Map
  Portal may be viewer-only; NLNI hazard layers (ITL_013) are the fallback.
- TSUNAGARI and the Hazard Map Portal may require manual browser confirmation:
  TSUNAGARI was TLS-unreachable in the sandbox and the portal export format is
  unclear.
- Service pages may be context-only rather than analyzable POI data: Tokyo housing
  policy, UR, Tokyo disaster prevention, TICC, CLAIR, and the ISA support portal
  are treated as context unless analyzable location data is identified.

## F. Output of this stage

The only outputs of this stage are:

- literature/02_matrices/official_table_layer_inspection_plan.csv
- literature/04_synthesis/official_table_layer_inspection_plan_note.md
- updated Claude reports (outputs/claude_reports/latest_verification_summary.txt,
  latest_changed_files.txt, latest_safety_check.txt)

No datasets, GIS files, PDFs, or DOCX files were downloaded or staged.

## G. Next step

Recommended next task: "official exact-table and exact-layer confirmation batch 1".

This next task should inspect the exact e-Stat / ISA table IDs and the exact NLNI
layer names (and the GSI / Hazard Map Portal layers), recording confirmed table
IDs, layer IDs, fields, CRS, and per-table/per-layer license terms. It should still
avoid downloading large datasets unless explicitly instructed. It must not write
the Introduction, must not assert novelty, and the gap status must remain: under
verification.
