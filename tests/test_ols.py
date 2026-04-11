import geopandas as gpd
import pytest
from shapely.geometry import Point

from tokyo_foreigners.ols import build_ols_design, prepare_baseline_ols_dataframe


def make_base_gdf():
    return gpd.GeoDataFrame(
        {
            "N03_007": ["001", "002", "003"],
            "N03_001": ["Tokyo", "Tokyo", "Saitama"],
            "N03_004": ["A", "B", "C"],
            "N03_005": ["x", "y", "z"],
            "foreign_ratio": ["0.10", "0.20", "bad"],
            "log_dist_to_station_m": ["1.0", "2.0", "3.0"],
            "log_median_land_price_jpy": ["10.0", "20.0", None],
        },
        geometry=[Point(0, 0), Point(1, 1), Point(2, 2)],
        crs="EPSG:4326",
    )


def test_prepare_baseline_ols_dataframe_raises_on_missing_columns():
    gdf = gpd.GeoDataFrame(
        {"foreign_ratio": [0.1]},
        geometry=[Point(0, 0)],
        crs="EPSG:4326",
    )

    with pytest.raises(KeyError):
        prepare_baseline_ols_dataframe(gdf)


def test_prepare_baseline_ols_dataframe_drops_rows_with_invalid_numeric_values():
    out = prepare_baseline_ols_dataframe(make_base_gdf())

    assert len(out) == 2
    assert set(out["N03_007"]) == {"001", "002"}


def test_build_ols_design_adds_constant_column():
    model_df = prepare_baseline_ols_dataframe(make_base_gdf())
    X, y = build_ols_design(model_df)

    assert "const" in X.columns
    assert len(X) == len(y) == 2
