# Spatial Concentration and Heterogeneous Mechanisms of Foreign Population Distribution in the Tokyo Metropolitan Mainland Area

## Overview

This project examines the spatial concentration of foreign population in the Tokyo metropolitan mainland area using official Japanese spatial and statistical data. It integrates administrative boundaries, foreign population attributes, railway station accessibility, and residential land-price data into a municipal-level spatial dataset.

This repository presents a compact academic portfolio relevant to urban environment, environmental geography, land-related spatial interpretation, and place-based analysis in metropolitan Japan.

The analysis combines global and local spatial methods, including OLS, Moran’s I, LISA, and MGWR, in order to identify:
- whether foreign population concentration is spatially clustered,
- how it is associated with railway accessibility and residential land price,
- and whether these relationships vary across municipalities.

It is intended as a concise research portfolio for applications in urban geography, environmental geography, spatial data science, and migration-related spatial analysis.

## Research Questions

1. Is foreign population concentration spatially clustered in the Tokyo metropolitan mainland area?
2. How are foreign population ratios associated with railway accessibility and residential land price?
3. Do these relationships remain constant across space, or do they vary locally?

## Study Area

The study focuses on the mainland part of the Tokyo metropolitan area, covering Tokyo and surrounding municipalities in the wider metropolitan belt. Outlying islands were excluded in order to avoid distortion in accessibility and distance-based measures.

## Data

This project integrates the following categories of data:

- Administrative boundary data
- Foreign population statistics
- Railway station data
- Official residential land-price data

A separate file, `data/data_sources.md`, documents the datasets and their roles in the workflow.

## Methods

The analytical workflow consists of the following stages:

1. Administrative boundary processing
2. Population attribute merging
3. Station accessibility feature engineering
4. Exploratory spatial data analysis
5. Residential land-price integration
6. Baseline OLS modeling
7. Spatial residual diagnostics using Moran’s I and LISA
8. MGWR estimation for local spatial heterogeneity

## Main Findings

The current results show that:

- Foreign population concentration is spatially clustered rather than randomly distributed.
- Baseline OLS captures a meaningful global relationship, but leaves significant spatial structure unexplained.
- OLS residuals show statistically significant positive spatial autocorrelation.
- MGWR reveals substantial local heterogeneity in the effects of station accessibility and residential land price.

These findings suggest that foreign population concentration in metropolitan Japan cannot be understood through a single global mechanism. Instead, it is shaped by spatially differentiated combinations of accessibility, land value, and local urban context.

## Repository Structure

```text
.
├─ README.md
├─ requirements.txt
├─ data/
│  ├─ raw/
│  ├─ processed/
│  └─ data_sources.md
├─ notebooks/
│  ├─ 00_project_setup.ipynb
│  ├─ 01_boundary_processing.ipynb
│  ├─ 02_population_merge.ipynb
│  ├─ 03_station_accessibility.ipynb
│  ├─ 04_exploratory_analysis.ipynb
│  ├─ 05_land_price_processing.ipynb
│  ├─ 06_baseline_ols.ipynb
│  ├─ 07_spatial_residual_diagnostics.ipynb
│  └─ 08_mgwr_analysis.ipynb
├─ outputs/
│  ├─ figures/
│  └─ tables/
└─ docs/
   ├─ research_summary_en.pdf
   ├─ future_research_plan_en.pdf
   ├─ cv_en.pdf
   └─ project_brief_en.pdf