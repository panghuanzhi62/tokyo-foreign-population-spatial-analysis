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
        raise ValueError("Input GeoDataFrame has no CRS; cannot safely project.")

    target_crs = f"EPSG:{epsg}"
    if str(gdf.crs) == target_crs:
        return gdf

    return gdf.to_crs(epsg=epsg)


def filter_tokyo_metro_by_prefecture(
    gdf: gpd.GeoDataFrame,
    prefectures: list[str],
    prefecture_col: str = "N03_001",
) -> gpd.GeoDataFrame:
    """Filter boundary polygons to the specified prefectures."""
    if prefecture_col not in gdf.columns:
        raise KeyError(f"Column not found: {prefecture_col}")

    return gdf[gdf[prefecture_col].isin(prefectures)].copy()


def clip_mainland_bbox(
    gdf: gpd.GeoDataFrame,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> gpd.GeoDataFrame:
    """Slice a GeoDataFrame by bounding box using GeoPandas .cx."""
    return gdf.cx[xmin:xmax, ymin:ymax].copy()


def select_case_areas_by_keywords(
    gdf: gpd.GeoDataFrame,
    keywords_pattern: str = "川口|江戸川",
    col_primary: str = "N03_004",
    col_secondary: str = "N03_005",
) -> gpd.GeoDataFrame:
    """Select case areas by keyword matching across two name columns."""
    missing = [col for col in [col_primary, col_secondary] if col not in gdf.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    mask = gdf[col_primary].astype(str).str.contains(keywords_pattern, na=False) | gdf[
        col_secondary
    ].astype(str).str.contains(keywords_pattern, na=False)

    return gdf[mask].copy()
