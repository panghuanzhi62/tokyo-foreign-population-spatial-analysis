from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd

from tokyo_foreigners.boundaries import project_gdf


def get_land_price_paths(data_raw: str | Path) -> dict[str, Path]:
    """Build canonical paths for the four prefecture land-price GeoJSON files."""
    data_raw = Path(data_raw)
    land_dir = data_raw / "landPrice"

    return {
        "saitama": land_dir / "L01-24_11_GML" / "L01-24_11.geojson",
        "chiba": land_dir / "L01-24_12_GML" / "L01-24_12.geojson",
        "tokyo": land_dir / "L01-24_13_GML" / "L01-24_13.geojson",
        "kanagawa": land_dir / "L01-24_14_GML" / "L01-24_14.geojson",
    }


def load_project_concat_land_price(
    paths: dict[str, Path],
    epsg: int = 6677,
) -> tuple[dict[str, gpd.GeoDataFrame], gpd.GeoDataFrame]:
    """Read, project, and concatenate prefecture land-price layers."""
    layers: dict[str, gpd.GeoDataFrame] = {}

    for name, path in paths.items():
        if not Path(path).exists():
            raise FileNotFoundError(f"Land-price file not found for {name}: {path}")

        gdf = gpd.read_file(path)
        gdf = project_gdf(gdf, epsg=epsg)
        layers[name] = gdf

    landprice = pd.concat(list(layers.values()), ignore_index=True)
    landprice = gpd.GeoDataFrame(landprice, geometry="geometry", crs=f"EPSG:{epsg}")

    return layers, landprice


def filter_residential_land_price(
    landprice: gpd.GeoDataFrame,
    usage_col: str = "L01_002",
    residential_code: str = "000",
    price_col: str = "L01_008",
) -> gpd.GeoDataFrame:
    """Keep residential land-price points and coerce valid positive prices."""
    for col in [usage_col, price_col]:
        if col not in landprice.columns:
            raise KeyError(f"Required column not found: {col}")

    out = landprice[landprice[usage_col].astype(str) == residential_code].copy()
    out[price_col] = pd.to_numeric(out[price_col], errors="coerce")
    out = out[out[price_col] > 0].copy()

    return out


def merge_median_land_price_by_district(
    tokyo_gdf: gpd.GeoDataFrame,
    residential_landprice_gdf: gpd.GeoDataFrame,
    area_id_col: str = "N03_007",
    price_col: str = "L01_008",
    output_col: str = "median_land_price_jpy",
    predicate: str = "within",
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame, pd.DataFrame]:
    """Spatially join residential land-price points to districts and attach median price."""
    if tokyo_gdf.crs is None or residential_landprice_gdf.crs is None:
        raise ValueError("Both GeoDataFrames must have CRS before spatial join.")

    if str(tokyo_gdf.crs) != str(residential_landprice_gdf.crs):
        raise ValueError(
            f"CRS mismatch: tokyo_gdf={tokyo_gdf.crs}, "
            f"residential_landprice_gdf={residential_landprice_gdf.crs}"
        )

    if area_id_col not in tokyo_gdf.columns:
        raise KeyError(f"Area id column not found in tokyo_gdf: {area_id_col}")

    if price_col not in residential_landprice_gdf.columns:
        raise KeyError(
            f"Price column not found in residential_landprice_gdf: {price_col}"
        )

    joined_lp = gpd.sjoin(
        residential_landprice_gdf,
        tokyo_gdf[[area_id_col, "geometry"]],
        how="inner",
        predicate=predicate,
    )

    district_price = (
        joined_lp.groupby(area_id_col)[price_col]
        .median()
        .reset_index()
        .rename(columns={price_col: output_col})
    )

    tokyo_with_price = tokyo_gdf.merge(district_price, on=area_id_col, how="left")

    return tokyo_with_price, joined_lp, district_price