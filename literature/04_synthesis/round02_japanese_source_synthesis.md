# Round 02 Japanese-Source Synthesis

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (synthesis across CiNii, J-STAGE, NDL, and official-source searches)
Provisional topic: Chinese Residents and Opportunity-Risk Mismatch in
Metropolitan Tokyo: A Public-Data Analysis of Housing, Accessibility, Services,
and Disaster Exposure

## A. Purpose and evidence boundary

This note synthesizes the Round 02 Japanese-source discovery and verification
work across CiNii, J-STAGE, NDL (National Diet Library), and the targeted
official-source search. It consolidates what was found and how far each item was
verified, so the project can plan the next step on a sound footing.

Evidence boundary (read this first):
- This is a synthesis of METADATA DISCOVERY, SOURCE-LEVEL VERIFICATION, and
  selected PRIORITY-CANDIDATE verification only.
- It is NOT a full-text literature review.
- It does NOT confirm the research gap.
- It does NOT prove novelty.
- It does NOT prove that no direct-overlap study exists.
- Current status: gap under verification.

## B. Search and verification coverage

Completed Round 02 rounds (all pushed):
- CiNii metadata-only search + CiNii priority-candidate verification.
- J-STAGE metadata-only search + J-STAGE priority-candidate verification.
- NDL metadata-only search + NDL priority-candidate and official-source verification.
- Targeted official-source search + high-value official-source verification.

Verified counts (from the current matrices/registry in this repo):
- round02_japanese_source_tracking.csv rows: 486
  (by platform: CiNii 102, J-STAGE 278, NDL 106)
- literature_matrix.csv rows: 23
- gap_verification_matrix.csv rows: 13
- official_source_registry.csv rows: 23

Per-platform discovery (from the prior status notes):
- CiNii: 102 candidates retrieved, 102 appended to the tracking CSV.
- J-STAGE: 294 candidates retrieved, 278 appended (16 dropped as duplicates;
  11 overlapped prior CiNii records).
- NDL: 123 candidates retrieved, 106 academic rows appended to the tracking CSV
  and 2 official rows to the registry (15 dropped as CiNii/J-STAGE duplicates).
- Targeted official-source search: 21 official rows appended to the registry
  (R02_OFF_TGT_001..021); plus the 2 earlier NDL_OFF rows = 23 registry rows.

Overlap-category tally across the 486 tracking rows (metadata-level triage; NOT
verified evidence):
- A_direct_overlap_candidate: 0
- B_partial_overlap_candidate: 61
- D_method_support_candidate: 11
- E_background_candidate: 115
- official_policy_context: 12
- hold_for_translation_or_manual_check: 287

Priority records promoted after verification:
- Added to literature_matrix.csv (Round 02 academic records, 10 total):
  R02_CINII_001, R02_CINII_022, R02_CINII_018, R02_CINII_019, R02_JSTAGE_007,
  R02_JSTAGE_011, R02_NDL_043, R02_NDL_087, R02_NDL_088, R02_NDL_068.
- Added to gap_verification_matrix.csv (Round 02 records, 4 total):
  R02_CINII_001, R02_CINII_022, R02_CINII_018, R02_NDL_043.
- Confirmed A_direct_overlap: 0 (none, at any stage).
- gap_verification_matrix overlap coding: all 13 rows are B_partial_overlap
  (one also tagged E_background_only); 0 are A_direct_overlap.

Note: the 61 B_partial_overlap_candidate count is a METADATA-LEVEL triage tally
in the tracking CSV; only a subset has been source-verified and promoted to the
matrices. The number of fully verified B_partial records is the matrix count
(gap_verification_matrix = 13 rows, of which 4 are Round 02 Japanese-source
records). Counts beyond these are "not re-counted in this synthesis".

## C. Core evidence map by module

(Records cited by ID; "tracking-level" = metadata triage only, not yet verified.)

| module | main supporting records | evidence type | geographic relevance | population relevance | strength for current project | limitations | next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Chinese residents/nationals in (Metropolitan) Tokyo | R02_CINII_001 / R02_JSTAGE_002; R02_CINII_022; R02_CINII_018; R02_CINII_019; R02_JSTAGE_007 | peer-reviewed / qualitative / historical | Greater Tokyo / Tokyo metro / Tokyo Prefecture | Chinese residents | moderate-partial (several Tokyo Chinese-resident records, but single-module each) | qualitative or historical; small-N; not integrated | full-text read of R02_CINII_001/R02_JSTAGE_002 and R02_CINII_022 |
| 2. Chinese residential concentration / ethnic community / enclave | R02_CINII_018 (Nishikawaguchi); R02_JSTAGE_007 & R02_CINII_019 (historical); R02_JSTAGE_011 (Osaka comparator) | case study / historical | Tokyo region (Saitama); Osaka (comparator) | Chinese residents/workers | moderate background; Sun 2026 already covers co-ethnic networks | enclave focus, not the risk profile; one comparator is non-Tokyo | position against Sun 2026; verify R02_CINII_018 |
| 3. Housing and residential disparity | R02_NDL_043 (migrant housing disparity, Japan); R02_CINII_001/_022; R01_RB_005, R01_RB_006, R01_RB_013 (Tokyo rental discrimination); R01_RB_007 (Toshima satisfaction) | book + experiments + surveys | Japan-wide + Tokyo (23 wards / wards) | migrants / foreigners / Chinese | relatively strong module | not Chinese-specific (mostly); single-module each; R02_NDL_043 full text not read | read R02_NDL_043; confirm Chinese subgroup in R01_RB_005/_006/_013 |
| 4. Public housing / housing support / policy context | R02_CINII_001 / R02_JSTAGE_002 (public estates); official: R02_OFF_TGT_007, _008 (UR), _009 (JKK) | one qualitative study + official context | Greater Tokyo / Tokyo | Chinese residents (academic); general (official) | thin academic, official context present | only one public-housing academic record | full-text read; inventory UR/JKK/Toei public-housing data |
| 5. Multilingual administrative services / settlement support | official: R02_OFF_TGT_013 (TSUNAGARI, held), _014 (TICC), _015 (ISA portal), _016 (CLAIR portal), _021 (KIF); R02_NDL_OFF_002 (CLAIR periodical) | official / quasi-official service infrastructure | Tokyo + Kanagawa + nationwide | foreign residents | strong as CONTEXT, thin as academic evidence | service context, not analysis; license/structure unchecked | manually inspect TSUNAGARI/TICC/CLAIR resources |
| 6. Education / childcare / welfare / health service access | R02_NDL_087, R02_NDL_088 (foreign-children education); R02_NDL_068 (language support, Okayama); R01_RB_011 (admin services); official: R02_OFF_TGT_017 (MEXT CLARINET), _018 (MHLW) | reports + article + official | Tokyo (Gakugei); Okayama (comparator); Japan | foreign residents / Brazilian (comparator) | background only | non-empirical reports; non-Tokyo / non-Chinese comparators | keep as service-access background |
| 7. Disaster prevention / hazard / risk exposure | R01_RB_004 (Adu-Gyamfi & Shaw 2021, Tokyo foreign-resident disaster vulnerability); R01_RB_008 (1923 Kanto, historical); R01_RB_009/_010 (preparedness); official: R02_OFF_TGT_010 (Tokyo disaster), _011 (Hazard Map Portal), _012 (Cabinet Office) | spatial study + historical + policy + official portals | Tokyo + Japan | foreign residents (not Chinese-specific) | moderate (one strong spatial comparator + official hazard data) | not Chinese-specific; not integrated with housing/services | check Hazard Map Portal license; compare against R01_RB_004 |
| 8. Spatial data / GIS / open data | official: R02_OFF_TGT_005 (MLIT NLNI), _006 (GSI), _001 (e-Stat), _002 (ISA stats), _004 (Tokyo stats), _011 (hazard portal) | official data/spatial catalogues | Japan + Tokyo region | foreign/Chinese population data | strong for FEASIBILITY of public-data construction | licensing/usability not yet checked; not analysis | license/format checks before use |
| 9. Chinese-vs-non-Chinese comparison | (none verified) | -- | -- | -- | WEAK / not yet evidenced | no verified record performs an explicit Chinese-vs-non-Chinese foreign-resident comparison | this is the main differentiation space to develop |
| 10. Full opportunity-risk mismatch combination | (none) | -- | -- | -- | ABSENT at metadata/verification stage | no record integrates housing + accessibility + services + disaster + typology for Chinese residents in Tokyo | continue verification; do not assert a gap |

## D. Priority academic records

1. Directly relevant but partial overlap
- R02_CINII_001 / R02_JSTAGE_002 | Wang & Fujii, "Living conditions and community
  involvement of highly-educated Chinese-nationality residents in two Greater
  Tokyo public-housing estates" | 2021 | CiNii + J-STAGE (DOI 10.24528/lifology.40.0_54)
  | module 1/4 (Chinese in Tokyo public housing) | why: closest single
  Chinese-resident + housing + Greater Tokyo record | limitation: qualitative
  two-estate case, single module, full text not read | next: translate/read.
- R02_CINII_022 | Zhang, "Housing purchase motives and preference of Chinese
  white-collar residents in the Tokyo metropolitan area" | 2020 | CiNii + J-STAGE
  (DOI 10.4157/grj.93.1) | module 1/3 | why: Chinese-specific housing choice in
  metro Tokyo | limitation: qualitative (n=22), owner-occupier subset | next:
  deeper verification/read.

2. Housing / residential disparity support
- R02_NDL_043 | Kim, "Where migrants live: empirical analysis of residential
  disparity in Japan's housing market" | 2026 | NDL (book, Keio Univ Press) |
  module 3 | why: recent empirical housing-disparity book on migrants | limitation:
  Japan-wide, not Chinese/Tokyo-specific, full text not read | next: read.
- R01_RB_005, R01_RB_006, R01_RB_013 | Tokyo rental-discrimination experiments |
  2023/2022/2026 | DOI-verified | module 3 | why: anchor the housing-constraint
  module for Tokyo | limitation: foreigner-vs-native, not Chinese-specific | next:
  confirm whether Chinese applicants are isolated in full text.

3. Chinese community / ethnic concentration background
- R02_CINII_018 | Takamatsu, "Formation factors of Nishikawaguchi Chinatown" |
  2020 | CiNii | module 2 | why: Chinese concentration area in the Tokyo region |
  limitation: single-district case (Saitama), full text not read | next: verify.

4. Historical or comparative background
- R02_CINII_019 (Abe 2000) and R02_JSTAGE_007 (Abe 1999) | historical Chinese
  workers/concentration in Tokyo (Prefecture) | DOI-verified | module 1/2 | why:
  historical depth/comparator | limitation: 1920s-1930s, not contemporary | next:
  background only.
- R02_JSTAGE_011 (Wang 2026, Osaka Chinese newcomers) | non-Tokyo comparator |
  next: comparator only.

5. Service access / education / language support background
- R02_NDL_087, R02_NDL_088 (foreign-children education, Tokyo Gakugei, 2006) |
  NDL | module 6 | why: education service-access background | limitation:
  non-empirical reports | next: background.
- R02_NDL_068 (Nakato 2014, Brazilian language support, Okayama; DOI
  10.19024/jajls.17.1_36) | module 6 | why: language-support comparator |
  limitation: non-Tokyo, non-Chinese | next: background comparator.

6. Held or still uncertain records
- R02_CINII_015 | "Chinese population in Chinese concentration areas in the Tokyo
  region" | CiNii dataset record, no author/year | held: may be a dataset/
  statistical source -> route to registry if confirmed | next: manual check.
- R02_JSTAGE_021 | Liu 2016, "Homes of Chinese newcomers in a less-concentrated
  area" | held: study area unclear from metadata | next: translate to confirm area.

## E. Official-source registry synthesis (23 rows)

By use_in_analysis (representative IDs):
- official_population_data (4): R02_OFF_TGT_001 (e-Stat), _002 (ISA 在留外国人統計),
  _003 (MIC Basic Resident Register), _004 (Tokyo statistics) -> Chinese/foreign
  population baseline by ward/municipality (denominators and the population layer).
- official_spatial_data (2): R02_OFF_TGT_005 (MLIT National Land Numerical
  Information), _006 (GSI; verified_by_official_page) -> boundaries, transit/
  stations, land use for the accessibility layer.
- housing_policy_context (3): R02_OFF_TGT_007 (Tokyo Bureau of Housing Policy),
  _008 (UR), _009 (JKK) -> public/affordable housing context.
- disaster_or_risk_context (3): R02_OFF_TGT_010 (Tokyo disaster portal), _011
  (Hazard Map Portal; verified_by_official_catalogue), _012 (Cabinet Office) ->
  hazard/exposure layer and risk-policy interpretation.
- multilingual_administrative_context (5): R02_OFF_TGT_013 (TSUNAGARI; held),
  _014 (TICC), _015 (ISA support portal), _016 (CLAIR portal), _021 (KIF) ->
  multilingual administrative-service context.
- service_infrastructure_context (1): R02_NDL_OFF_002 (CLAIR periodical).
- health_welfare_education_context (2): R02_OFF_TGT_017 (MEXT CLARINET), _018
  (MHLW) -> education/health service context.
- municipal_context_source (2): R02_OFF_TGT_019 (Saitama), _020 (Chiba) ->
  prefectural/municipal service context.
- weak_background_only (1): R02_NDL_OFF_001 (MOJ adoption directive; off-topic).
- hold_for_manual_check (1): R02_OFF_TGT_013 (TSUNAGARI; live page not reachable
  in the automated environment).

Explicit statements:
- Official sources support VARIABLE CONSTRUCTION, the DATA-SOURCE INVENTORY, and
  POLICY/SERVICE CONTEXT interpretation.
- Official sources do NOT establish an academic research gap.
- GSI (R02_OFF_TGT_006) and the Hazard Map Portal (R02_OFF_TGT_011) are
  reachability-verified but still require LICENSING / DATA-USABILITY checks
  before any data is used.
- TSUNAGARI (R02_OFF_TGT_013) remains hold_for_manual_check: the live page could
  not be confirmed in the automated environment (TLS handshake failure) and needs
  a manual browser check.

## F. Relationship to Sun 2026

Per sun_2026_positioning_note.md, Sun 2026 (Cities) already covers the Tokyo
metropolitan area (242 municipalities, 2012-2018), Chinese / Vietnamese /
Filipino / Brazilian immigrants, co-ethnic networks, spatial assimilation, and
dynamic spatial Durbin modeling. The Round 02 Japanese-source records reinforce
that several adjacent themes are already occupied: Chinese co-ethnic networks,
Chinese immigrant location choice, and spatial assimilation in Tokyo.

Therefore this project should NOT be framed as filling a gap in:
- Chinese co-ethnic networks in Tokyo,
- Chinese immigrant location choice in Tokyo, or
- spatial assimilation of Chinese immigrants in Tokyo.

Instead, the provisional differentiation should be framed more narrowly as an
OPPORTUNITY-RISK ENVIRONMENTAL PROFILE that compares Chinese residents with
non-Chinese foreign residents, using public data on housing, accessibility,
services, and disaster/risk exposure. The Round 02 evidence map shows that the
Chinese-vs-non-Chinese comparison (module 9) and the integrated opportunity-risk
combination (module 10) are the least-occupied directions among the records found
so far - but this is positioning, not a verified gap claim.

## G. Provisional gap status after Round 02

At the metadata and selected source-verification level, Round 02 Japanese-source
searches have not identified a confirmed direct-overlap study that simultaneously
covers Chinese residents or Chinese nationals in Metropolitan Tokyo, a
Chinese-vs-non-Chinese foreign-resident comparison, housing, transit/
accessibility, service infrastructure, disaster/risk exposure, and an explicit
opportunity-risk typology or mismatch framework. However, this is NOT a final
gap claim, because full-text review, translation checks, and additional targeted
verification remain necessary. Current status: gap under verification.

## H. What can be safely claimed now

- The topic should be positioned against Sun 2026 rather than as a
  co-ethnic-network or spatial-assimilation study.
- Japanese-source metadata searches found multiple PARTIAL-overlap studies on
  Chinese residents, housing, ethnic-community formation, and service contexts in
  or near Tokyo.
- No confirmed FULL-combination direct overlap has been identified at the
  metadata / source-verification stage (0 A_direct_overlap at every stage).
- Official sources are sufficient to justify the FEASIBILITY of public-data
  construction (population, spatial, hazard, service context), but licensing and
  variable-level data usability must still be checked.

## I. What cannot be claimed yet

- Cannot claim a final research gap.
- Cannot claim novelty.
- Cannot claim absence of direct-overlap literature.
- Cannot claim official data are fully usable before licensing/format checks.
- Cannot write the manuscript Introduction yet as if the gap were final.
- Cannot rely on metadata alone for a final literature review.

## J. Remaining manual checks

- Translate/read R02_CINII_001 / R02_JSTAGE_002 (Chinese public-housing study).
- Verify R02_CINII_022 in more depth (Chinese white-collar housing choice).
- Verify R02_CINII_018 in more depth (Nishikawaguchi Chinatown).
- Check R02_CINII_015 - whether it is a dataset/statistical source (route to the
  official registry if so).
- Check R02_JSTAGE_021 (study area unclear).
- Read/verify R02_NDL_043 (migrant housing disparity).
- Inspect R02_NDL_OFF_002 (CLAIR periodical) if used as official context.
- Check GSI (R02_OFF_TGT_006) and Hazard Map Portal (R02_OFF_TGT_011)
  licensing/data usability before any data use.
- Manually open TSUNAGARI (R02_OFF_TGT_013) in a normal browser and identify
  stable multilingual-resource pages.

## K. Recommended next step

Prepare a "Round 02 gap-evidence audit table" that converts this synthesis into
an evidence grid by record and by concept dimension (Chinese residents, Tokyo,
Chinese-vs-non-Chinese comparison, housing, transit/accessibility, services,
disaster/risk, arrival/settlement infrastructure, opportunity-risk typology,
spatial method). This will make the partial-overlap pattern explicit per record
and show exactly which concept dimensions remain thin.

Do NOT write the manuscript Introduction yet. Do NOT assert novelty. Status
remains: gap under verification.
