# Manual Full-Text and Translation Checklist

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (manual full-text / translation / source-verification checklist)
Provisional topic: Chinese Residents and Opportunity-Risk Environments in
Metropolitan Tokyo: A Public-Data Analysis of Housing, Accessibility, Services,
and Disaster Exposure

## A. Purpose

This note identifies the manual full-text, translation, metadata, licensing, and
official-source checks required before any formal manuscript text (Introduction
or literature-gap statement) is drafted. The companion machine-readable file is
literature/02_matrices/manual_fulltext_translation_checklist.csv (23 rows).

Explicitly:
- This is a CHECKLIST, not a literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- It does NOT involve PDF or dataset download.
- Current status: gap under verification.

## B. Evidence base

- Gap-safe topic positioning memo (gap_safe_topic_positioning_memo.md).
- Round 02 gap-evidence audit (round02_gap_evidence_audit.md +
  round02_gap_evidence_audit_table.csv).
- Round 02 Japanese-source synthesis (round02_japanese_source_synthesis.md).
- literature_matrix.csv, gap_verification_matrix.csv, official_source_registry.csv.
- Sun 2026 positioning note (sun_2026_positioning_note.md).

Checklist totals: 23 rows (P1 = 13; P2 = 10; academic/dataset = 12; official = 11).

## C. P1 checks required before manuscript Introduction

| source_id | title_or_source_title | why_it_is_P1 | manual_check_needed | specific_questions | possible_decision_after_check |
| --- | --- | --- | --- | --- | --- |
| R02_CINII_001 / R02_JSTAGE_002 | Chinese-nationality residents in two Greater Tokyo public-housing estates (Wang & Fujii 2021) | strongest Chinese + Tokyo + (public) housing record | full-text reading + translation | Chinese nationals in public housing in metro Tokyo? housing/community only or opportunity/risk? non-Chinese comparison? services/disaster/transit? | add to formal literature review (housing/public-housing) |
| R02_CINII_022 | Chinese white-collar housing purchase motives, Tokyo metropolitan area (Zhang 2020) | Chinese-specific housing-choice in metro Tokyo | full-text reading + translation | spatial/accessibility/services/risk? comparison with other groups? housing-preference vs boundary record? | add to formal literature review (housing) |
| R02_CINII_018 | Nishikawaguchi Chinatown formation, Tokyo region (Takamatsu 2020) | Chinese concentration area in the Tokyo region | full-text reading + translation | community vs commercial vs residential? metropolitan-scale detail? opportunity/risk? | background, partial overlap, or boundary |
| R02_NDL_043 | Residential disparity for migrants in Japan's housing market (Kim 2026, book) | housing/residential-disparity support; possible comparison framework | full-text reading + translation | Chinese/nationality comparison? framework for Chinese-vs-non-Chinese? | add to formal literature review (housing disparity) |
| R02_CINII_015 | Chinese population in Chinese concentration areas in the Tokyo region (CiNii record) | may be a dataset/statistical source affecting the evidence boundary | dataset/statistical-source check | dataset, thesis, article, or bibliographic record? usable Chinese-population data? | use for variable construction / move to registry / hold / exclude |
| R02_JSTAGE_021 | Homes of Chinese newcomers in a less-concentrated area (Liu 2016) | scope unclear but potentially relevant | metadata disambiguation + translation | exact area/population/method? Tokyo-region relevance? | add to matrix or hold |
| R02_OFF_TGT_001 | e-Stat | foreign-resident population baseline / denominators | license/data-usability check | which tables? granularity? license/format? | use for variable construction |
| R02_OFF_TGT_002 | ISA Statistics on foreign residents | Chinese counts by nationality and area | license/data-usability check | nationality/area breakdown? time series? license? | use for variable construction |
| R02_OFF_TGT_005 | MLIT National Land Numerical Information | spatial layers for accessibility/exposure | license/data-usability check | which layers? CRS? vintage? license? | use for variable construction |
| R02_OFF_TGT_006 | GSI Maps | basemaps / geocoding reference | license/data-usability check | basemap/geocoding terms? attribution? | use for data feasibility |
| R02_OFF_TGT_010 | Tokyo Metropolitan Government Disaster Prevention | disaster + multilingual disaster information | official-page manual verification | hazard/evacuation/multilingual scope? data vs guidance? | use for policy context |
| R02_OFF_TGT_011 | Hazard Map Portal Site | hazard-exposure layer | license/data-usability check | downloadable vs view-only layers? coverage? license? | use for variable construction |
| R02_OFF_TGT_013 | TSUNAGARI / Tokyo multilingual living information | core Tokyo multilingual service infra; reachability unconfirmed | official-page manual verification | live URL/stable pages? multilingual resources? TMG relationship? | use for service context or hold |

## D. P2 checks required before formal literature review

| source_id | title_or_source_title | module | manual_check_needed | expected_use |
| --- | --- | --- | --- | --- |
| R02_CINII_019 | Exclusion/decline of Chinese-worker districts, early-Showa Tokyo (Abe 2000) | historical concentration | translation check | background only |
| R02_JSTAGE_007 | Residential differentiation of Chinese workers, 1920s Tokyo Prefecture (Abe 1999) | historical housing/differentiation | translation check | background only |
| R02_JSTAGE_011 | Chinese newcomers, dispersed residence, Osaka (Wang 2026) | non-Tokyo comparator | translation check | background/comparator only |
| R02_NDL_087 | Forum on education of foreign children: report (Saito ed. 2006) | service/education | full-text/content-type check | background only |
| R02_NDL_088 | Pre-school education for foreign children (Saito ed. 2006) | service/childcare | full-text/content-type check | background only |
| R02_NDL_068 | Brazilian residents' language support, Okayama (Nakato 2014) | service/language | translation check | background/comparator only |
| R02_OFF_TGT_004 | Tokyo statistics / population estimates | population | license/data-usability check | variable construction |
| R02_OFF_TGT_007 | Tokyo Bureau of Housing Policy | housing/public-housing policy | policy-context check | policy context |
| R02_OFF_TGT_016 | CLAIR Multicultural Coexistence Portal | service/multilingual | service-infrastructure check | service context |
| R02_NDL_OFF_002 | CLAIR periodical | service/multilingual | policy-context check | policy context |

## E. What each P1 academic check must answer

- R02_CINII_001 / R02_JSTAGE_002: Does it focus specifically on Chinese
  nationals/residents in public housing in the Tokyo metropolitan area? Living
  conditions and community involvement only, or also opportunity/risk dimensions?
  Any comparison with non-Chinese foreign residents? Services, disaster risk,
  transit/accessibility, or only housing/community? Treat as housing-module
  support, public-housing context, or a gap boundary record?
- R02_CINII_022: Does it focus on Chinese white-collar housing purchase
  motivation in Metropolitan Tokyo? Include spatial patterns, accessibility,
  services, or risk dimensions? Compare Chinese residents with other foreign
  groups or Japanese residents? Use as housing-preference literature or boundary?
- R02_CINII_018: Does it analyze Nishikawaguchi Chinatown formation as ethnic-
  community formation, commercial concentration, or residential settlement?
  Spatial/municipal detail at the metropolitan scale? Opportunity/risk dimensions
  or only community formation? Background, partial overlap, or boundary?
- R02_NDL_043: Does it provide empirical evidence on immigrant housing inequality
  in Japan? Include Chinese residents or nationality-specific comparisons? A
  framework relevant to Chinese-vs-non-Chinese comparison? Enter formal review as
  housing/residential-disparity support?
- R02_CINII_015: Is it a dataset/statistical source, thesis, article, or
  bibliographic record? Does it contain usable data on Chinese population in
  Tokyo-area concentration? Should it move to official_source_registry, remain
  hold, or be excluded?
- R02_JSTAGE_021: What is its exact title, area, population group, and method? Is
  it relevant to Chinese newcomers / ethnic community / Tokyo-region settlement?
  Add to the literature matrix, gap matrix, or hold?

## F. Official-source manual checks

| source_id | institution | domain | manual_check | use_if_confirmed | caution |
| --- | --- | --- | --- | --- | --- |
| R02_OFF_TGT_001 | Statistics Bureau / e-Stat | population statistics | license/data usability | variable construction (population baseline) | confirm license + table granularity; data not downloaded |
| R02_OFF_TGT_002 | Immigration Services Agency | foreign-resident statistics | license/data usability | variable construction (Chinese by nationality) | confirm nationality/area tables + license |
| R02_OFF_TGT_005 | MLIT (NLNI) | spatial base data | license/data usability | variable construction (accessibility/exposure) | confirm layers/CRS/license; dataset not downloaded |
| R02_OFF_TGT_006 | GSI | base maps / geocoding | license/data usability | data feasibility (basemap/geocoding) | confirm terms of use; reachability re-verified |
| R02_OFF_TGT_010 | Tokyo Metropolitan Government | disaster prevention | official-page verification | policy/service context | guidance vs data; confirm multilingual scope |
| R02_OFF_TGT_011 | MLIT/GSI | hazard maps | license/data usability | variable construction (exposure layer) | confirm downloadable layers + license; reachability re-verified |
| R02_OFF_TGT_013 | Tokyo Metropolitan Foundation TSUNAGARI | multilingual living information | official-page manual verification | service context | live page not reachable in sandbox; open in a normal browser |
| R02_OFF_TGT_007 | Tokyo Bureau of Housing Policy | housing policy | policy-context check | policy context | context, not analysis |
| R02_OFF_TGT_016 / R02_NDL_OFF_002 | CLAIR | multicultural coexistence | service/policy context | service/policy context | quasi-official; periodical access to confirm |

For each: e-Stat, ISA, NLNI, GSI, and the Hazard Map Portal support VARIABLE
CONSTRUCTION (subject to licensing/usability checks); Tokyo disaster prevention,
Tokyo housing policy, TSUNAGARI, and CLAIR support OFFICIAL CONTEXT / SERVICE
INTERPRETATION (background, not analysis). None is academic gap evidence.

## G. Do-not-do list for the manual phase

- Do not download copyrighted PDFs into the public repo.
- Do not commit PDFs or screenshots.
- Do not scrape Google Scholar.
- Do not assert a final gap from metadata.
- Do not write the final Introduction before the P1 checks are complete.
- Do not treat official sources as academic gap evidence.
- Do not conflate Chinese nationals (by nationality, as in official data) with
  Chinese-origin residents (as in some migration literature) without
  clarification.

## H. Decision rules after manual checks

| manual_check_result | matrix_or_memo_action | effect_on_gap_status |
| --- | --- | --- |
| full text confirms only housing/public-housing module | keep as partial overlap, not direct gap evidence | unchanged (gap under verification) |
| full text includes Chinese-vs-non-Chinese comparison but not services/risk | strengthen the comparison dimension in the audit | still not full combination; gap under verification |
| full text covers the full opportunity-risk combination | upgrade to A_direct_overlap_candidate and revise topic positioning | requires re-evaluation; do NOT assert novelty |
| record is a dataset/statistical source | move to official_source_registry (not literature) | neutral for the literature gap |
| official source license usable | mark usable for variable construction | feasibility supported (not a gap claim) |
| official source page unstable/unreachable | keep as context only or hold | feasibility caveat noted |

## I. Recommended sequence

1. R02_CINII_001 / R02_JSTAGE_002
2. R02_CINII_022
3. R02_NDL_043
4. R02_CINII_018
5. R02_CINII_015
6. R02_JSTAGE_021
7. Official data feasibility checks: e-Stat (R02_OFF_TGT_001), ISA
   (R02_OFF_TGT_002), NLNI (R02_OFF_TGT_005), GSI (R02_OFF_TGT_006), Hazard Map
   Portal (R02_OFF_TGT_011)
8. TSUNAGARI (R02_OFF_TGT_013) and multilingual/service-context checks
   (R02_OFF_TGT_010, R02_OFF_TGT_016, R02_NDL_OFF_002)

## J. Next repo task

Prepare a local "manual_check_results_template.csv" for recording outcomes once
the listed sources are manually checked. (A header-only template has been created
at literature/02_matrices/manual_check_results_template.csv this pass; the next
task can populate it as checks are completed.)

Do NOT write the final Introduction yet. Do NOT assert novelty. Status remains:
gap under verification.
