# Tokyo Foreign Population Spatial Analysis Project

## Project objective
Build a reproducible municipal-level geospatial research pipeline for analyzing the spatial concentration of foreign population in the Tokyo metropolitan mainland area and its determinants.

## Current analytical baseline
The current explanatory workflow must be preserved unless explicitly asked otherwise:

1. Descriptive statistics and exploratory checks
2. OLS baseline model
3. Residual Moran's I
4. LISA / local cluster diagnostics
5. MGWR for local spatial heterogeneity

Do not remove this explanatory workflow when adding predictive layers.

## Research framing
This is not a generic data-science demo project.
It is a research-engineering repository intended to support:
- geospatial data integration from official Japanese sources
- municipal-level feature engineering
- spatial diagnostics
- interpretable explanatory modelling
- later predictive modelling with spatial cross-validation
- publication-ready outputs and portfolio-ready deliverables

## Data policy
- Prefer official Japanese sources, especially MLIT / 国土数値情報 and e-Stat.
- Never modify files under `data_raw/` or `data/raw/` directly.
- Any cleaned or derived outputs must go to processed/output folders, not back into raw storage.
- Preserve municipality identifiers, CRS assumptions, and documented join keys.
- If a script creates a new derived dataset, also create a short manifest/log note if feasible.

## Coding policy
- Keep reusable logic in Python modules or scripts that can be rerun.
- Avoid hard-coded absolute local paths.
- Keep scripts thin where possible; move reusable logic into structured functions/modules over time.
- Do not silently rewrite unrelated notebooks or outputs.
- Prefer minimal safe patches over broad rewrites.

## Modeling policy
- Baseline explanatory spatial workflow comes first.
- Predictive additions such as XGBoost, SHAP, and spatial CV are a second layer, not a replacement.
- Do not introduce leakage across spatial folds.
- Keep model settings, assumptions, and outputs explicit.

## Output policy
When making meaningful changes, always report:
1. files changed
2. commands run
3. tests or smoke checks run
4. remaining risks
5. recommended next step

## Safe behavior rules
- Ask before making destructive changes.
- Do not delete folders such as `outputs/`, `notebooks/`, `data_raw/`, or `data/raw/`.
- Do not overwrite raw source files.
- Do not invent unavailable data sources.
- If uncertain about a join key, CRS, or administrative code, inspect first and explain.

## Immediate priorities
1. Stabilize project structure for agentic workflow
2. Standardize path handling and raw/processed/output boundaries
3. Preserve and document current Tokyo municipal analysis workflow
4. Prepare for official-data feature expansion
5. Later add spatial CV XGBoost + SHAP
6. Later build a minimal Streamlit demonstration layer