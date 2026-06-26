# DF_M01 MVP - Residual Spatial Autocorrelation Check Note

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26

## Status: NOT RUN - no compatible existing weights found

A search for an existing spatial-weights file or prior Moran's I workflow returned:
- src/tokyo_foreigners/spatial_diagnostics.py (a module)
- notebooks/07_spatial_residual_diagnostics.ipynb
- outputs/figures/lisa_cluster_map.png

No serialized spatial-weights file (.gal / .gwt / .npz / .pkl) compatible with the current
251 / 218 ISA-MOJ municipality frame was found. The existing module/notebook target the
earlier Tokyo-only N03 feature frame (different unit set and keys), so they are not directly
usable for the 218 complete-case municipalities here.

Per task scope, new spatial weights are NOT created in this task. Residual Moran's I for
primary Model 2, primary Model 4, and the best reduced-collinearity Model 2/Model 4 is
therefore deferred.

## Recommended follow-up (separate approved step)
Build queen-contiguity weights for the 218 complete-case municipalities from the
N03-20250101 boundary (already local), then compute residual Moran's I for Models 2 and 4
(primary and reduced-collinearity). Until then, spatial autocorrelation in the growth (Y)
residuals is UNVERIFIED; the null M -> Y result should be read with that caveat.
