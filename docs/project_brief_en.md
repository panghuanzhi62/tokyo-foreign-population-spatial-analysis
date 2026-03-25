# Project Brief

## Tokyo Foreign Population Spatial Analysis Repository

**Repository basis:** current public GitHub README describing a project on the spatial concentration of foreign population in the Tokyo metropolitan mainland area.

**Repository Title:**  
*Spatial Concentration and Heterogeneous Mechanisms of Foreign Population Distribution in the Tokyo Metropolitan Mainland Area*

## 1. Project Objective

This project examines whether foreign population concentration in metropolitan Japan is spatially clustered and whether its association with railway accessibility and residential land price is globally stable or locally variable. The repository presents the work as a compact academic portfolio relevant to urban geography, environmental geography, spatial data science, and migration-related spatial analysis.

## 2. Study Area and Data

- **Study area:** the mainland part of the Tokyo metropolitan area, excluding outlying islands to avoid distortion in accessibility and distance-based measures.
- **Data categories:** administrative boundaries, foreign population statistics, railway station data, and official residential land-price data.
- **Analytical unit:** a municipal-level spatial dataset assembled from official Japanese spatial and statistical sources.

## 3. Analytical Workflow

| Stage | Description |
|------:|-------------|
| 1 | Administrative boundary processing |
| 2 | Population attribute merging |
| 3 | Station accessibility feature engineering |
| 4 | Exploratory spatial data analysis |
| 5 | Residential land-price integration |
| 6 | Baseline OLS modeling |
| 7 | Spatial residual diagnostics using Moran's *I* and LISA |
| 8 | MGWR estimation for local spatial heterogeneity |

## 4. Current Findings

- In municipalities such as Kawaguchi, concentration appears to be supported by near-core accessibility and settlement capacity rather than by low land value alone, suggesting the combined importance of commuting conditions, employment structure, and migrant networks.
- In eastern inner metropolitan areas such as Edogawa, higher land value does not translate into a straightforward negative effect on foreign concentration. This challenges a simple cost-exclusion narrative and points to the importance of rental-market segmentation, service infrastructure, and established settlement effects.
- The identified concentration clusters should therefore be interpreted as land-system units in which demographic concentration, housing conditions, transport dependence, and environmental exposure may overlap. This provides a strong basis for future research linking migrant settlement to flood risk, heat stress, evacuation accessibility, and socio-ecological vulnerability.

## 5. Why this Repository Matters

As a portfolio piece, the repository demonstrates the full chain from data assembly to spatial diagnosis, local modeling, figure production, and structured documentation. Its value is not limited to one empirical case; it also shows methodological readiness for broader work on migration, urban structure, land-related processes, and place-sensitive policy analysis.

## 6. Materials Visible in the Repository

- Notebook-based workflow from project setup through MGWR analysis.
- Output folders for figures and tables, including selected maps shown in the README.
- A `docs` folder listing supporting application materials such as the project brief.

## Repository URL

`https://github.com/panghuanzhi62/tokyo-foreign-population-spatial-analysis`