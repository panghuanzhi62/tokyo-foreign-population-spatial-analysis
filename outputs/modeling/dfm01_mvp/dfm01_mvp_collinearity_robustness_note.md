# DF_M01 MVP - Collinearity Robustness Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
All HC3 robust SEs; complete-case N=218 for every spec. commercial_density and
population_density already enter as z of log1p; raw commercial skew 4.72, log_commercial
skew -0.13 (logging already removes the skew, so winsorizing changes little).

## Specifications
- baseline: full controls.
- A: drop population_density (collinear with commercial_density).
- B: drop commercial_density except in Model 3 (its focal moderator).
- C: residualized commercial = resid(log_commercial_density ~ population_density + pref FE),
  used in the Model 3 interaction.
- D: winsorized log_commercial (1/99 pct) then z.

## Focal coefficients (coef, p)

Model 1 (X -> M, z_log_chinese_stock_2023_12):
- baseline 0.427, p<0.001 ; A 0.254, p=0.077 ; B 0.400, p=0.002 ; C 0.427, p<0.001 ;
  D 0.423, p<0.001.
- Robust and positive in 4 of 5 specs; attenuates to marginal only when population_density
  is dropped (A), indicating the X->M magnitude is partly shared with population density.

Model 2 (M -> Y, z_log_service_2024_12):
- baseline 0.013, p=0.17 ; A 0.002, p=0.76 ; B 0.011, p=0.11 ; C 0.013, p=0.17 ;
  D 0.012, p=0.16.
- STABLY NULL across every specification.

Model 3 (X x commercial_density interaction):
- baseline 0.106, p=0.040 ; A 0.329, p<0.001 ; B 0.106, p=0.040 ; C (resid) 0.145,
  p=0.006 ; D (winsor) 0.098, p=0.071.
- Positive in all specs; significant in baseline/A/B/C (and STRENGTHENS under reduced
  collinearity A and residualization C); only marginal under winsorization D. Survives
  reduced-collinearity specifications.

Model 4 (M x housing_cost interaction):
- baseline -0.008, p=0.27 ; A -0.009, p=0.063 ; B -0.006, p=0.39 ; C -0.008, p=0.27 ;
  D -0.008, p=0.27.
- Stably null (one marginal under A); not a robust effect.

## Conclusion
- X -> M: robust positive (mildly sensitive to dropping population_density).
- M -> Y: robustly null.
- Model 3 interaction: survives reduced-collinearity (PARTIAL/robust; marginal only under
  winsorization).
- Model 4 interaction: robustly null.
High baseline VIFs (commercial 21.8, population_density 12.0) inflate SEs but do not overturn
the qualitative pattern: the reduced-collinearity specs A and C make the Model 3 interaction
clearer, not weaker.
