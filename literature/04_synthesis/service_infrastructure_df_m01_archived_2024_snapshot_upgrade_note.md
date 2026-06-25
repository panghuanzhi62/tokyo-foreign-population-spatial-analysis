# DF_M01 Archived 2024 Snapshot Upgrade Note (B -> A path)

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-25

## Purpose

DF_M01 (registered support organizations) is currently classified B_observable_by_2024_or_2025
because the public registry edition is a CURRENT-active snapshot with per-record registration
dates but NO cancellation/deletion date. A registration-date filter on the current file
therefore undercounts the true 2024 active stock (organizations active in 2024 but cancelled
before the snapshot are absent). This note records how DF_M01 could be upgraded to
A_2024_stock.

## Upgrade path

1. Locate an archived OFFICIAL registry edition dated near 2024-12 (the agency publishes
   periodic editions; dated editions are also independently mirrored, and the Internet Archive
   Wayback Machine may hold the ISA list page or the linked Excel for late 2024).
2. Acquire that archived edition local-only into the same raw folder; record URL, capture date,
   edition as-of date, and SHA256 in metadata only.
3. Re-run the parser against the archived edition to obtain the active-as-of-2024 organization
   set, which directly observes 2024 active stock and resolves right-censoring.
4. Construct true_active_2024_12 counts and compare them to the current-file
   registered_by_2024_12_31 counts; report the difference as a measurement-sensitivity check.
5. If the archived edition is confirmed official and dated, reclassify DF_M01 to A_2024_stock
   for that vintage; otherwise keep B and document the attempt.

## Caution

Only an OFFICIAL or verifiably-faithful archived edition justifies the A upgrade. Third-party
re-postings without a verifiable as-of date remain B. Do not commit any acquired raw edition,
address-level records, or geocoded records.
