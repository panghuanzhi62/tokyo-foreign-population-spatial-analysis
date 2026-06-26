import geopandas as gpd
import pytest
from shapely.geometry import Point

from tokyo_foreigners.boundaries import (
    ensure_crs,
    filter_tokyo_metro_by_prefecture,
    select_case_areas_by_keywords,
)


def test_ensure_crs_raises_when_input_has_no_crs():
    gdf = gpd.GeoDataFrame(
        {"name": ["a"]},
        geometry=[Point(0, 0)],
    )

    with pytest.raises(ValueError):
        ensure_crs(gdf, target_crs="EPSG:6677")


def test_filter_tokyo_metro_by_prefecture_returns_subset():
    gdf = gpd.GeoDataFrame(
        {
            "N03_001": ["Tokyo", "Saitama", "Chiba"],
            "N03_004": ["A", "B", "C"],
            "N03_005": ["x", "y", "z"],
        },
        geometry=[Point(0, 0), Point(1, 1), Point(2, 2)],
        crs="EPSG:4326",
    )

    out = filter_tokyo_metro_by_prefecture(gdf, ["Tokyo", "Saitama"])

    assert len(out) == 2
    assert set(out["N03_001"]) == {"Tokyo", "Saitama"}


def test_select_case_areas_by_keywords_matches_primary_or_secondary_name():
    gdf = gpd.GeoDataFrame(
        {
            "N03_001": ["Saitama", "Tokyo", "Chiba"],
            "N03_004": ["Kawaguchi", "AWard", "BCity"],
            "N03_005": ["x", "Edogawa", "z"],
        },
        geometry=[Point(0, 0), Point(1, 1), Point(2, 2)],
        crs="EPSG:4326",
    )

    out = select_case_areas_by_keywords(
        gdf,
        keywords_pattern="Kawaguchi|Edogawa",
    )

    assert len(out) == 2
    assert "Kawaguchi" in set(out["N03_004"])
    assert "Edogawa" in set(out["N03_005"])
