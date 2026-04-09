from __future__ import annotations

from pathlib import Path

import geopandas as gpd


def load_population_features(path: str | Path) -> gpd.GeoDataFrame:
    """Read the municipal population-feature GeoJSON."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Population feature file not found: {path}")

    return gpd.read_file(path)


def load_station_points(
    path: str | Path,
    encoding: str | None = None,
) -> gpd.GeoDataFrame:
    """Read station point data from a shapefile."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Station file not found: {path}")

    if encoding is None:
        return gpd.read_file(path)

    return gpd.read_file(path, encoding=encoding)


def add_centroid_column(
    gdf: gpd.GeoDataFrame,
    centroid_col: str = "centroid",
) -> gpd.GeoDataFrame:
    """Return a copy of the GeoDataFrame with a centroid column added."""
    if gdf.crs is None:
        raise ValueError(
            "Input GeoDataFrame has no CRS; centroid computation should be done "
            "after projecting to a suitable CRS."
        )

    out = gdf.copy()
    out[centroid_col] = out.geometry.centroid
    return out


def make_centroid_gdf(
    gdf: gpd.GeoDataFrame,
    centroid_col: str = "centroid",
) -> gpd.GeoDataFrame:
    """Return a centroid-geometry GeoDataFrame from an existing centroid column."""
    if centroid_col not in gdf.columns:
        raise KeyError(f"Centroid column not found: {centroid_col}")

    out = gdf.copy()
    out = out.set_geometry(centroid_col)
    return out