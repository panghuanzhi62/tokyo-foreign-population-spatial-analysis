# Project Brief

## Title
Spatial Concentration and Heterogeneous Mechanisms of Foreign Population Distribution in the Tokyo Metropolitan Mainland Area

## Project Summary
This project investigates how foreign population concentration is distributed across the Tokyo metropolitan mainland area and how it is shaped by transport accessibility and residential land value.

Using official Japanese spatial and statistical data, I constructed a municipal-level spatial dataset integrating administrative boundaries, foreign population attributes, railway station accessibility, and residential land-price information. The analytical workflow combines OLS, spatial residual diagnostics, and MGWR in order to move from global association to local spatial heterogeneity.

## Research Motivation
Foreign population concentration in metropolitan Japan is relevant not only to migration studies, but also to urban governance, labor mobility, housing, accessibility, and place-based public policy. Rather than assuming a single metropolitan process, this project asks whether different municipalities follow different socio-spatial mechanisms.

## Methods
The project proceeds through the following stages:

1. Administrative boundary processing
2. Population attribute merging
3. Nearest-station accessibility calculation
4. Exploratory spatial analysis
5. Residential land-price integration
6. Baseline OLS modeling
7. Spatial residual diagnostics using Moran’s I and LISA
8. MGWR estimation

## Main Results
The current results show that foreign population concentration is spatially clustered rather than randomly distributed.

The baseline OLS model identifies:
- a negative association between foreign population ratio and distance to the nearest station,
- and a positive association between foreign population ratio and residential land price.

However, significant spatial autocorrelation remains in the OLS residuals, indicating that the global model is incomplete.

The MGWR results show that the effects of station accessibility and residential land price vary substantially across municipalities. This suggests that foreign population concentration in metropolitan Japan is shaped by spatially differentiated combinations of accessibility, land value, and local urban context.

## Relevance to Urban and Environmental Geography
This project is relevant to urban environment and environmental geography in three ways.

First, it provides a spatially explicit interpretation of urban differentiation within a major metropolitan system.

Second, it links land-related conditions and transport accessibility to socio-spatial concentration patterns.

Third, it demonstrates how spatial data science and spatial econometric methods can be applied to policy-relevant urban questions using official Japanese data.

## Technical Strengths Demonstrated
- GeoPandas-based spatial data integration
- Official Japanese spatial data handling
- Distance-based accessibility feature engineering
- OLS and regression diagnostics
- Moran’s I and LISA
- MGWR for local spatial heterogeneity
- Map-based interpretation for place-based analysis

## Future Extensions
Planned extensions include:
- comparison with Chinese-population-specific proxies,
- broader metropolitan and inter-regional comparison,
- additional explanatory variables related to labor and housing,
- and future predictive or scenario-based spatial modeling.

## Author
Jun Li, Ph.D.  
Human Geography / GIS / Spatial Econometrics / Spatial Data Science