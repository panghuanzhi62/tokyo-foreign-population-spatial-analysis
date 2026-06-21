# Round 02 High-Value Official-Source Verification

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (verification of high-value official sources held from the targeted search)

## A. Purpose

This note verifies three high-value official-source records that were marked
hold_for_manual_check in the targeted official-source search because automated
reachability checks did not confirm them:

- R02_OFF_TGT_006 - GSI Maps / Geospatial Information Authority of Japan
- R02_OFF_TGT_011 - Hazard Map Portal Site (MLIT/GSI)
- R02_OFF_TGT_013 - Tokyo Metropolitan Foundation "TSUNAGARI" / multilingual life information

Verification used a single reachability GET of each official landing page (page
title only, to confirm identity). No site was crawled, and no PDF or dataset was
downloaded.

## B. Evidence status

- This is official-source verification, not academic literature review.
- It does NOT confirm the research gap.
- It does NOT prove novelty.
- It does NOT involve full dataset use.
- PDFs and datasets were NOT downloaded.
- Current status: gap under verification.

## C. Verification table

| source_id | institution | source_title | domain | verification_status | use_in_analysis | registry_action | reason | remaining_manual_check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R02_OFF_TGT_006 | 国土地理院 (Geospatial Information Authority of Japan, GSI) | 地理院地図 / GSI Maps | national base maps / geospatial reference | verified_by_official_page | official_spatial_data | updated (status + notes) | HTTPS GET of https://www.gsi.go.jp/ returned HTTP 200, title "GSI HOME PAGE - 国土地理院"; prior hold was an SSL legacy-renegotiation handshake artifact, not a dead link. | Confirm GSI Maps / 地理院地図 layer terms and data usability/license before use. |
| R02_OFF_TGT_011 | 国土交通省 (MLIT) / 国土地理院 | ハザードマップポータルサイト | hazard maps / disaster-risk exposure | verified_by_official_catalogue | disaster_or_risk_context | updated (status + notes) | HTTPS GET of https://disaportal.gsi.go.jp/ returned HTTP 200, title "ハザードマップポータルサイト"; prior hold was a TLS handshake timeout. | Confirm specific hazard layers and data usability/license before building the exposure layer. |
| R02_OFF_TGT_013 | 公益財団法人東京都つながり創成財団 (Tokyo Metropolitan Foundation "Tsunagari") | 東京都つながり創成財団 / 東京都多言語生活情報 | multilingual living information / foreign-resident support | hold_for_manual_check | multilingual_administrative_context | updated (notes only; status unchanged) | HTTPS GET of https://www.tsunagari-tokyo.jp/ still failed with SSL UNEXPECTED_EOF_WHILE_READING under strict and legacy TLS in this environment (likely network/TLS blocking, not necessarily a dead site). | Manually confirm the live page, structure, multilingual resources, and license. |

## D. Source-by-source notes

- R02_OFF_TGT_006 (GSI): authoritative national base maps and geospatial
  reference (基盤地図情報, 地理院地図). Supports the SPATIAL DATA / basemap and
  geocoding context for the analysis. Now reachability-confirmed at the official
  GSI homepage; the specific GSI Maps layers and their terms still require manual
  checking before any data is used. No dataset downloaded.

- R02_OFF_TGT_011 (Hazard Map Portal): the official MLIT/GSI portal aggregating
  municipal hazard maps (flood, sediment/landslide, storm surge, tsunami) and a
  national "重ねるハザードマップ" overlay. Supports the DISASTER / RISK EXPOSURE
  interpretation and the open spatial-data inventory for Tokyo-region
  municipalities. Now reachability-confirmed; specific layer availability and
  data usability/license still require manual checking. No hazard data downloaded.

- R02_OFF_TGT_013 (TSUNAGARI): a Tokyo Metropolitan quasi-official foundation
  providing multilingual living information and foreign-resident support; it is
  part of Tokyo's foreign-resident service infrastructure. Supports the
  MULTILINGUAL ADMINISTRATIVE / SERVICE-INFRASTRUCTURE context. The live page
  could not be reached in this environment (TLS UNEXPECTED_EOF), so the record is
  kept hold_for_manual_check; the institution identity and relevance are sound,
  but the page structure, multilingual resources, and license must be confirmed
  manually before citing.

## E. Registry updates

Exactly three rows in literature/02_matrices/official_source_registry.csv were
updated (no new rows; no rows removed; no rows moved):

- R02_OFF_TGT_006: verified_status hold_for_manual_check -> verified_by_official_page;
  notes updated to record the HTTP 200 confirmation and the SSL legacy-
  renegotiation explanation.
- R02_OFF_TGT_011: verified_status hold_for_manual_check -> verified_by_official_catalogue;
  notes updated to record the HTTP 200 confirmation and operator (MLIT/GSI).
- R02_OFF_TGT_013: verified_status unchanged (hold_for_manual_check); notes
  updated to record the persistent TLS failure, the known institutional identity,
  and the manual checks still required.

No official source was added to literature_matrix.csv or
gap_verification_matrix.csv; both academic matrices are unchanged.

## F. Caution

- These official sources support variable construction (spatial/hazard layers),
  the data-source inventory, and policy/service context interpretation.
- They do NOT by themselves establish an academic research gap.
- They must NOT be cited as evidence that no prior study exists.
- Status remains: gap under verification.

## G. Next steps

- Manually check license/data usability for GSI (R02_OFF_TGT_006) and the Hazard
  Map Portal (R02_OFF_TGT_011) before using any data.
- Manually inspect the TSUNAGARI (R02_OFF_TGT_013) page structure and multilingual
  resources before citing; re-verify reachability outside the sandbox.
- Then prepare a Round 02 Japanese-source synthesis across CiNii, J-STAGE, NDL,
  and the official-source searches.
- Do not write the Introduction yet.
- Do not assert novelty yet.
