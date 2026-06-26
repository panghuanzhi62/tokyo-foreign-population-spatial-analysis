# DF_M01 MVP - Alternative M Scaling Diagnostics Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Diagnostics only - NOT a replacement main model. HC3; complete-case N=218.

## Purpose
Test whether the null M -> Y result (Model 2) depends on how the DF_M01 service variable is
scaled. Diagnostic Model 2: chinese_growth_2024_12_2025_06 ~ alt_service +
z_log_chinese_stock_2023_12 + full controls + prefecture FE.

## Denominator-endogeneity caveat
Per-capita / per-foreigner service intensity uses a denominator (population or foreign stock)
that is itself part of the X-M-Y process; such scalings are reported as diagnostics only and
must NOT be promoted to the primary M without addressing denominator endogeneity.

## Results (z_alt_service coef, p)
- service_count_raw (z): -0.0002, p=0.96 (null)
- log1p_service_count (z; = baseline M): 0.013, p=0.17 (null)
- service_per_10000_foreigners (z; foreigners = Chinese 2023 + non-Chinese 2020 census):
  0.001, p=0.90 (null)
- service_per_10000_total_population (z; pop 2024): -0.002, p=0.78 (null)

## Conclusion
The M -> Y null is INVARIANT to service scaling (raw count, log count, per-10k foreigners,
per-10k population): none is associated with subsequent Chinese-stock growth. The null is a
property of the data, not an artifact of the log-count parameterization.
