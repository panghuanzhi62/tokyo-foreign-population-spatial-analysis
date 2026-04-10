from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from mgwr.gwr import MGWR
from mgwr.sel_bw import Sel_BW


def load_mgwr_ready_features(path: str | Path) -> gpd.GeoDataFrame:
    """Read the GeoJSON used as input for the MGWR notebook."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"MGWR input file not found: {path}")

    return gpd.read_file(path)


def prepare_mgwr_inputs(
    gdf: gpd.GeoDataFrame,
    response_col: str = "foreign_ratio",
    predictor_cols: tuple[str, ...] = (
        "log_dist_to_station_m",
        "log_median_land_price_jpy",
    ),
    centroid_col: str = "centroid",
) -> tuple[gpd.GeoDataFrame, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Prepare centroid column, coords, y, X, and predictor moments for MGWR."""
    required_cols = [response_col, *predictor_cols, "geometry"]
    missing = [col for col in required_cols if col not in gdf.columns]
    if missing:
        raise KeyError(f"Missing required columns for MGWR prep: {missing}")

    if gdf.crs is None:
        raise ValueError(
            "Input GeoDataFrame has no CRS. MGWR prep expects projected geometries."
        )

    out = gdf.copy()

    numeric_cols = [response_col, *predictor_cols]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out.dropna(subset=numeric_cols).copy()

    out[centroid_col] = out.geometry.centroid

    coords = np.array([(geom.x, geom.y) for geom in out[centroid_col]])
    y = out[response_col].to_numpy().reshape((-1, 1))
    X = out[list(predictor_cols)].to_numpy()

    X_mean = X.mean(axis=0)
    X_std = X.std(axis=0)

    if np.any(X_std == 0):
        zero_std_cols = [
            predictor_cols[i] for i, std in enumerate(X_std) if std == 0
        ]
        raise ValueError(
            f"Predictor columns have zero standard deviation: {zero_std_cols}"
        )

    return out, coords, y, X, X_mean, X_std


def standardize_predictors(
    X: np.ndarray,
    X_mean: np.ndarray,
    X_std: np.ndarray,
) -> np.ndarray:
    """Standardize predictor matrix using supplied mean and std."""
    return (X - X_mean) / X_std


def fit_mgwr_with_bandwidth_search(
    coords: np.ndarray,
    y: np.ndarray,
    X_scaled: np.ndarray,
    multi: bool = True,
):
    """Run MGWR bandwidth selection and fit the model.

    Returns
    -------
    selector
        Fitted Sel_BW selector object.
    bw
        Selected bandwidth output from selector.search().
    mgwr_model
        MGWR model object.
    mgwr_results
        Fitted MGWR results object.
    """
    selector = Sel_BW(coords, y, X_scaled, multi=multi)
    bw = selector.search()

    mgwr_model = MGWR(coords, y, X_scaled, selector=selector)
    mgwr_results = mgwr_model.fit()

    return selector, bw, mgwr_model, mgwr_results