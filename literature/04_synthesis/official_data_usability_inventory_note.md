# Official Data-Usability Inventory Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/official_data_usability_inventory.csv

## A. Purpose

This note converts the verified P1 official-source feasibility/license checks into
a structured data-usability inventory for the empirical construction of the
Tokyo-China opportunity-risk project. It records which official sources can
support which empirical variables, what exact tables/layers still need to be
inspected or downloaded later, the expected spatial/temporal granularity, and the
remaining licensing/access constraints. No datasets were downloaded in this task.

## B. Evidence boundary

- This is NOT a literature gap confirmation.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No datasets were downloaded; only landing/catalogue pages were referenced.
- Exact tables and exact layers still require later manual inspection before any
  analysis.
- Current gap status: under verification.

## C. Source-to-variable map

Readiness values: ready_table = ready_for_table_level_inspection;
ready_layer = ready_for_layer_level_inspection; context = context_only;
browser = browser_manual_check_needed; hold = access_unclear_hold.

| project dimension | candidate variable or analytical use | supporting source_id | current readiness | remaining checks |
| --- | --- | --- | --- | --- |
| Chinese resident baseline | Chinese resident counts by municipality | R02_OFF_TGT_002 (ISA); R02_OFF_TGT_001 (e-Stat) | ready_table | confirm exact table, reference period, municipality code field |
| Non-Chinese foreign comparison baseline | total/other-nationality foreign counts for comparison | R02_OFF_TGT_002 (ISA); R02_OFF_TGT_001 (e-Stat) | ready_table | confirm comparable nationality breakdown at same spatial unit |
| Municipality-level foreign resident composition | foreign share / composition by municipality | R02_OFF_TGT_001 (e-Stat); R02_OFF_TGT_003 (MIC BRR); R02_OFF_TGT_004 (Tokyo stats) | ready_table | confirm denominators reconcile across sources |
| Administrative boundary / spatial unit support | municipality boundary polygons for joins/mapping | R02_OFF_TGT_005 (NLNI boundaries); R02_OFF_TGT_006 (GSI) | ready_layer | open exact boundary layer; confirm year and code field |
| Station / rail accessibility support | distance/access to stations and rail lines | R02_OFF_TGT_005 (NLNI railways/stations) | ready_layer | open exact railway/station layer; confirm currency and completeness |
| Housing / public housing context | public/affordable housing context | R02_OFF_TGT_007 (Tokyo Housing Policy); R02_OFF_TGT_008 (UR); R02_OFF_TGT_009 (JKK) | context | confirm whether any structured stock/location data exists |
| Disaster / risk exposure context | hazard exposure overlay (flood/sediment/etc.) | R02_OFF_TGT_005 (NLNI hazard family); R02_OFF_TGT_011 (Hazard Map Portal); R02_OFF_TGT_010 (Tokyo disaster, context) | ready_layer / browser | confirm exact hazard layers and clean GIS export/license |
| Multilingual administrative / service context | service-access context for foreign residents | R02_OFF_TGT_013 (TSUNAGARI); R02_OFF_TGT_014 (TICC); R02_OFF_TGT_015 (ISA portal); R02_OFF_TGT_016 (CLAIR) | context / hold | re-verify TSUNAGARI access; identify relevant resource pages |
| Basemap / geocoding / reference support | basemap, geocoding, spatial reference | R02_OFF_TGT_006 (GSI) | ready_layer | confirm specific GSI Maps / basic geospatial products and terms |

## D. Recommended empirical construction sequence

This sequence is conservative and assumes exact tables/layers are confirmed by
manual inspection before any download.

1. Confirm population tables: e-Stat (R02_OFF_TGT_001) and Immigration Services
   Agency (R02_OFF_TGT_002); cross-check with MIC Basic Resident Register
   (R02_OFF_TGT_003) and Tokyo statistics (R02_OFF_TGT_004).
2. Confirm spatial units and boundary files: NLNI administrative boundaries
   (R02_OFF_TGT_005) and GSI (R02_OFF_TGT_006).
3. Confirm accessibility layers: railway/station candidate layers from NLNI
   (R02_OFF_TGT_005) or another official spatial source.
4. Confirm hazard/risk exposure layers: NLNI hazard-related candidate layers
   (R02_OFF_TGT_005) and the Hazard Map Portal (R02_OFF_TGT_011), with the Tokyo
   disaster prevention site (R02_OFF_TGT_010) as context.
5. Confirm service/context sources: TSUNAGARI (R02_OFF_TGT_013) and other Tokyo
   multilingual service pages (TICC, ISA portal, CLAIR).
6. Only after exact table/layer confirmation, start download and preprocessing
   scripts.

## E. Risk register

| risk | affected source | impact | mitigation |
| --- | --- | --- | --- |
| Nationality vs ethnicity/origin mismatch | R02_OFF_TGT_001, R02_OFF_TGT_002 | "Chinese" is by registered nationality, not ethnicity/origin; may under/over-count | State the operational definition explicitly; treat as nationality-based; avoid ethnicity claims |
| Chinese vs all-foreigners comparison problem | R02_OFF_TGT_001, R02_OFF_TGT_002 | Comparing Chinese to "all foreigners" double-counts Chinese in the comparator | Construct non-Chinese foreign comparator explicitly (all minus Chinese) at the same unit |
| Municipal vs smaller spatial unit availability | R02_OFF_TGT_001, R02_OFF_TGT_002, R02_OFF_TGT_003 | Nationality detail may exist only at municipality, not sub-municipal | Confirm finest available unit; design analysis at the confirmed unit |
| License/terms uncertainty | e-Stat, NLNI, GSI, Hazard Map Portal | Reuse/redistribution terms unconfirmed before download | Inspect terms per product before download; record license in metadata |
| TLS/access instability | R02_OFF_TGT_013 (TSUNAGARI), R02_OFF_TGT_011 (Hazard Map Portal) | Pages unreachable or unstable in sandbox; may block automated access | Re-verify outside sandbox via manual browser check before relying on them |
| Official service pages context-only | R02_OFF_TGT_007/008/009/010/012/014/015/016 | May provide narrative/policy text, not analyzable spatial data | Keep as context; do not treat as datasets without confirmation |
| Hazard interfaces may lack clean GIS layers | R02_OFF_TGT_011 (Hazard Map Portal) | Viewer-only access could prevent clean downloadable GIS exposure layers | Manual browser check; fall back to NLNI hazard-related layers (ODU_009) |

## F. Safe interpretation

- These official sources support data feasibility and empirical operationalization
  of the project variables.
- They must NOT be cited as evidence that no prior academic study exists.
- Academic novelty and the research gap must still come from audited literature
  records and, later, full-text verification.
- Status remains: gap under verification.

## G. Next step

Recommended next task: "official table/layer-level inspection plan".

This next step should identify the exact e-Stat / Immigration Services Agency
tables and the exact NLNI / GSI / Hazard Map Portal layers, but should still avoid
downloading large datasets unless explicitly instructed.
