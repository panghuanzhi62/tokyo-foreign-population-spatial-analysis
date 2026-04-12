from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd
import statsmodels.api as sm


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


def build_ols_design(
    model_df: pd.DataFrame,
    response_col: str = "foreign_ratio",
    predictor_cols: tuple[str, ...] = (
        "log_dist_to_station_m",
        "log_median_land_price_jpy",
    ),
    add_constant: bool = True,
) -> tuple[pd.DataFrame, pd.Series]:
    """Build X and y for baseline OLS."""
    missing = [col for col in [response_col, *predictor_cols] if col not in model_df.columns]
    if missing:
        raise KeyError(f"Missing required columns for OLS design: {missing}")

    X = model_df[list(predictor_cols)].copy()
    y = model_df[response_col].copy()

    if add_constant:
        X = sm.add_constant(X)

    return X, y


def fit_baseline_ols(
    model_df: pd.DataFrame,
    response_col: str = "foreign_ratio",
    predictor_cols: tuple[str, ...] = (
        "log_dist_to_station_m",
        "log_median_land_price_jpy",
    ),
    add_constant: bool = True,
):
    """Fit baseline OLS and return model, X, y."""
    X, y = build_ols_design(
        model_df,
        response_col=response_col,
        predictor_cols=predictor_cols,
        add_constant=add_constant,
    )

    ols_model = sm.OLS(y, X).fit()
    return ols_model, X, y
