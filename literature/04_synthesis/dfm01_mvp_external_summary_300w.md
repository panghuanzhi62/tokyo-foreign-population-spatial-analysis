# DF_M01 MVP - External Summary (approx. 300 words)

This project uses public official Japanese data to study how institutional migrant-support
infrastructure relates to Chinese registered-resident population dynamics across metropolitan
(Greater) Tokyo: the municipalities of Tokyo, Saitama, Chiba, and Kanagawa. The analysis is
fully reproducible from government sources (Immigration Services Agency / Ministry of Justice
registered-resident statistics, the registry of registered support organizations, the 2021
Economic Census, posted land prices, rail-network and municipal-boundary geographies, and the
Basic Resident Register).

We examine a temporally ordered design. The exposure is the Chinese registered stock in
December 2023; the service variable (DF_M01) is the municipality count of registered support
organizations observable by 2024; the outcome is the change in Chinese registered stock from
December 2024 to June 2025. Models adjust for rail accessibility, housing cost, commercial
density, population density, non-Chinese foreign stock, and prefecture fixed effects. The
complete-case sample is 218 municipalities, interpretable as the mainland populated core of
Greater Tokyo with complete housing and rail controls; small peripheral and island units are
excluded by missing controls.

Two patterns are robust. First, prior Chinese population is strongly associated with the
presence of institutional support organizations, particularly in commercially dense
municipalities. Second, this support infrastructure does not robustly predict short-term
subsequent Chinese registered-stock growth. The second (null) result is stable across
collinearity diagnostics, alternative service scalings, alternative timing windows, and
explicit spatial-dependence models (SLX, spatial-error, and spatial-lag, under two spatial
weighting schemes). Residual spatial dependence is negative, suggesting local dispersion rather
than clustering.

We interpret these as temporally ordered associations, not causal effects, and we make no
mediation claim. The evidence is consistent with support infrastructure following existing
population rather than driving its short-term growth. The support measure is institutional and
not China-specific, and the outcome window is short; these are stated limitations.
