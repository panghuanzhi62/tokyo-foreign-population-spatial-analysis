# Manual Full-Text / Translation Results - Batch 1 (P1 academic records)

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (P1 manual verification, batch 1)
Provisional topic: Chinese Residents and Opportunity-Risk Environments in
Metropolitan Tokyo: A Public-Data Analysis of Housing, Accessibility, Services,
and Disaster Exposure

## A. Purpose

This is the FIRST batch of P1 manual full-text / translation / source-access
verification, following the manual checklist. It verifies the six P1 academic
records in the recommended order and records results in
literature/02_matrices/manual_check_results_template.csv (6 rows appended).

## B. Evidence boundary

- This is assisted manual verification (official pages / abstracts / metadata),
  NOT a final literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- Current status: gap under verification.

## C. Access status table

| source_id | access route | legal/open access | full text saved locally (outside repo) | result | remaining issue |
| --- | --- | --- | --- | --- | --- |
| R02_CINII_001 / R02_JSTAGE_002 | J-STAGE official article page (DOI 10.24528/lifology.40.0_54) | open abstract (English) read | page HTML saved outside repo | verified_partial_overlap | full PDF not read |
| R02_CINII_022 | J-STAGE via doi.org (DOI 10.4157/grj.93.1) | open abstract (Japanese) read | page HTML saved outside repo | verified_partial_overlap | owner-occupier subset (n=22) |
| R02_NDL_043 | NDL landing page (HTTP 503) | commercial book; no open full text | none | verified_partial_overlap | Chinese/Tokyo coverage unconfirmed |
| R02_CINII_018 | CiNii record page | metadata/title confirmed; no open abstract | page HTML saved outside repo | verified_partial_overlap | full text not read |
| R02_CINII_015 | CiNii record page | Dataset-type record; provenance unclear | page HTML saved outside repo | still_unclear_hold | data provenance/usability unclear |
| R02_JSTAGE_021 | J-STAGE official article page (DOI 10.20790/easoc.2016.8_92) | open abstract (English) read | page HTML saved outside repo | verified_background_only | exact city not stated; appears non-Tokyo |

Local full-text/page cache (OUTSIDE the Git repo, never committed):
E:\rsch\laborJapan_local_fulltext\round02_manual_check\

## D. Findings by record

1. R02_CINII_001 / R02_JSTAGE_002 (Wang & Fujii 2021) - verified_partial_overlap.
   Confirmed: highly-educated, technically-skilled Chinese in public-housing
   estates in the Tokyo metropolitan area; two estates (Kawaguchi Shibazono,
   Saitama; Oshima 4-chome, Tokyo); 10 Chinese-resident interviews; employer-
   assisted public housing; limited community involvement. Confirmed dimensions:
   Chinese residents (yes), Metropolitan Tokyo (yes), housing/public housing
   (yes), community/service (partial). NOT confirmed: services/accessibility
   analysis, transit, disaster, Chinese-vs-non-Chinese comparison. Recommended:
   keep existing matrix rows; housing/public-housing partial-overlap evidence.

2. R02_CINII_022 (Zhang 2020) - verified_partial_overlap. Confirmed: Chinese
   white-collar housing purchase motives/preferences, Tokyo metropolitan area;
   22 interviews; economic motives plus long-term settlement intention. Single
   housing module. NOT confirmed: comparison, services, disaster, transit.
   Recommended: keep existing matrix rows; housing-preference partial overlap.

3. R02_NDL_043 (Kim 2026, book) - verified_partial_overlap (metadata only; NDL
   page 503). Confirmed from metadata: empirical residential-disparity analysis
   for migrants in Japan's housing market; Japan-wide. NOT confirmed: Chinese
   subgroup, Tokyo specificity, comparison framework (need book full text).
   Recommended: keep existing matrix rows; confirm Chinese/Tokyo coverage via a
   library copy; if absent, consider literature_matrix-only rather than gap_matrix.

4. R02_CINII_018 (Takamatsu 2020) - verified_partial_overlap. Confirmed:
   formation of Nishikawaguchi Chinatown as a Chinese concentration area in the
   Tokyo region (Kawaguchi, Saitama); ethnic-community formation; housing partial.
   NOT confirmed: opportunity/risk dimensions. Recommended: keep existing matrix
   rows; concentration/community partial overlap; enclave framing is
   Sun-2026-adjacent (boundary).

5. R02_CINII_015 - still_unclear_hold. The CiNii record is a Dataset-type entry
   ("Chinese population in Chinese concentration areas in the Tokyo region"), no
   author/year, with unclear data provenance (a prior pass noted the linked
   identifier points to an unrelated repository). Likely an aggregated
   population/statistical record, not a literature article. Recommended: keep
   hold; manually open the linked identifier; if confirmed as aggregated public
   statistics, move/copy to official_source_registry later; else hold or exclude.

6. R02_JSTAGE_021 (Liu 2016) - verified_background_only. Confirmed: the sense of
   "Homes" of Chinese newcomer adolescents in a city WITHOUT a concentrated
   Chinese-resident area; 6 interviews; identity/belonging, bullying/
   discrimination. Study area is an unspecified less-concentrated city, NOT
   identified as Metropolitan Tokyo; theme is identity/belonging, not housing/
   services/disaster. Recommended: treat as background (Chinese-newcomer
   identity); add to literature_matrix later as background; do not use for the
   housing/opportunity-risk modules.

## E. Matrix-action recommendations (future only; NO edits performed now)

- keep_existing_matrix_rows: R02_CINII_001 / R02_JSTAGE_002, R02_CINII_022,
  R02_NDL_043, R02_CINII_018.
- add_to_literature_matrix_later (background): R02_JSTAGE_021.
- keep_hold (and possibly move to official_source_registry later if confirmed as
  statistics): R02_CINII_015.

No row in literature_matrix.csv or gap_verification_matrix.csv was modified in
this task. All recommendations are recorded only in
manual_check_results_template.csv.

## F. Direct-overlap caution

None of the records checked in this batch can be treated as a confirmed
full-combination direct-overlap record at this stage. None covers the full
combination of Chinese residents/nationals in Metropolitan Tokyo + Chinese-vs-
non-Chinese comparison + housing + transit/accessibility + service infrastructure
+ disaster/risk exposure + an explicit opportunity-risk typology/mismatch. Each
verified item covers one or two modules only (housing, public housing,
concentration/community, or identity/belonging). Status remains: gap under
verification.

## G. Copyright and repository safety

- No copyrighted full texts were committed to the repository.
- No paywalled or subscription-only files were downloaded; no Sci-Hub or mirror
  copies were used.
- Only official pages / open abstracts / existing metadata were accessed for
  verification (single GET per record).
- Any saved page HTML is stored OUTSIDE the Git repo
  (E:\rsch\laborJapan_local_fulltext\round02_manual_check\) and is never staged
  or committed.
- No PDFs, datasets, or screenshots were staged.
