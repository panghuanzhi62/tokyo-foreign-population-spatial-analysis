import geopandas as gpd
import pytest
from shapely.geometry import Point

from tokyo_foreigners.station_accessibility import (
    attach_station_attributes,
    make_centroid_gdf,
)


def test_make_centroid_gdf_raises_when_centroid_column_missing():
    gdf = gpd.GeoDataFrame(
        {"N03_007": ["001"]},
        geometry=[Point(0, 0)],
        crs="EPSG:4326",
    )

    with pytest.raises(KeyError):
        make_centroid_gdf(gdf)


def test_attach_station_attributes_maps_expected_columns():
    base_gdf = gpd.GeoDataFrame(
        {"N03_007": ["001", "002"]},
        geometry=[Point(0, 0), Point(1, 1)],
        crs="EPSG:4326",
    )

    nearest_station_gdf = gpd.GeoDataFrame(
        {
            "N03_007": ["001", "002"],
            "dist_to_station_m": [100.0, 250.0],
            "N02_005": ["Station A", "Station B"],
            "N02_003": ["Line A", "Line B"],
            "N02_004": ["Operator A", "Operator B"],
        },
        geometry=[Point(0, 0), Point(1, 1)],
        crs="EPSG:4326",
    )

    out = attach_station_attributes(base_gdf, nearest_station_gdf)

    assert "nearest_station_name" in out.columns
    assert "nearest_line_name" in out.columns
    assert "nearest_operator" in out.columns
    assert out.loc[out["N03_007"] == "001", "nearest_station_name"].iloc[0] == "Station A"
    assert out.loc[out["N03_007"] == "002", "dist_to_station_m"].iloc[0] == 250.0
