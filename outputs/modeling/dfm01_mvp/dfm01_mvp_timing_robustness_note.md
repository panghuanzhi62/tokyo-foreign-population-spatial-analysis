# DF_M01 MVP - Timing Robustness Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
HC3; complete-case N=218 in both windows. Source: committed primary/robustness coefficients.

## Windows
- Primary:    M = service registered by 2024-12 ; Y = growth 2024-12 -> 2025-06.
- Robustness: M = service registered by 2024-06 ; Y = growth 2024-06 -> 2025-06.

## X -> M (Model 1, z_log_chinese_stock_2023_12)
- Primary 0.427, p<0.001 ; Robustness 0.441, p<0.001.
- STABLE: prior Chinese stock predicts DF_M01 support-organization infrastructure in both
  windows.

## M -> Y (Model 2, service coefficient)
- Primary z_log_service_2024_12 = 0.013, p=0.17 ; Robustness z_log_service_2024_06 = 0.007,
  p=0.51.
- STABLY NULL in both windows. (The robustness window has a higher overall adj R2 ~0.087 vs
  0.019, driven by controls, not by service.)

## Interactions
- Model 3 (X x commercial): Primary 0.106, p=0.040 ; Robustness 0.124, p=0.020. STABLE
  positive across windows.
- Model 4 (M x housing): Primary -0.008, p=0.27 ; Robustness window null as well. STABLE null.

## Conclusion
Timing choice does not change the qualitative findings: X -> M stable positive, M -> Y stable
null, Model 3 interaction stable positive, Model 4 interaction stable null.
