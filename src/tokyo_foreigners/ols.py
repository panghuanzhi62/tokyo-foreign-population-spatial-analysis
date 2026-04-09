from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd


def load_ols_features(path: str | Path) -> gpd.GeoDataFrame:
    """Read the GeoJSON used as input for the baseline OLS notebook."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"OLS input file not found: {path}")

    return gpd.read_file(path)


def prepare_baseline_ols_dataframe(
    gdf: gpd.GeoDataFrame,
    response_col: str = "foreign_ratio",
    predictor_cols: tuple[str, ...] = (
        "log_dist_to_station_m",
        "log_median_land_price_jpy",
    ),
    id_cols: tuple[str, ...] = ("N03_007", "N03_001", "N03_004", "N03_005"),
    geometry_col: str = "geometry",
) -> gpd.GeoDataFrame:
    """Build the cleaned GeoDataFrame used for baseline OLS."""
    required_cols = list(id_cols) + [response_col, *predictor_cols, geometry_col]
    missing = [col for col in required_cols if col not in gdf.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    out = gdf.copy()

    numeric_cols = [response_col, *predictor_cols]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out[required_cols].copy()
    out = out.dropna(subset=numeric_cols).copy()

    return out