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


def nearest_station_join(
    centroids_gdf: gpd.GeoDataFrame,
    stations_gdf: gpd.GeoDataFrame,
    area_id_col: str = "N03_007",
    how: str = "left",
    distance_col: str = "dist_to_station_m",
) -> gpd.GeoDataFrame:
    """Run sjoin_nearest and deduplicate by area id."""
    if centroids_gdf.crs is None or stations_gdf.crs is None:
        raise ValueError("Both GeoDataFrames must have a CRS before nearest join.")

    if str(centroids_gdf.crs) != str(stations_gdf.crs):
        raise ValueError(
            f"CRS mismatch: centroids={centroids_gdf.crs}, stations={stations_gdf.crs}"
        )

    if area_id_col not in centroids_gdf.columns:
        raise KeyError(f"Area id column not found in centroids_gdf: {area_id_col}")

    joined = gpd.sjoin_nearest(
        centroids_gdf,
        stations_gdf,
        how=how,
        distance_col=distance_col,
    )

    if area_id_col not in joined.columns:
        raise KeyError(f"Area id column missing after join: {area_id_col}")

    joined = joined.drop_duplicates(subset=[area_id_col]).copy()
    return joined


def attach_station_attributes(
    base_gdf: gpd.GeoDataFrame,
    nearest_station_gdf: gpd.GeoDataFrame,
    area_id_col: str = "N03_007",
    distance_col: str = "dist_to_station_m",
    station_name_col: str = "N02_005",
    line_name_col: str = "N02_003",
    operator_col: str = "N02_004",
) -> gpd.GeoDataFrame:
    """Attach nearest-station attributes back to the base municipal GeoDataFrame."""
    if area_id_col not in base_gdf.columns:
        raise KeyError(f"Area id column not found in base_gdf: {area_id_col}")

    if area_id_col not in nearest_station_gdf.columns:
        raise KeyError(f"Area id column not found in nearest_station_gdf: {area_id_col}")

    required_cols = [
        distance_col,
        station_name_col,
        line_name_col,
        operator_col,
    ]
    missing = [col for col in required_cols if col not in nearest_station_gdf.columns]
    if missing:
        raise KeyError(f"Missing required columns in nearest_station_gdf: {missing}")

    lookup = nearest_station_gdf.set_index(area_id_col)

    out = base_gdf.copy()
    out[distance_col] = out[area_id_col].map(lookup[distance_col])
    out["nearest_station_name"] = out[area_id_col].map(lookup[station_name_col])
    out["nearest_line_name"] = out[area_id_col].map(lookup[line_name_col])
    out["nearest_operator"] = out[area_id_col].map(lookup[operator_col])

    return out
