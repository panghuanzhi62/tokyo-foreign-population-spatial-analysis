from __future__ import annotations

from pathlib import Path

import geopandas as gpd


def read_boundary_file(path: str | Path) -> gpd.GeoDataFrame:
    """Read a boundary file into a GeoDataFrame."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Boundary file not found: {path}")

    return gpd.read_file(path)


def ensure_crs(
    gdf: gpd.GeoDataFrame,
    target_crs: str | int | None = None,
) -> gpd.GeoDataFrame:
    """Return a GeoDataFrame in the requested CRS."""
    if target_crs is None:
        return gdf

    if gdf.crs is None:
        raise ValueError(
            "Input GeoDataFrame has no CRS; cannot safely reproject. "
            "Set CRS explicitly before calling ensure_crs()."
        )

    if str(gdf.crs) == str(target_crs):
        return gdf

    return gdf.to_crs(target_crs)


def load_boundaries(
    path: str | Path,
    target_crs: str | int | None = None,
) -> gpd.GeoDataFrame:
    """Read boundary data and optionally project to a target CRS."""
    gdf = read_boundary_file(path)
    gdf = ensure_crs(gdf, target_crs=target_crs)
    return gdf


def project_gdf(
    gdf: gpd.GeoDataFrame,
    epsg: int,
) -> gpd.GeoDataFrame:
    """Project a GeoDataFrame to a target EPSG code."""
    if gdf.crs is None:
        raise ValueError(
            "Input GeoDataFrame has no CRS; cannot safely project."
        )

    target_crs = f"EPSG:{epsg}"
    if str(gdf.crs) == target_crs:
        return gdf

    return gdf.to_crs(epsg=epsg)