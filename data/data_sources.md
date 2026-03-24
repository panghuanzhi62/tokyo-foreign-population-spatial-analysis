
---

## 2) `data/data_sources.md`

```markdown
# Data Sources

This file documents the main datasets used in this project and their analytical roles.

## 1. Administrative Boundary Data

### Dataset
Japanese administrative boundary data (municipal-level boundary shapefiles / geojson)

### Role
Used to define the spatial units of analysis and construct the study area for the Tokyo metropolitan mainland region.

### Use in this project
- reading municipal boundaries,
- filtering the metropolitan study area,
- excluding outlying islands when necessary,
- linking statistical attributes to polygon geometry.

---

## 2. Foreign Population Statistics

### Dataset
Municipal-level foreign population statistics

### Role
Used to construct the dependent variable: foreign population ratio.

### Use in this project
- merging population attributes with administrative boundaries,
- calculating foreign population ratio,
- supporting exploratory and regression-based analysis.

### Notes
Population attributes were cleaned and merged using administrative codes. Particular attention was paid to code formatting and matching consistency.

---

## 3. Railway Station Data

### Dataset
Official railway station spatial data

### Role
Used to construct transport accessibility indicators.

### Use in this project
- reading station locations,
- projecting data into an appropriate planar CRS,
- computing municipal centroid-to-nearest-station distance,
- generating the station accessibility variable.

### Notes
Distance was calculated in meters after coordinate transformation into a projected CRS suitable for the Tokyo metropolitan area.

---

## 4. Residential Land-Price Data

### Dataset
Official land-price data for Tokyo and surrounding prefectures

### Role
Used to construct a municipal-level housing/land value indicator.

### Use in this project
- reading point-based land-price data,
- filtering residential-use observations,
- spatially joining land-price points to municipal polygons,
- calculating median residential land price for each municipality.

### Notes
The median was used instead of the mean in order to reduce the effect of extreme values.

---

## 5. Derived Variables

### Foreign population ratio
Dependent variable representing the share of foreign population in each municipality.

### Distance to nearest station
Accessibility proxy based on centroid-to-nearest-station distance.

### Log distance to station
Log-transformed version of station accessibility for regression analysis.

### Median residential land price
Municipal-level residential land-price indicator.

### Log median residential land price
Log-transformed version of land price for regression analysis.

---

## 6. Analytical Outputs

The integrated dataset supports:

- thematic mapping,
- exploratory data analysis,
- OLS regression,
- residual spatial diagnostics,
- and MGWR-based local coefficient estimation.

---

## 7. Data Management Note

To keep the repository lightweight and reproducible, raw files may not always be re-uploaded directly. Instead, the repository documents:
- file structure,
- source categories,
- and processing steps,
so that the workflow can be reconstructed from the original official sources.