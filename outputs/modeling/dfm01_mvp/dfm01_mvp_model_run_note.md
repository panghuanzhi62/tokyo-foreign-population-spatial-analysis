# DF_M01 MVP Model Run Note - MISSING-INPUT STOP

Panel: tokyo_china_dfm01_mvp_model_panel_local_only.csv (251 municipality rows)

Status: MODELS NOT FITTED.

Reason: the MVP design requires a fixed control set, and the following
required controls are not available as processed, municipality-level fields
for the 251 Greater Tokyo frame. Per the task design, proxies must NOT be
invented and geocoding is not permitted in this task, so no model is fitted.

Missing required controls:
- rail_accessibility
- housing_cost
- commercial_density
- population_density

Models 3 and 4 additionally depend on commercial_density and housing_cost
respectively, so the interaction models cannot be specified at all.

Available inputs (X, Y, M=DF_M01, non_chinese_foreign_stock, prefecture FE)
are assembled in the local-only panel and itemized in
outputs/modeling/dfm01_mvp/model_readiness_inventory.csv.

Shortest next action: build a local-only, processed, municipality-level
controls table for the 251 frame (population_density, housing_cost/land_price,
rail_accessibility from the existing GIS layers, plus commercial_density via
economic-census acquisition) in a separate approved step, then re-run.
