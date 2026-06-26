# Automated Literature Discovery Protocol

Project: Tokyo-China opportunity-risk mismatch (provisional)
Repo: E:\rsch\laborJapan

## Why API-based metadata discovery is used before manual SciSpace review

API-based metadata discovery (OpenAlex, Crossref, Semantic Scholar, optionally
CiNii) gives broad, reproducible, machine-readable coverage of the published
record at low cost. It is used first because:

- it is exhaustive and fast across many query groups;
- it returns structured fields (DOI, year, venue, authors) that can be
  deduplicated and triaged automatically;
- it produces a transparent, re-runnable candidate list that a human can then
  review, rather than starting from ad hoc manual searching.

Manual SciSpace review is reserved for later because deep semantic reading is
expensive and should be spent only on the highest-risk candidates that the API
pass surfaces.

## Why no final gap claim is allowed at this stage

This stage produces candidates and PRELIMINARY keyword triage only. It cannot
establish what a paper actually did, how it framed its question, or whether it
truly integrates Chinese residents, housing, accessibility, services, disaster
risk, and an opportunity-risk typology in Metropolitan Tokyo. Therefore:

- the research gap must NOT be asserted here;
- the provisional working title remains provisional;
- only manual deep reading can confirm or refute overlap.

## Why Google Scholar should not be scraped automatically

Google Scholar prohibits automated scraping, offers no official API, blocks
robots, and returns unstable, non-citable HTML. Automated scraping would be a
terms-of-service violation and would produce unverifiable records. Google
Scholar may still be used MANUALLY by a human for spot checks.

## Why SciSpace should be used later as a validation and deep-review tool

SciSpace is best applied after the API pass has narrowed the field. It is used
to validate the high-risk (A_direct_overlap and B_partial_overlap) candidates,
read them deeply, and extract what they actually cover. It is a validation and
deep-review tool, not the first-round discovery engine.

## Which APIs are used

- OpenAlex Works API (open, no key required).
- Crossref REST API (open, no key required).
- Semantic Scholar Graph API (used only if reachable without a key).
- CiNii (used ONLY if CINII_APP_ID is present in the environment).

No API keys are stored, written, or printed by the pipeline. Google Scholar is
never queried automatically.

## How duplicate records are handled

Records are deduplicated by DOI first. When a DOI is absent, deduplication
falls back to a normalized title (lowercased, punctuation stripped). The first
occurrence is kept.

## How DOI and stable URL verification are recorded

Each normalized record stores its DOI and a URL (DOI-resolver or landing page)
plus a verification_status field. At the automated stage every record is marked
verification_status = unverified_auto. A DOI or stable URL is only considered
verified after a human confirms it resolves to the correct publisher record;
that promotion happens during manual review, not here.

## How A_direct_overlap candidates are identified

A record is flagged A_direct_overlap_candidate only when keyword triage detects
ALL of: Chinese population signal, an opportunity/risk signal, at least two
settlement-environment modules (housing, transit, service, disaster, arrival
infrastructure), and a Tokyo/Japan signal. This is a deliberately strict
preliminary filter to surface the items most likely to threaten the gap.

## Why automated classification is only preliminary

Keyword triage matches surface strings in titles and venues. It cannot read
abstracts in context, cannot judge study design, and will both over-flag
(false positives) and miss (false negatives). The preliminary_overlap_category
is a triage hint to order human effort, not a finding.

## Why final gap confirmation requires manual deep reading

Only a human reading the full text can determine whether a paper genuinely
integrates the Chinese-resident opportunity-risk framing in Metropolitan Tokyo.
Final gap confirmation requires: manual DOI/publisher verification, SciSpace or
full-text deep reading of all A and B candidates, explicit positioning against
Sun 2026, and entry into literature_matrix.csv and gap_verification_matrix.csv.
