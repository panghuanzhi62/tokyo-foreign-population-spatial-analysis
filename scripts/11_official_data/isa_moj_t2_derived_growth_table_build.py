#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISA/MOJ t2 derived-growth table - LOCAL-ONLY build scaffold.

Builds (when later authorized) a LOCAL-ONLY municipality-level derived-growth table from the
existing local-only ISA/MOJ t2 zero-filled registered Chinese foreign-resident STOCK panel
(data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv).

The derived variables capture 2023-12 -> 2025-06 MOJ/ISA REGISTERED Chinese foreign-resident
STOCK change. They are NOT Census population growth and NOT causal settlement growth.

Variables (approved candidates, pending user confirmation):
  chinese_registered_change_2023_12_to_2025_06        = end - base                (primary descriptive)
  chinese_registered_log1p_change_2023_12_to_2025_06  = log(end+1) - log(base+1)  (primary model candidate)
  chinese_registered_zero_base_2023_12                = 1 if base == 0 else 0      (mandatory flag)
  chinese_registered_pct_change_2023_12_to_2025_06    = (end-base)/base where base>0 (robustness; with flag)
  chinese_registered_growth_positive_2023_12_to_2025_06 = 1 if end > base else 0   (optional binary)
Raw log-difference (log(end) - log(base)) is NOT used as the default (undefined at zero base/end).

This is a SCAFFOLD. By default it performs NO table writing. --dry-run and --schema-only are
safe and read-only. --write-local-derived-table is guarded by --force, writes ONLY to a
local-only outdir, and is NOT exercised in this scaffold task. The full panel, the local QC,
and any municipality-level derived values remain LOCAL-ONLY and must never be staged/committed.
"""
import argparse
import csv
import math
import os
import sys

REQUIRED_COLUMNS = ["survey_time", "municipality_code", "chinese_registered", "zero_filled"]
EXPECTED_ROWS = 251
EXPECTED_ZERO_BASE = 6
LOCAL_ONLY_PREFIXES = ("data_processed_official", "data_processed", "data_raw_official", "data_raw")
DERIVED_TABLE_FILENAME = "isa_moj_t2_derived_growth_2023_12_2025_06.csv"
DERIVED_QC_FILENAME = "isa_moj_t2_derived_growth_qc.csv"
DERIVED_COLUMNS = [
    "municipality_code", "prefecture_code", "municipality_name",
    "chinese_registered_2023_12", "chinese_registered_2025_06",
    "chinese_registered_change_2023_12_to_2025_06",
    "chinese_registered_log1p_change_2023_12_to_2025_06",
    "chinese_registered_zero_base_2023_12",
    "chinese_registered_pct_change_2023_12_to_2025_06",
    "chinese_registered_growth_positive_2023_12_to_2025_06",
    "base_zero_filled", "end_zero_filled",
]
CANDIDATE_VARIABLES = [
    "chinese_registered_change_2023_12_to_2025_06 (primary descriptive)",
    "chinese_registered_log1p_change_2023_12_to_2025_06 (primary model candidate)",
    "chinese_registered_zero_base_2023_12 (mandatory flag)",
    "chinese_registered_pct_change_2023_12_to_2025_06 (robustness; base>0 + flag)",
    "chinese_registered_growth_positive_2023_12_to_2025_06 (optional binary)",
]


def build_parser():
    p = argparse.ArgumentParser(
        prog="isa_moj_t2_derived_growth_table_build.py",
        description="ISA/MOJ t2 derived-growth table LOCAL-ONLY build scaffold "
                    "(scaffold; table writing is guarded by --force and deferred).",
    )
    p.add_argument("--project-root", default=".")
    p.add_argument("--input-panel",
                   default="data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv")
    p.add_argument("--input-qc",
                   default="data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_panel_qc.csv")
    p.add_argument("--outdir", default="data_processed_official/isa_moj_panel")
    p.add_argument("--base-time", default="2023-12")
    p.add_argument("--end-time", default="2025-06")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--schema-only", action="store_true")
    p.add_argument("--write-local-derived-table", action="store_true",
                   help="Write the derived-growth table to the local-only outdir (requires --force).")
    p.add_argument("--write-qc-summary", action="store_true")
    p.add_argument("--force", action="store_true")
    return p


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def load_panel(args):
    path = os.path.join(args.project_root, args.input_panel)
    if not os.path.isfile(path):
        raise FileNotFoundError("input panel not found: %s" % path)
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []
        rows = list(reader)
    return cols, rows


def split_base_end(rows, base_time, end_time):
    """Return (base{code:row}, end{code:row}) for the two target time points."""
    base, end = {}, {}
    for r in rows:
        if r["survey_time"] == base_time:
            base[r["municipality_code"]] = r
        elif r["survey_time"] == end_time:
            end[r["municipality_code"]] = r
    return base, end


def to_int(s):
    try:
        return int(float(str(s).strip()))
    except (ValueError, TypeError):
        return None


def compute_record(code, base_row, end_row):
    """Compute the derived-growth record for one municipality (used only in the write path)."""
    b = to_int(base_row["chinese_registered"])
    e = to_int(end_row["chinese_registered"])
    rec = {
        "municipality_code": code,
        "prefecture_code": base_row.get("prefecture_code", ""),
        "municipality_name": base_row.get("municipality_name", ""),
        "chinese_registered_2023_12": b,
        "chinese_registered_2025_06": e,
        "chinese_registered_change_2023_12_to_2025_06": e - b,
        "chinese_registered_log1p_change_2023_12_to_2025_06":
            round(math.log(e + 1) - math.log(b + 1), 6),
        "chinese_registered_zero_base_2023_12": 1 if b == 0 else 0,
        # robustness: percent change only where base > 0; blank (flagged) otherwise
        "chinese_registered_pct_change_2023_12_to_2025_06":
            (round((e - b) / b, 6) if b > 0 else ""),
        "chinese_registered_growth_positive_2023_12_to_2025_06": 1 if e > b else 0,
        "base_zero_filled": base_row.get("zero_filled", ""),
        "end_zero_filled": end_row.get("zero_filled", ""),
    }
    return rec


# ---------------------------------------------------------------------------
# modes
# ---------------------------------------------------------------------------
def cmd_dry_run(args):
    print("=== ISA/MOJ t2 derived-growth table build : DRY RUN ===")
    print("mode: dry-run (confirms paths + candidate variables; NO table write; panel not read)")
    print("input panel (intended):", os.path.join(args.project_root, args.input_panel))
    print("input qc    (intended):", os.path.join(args.project_root, args.input_qc))
    out = os.path.normpath(args.outdir).replace("\\", "/")
    print("output dir  (local-only):", out)
    print("derived table (future):", os.path.join(out, DERIVED_TABLE_FILENAME))
    print("derived qc    (future):", os.path.join(out, DERIVED_QC_FILENAME))
    print("base time:", args.base_time, "| end time:", args.end_time)
    print("candidate variables:")
    for v in CANDIDATE_VARIABLES:
        print("  -", v)
    print("raw logdiff used as default: NO (undefined at zero base/end)")
    print("measurement: MOJ/ISA REGISTERED Chinese foreign-resident STOCK change, NOT Census population growth")
    print("output is LOCAL-ONLY and is NOT written in this mode.")
    print("=== DRY RUN OK ===")
    return 0


def cmd_schema_only(args):
    print("=== ISA/MOJ t2 derived-growth table build : SCHEMA-ONLY ===")
    print("mode: schema-only (read-only inspect of the local panel; NO table write)")
    try:
        cols, rows = load_panel(args)
    except Exception as e:
        print("ERROR:", str(e)[:160]); return 5
    missing = [c for c in REQUIRED_COLUMNS if c not in cols]
    print("required columns present:", not missing, ("(missing: %s)" % missing) if missing else "")
    if missing:
        return 6
    base, end = split_base_end(rows, args.base_time, args.end_time)
    base_ok = len(base) == EXPECTED_ROWS
    end_ok = len(end) == EXPECTED_ROWS
    sets_identical = set(base.keys()) == set(end.keys())
    codes5 = all(len(c) == 5 for c in base) and all(len(c) == 5 for c in end)
    numeric = all(to_int(r["chinese_registered"]) is not None for r in rows)
    print("base time %s rows: %d (expected %d) ok=%s" % (args.base_time, len(base), EXPECTED_ROWS, base_ok))
    print("end  time %s rows: %d (expected %d) ok=%s" % (args.end_time, len(end), EXPECTED_ROWS, end_ok))
    print("municipality_code sets identical (base vs end):", sets_identical)
    print("municipality_code all 5-char:", codes5)
    print("chinese_registered all numeric:", numeric)
    all_ok = base_ok and end_ok and sets_identical and codes5 and numeric
    print("schema check passed:", all_ok)
    print("no table was written.")
    return 0 if all_ok else 7


def cmd_write_local_derived_table(args):
    if not args.force:
        print("REFUSED: --write-local-derived-table requires --force (explicit authorization). No table written.")
        return 11
    out = os.path.normpath(args.outdir).replace("\\", "/")
    if not any(out == p or out.startswith(p + "/") for p in LOCAL_ONLY_PREFIXES):
        print("REFUSED: outdir '%s' is not a known local-only path; refusing to write table." % out)
        return 13
    cols, rows = load_panel(args)
    missing = [c for c in REQUIRED_COLUMNS if c not in cols]
    if missing:
        print("ABORT: panel missing required columns:", missing); return 14
    base, end = split_base_end(rows, args.base_time, args.end_time)
    if len(base) != EXPECTED_ROWS or len(end) != EXPECTED_ROWS:
        print("ABORT: base/end rows %d/%d, expected %d each." % (len(base), len(end), EXPECTED_ROWS)); return 15
    if set(base.keys()) != set(end.keys()):
        print("ABORT: base/end municipality_code sets differ."); return 16
    codes = sorted(base.keys())
    records, zero_base = [], 0
    for code in codes:
        b = to_int(base[code]["chinese_registered"])
        e = to_int(end[code]["chinese_registered"])
        if b is None or e is None:
            print("ABORT: non-numeric value at %s." % code); return 17
        if b < 0 or e < 0:
            print("ABORT: negative value at %s." % code); return 18
        if b == 0:
            zero_base += 1
        records.append(compute_record(code, base[code], end[code]))
    if zero_base != EXPECTED_ZERO_BASE:
        print("WARN: zero-base count %d != expected %d (review before use)." % (zero_base, EXPECTED_ZERO_BASE))
    outdir_abs = os.path.join(args.project_root, args.outdir)
    os.makedirs(outdir_abs, exist_ok=True)
    table_path = os.path.join(outdir_abs, DERIVED_TABLE_FILENAME)
    with open(table_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=DERIVED_COLUMNS)
        w.writeheader(); w.writerows(records)
    print("wrote LOCAL-ONLY derived table:", table_path, "| rows:", len(records), "(expected 251)")
    if args.write_qc_summary:
        qc_path = os.path.join(outdir_abs, DERIVED_QC_FILENAME)
        pct_n = sum(1 for r in records if r["chinese_registered_pct_change_2023_12_to_2025_06"] != "")
        with open(qc_path, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["metric", "value"])
            w.writerow(["rows", len(records)])
            w.writerow(["zero_base_count", zero_base])
            w.writerow(["pct_change_defined_count", pct_n])
            w.writerow(["base_time", args.base_time])
            w.writerow(["end_time", args.end_time])
        print("wrote LOCAL-ONLY derived QC:", qc_path)
    print("NOTE: derived table + QC are LOCAL-ONLY; do NOT stage or commit them.")
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    modes = [args.schema_only, args.write_local_derived_table]
    if sum(bool(x) for x in modes) > 1:
        print("ERROR: choose at most one of --schema-only / --write-local-derived-table."); return 3
    if args.write_local_derived_table:
        return cmd_write_local_derived_table(args)
    if args.schema_only:
        return cmd_schema_only(args)
    return cmd_dry_run(args)


if __name__ == "__main__":
    sys.exit(main())
