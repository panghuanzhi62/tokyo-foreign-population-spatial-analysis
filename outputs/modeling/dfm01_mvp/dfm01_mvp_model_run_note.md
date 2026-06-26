# DF_M01 MVP Model Run Note

Panel: tokyo_china_dfm01_mvp_model_panel_local_only.csv ; complete-case N (primary) = 218/251 ; robustness = 218/251.
OLS with HC3 robust standard errors. NOT causal mediation; temporally ordered,
mechanism-consistent associations only.

Controls: rail accessibility, housing cost (log land price), commercial density
(z of log1p 2021 Economic Census establishments/area), population density (z of log1p
2024 BRR pop/area), non-Chinese foreign stock (z of log1p), prefecture fixed effects.

Complete-case excludes 33 peripheral municipalities (Tokyo islands/mountain, Chiba Boso,
Saitama Chichibu) that lack v5 rail/housing; see missingness summary. Estimand is
therefore mainland populated Greater Tokyo, not all 251.

Model 2 (Y growth ~ service + X + controls): service coef 0.0125 (p=0.1676), adj R2 0.0195, n 218.
