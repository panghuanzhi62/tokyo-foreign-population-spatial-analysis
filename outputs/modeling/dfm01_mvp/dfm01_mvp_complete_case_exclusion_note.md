# DF_M01 MVP - Complete-Case Exclusion Audit Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26

## Summary

The full-specification complete-case sample is N=218; 33 municipalities are excluded.
Binding constraint: housing_cost (all 33 excluded lack housing; 24 of them also lack rail;
0 lack rail only). See dfm01_mvp_complete_case_exclusion_audit.csv.

## Included (218) vs excluded (33), medians

- Chinese stock 2023-12: 808 vs 10
- DF_M01 support count 2024-12: 5 vs 0
- population 2024: 131,321 vs 6,968
- commercial_density: 127 vs 9
- population_density: 4,774 vs 157
- non-Chinese foreign stock: 1,766 vs 71
- area_km2: 30.8 vs 46.3 (excluded are larger and far less dense)

Prefecture composition of the 33 excluded: Chiba 20, Tokyo 11, Saitama 2, Kanagawa 0.

## Answers

- Are excluded municipalities mostly peripheral islands/towns/villages? YES. They are the
  Tokyo islands and mountain villages (Hinohara, Okutama, Izu/Ogasawara), the Chiba Boso/
  eastern towns and small cities, and two Saitama Chichibu-area towns/villages. They are
  systematically tiny, rural, low-density, with near-zero Chinese stock and growth.
- Does the 218-case model represent mainland populated Greater Tokyo? YES. With Kanagawa
  fully retained and only peripheral Chiba/Tokyo/Saitama units dropped, the estimand is the
  populated mainland core of Greater Tokyo.
- Is complete-case modeling defensible? YES, with a stated caveat. The excluded units carry
  almost no information about the X-M-Y process (near-zero Chinese stock/growth and almost
  no DF_M01 service), so their exclusion does not distort the core relationships; but the
  exclusion is NON-RANDOM (driven by missing housing/rail controls in peripheral areas), so
  generalization is limited to populated mainland municipalities.
- Manuscript estimand wording: YES - describe it as "mainland/populated Greater Tokyo
  municipalities with complete housing and rail controls (N=218)", not "all 251".
