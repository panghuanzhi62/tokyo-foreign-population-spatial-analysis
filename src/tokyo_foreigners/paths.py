from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Current canonical paths actually used by notebooks/code
DATA_RAW_DIR = PROJECT_ROOT / "data_raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data_processed"

# Existing alternative directories in repo, not yet canonical
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_ALT_DIR = DATA_DIR / "raw"
DATA_PROCESSED_ALT_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DOCS_DIR = PROJECT_ROOT / "docs"


def path_inventory():
    return {
        "PROJECT_ROOT": PROJECT_ROOT,
        "DATA_RAW_DIR": DATA_RAW_DIR,
        "DATA_PROCESSED_DIR": DATA_PROCESSED_DIR,
        "DATA_RAW_ALT_DIR": DATA_RAW_ALT_DIR,
        "DATA_PROCESSED_ALT_DIR": DATA_PROCESSED_ALT_DIR,
        "OUTPUTS_DIR": OUTPUTS_DIR,
        "NOTEBOOKS_DIR": NOTEBOOKS_DIR,
        "SCRIPTS_DIR": SCRIPTS_DIR,
        "DOCS_DIR": DOCS_DIR,
    }