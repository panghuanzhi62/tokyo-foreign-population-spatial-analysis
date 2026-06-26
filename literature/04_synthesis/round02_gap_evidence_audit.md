# Round 02 Gap-Evidence Audit

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (record-by-dimension gap-evidence audit)
Provisional topic: Chinese Residents and Opportunity-Risk Mismatch in
Metropolitan Tokyo: A Public-Data Analysis of Housing, Accessibility, Services,
and Disaster Exposure

## A. Purpose

This note converts the Round 02 Japanese-source synthesis into a structured
record-by-dimension audit. The companion machine-readable grid is
literature/02_matrices/round02_gap_evidence_audit_table.csv: one row per key
literature record or official source, with cautious coverage codes (yes /
partial / no / unclear / not_applicable) for each conceptual dimension of the
provisional project.

## B. Evidence boundary

- This is an evidence audit based on metadata, source-level verification,
  selected priority-candidate verification, and the existing synthesis notes.
- It is NOT a full-text review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- It does NOT prove the absence of direct-overlap literature.
- Current status: gap under verification.

## C. Audit table summary

- Rows in round02_gap_evidence_audit_table.csv: 43
- Academic / literature records: 20 (includes 1 Sun 2026 boundary reference that
  is NOT a matrix record; the other 19 are Round 01/Round 02 matrix records)
- Official-source records: 23 (the full official_source_registry)
- Records with covers_full_combination = yes: 0
- Records with covers_chinese_vs_non_chinese_comparison = yes or partial: 6
  (Sun 2026 boundary [partial]; R01_HRB_002 Liang [partial]; and the 4 official
  population-data sources R02_OFF_TGT_001/002/003/004 [partial, via nationality
  disaggregation] - no record provides a designed Chinese-vs-non-Chinese
  opportunity-risk comparison)
- Records covering housing (yes or partial): 15
- Records covering service access (yes or partial): 14
- Records covering disaster/risk exposure (yes or partial): 6
- Official data / context sources: 23
- Held / weak records: 2 (R02_OFF_TGT_013 TSUNAGARI = hold;
  R02_NDL_OFF_001 MOJ directive = weak)

Note on Sun 2026: it is referenced in the synthesis/positioning notes but has no
record_id in literature_matrix.csv or gap_verification_matrix.csv; it is audited
as a sun2026_boundary_reference row (matrix_or_registry_location =
"not_in_matrices"). All other listed source IDs were present and were included.

## D. Main findings by dimension

1. Chinese residents / Chinese nationals in (Metropolitan) Tokyo - PARTIAL.
   Strongest: R02_CINII_001 / R02_JSTAGE_002 (Chinese public-housing residents,
   Greater Tokyo) and R02_CINII_022 (Chinese white-collar housing choice, metro
   Tokyo). Limitation: qualitative, single-module, small-N; full text not read.
   Manual check: translate/read both.

2. Chinese residential concentration / ethnic community - PARTIAL (mostly
   background). R02_CINII_018 (Nishikawaguchi Chinatown, Tokyo region) plus
   historical R02_CINII_019 and R02_JSTAGE_007; R02_JSTAGE_011 is an Osaka
   comparator. Limitation: enclave/historical focus; Sun 2026 already covers
   co-ethnic networks. Manual check: verify R02_CINII_018.

3. Housing and residential disparity - RELATIVELY STRONG (partial). R02_NDL_043
   (migrant housing disparity, Japan), R02_CINII_001/_022 (Chinese housing),
   and R01_RB_005/_006/_013 (Tokyo rental discrimination), R01_RB_007 (Toshima
   satisfaction). Limitation: mostly not Chinese-specific; single-module each;
   R02_NDL_043 full text not read. Manual check: read R02_NDL_043; isolate
   Chinese subgroup in the R01 experiments.

4. Public housing and housing policy context - PARTIAL/CONTEXT. Academic:
   R02_CINII_001 (public estates). Official: R02_OFF_TGT_007 (Tokyo Bureau of
   Housing Policy), _008 (UR), _009 (JKK). Limitation: one academic record;
   official items are context, not analysis. Manual check: inventory
   public-housing data.

5. Transit / accessibility - WEAK (academic) / official spatial support. No
   verified academic record codes transit accessibility as yes. Official
   R02_OFF_TGT_005 (MLIT National Land Numerical Information; transit layers) is
   the main feasibility source. Manual check: confirm transit layers/usability.

6. Service accessibility and multilingual administrative infrastructure -
   CONTEXT-STRONG, academically thin. Official: R02_OFF_TGT_013 (TSUNAGARI;
   held), _014 (TICC), _015 (ISA portal), _016 (CLAIR), _021 (KIF),
   R02_NDL_OFF_002 (CLAIR periodical). Academic support is partial/background
   only. Manual check: inspect TSUNAGARI/TICC/CLAIR resources.

7. Education / childcare / welfare / health access - BACKGROUND. R02_NDL_087,
   R02_NDL_088 (foreign-children education); R02_NDL_068 (language support,
   Okayama). Official: R02_OFF_TGT_017 (MEXT CLARINET), _018 (MHLW). Limitation:
   non-empirical / non-Tokyo / non-Chinese. Manual check: keep as background.

8. Disaster prevention / hazard / risk exposure - PARTIAL (one strong spatial
   comparator + official data). R01_RB_004 (foreign-resident disaster
   vulnerability, Tokyo) is the closest academic comparator; R01_RB_008
   (historical). Official: R02_OFF_TGT_010 (Tokyo disaster portal), _011 (Hazard
   Map Portal; verified catalogue), _012 (Cabinet Office). Limitation: not
   Chinese-specific; not integrated. Manual check: Hazard Map Portal licensing.

9. Spatial data / GIS source feasibility - STRONG for feasibility. Official:
   R02_OFF_TGT_005 (MLIT NLNI), _006 (GSI; verified), _001/_002/_003/_004
   (population data), _011 (hazard). Limitation: licensing / data usability not
   yet checked; these are not analysis. Manual check: license/format checks.

10. Chinese-vs-non-Chinese comparison - WEAK / NOT YET EVIDENCED. No verified
    academic record performs a designed Chinese-vs-non-Chinese foreign-resident
    comparison; only official population data (R02_OFF_TGT_001/002/003/004) can
    support such a comparison via nationality disaggregation (coded partial).
    This is the main differentiation space to develop.

11. Full opportunity-risk mismatch combination - ABSENT. 0 audited records have
    covers_full_combination = yes, and 0 have covers_opportunity_risk_typology_
    or_mismatch = yes. No record integrates Chinese residents in Metropolitan
    Tokyo + Chinese-vs-non-Chinese comparison + housing + transit/accessibility
    + services + disaster/risk + an explicit opportunity-risk typology. This is
    a provisional audit observation, not a verified gap claim.

## E. Sun 2026 boundary check

Per sun_2026_positioning_note.md, Sun 2026 (Cities) already covers the Tokyo
metropolitan area (242 municipalities, 2012-2018), Chinese / Vietnamese /
Filipino / Brazilian immigrants, co-ethnic networks, spatial assimilation, and
dynamic spatial Durbin modeling. Therefore:

- Do NOT frame the project as a co-ethnic-network study.
- Do NOT frame the project as a spatial-assimilation study.
- Do NOT claim a gap in Chinese immigrant location choice in Tokyo.

The safer provisional distinction is an OPPORTUNITY-RISK ENVIRONMENTAL PROFILE
that compares Chinese residents with non-Chinese foreign residents using
public-data construction across housing, accessibility, services, and
disaster/risk exposure. The audit shows that dimensions 9-11 (Chinese-vs-non-
Chinese comparison; transit accessibility integration; full opportunity-risk
combination) are the least-occupied among the audited records - this is
positioning, not a verified gap.

## F. Gap status after audit

At the current metadata / source-verification / audit stage, no audited record
is confirmed to cover the full combination of Chinese residents or Chinese
nationals in Metropolitan Tokyo, Chinese-vs-non-Chinese foreign-resident
comparison, housing, transit/accessibility, service infrastructure,
disaster/risk exposure, and an explicit opportunity-risk typology or mismatch.
However, this remains a provisional evidence status, not a final gap claim,
because full-text review, translation, and additional targeted checks remain
necessary. Current status: gap under verification.

## G. Safe claims now

- The topic should be positioned against Sun 2026, not inside the
  co-ethnic-network / spatial-assimilation gap.
- Existing Japanese-source records provide PARTIAL support for the Chinese-
  residents, housing, residential-concentration, and service-context modules.
- Official sources support public-data feasibility and policy/service context.
- The full opportunity-risk mismatch combination has NOT been confirmed in the
  audited records (0 full-combination).
- The gap remains under verification.

## H. Unsafe claims now

- Cannot claim a final research gap.
- Cannot claim novelty.
- Cannot claim absence of direct-overlap literature.
- Cannot claim all official data are usable before licensing/format checks.
- Cannot write the Introduction as if the gap were final.
- Cannot rely on metadata alone for a final literature review.

## I. Remaining manual checks

- Translate/read R02_CINII_001 / R02_JSTAGE_002.
- Verify R02_CINII_022 in more depth.
- Verify R02_CINII_018 in more depth.
- Check R02_CINII_015 - whether it is a dataset/statistical source.
- Check R02_JSTAGE_021 (study area unclear).
- Read/verify R02_NDL_043.
- Inspect R02_NDL_OFF_002 (CLAIR periodical) if used as official context.
- Check GSI (R02_OFF_TGT_006) and Hazard Map Portal (R02_OFF_TGT_011)
  licensing/data usability.
- Manually open TSUNAGARI (R02_OFF_TGT_013) and identify stable
  multilingual-resource pages.
- Inspect whether any non-Japanese English literature published after Sun 2026
  changes the status.

## J. Recommended next step

Prepare a "gap-safe topic positioning memo" for internal use, based strictly on
this audit table - articulating the opportunity-risk environmental-profile
framing, the Chinese-vs-non-Chinese comparison, and the public-data feasibility,
while explicitly avoiding any final-gap or novelty language.

Do NOT write the manuscript Introduction yet. Do NOT assert novelty. Status
remains: gap under verification.
