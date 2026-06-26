#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISA/MOJ registered Chinese foreign-resident STOCK panel - t2 zero-filled build scaffold.

Builds (when later authorized) a LOCAL-ONLY 251 x 4 municipality panel of MOJ/ISA REGISTERED
Chinese foreign residents for Tokyo/Saitama/Chiba/Kanagawa, from the four verified
China-filtered t2 value Excel files in data_raw/isa_estat:

  2023-12 -> 23-12-t2_china_values.xlsx   (matched 245/251; zero-fill 6)
  2024-06 -> 24-06-t2_china_values.xlsx   (matched 246/251; zero-fill 5)
  2024-12 -> 24-12-t2_china_values.xlsx   (matched 245/251; zero-fill 6)
  2025-06 -> 25-06-t2_china_values.xlsx   (matched 247/251; zero-fill 4)

IMPORTANT MEASUREMENT NOTE
  These values are MOJ/ISA REGISTERED Chinese foreign residents, NOT Census population. Any
  growth variable derived here is registered Chinese foreign-resident STOCK change, NOT Census
  population growth.

This is a SCAFFOLD. By default it performs NO panel writing and NO raw-file modification.
--dry-run and --schema-only are safe and read-only. --write-local-panel is guarded by --force,
writes ONLY to a local-only outdir, and is NOT exercised in this scaffold task.

Note: the four t2 files do NOT share a fixed column order (e.g. the municipality-code column is
column 0 in 2025-06 but column 1 in 2023-12). Columns are therefore located BY HEADER, not by
position. CJK header tokens are matched via UTF-8 literals (this file declares utf-8 coding).
"""
import argparse
import csv
import os
import sys

# CJK header match tokens (UTF-8 literals; file declares utf-8 coding above)
TOK_CODE = "市区町村コード"  # shikuchoson code
TOK_NAME = "市区町村"                    # shikuchoson (municipality name)
TOK_VALUE = "在留外国人数"       # zairyu gaikokujin-su (registered foreigners)
TOK_PREF = "都道府県"                    # todofuken (prefecture)

FILE_MAP = {
    "2023-12": "23-12-t2_china_values.xlsx",
    "2024-06": "24-06-t2_china_values.xlsx",
    "2024-12": "24-12-t2_china_values.xlsx",
    "2025-06": "25-06-t2_china_values.xlsx",
}
TIME_POINTS = ["2023-12", "2024-06", "2024-12", "2025-06"]
# Target prefecture code prefixes: 11 Saitama, 12 Chiba, 13 Tokyo, 14 Kanagawa.
# The t2 files are nationwide; rows outside these prefixes are out-of-scope, NOT errors.
TARGET_PREF = {"11", "12", "13", "14"}
EXPECTED_MATCHED = {"2023-12": 245, "2024-06": 246, "2024-12": 245, "2025-06": 247}
EXPECTED_ZERO_FILL = {"2023-12": 6, "2024-06": 5, "2024-12": 6, "2025-06": 4}
MASTER_FRAME_CODES = 251
SOURCE_TYPE = "isa_moj_t2_china_values"
PANEL_FILENAME = "isa_moj_chinese_stock_t2_2023_12_2025_06.csv"
LOCAL_ONLY_PREFIXES = ("data_processed_official", "data_processed", "data_raw_official", "data_raw")
PANEL_COLUMNS = ["survey_time", "municipality_code", "prefecture_code", "municipality_name",
                 "chinese_registered", "zero_filled", "source_file", "source_type",
                 "master_frame_included"]


def build_parser():
    p = argparse.ArgumentParser(
        prog="isa_moj_t2_chinese_stock_panel_build.py",
        description="ISA/MOJ t2 zero-filled Chinese registered-stock panel build scaffold "
                    "(scaffold; panel writing is guarded by --force and deferred).",
    )
    p.add_argument("--project-root", default=".")
    p.add_argument("--input-dir", default="data_raw/isa_estat")
    p.add_argument("--master-code-frame",
                   default="literature/02_matrices/census_00200521_municipality_area_code_confirmation.csv")
    p.add_argument("--verification-csv",
                   default="literature/02_matrices/isa_moj_t2_chinese_values_file_verification.csv")
    p.add_argument("--zero-fill-design-csv",
                   default="literature/02_matrices/isa_moj_t2_chinese_stock_zero_fill_panel_design.csv")
    p.add_argument("--outdir", default="data_processed_official/isa_moj_panel")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--schema-only", action="store_true")
    p.add_argument("--write-local-panel", action="store_true",
                   help="Write the 251x4 panel to the local-only outdir (requires --force).")
    p.add_argument("--write-qc-summary", action="store_true")
    p.add_argument("--force", action="store_true")
    return p


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def load_master_frame(args):
    """Return (frame_set, meta) where frame_set is the 251 target codes and meta maps
    code -> {'prefecture_code', 'municipality_name'}."""
    path = os.path.join(args.project_root, args.master_code_frame)
    if not os.path.isfile(path):
        raise FileNotFoundError("master frame not found: %s" % path)
    frame_set = set()
    meta = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("included_in_target_scope", "").strip() == "yes":
                code = str(row.get("municipality_code", "")).strip().zfill(5)
                frame_set.add(code)
                meta[code] = {
                    "prefecture_code": str(row.get("prefecture_code", "")).strip(),
                    "municipality_name": str(row.get("municipality_name", "")).strip(),
                }
    return frame_set, meta


def load_design_counts(args):
    """Read matched/zero-fill counts from the committed zero-fill design CSV (fallback to constants)."""
    path = os.path.join(args.project_root, args.zero_fill_design_csv)
    matched, zfill = dict(EXPECTED_MATCHED), dict(EXPECTED_ZERO_FILL)
    if os.path.isfile(path):
        with open(path, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                t = str(row.get("survey_time", "")).strip()
                if t in TIME_POINTS:
                    try:
                        matched[t] = int(row.get("matched_codes", matched[t]))
                        zfill[t] = int(row.get("zero_fill_codes", zfill[t]))
                    except (ValueError, TypeError):
                        pass
    return matched, zfill


def norm_code(raw):
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    if s.endswith(".0"):  # guard against float-coerced codes
        s = s[:-2]
    return s.zfill(5)


def parse_value(raw):
    """ISA notation: '-' means zero; non-numeric -> None (missing)."""
    s = str(raw).strip().replace(",", "") if raw is not None else ""
    if s in ("-", "−", "－"):
        return 0
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def find_columns(header):
    """Locate columns by header token. Code is checked before name because the code header
    ('...code') contains the bare municipality-name token as a substring."""
    cols = {}
    for idx, h in enumerate(header):
        if h is None:
            continue
        s = str(h).strip()
        if TOK_CODE in s:
            cols["code"] = idx
        elif TOK_VALUE in s:
            cols["value"] = idx
        elif s == TOK_NAME:
            cols["name"] = idx
        elif TOK_PREF in s:
            cols["pref"] = idx
    return cols


def read_t2_file(path, frame_set):
    """Read one t2 China-values workbook read-only. Returns
    (cols, observed{code:value}, extra[], dup[], sample_numeric_ok)."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    it = ws.iter_rows(values_only=True)
    header = next(it)
    cols = find_columns(header)
    observed, extra, dup, seen = {}, [], [], set()
    sample_numeric_ok = True
    if "code" in cols and "value" in cols:
        for r in it:
            if cols["code"] >= len(r):
                continue
            code = norm_code(r[cols["code"]])
            if code is None:
                continue
            if code[:2] not in TARGET_PREF:
                continue  # nationwide out-of-scope row; not an error, just filtered out
            val = parse_value(r[cols["value"]])
            if val is None:
                sample_numeric_ok = False
                continue
            if code in seen:
                dup.append(code)
            seen.add(code)
            if code in frame_set:
                observed[code] = val
            else:
                extra.append(code)  # target-prefecture code not in the 251 frame (expected: none)
    wb.close()
    return cols, observed, extra, dup, sample_numeric_ok


def build_records(survey_time, observed, frame_set, meta, source_file):
    """Zero-fill the master frame for one time point. Returns (records, zero_fill_count)."""
    records, zf = [], 0
    for code in sorted(frame_set):
        if code in observed:
            value, zflag = observed[code], 0
        else:
            value, zflag = 0, 1
            zf += 1
        m = meta.get(code, {})
        records.append({
            "survey_time": survey_time,
            "municipality_code": code,
            "prefecture_code": m.get("prefecture_code", ""),
            "municipality_name": m.get("municipality_name", ""),
            "chinese_registered": value,
            "zero_filled": zflag,
            "source_file": source_file,
            "source_type": SOURCE_TYPE,
            "master_frame_included": 1,
        })
    return records, zf


# ---------------------------------------------------------------------------
# modes
# ---------------------------------------------------------------------------
def cmd_dry_run(args):
    print("=== ISA/MOJ t2 Chinese stock panel build : DRY RUN ===")
    print("mode: dry-run (reads verification/design/master CSVs; NO panel read/write; NO raw-file change)")
    try:
        frame_set, _ = load_master_frame(args)
        print("master frame codes:", len(frame_set), "(expected %d)" % MASTER_FRAME_CODES)
    except Exception as e:
        print("WARN master frame:", str(e)[:120]); frame_set = set()
    matched, zfill = load_design_counts(args)
    print("time points:", ",".join(TIME_POINTS))
    print("per time point (expected 251 codes each after zero-fill):")
    for t in TIME_POINTS:
        print("  %s  file=%-26s matched=%3d  zero_fill=%d  -> 251" %
              (t, FILE_MAP[t], matched[t], zfill[t]))
    print("zero-fill rule: missing target codes set to 0, flagged zero_filled=1; restrict to 251 frame;")
    print("                reject extra codes; reject duplicate codes; reject aggregate rows.")
    print("planned local-only outdir:", args.outdir, "(NOT written in this mode)")
    print("panel file (future):", PANEL_FILENAME, "| columns:", ",".join(PANEL_COLUMNS))
    print("=== DRY RUN OK ===")
    return 0


def cmd_schema_only(args):
    print("=== ISA/MOJ t2 Chinese stock panel build : SCHEMA-ONLY ===")
    print("mode: schema-only (read-only inspect of the four t2 Excel files; NO panel write)")
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        print("openpyxl not available; schema-only needs it. Use --dry-run (CSV-based) instead.")
        return 4
    try:
        frame_set, _ = load_master_frame(args)
    except Exception as e:
        print("ERROR master frame:", str(e)[:120]); return 5
    indir = os.path.join(args.project_root, args.input_dir)
    print("input dir:", indir, "(exists)" if os.path.isdir(indir) else "(MISSING)")
    all_ok = True
    for t in TIME_POINTS:
        path = os.path.join(indir, FILE_MAP[t])
        if not os.path.isfile(path):
            print("  %s  MISSING %s" % (t, FILE_MAP[t])); all_ok = False; continue
        cols, observed, extra, dup, num_ok = read_t2_file(path, frame_set)
        have = all(k in cols for k in ("code", "value"))
        codes5 = all(len(c) == 5 for c in observed)
        print("  %s  cols{code,value,name,pref}=%s | numeric=%s | code5char=%s | matched=%d extra=%d dup=%d"
              % (t, {k: cols.get(k) for k in ("code", "value", "name", "pref")},
                 num_ok, codes5, len(observed), len(extra), len(dup)))
        if not (have and num_ok and codes5 and not extra and not dup):
            all_ok = False
    print("required columns + numeric values + 5-char codes confirmed:", all_ok)
    print("no workbook was modified.")
    print("=== SCHEMA-ONLY OK ===")
    return 0 if all_ok else 6


def cmd_write_local_panel(args):
    if not args.force:
        print("REFUSED: --write-local-panel requires --force (explicit authorization). No panel written.")
        return 11
    out = os.path.normpath(args.outdir).replace("\\", "/")
    if not any(out == p or out.startswith(p + "/") for p in LOCAL_ONLY_PREFIXES):
        print("REFUSED: outdir '%s' is not a known local-only path; refusing to write panel." % out)
        return 13
    frame_set, meta = load_master_frame(args)
    if len(frame_set) != MASTER_FRAME_CODES:
        print("ABORT: master frame has %d codes, expected %d." % (len(frame_set), MASTER_FRAME_CODES))
        return 14
    indir = os.path.join(args.project_root, args.input_dir)
    all_records, qc_rows = [], []
    for t in TIME_POINTS:
        path = os.path.join(indir, FILE_MAP[t])
        if not os.path.isfile(path):
            print("ABORT: missing input %s" % FILE_MAP[t]); return 15
        cols, observed, extra, dup, num_ok = read_t2_file(path, frame_set)
        if extra:
            print("ABORT: %s has extra codes not in frame: %s" % (t, sorted(set(extra))[:5])); return 16
        if dup:
            print("ABORT: %s has duplicate codes: %s" % (t, sorted(set(dup))[:5])); return 17
        recs, zf = build_records(t, observed, frame_set, meta, FILE_MAP[t])
        all_records.extend(recs)
        qc_rows.append({"survey_time": t, "rows": len(recs), "matched": len(observed),
                        "zero_filled": zf, "expected_zero_fill": EXPECTED_ZERO_FILL[t]})
    outdir_abs = os.path.join(args.project_root, args.outdir)
    os.makedirs(outdir_abs, exist_ok=True)
    panel_path = os.path.join(outdir_abs, PANEL_FILENAME)
    with open(panel_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PANEL_COLUMNS)
        w.writeheader()
        w.writerows(all_records)
    print("wrote LOCAL-ONLY panel:", panel_path, "| rows:", len(all_records), "(expected 1004 = 251x4)")
    if args.write_qc_summary:
        qc_path = os.path.join(outdir_abs, "isa_moj_chinese_stock_t2_panel_qc.csv")
        with open(qc_path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["survey_time", "rows", "matched", "zero_filled", "expected_zero_fill"])
            w.writeheader(); w.writerows(qc_rows)
        print("wrote LOCAL-ONLY QC:", qc_path)
    print("NOTE: panel + QC are LOCAL-ONLY; do NOT stage or commit them.")
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    modes = [args.schema_only, args.write_local_panel]
    if sum(bool(x) for x in modes) > 1:
        print("ERROR: choose at most one of --schema-only / --write-local-panel."); return 3
    if args.write_local_panel:
        return cmd_write_local_panel(args)
    if args.schema_only:
        return cmd_schema_only(args)
    return cmd_dry_run(args)


if __name__ == "__main__":
    sys.exit(main())
