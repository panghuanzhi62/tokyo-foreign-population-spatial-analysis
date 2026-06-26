# Tokyo Chinese Population - Service - Growth Design Feasibility Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Date: 2026-06-25

## A. Purpose

This note objectively assesses the feasibility of the current research design BEFORE
moving into full migrant-service-data acquisition. It is grounded in (1) a rapid bilingual
scoping literature search and (2) the data sources actually available locally or
reproducibly. No modeling is run, no raw data is downloaded, no POI/geocoded/service data
is created, and no manuscript text is written. The academic gap remains UNDER VERIFICATION;
no novelty is claimed.

## B. Current research design

- X: Chinese registered-resident stock, 2023-12 (municipality level, Greater Tokyo).
- M: migrant-oriented service infrastructure, 2024 or observable-by-2024.
- Y: Chinese registered-resident stock change, ending 2025-06 (start 2024-06 or 2024-12).
- Controls: rail accessibility, housing cost, commercial density, population density,
  non-Chinese foreign stock, prefecture fixed effects.
- Interpretive stance: causally cautious, temporally ordered, mechanism-clear. The outcome
  measures MOJ/ISA REGISTERED Chinese foreign-resident STOCK change, NOT Census population
  growth and NOT causal settlement growth.

## C. Literature gap status

Status: UNDER VERIFICATION. In this rapid scoping search, NO direct match (A_direct_match)
was located - that is, no study was found that empirically models the full chain (prior
Chinese registered stock -> a MEASURED migrant-oriented service-infrastructure mediator ->
subsequent Chinese registered stock change at the Greater-Tokyo municipality level for the
2024-2025 window). However, the design is closely flanked on every segment, so the
contribution is best framed as INTEGRATING and formalizing a fragmented literature into one
mediated, temporally ordered chain - not as opening an untouched field. The gap is not
confirmed and must stay under verification pending a dedicated CiNii/J-STAGE full-text pass.

## D. Closest competing literatures

- Sun, Mingchao (2025/2026, Cities; 2022 SSRN) - closest competitor. Dynamic spatial panel
  of registered municipal foreign-resident counts in Greater Tokyo (2012-2018) for Chinese
  and others. Covers X to Y directly but proxies the co-ethnic network by prior stock and
  does NOT measure a service-infrastructure mediator M. Threat: HIGH.
- Takamatsu, Hiroya (2026, Asia Pacific Viewpoint; APSSR) - Chinese ethnoburb and
  ethnic-business formation in suburban Tokyo (Nishi-Kawaguchi). Covers X to M qualitatively,
  single site, no longitudinal stock outcome. Threat: MEDIUM.
- Yamashita, Kiyomi (Ikebukuro Chinatown corpus) - foundational descriptive mapping of
  Chinese concentration and co-ethnic services in a Tokyo ward (X to M). Threat: LOW.
- Honorable mention: multilingual-medical-accessibility preprint (2025) demonstrates the
  stock-to-service spatial-coupling method that an M-measurement step would use.

## E. Direct-match search result

In this rapid scoping search, no A_direct_match was located. Counts: A_direct_match = 0;
B_close_match = 6 (LIT_001-005, LIT_007, LIT_008 borderline); C_adjacent_background = 9;
D = 1. Full classification: literature/02_matrices/tokyo_chinese_population_service_growth_literature_scoping.csv.
Search limitations: several publisher pages (ScienceDirect, Wiley, Springer, SSRN) blocked
full-text fetch; two Japanese PDFs could not be parsed; CiNii/J-STAGE deep full-text search
was not exhausted. Therefore "no direct match LOCATED" - not "no study exists".

## F. Data feasibility by component

- X (Chinese registered stock 2023-12): FEASIBLE. Already local in the validated four-period
  zero-filled ISA/MOJ Chinese-stock panel (251 municipalities). Time point valid. Limitation:
  registered address, not actual residence.
- Y (Chinese registered stock change to 2025-06): FEASIBLE. The same local panel contains
  2024-06, 2024-12 and 2025-06, so both 2024-06->2025-06 and 2024-12->2025-06 are derivable.
  The existing built DV uses 2023-12->2025-06, which spans the pre-M and post-M periods;
  for temporal ordering it should be re-specified to start AFTER M (recommended primary:
  2024-12->2025-06; robustness: 2024-06->2025-06). Use log1p change and retain the
  zero_base flag (6 municipalities); report absolute change as primary descriptive.
- M (migrant-oriented service infrastructure 2024): PARTIAL. See section G.
- Controls: see section H.

Full source matrix: literature/02_matrices/tokyo_chinese_population_service_growth_data_feasibility.csv.

## G. Service 2024 feasibility assessment

PARTIALLY FEASIBLE. Four A_2024_stock licensed/registry sources carry registration,
license, or designation dates plus active status, so existence by/during 2024 can be
inferred directly and used as a true sequential mediator/predictor:

- DF_M01 Registered support organizations for specified skilled workers (ISA) - explicitly
  migrant-oriented; best first source.
- DF_M02 Real estate broker (takken) license search (MLIT/prefectures) - housing brokerage.
- DF_M03 Designated Japanese-language institutions list (MOJ/MEXT/ACA) - migrant education.
- DF_M04 Licensed employment placement / dispatch directory (MHLW) - labor brokerage.

A B_observable_by_2024_or_2025 public-support layer adds a second main dimension
(DF_M05 one-stop consultation centers; DF_M06 international associations). OpenStreetMap
(DF_M08) provides an observable-by-2024 cross-check via element timestamps but has uneven
coverage. Chinese restaurant/ethnic-commercial POI (DF_M09) is VISIBILITY/ROBUSTNESS ONLY
and must never define the main variable. The strictly CHINA-oriented refinement (versus
generic migrant-oriented) is harder, would rely on name markers or manual verification, and
remains PARTIAL and under verification. Net: a defensible 2024 migrant-oriented service-STOCK
count is achievable for the licensed-registry core, but the source pipeline must be validated
(sampled, dated, geocoded to the 251-code frame) before modeling.

## H. Control-variable feasibility assessment

- Rail accessibility: FEASIBLE. NLNI N02 railway/station layer is local (2022 vintage,
  data_raw/N02-22_GML); compute nearest-station distance or population-weighted accessibility.
  Risk: 2022 vintage slightly pre-period; MAUP at municipal aggregation.
- Housing cost: FEASIBLE. NLNI L01-24 land-price points local for the four prefectures
  (data_raw/landPrice); aggregate residential land price to municipality. Time point 2024 is
  ideal. Risk: point sample to areal aggregation; residential vs commercial split.
- Commercial density: FEASIBLE (PARTIAL vintage). e-Stat Economic Census establishment counts
  by municipality (2021 latest; 2024 round in field). Risk: aggregate only; 2021 may pre-date
  period; can double as a denominator.
- Population density: FEASIBLE. Census 2020 municipality population is local; N03 2025-01-01
  boundary is local for area. Compute density by local join. Risk: 2020 Census slightly stale.
- Non-Chinese foreign stock: PARTIAL/FEASIBLE. Derive from ISA/MOJ all-nationality registered
  totals minus Chinese at 2023-12 on the 251-code frame - same source family as X, so
  consistent. Requires an extraction step. A Census fallback exists but introduces a
  measurement mismatch and should be avoided as the primary.
- Prefecture fixed effects: FEASIBLE. Derive from the 5-character municipality_code prefix.

## I. Causal-inference feasibility assessment

- A. Descriptive spatial association: FEASIBLE now.
- B. Temporally ordered association: FEASIBLE if (i) M is measured as an observable-by-2024
  stock (A-class dated sources) and (ii) Y is re-specified to a strictly post-M window
  (2024-12->2025-06 primary). This is the realistic target level for the first paper.
- C. Mechanism-consistent evidence: PARTIAL. Subcategory heterogeneity, dose-response, and
  placebo-service checks can make the mechanism credible but not proven.
- D. Causal mediation (X->M->Y): NOT supported now. Needs exogenous variation in M and strong
  no-unmeasured-confounding assumptions not currently met.
- E. Causal effect: NOT supported now. Needs an exogenous service shock or policy change with
  DID/event-study/IV.

Principal threats (see identification-risk CSV): omitted variable bias (high), reverse
causality (high), anticipatory service location (medium), common trend / shared shock
(medium), spatial selection bias (medium), timing ambiguity in service data (medium, mitigated
by restricting M to A-class dated sources), MAUP and municipality-level aggregation bias
(medium), registered-vs-actual residence (low-medium), zero-base small-count instability
(low-medium). What would be needed for a stronger causal design: panel service data,
municipal fixed effects, pre-trend tests, and a quasi-experiment / DID / event study / IV
built on an exogenous service or policy shock.

## J. Decision table

Design component | Feasibility | Main risk | Required next action
--- | --- | --- | ---
X Chinese registered stock 2023-12 | YES | registered vs actual residence | reuse local 2023-12 panel as X
Y Chinese registered stock change to 2025-06 | YES | endpoint spans pre-M; zero-base | re-specify Y to 2024-12->2025-06 (primary), 2024-06->2025-06 (robustness)
M migrant-oriented service infrastructure 2024 | PARTIAL | service 2024 stock + China-orientation unvalidated | acquire/sample and date the A-class registry sources; geocode to 251 frame
Control rail accessibility | YES | 2022 vintage; MAUP | compute station accessibility from local N02
Control housing cost | YES | point-to-area aggregation | aggregate local L01-24 residential land price
Control commercial density | YES (vintage) | 2021 vintage; aggregate | extract e-Stat establishment counts
Control population density | YES | 2020 Census stale | join local Census2020 + N03 area
Control non-Chinese foreign stock | PARTIAL | extraction step; mismatch if Census used | derive from ISA all-foreign minus Chinese
Control prefecture fixed effects | YES | within-prefecture variation reduced | derive from municipality_code
Identification (temporal ordering) | PARTIAL | reverse causality, OVB | restrict M to dated 2024 stock; post-M Y window

## K. Decision

PARTIAL_GO_REQUIRES_SERVICE_SOURCE_VALIDATION

X and Y are ready (local, validated), and all controls are feasible (most already local).
The design can defensibly support a DESCRIPTIVE and a TEMPORALLY ORDERED association, and a
mechanism-consistent argument, but NOT a causal-mediation or causal-effect claim. The single
open dependency is M: the migrant-oriented service infrastructure must be acquired, dated to
an observable-by-2024 stock from the A-class licensed-registry sources, and geocoded to the
251-code frame before modeling. Proceed to service-source validation; do not run modeling and
do not adopt causal wording.

## L. Recommended revised design (if needed)

Keep X, M, Y, and controls as specified, with two refinements: (1) re-specify Y to a strictly
post-M window (2024-12->2025-06 primary; 2024-06->2025-06 robustness) so the temporal order
X(2023-12) -> M(2024) -> Y(post-2024) holds; (2) build M from the four A-class dated registry
sources as the core count, add the public-support layer as a second dimension, and keep
Chinese restaurant/ethnic-commercial POI strictly as a visibility/robustness layer. Frame
inference at level B (temporally ordered association) with mechanism-consistent probes, not as
causal mediation.

## M. Immediate next three tasks

1. Acquire metadata and a small sample for the first A-class M source (DF_M01 registered
   support organizations), then DF_M02 (takken) and DF_M03 (language institutions); date and
   design geocoding to the 251-code frame. Do not bulk-download or commit POI data.
2. Re-derive Y as 2024-12->2025-06 (primary) and 2024-06->2025-06 (robustness) from the
   existing local four-period panel; retain the zero_base flag and log1p change.
3. Derive the non-Chinese foreign-stock control from ISA all-nationality totals minus Chinese
   (2023-12) on the 251-code frame, and assemble the local control layers (N02 rail, L01-24
   land price, Census2020+N03 density, prefecture FE).

## N. Cautious gap statement

In this rapid bilingual scoping search, no study was located that jointly models prior
Chinese registered stock, a measured migrant-oriented service-infrastructure mediator, and
subsequent Chinese registered stock change at the Greater-Tokyo municipality level for
2024-2025. The closest work (Sun 2025/2026) models the stock-to-stock relationship without a
measured service mediator, and ethnic-business studies (Takamatsu; Yamashita) cover the
concentration-to-service link qualitatively. The apparent gap is therefore the INTEGRATION of
these strands into one temporally ordered, mechanism-clear chain. This is not a confirmed gap
and no novelty is claimed; the gap remains UNDER VERIFICATION pending a dedicated CiNii/J-STAGE
full-text pass and verification of the closest competitors.

## O. Recommended title (provisional, non-novelty)

"Co-ethnic Service Infrastructure and Subsequent Chinese Registered-Resident Stock Change in
Metropolitan Tokyo: A Temporally Ordered Municipality-Level Analysis (2023-2025)".
Alternative: "Does Migrant-Oriented Service Infrastructure Precede Chinese Settlement Change
in Greater Tokyo? A Cautious Municipality-Level Assessment".

## P. Recommended first Japanese scholars to ask for advice

- Yamashita Kiyomi - geographer of the Chinese diaspora and new Chinatowns (M side: Chinese
  ethnic businesses/services).
- Takamatsu Hiroya - Chinese ethnoburb / ethnic-business formation in suburban Tokyo (X-M link).
- Sun Mingchao - dynamic spatial-panel modeling of co-ethnic networks and immigrant location
  choice in Tokyo (X-Y modeling and registered-panel methods).
- Fukumoto Taku - quantitative geography of ethnic-concentration change and ethnic-business
  distribution (measurement of concentration change and segregation).
- Networks: Japan Association for Migration Policy Studies (iminseisaku) and CLAIR
  multicultural-coexistence research network (registered-support-organization and
  consultation-window infrastructure that defines M).

## Q. Evidence limitations

- Scoping search is non-exhaustive; publisher full-text and CiNii/J-STAGE deep search were
  partly blocked; several authors/years are marked UNCLEAR and need verification.
- M feasibility is a source audit, not an acquired dataset; service-2024 stock and the
  China-specific refinement are not yet validated.
- Control vintages are mixed (rail 2022, land price 2024, commercial 2021, population 2020).
- The dependent variable measures ISA/MOJ REGISTERED stock, not Census population or actual
  settlement.
- No modeling was run; no causal claim is made.

## R. Gap status

UNDER VERIFICATION.
