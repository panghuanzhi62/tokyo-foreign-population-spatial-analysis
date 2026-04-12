from tokyo_foreigners import paths


def test_project_root_exists():
    assert paths.PROJECT_ROOT.exists()


def test_path_inventory_contains_expected_keys():
    inv = paths.path_inventory()

    expected = {
        "PROJECT_ROOT",
        "DATA_RAW_DIR",
        "DATA_PROCESSED_DIR",
        "DATA_RAW_ALT_DIR",
        "DATA_PROCESSED_ALT_DIR",
        "OUTPUTS_DIR",
        "NOTEBOOKS_DIR",
        "SCRIPTS_DIR",
        "DOCS_DIR",
    }

    assert expected.issubset(inv.keys())
    assert inv["DATA_RAW_DIR"].name == "data_raw"
    assert inv["DATA_PROCESSED_DIR"].name == "data_processed"
