from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd
from esda.moran import Moran, Moran_Local
from libpysal.weights import Queen


def load_residual_features(path: str | Path) -> gpd.GeoDataFrame:
    """Read the OLS-output GeoJSON used by spatial residual diagnostics."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Residual diagnostics input file not found: {path}")

    return gpd.read_file(path)


def prepare_residual_diagnostics_gdf(
    gdf: gpd.GeoDataFrame,
    resid_col: str = "ols_resid",
) -> gpd.GeoDataFrame:
    """Coerce residual column to numeric while preserving notebook workflow."""
    if resid_col not in gdf.columns:
        raise KeyError(f"Residual column not found: {resid_col}")

    out = gdf.copy()
    out[resid_col] = pd.to_numeric(out[resid_col], errors="coerce")
    return out


def build_queen_weights(gdf: gpd.GeoDataFrame):
    """Build row-standardized Queen contiguity weights."""
    w = Queen.from_dataframe(gdf)
    w.transform = "r"
    return w


def compute_global_moran(
    gdf: gpd.GeoDataFrame,
    weights,
    resid_col: str = "ols_resid",
):
    """Compute global Moran's I for the specified residual column."""
    if resid_col not in gdf.columns:
        raise KeyError(f"Residual column not found: {resid_col}")

    return Moran(gdf[resid_col], weights)


def compute_local_moran(
    gdf: gpd.GeoDataFrame,
    weights,
    resid_col: str = "ols_resid",
):
    """Compute Local Moran statistics for the specified residual column."""
    if resid_col not in gdf.columns:
        raise KeyError(f"Residual column not found: {resid_col}")

    return Moran_Local(gdf[resid_col], weights)


def attach_lisa_results_and_clusters(
    gdf: gpd.GeoDataFrame,
    lisa,
    p_threshold: float = 0.05,
    lisa_i_col: str = "lisa_I",
    lisa_p_col: str = "lisa_p",
    lisa_q_col: str = "lisa_q",
    lisa_sig_col: str = "lisa_sig",
    lisa_cluster_col: str = "lisa_cluster",
) -> gpd.GeoDataFrame:
    """Attach local Moran outputs and assign standard LISA cluster labels."""
    out = gdf.copy()

    out[lisa_i_col] = lisa.Is
    out[lisa_p_col] = lisa.p_sim
    out[lisa_q_col] = lisa.q

    out[lisa_sig_col] = out[lisa_p_col] < p_threshold
    out[lisa_cluster_col] = "Not significant"

    out.loc[(out[lisa_q_col] == 1) & (out[lisa_sig_col]), lisa_cluster_col] = "High-High"
    out.loc[(out[lisa_q_col] == 2) & (out[lisa_sig_col]), lisa_cluster_col] = "Low-High"
    out.loc[(out[lisa_q_col] == 3) & (out[lisa_sig_col]), lisa_cluster_col] = "Low-Low"
    out.loc[(out[lisa_q_col] == 4) & (out[lisa_sig_col]), lisa_cluster_col] = "High-Low"

    return out


def prepare_mgwr_ready_gdf(
    gdf: gpd.GeoDataFrame,
    keep_cols: tuple[str, ...] = (
        "N03_007",
        "N03_001",
        "N03_004",
        "N03_005",
        "foreign_ratio",
        "log_dist_to_station_m",
        "log_median_land_price_jpy",
        "ols_resid",
        "lisa_cluster",
        "geometry",
    ),
) -> gpd.GeoDataFrame:
    """Prepare the minimal GeoDataFrame exported for the MGWR notebook."""
    missing = [col for col in keep_cols if col not in gdf.columns]
    if missing:
        raise KeyError(f"Missing required columns for MGWR export: {missing}")

    return gdf[list(keep_cols)].copy()