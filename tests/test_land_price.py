import geopandas as gpd
import pytest
from shapely.geometry import Point

from tokyo_foreigners.land_price import filter_residential_land_price


def test_filter_residential_land_price_keeps_residential_positive_numeric_only():
    gdf = gpd.GeoDataFrame(
        {
            "L01_002": ["000", "000", "111", "000"],
            "L01_008": ["100", "-5", "200", "bad"],
        },
        geometry=[Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)],
        crs="EPSG:4326",
    )

    out = filter_residential_land_price(gdf)

    assert len(out) == 1
    assert float(out.iloc[0]["L01_008"]) == 100.0


def test_filter_residential_land_price_raises_on_missing_column():
    gdf = gpd.GeoDataFrame(
        {"L01_002": ["000"]},
        geometry=[Point(0, 0)],
        crs="EPSG:4326",
    )

    with pytest.raises(KeyError):
        filter_residential_land_price(gdf)
