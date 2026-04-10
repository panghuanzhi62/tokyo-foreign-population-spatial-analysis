# Spatial Concentration and Heterogeneous Mechanisms of Foreign Population Distribution in the Tokyo Metropolitan Mainland Area

This repository examines whether foreign population concentration in the Tokyo metropolitan mainland area is spatially clustered, and whether its association with railway accessibility and residential land price is globally stable or locally heterogeneous. The project is organized as a notebook-centered spatial analysis workflow with reusable helpers under `src/tokyo_foreigners/`.

## Research focus

This project asks three linked questions:

1. Is foreign population concentration spatially clustered across municipalities in the Tokyo metropolitan mainland area?
2. How is foreign population concentration associated with station accessibility and residential land price?
3. Are these relationships globally stable, or do they vary locally across municipalities?

## Study area

The study focuses on the mainland part of the Tokyo metropolitan area. Outlying islands are excluded to avoid distortion in distance-based and accessibility-based measures.

## Data

The repository integrates municipal-scale spatial and statistical data from official Japanese sources, including:

- administrative boundaries
- foreign population statistics
- railway station data
- official residential land-price data

Current project convention:

- `data_raw/` is the canonical raw-data directory
- `data_processed/` stores intermediate and derived datasets used in later analysis stages

## Analytical workflow

The core workflow is organized across notebooks `00` to `08`:

- `00_project_setup.ipynb`  
  Project setup, path checks, and environment validation

- `01_boundary_processing.ipynb`  
  Administrative boundary preparation and case-area filtering

- `02_population_merge.ipynb`  
  Merge foreign population attributes into municipal boundaries

- `03_station_accessibility.ipynb`  
  Railway station accessibility feature engineering

- `04_exploratory_analysis.ipynb`  
  Exploratory spatial data analysis

- `05_land_price_processing.ipynb`  
  Residential land-price data preparation and integration

- `06_baseline_ols.ipynb`  
  Baseline global regression modeling

- `07_spatial_residual_diagnostics.ipynb`  
  Moran’s I and LISA residual diagnostics

- `08_mgwr_analysis.ipynb`  
  MGWR estimation and local interpretation

## Current repository structure

```text
.
├── data/
├── data_processed/
├── data_raw/
├── docs/
├── notebooks/
│   ├── 00_project_setup.ipynb
│   ├── 01_boundary_processing.ipynb
│   ├── 02_population_merge.ipynb
│   ├── 03_station_accessibility.ipynb
│   ├── 04_exploratory_analysis.ipynb
│   ├── 05_land_price_processing.ipynb
│   ├── 06_baseline_ols.ipynb
│   ├── 07_spatial_residual_diagnostics.ipynb
│   └── 08_mgwr_analysis.ipynb
├── outputs/
│   ├── figures/
│   ├── html/
│   ├── maps/
│   └── tables/
├── scripts/
├── src/
│   └── tokyo_foreigners/
│       ├── __init__.py
│       ├── boundaries.py
│       ├── land_price.py
│       ├── mgwr.py
│       ├── ols.py
│       ├── paths.py
│       ├── spatial_diagnostics.py
│       └── station_accessibility.py
├── pyproject.toml
├── uv.lock
├── requirements.txt
└── README.md