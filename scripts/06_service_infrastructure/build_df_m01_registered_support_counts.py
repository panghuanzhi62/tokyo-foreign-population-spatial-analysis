# -*- coding: utf-8 -*-
"""
Build local-only municipality-level counts of DF_M01 registered support organizations
(toroku shien kikan) for Greater Tokyo, from the official ISA/MOJ registry Excel file.

LOCAL-ONLY. This script reads a local raw registry file and the local 251-municipality
ISA panel frame, and writes ONLY municipality-level aggregate counts plus an aggregate
parse-QC file. It never writes or commits raw, address-level, or geocoded records.

The current public registry file has NO cancellation/deletion date, so the date filters
below are REGISTERED-BY snapshot filters (existence by a date among orgs still listed in
the current edition), NOT true active-stock filters. Time validity remains
B_observable_by_2024_or_2025 unless an archived ~2024 snapshot is added.

No modeling. No normalization of the ISA/MOJ dependent variable. No network access.
"""
import argparse
import csv
import datetime
import re
import sys
from pathlib import Path

import openpyxl

# 47 prefecture names (used for content-based address-cell detection).
PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県",
]
PREF_BY_LEN = sorted(PREFECTURES, key=len, reverse=True)

# Greater Tokyo target prefectures -> 2-digit prefecture code.
GREATER_TOKYO = {"埼玉県": "11", "千葉県": "12", "東京都": "13", "神奈川県": "14"}

CUTOFFS = {
    "2024_06_30": datetime.date(2024, 6, 30),
    "2024_12_31": datetime.date(2024, 12, 31),
    "2025_06_30": datetime.date(2025, 6, 30),
    "current_snapshot": None,  # no date filter
}

REG_NUMBER_RE = re.compile(r"^\s*\d{1,2}登[-－]?\d{3,}\s*$")  # e.g. 19登-000003
DATE_TEXT_RE = re.compile(r"(\d{4})\D+(\d{1,2})\D+(\d{1,2})")
GUN_RE = re.compile(r"^.*?郡")  # leading county prefix to strip for towns/villages


def norm(s: str) -> str:
    # collapse whitespace; unify the small/large "ke" used in place names (茅ヶ崎/茅ケ崎)
    return re.sub(r"\s+", "", str(s)).strip().replace("ヶ", "ケ")


def parse_date(value):
    if value is None:
        return None
    if isinstance(value, (datetime.datetime, datetime.date)):
        return datetime.date(value.year, value.month, value.day)
    m = DATE_TEXT_RE.search(str(value))
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None


def starts_with_prefecture(text):
    s = str(text).strip()
    for p in PREF_BY_LEN:
        if s.startswith(p):
            return p
    return None


def municipality_candidates(addr_after_pref: str):
    """Return ordered candidate municipality strings for frame matching.

    Handles: Tokyo special wards (ward unit), designated-city wards (truncate to city),
    plain cities, and gun-prefixed towns/villages (gun stripped).
    """
    s = norm(addr_after_pref)
    cands = []
    # search suffix chars from index 1 so a name that STARTS with the suffix char
    # (e.g. 市原市 Ichihara, 市川市 Ichikawa) is not truncated to the bare suffix.
    i_shi = s.find("市", 1)
    i_ku = s.find("区", 1)
    i_cho = min([x for x in (s.find("町", 1), s.find("村", 1)) if x != -1], default=-1)

    # designated-city ward or plain city: truncate at first 市
    if i_shi != -1 and (i_ku == -1 or i_shi < i_ku):
        cands.append(s[: i_shi + 1])                 # e.g. 横浜市 / 八王子市
        if i_ku != -1 and i_ku > i_shi:
            cands.append(s[: i_ku + 1])              # e.g. 横浜市中区 (ward-level frame)
            cands.append(s[i_shi + 1 : i_ku + 1])    # e.g. 中区 (bare ward)
    # Tokyo special ward (区 before any 市)
    elif i_ku != -1 and (i_shi == -1 or i_ku < i_shi):
        cands.append(s[: i_ku + 1])                  # e.g. 新宿区
    # town / village (possibly gun-prefixed)
    if i_cho != -1:
        token = s[: i_cho + 1]
        stripped = GUN_RE.sub("", token)
        if stripped:
            cands.append(stripped)                   # e.g. 三芳町
        cands.append(token)                          # e.g. 入間郡三芳町
    # de-duplicate preserving order
    seen, out = set(), []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def load_frame(panel_path: Path):
    """Load the 251 municipality frame from the local ISA panel CSV.

    Returns (frame_codes, lookup) where frame_codes is a list of
    (municipality_code, prefecture_code, municipality_name) and lookup maps
    (prefecture_code, normalized_key) -> municipality_code.
    """
    frame = {}
    with panel_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            inc = str(row.get("master_frame_included", "")).strip().lower()
            if inc not in ("", "true", "1", "yes", "y"):
                continue
            code = str(row["municipality_code"]).strip()
            pref = str(row["prefecture_code"]).strip().zfill(2)
            name = str(row["municipality_name"]).strip()
            frame[code] = (code, pref, name)
    frame_codes = sorted(frame.values(), key=lambda r: r[0])

    lookup = {}
    for code, pref, name in frame_codes:
        keys = set()
        n = norm(name)
        keys.add(n)
        keys.add(GUN_RE.sub("", n))
        # strip a leading city if frame stores city+ward, and vice versa
        keys.add(n)
        for k in keys:
            if k:
                lookup[(pref, k)] = code
    return frame_codes, lookup


def detect_records(ws):
    """Yield dicts with reg_number, reg_date, org_address, support_office_address.

    Content-based detection (robust to merged-cell / column shifts): a row is an
    organization when a cell matches the registration-number pattern; address cells
    are detected as cells starting with a prefecture name (first = org, second =
    support office).
    """
    for row in ws.iter_rows(values_only=True):
        cells = [c for c in row]
        reg = None
        for c in cells:
            if c is not None and REG_NUMBER_RE.match(str(c)):
                reg = str(c).strip()
                break
        if not reg:
            continue
        addrs = []
        date_val = None
        for c in cells:
            if c is None:
                continue
            if date_val is None:
                d = parse_date(c)
                # only accept a plausible registration date (>= 2019)
                if d and d >= datetime.date(2019, 1, 1) and d <= datetime.date(2030, 1, 1):
                    date_val = d
            p = starts_with_prefecture(c)
            if p:
                addrs.append(str(c).strip())
        org_addr = addrs[0] if len(addrs) >= 1 else None
        office_addr = addrs[1] if len(addrs) >= 2 else org_addr
        yield {
            "reg_number": reg,
            "reg_date": date_val,
            "org_address": org_addr,
            "support_office_address": office_addr,
        }


def pick_address(rec, role):
    if role == "org":
        return rec["org_address"]
    if role == "support_office":
        return rec["support_office_address"] or rec["org_address"]
    return rec["support_office_address"] or rec["org_address"]


def link_municipality(address, lookup):
    """Return (prefecture_code, municipality_code) or (pref_code|None, None)."""
    if not address:
        return None, None
    pref = starts_with_prefecture(address)
    if pref not in GREATER_TOKYO:
        return None, None
    pref_code = GREATER_TOKYO[pref]
    after = norm(address)[len(pref):]
    for cand in municipality_candidates(after):
        for key in (norm(cand), GUN_RE.sub("", norm(cand))):
            code = lookup.get((pref_code, key))
            if code:
                return pref_code, code
    return pref_code, None


def build(args):
    input_dir = Path(args.input_dir)
    jp = input_dir / "registered_support_organizations_JP_2026-06-18.xlsx"
    en = input_dir / "registered_support_organizations_EN_2026-06-18.xlsx"
    # also accept any *_JP_*.xlsx / *.xlsx fallback
    if not jp.exists():
        jps = sorted(input_dir.glob("*_JP_*.xlsx"))
        jp = jps[0] if jps else None
    src = jp if (jp and jp.exists()) else (en if en.exists() else None)
    if src is None:
        print("ERROR: no local DF_M01 raw Excel found in", input_dir, file=sys.stderr)
        return 2
    print("source_file:", src.name)

    panel = Path(args.panel_path) if args.panel_path else (
        Path(args.project_root) / "data_processed_official" / "isa_moj_panel"
        / "isa_moj_chinese_stock_t2_2023_12_2025_06.csv")
    if not panel.exists():
        print("ERROR: 251-frame panel not found:", panel, file=sys.stderr)
        return 2
    frame_codes, lookup = load_frame(panel)
    print("frame_municipalities:", len(frame_codes))

    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    records = list(detect_records(ws))
    raw_count = len(records)
    unique_reg = len({r["reg_number"] for r in records})
    print("raw_records:", raw_count, "unique_reg_numbers:", unique_reg)

    roles = ["support_office", "org"] if args.address_role == "both" else [args.address_role]
    cut_items = ([(args.date_cutoff, CUTOFFS[args.date_cutoff])]
                 if args.date_cutoff and args.date_cutoff != "all"
                 else list(CUTOFFS.items()))

    outdir = Path(args.outdir) if args.outdir else (
        Path(args.project_root) / "data_processed_official" / "service_infrastructure"
        / "DF_M01_registered_support_organizations")

    qc_rows = []
    primary_role = "support_office" if "support_office" in roles else roles[0]

    for role in roles:
        # link each record once for this role
        linked = []
        gt_count = 0
        muni_parse_ok = 0
        muni_link_ok = 0
        date_ok = 0
        for r in records:
            if r["reg_date"]:
                date_ok += 1
            addr = pick_address(r, role)
            pref = starts_with_prefecture(addr) if addr else None
            if pref in GREATER_TOKYO:
                gt_count += 1
                cands = municipality_candidates(norm(addr)[len(pref):]) if addr else []
                if cands:
                    muni_parse_ok += 1
                pcode, mcode = link_municipality(addr, lookup)
                if mcode:
                    muni_link_ok += 1
                linked.append((r["reg_date"], pcode, mcode))
        for cut_name, cut_date in cut_items:
            counts = {code: 0 for code, _, _ in frame_codes}
            gt_by_cut = 0
            for d, pcode, mcode in linked:
                if cut_date is not None:
                    if not d or d > cut_date:
                        continue
                gt_by_cut += 1
                if mcode in counts:
                    counts[mcode] += 1
            positive = sum(1 for v in counts.values() if v > 0)
            zeros = sum(1 for v in counts.values() if v == 0)
            if args.write_local_counts:
                outdir.mkdir(parents=True, exist_ok=True)
                suffix = "" if role == primary_role else f"_role_{role}"
                opath = outdir / f"df_m01_counts_by_municipality_{cut_name}{suffix}.csv"
                with opath.open("w", encoding="utf-8", newline="") as f:
                    w = csv.writer(f, lineterminator="\n")
                    w.writerow(["municipality_code", "prefecture_code",
                                "municipality_name", "df_m01_count", "address_role",
                                "cutoff", "registered_by_filter_note"])
                    for code, pref, name in frame_codes:
                        w.writerow([code, pref, name, counts[code], role, cut_name,
                                    "registered_by_snapshot_not_active_stock"])
            qc_rows.append({
                "address_role": role, "cutoff": cut_name,
                "raw_record_count": raw_count, "unique_reg": unique_reg,
                "greater_tokyo_record_count": gt_count,
                "date_parse_success_count": date_ok,
                "registered_by_cutoff_count": gt_by_cut,
                "municipality_parse_success_count": muni_parse_ok,
                "municipality_code_link_success_count": muni_link_ok,
                "municipalities_with_positive_count": positive,
                "municipalities_total_frame": len(frame_codes),
                "zero_count_municipalities": zeros,
            })

    if args.write_local_counts:
        qpath = outdir / "df_m01_parse_qc_local_only.csv"
        with qpath.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(qc_rows[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(qc_rows)
        print("wrote local-only outputs to:", outdir)

    # console QC (aggregate; public place-level only)
    print("--- AGGREGATE QC (role,cutoff: gt / registered_by / parse_ok / link_ok / positive_muni) ---")
    for q in qc_rows:
        print(f"  {q['address_role']:>14} {q['cutoff']:>16}: "
              f"gt={q['greater_tokyo_record_count']} "
              f"reg_by={q['registered_by_cutoff_count']} "
              f"parse_ok={q['municipality_parse_success_count']} "
              f"link_ok={q['municipality_code_link_success_count']} "
              f"pos_muni={q['municipalities_with_positive_count']}/{q['municipalities_total_frame']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build local-only DF_M01 municipality counts")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--input-dir", default=str(Path("data_raw_official") / "service_infrastructure"
                    / "DF_M01_registered_support_organizations"))
    ap.add_argument("--outdir", default="")
    ap.add_argument("--panel-path", default="")
    ap.add_argument("--address-role", choices=["org", "support_office", "both"],
                    default="support_office")
    ap.add_argument("--date-cutoff", default="all",
                    choices=["all", "2024_06_30", "2024_12_31", "2025_06_30", "current_snapshot"])
    ap.add_argument("--write-local-counts", action="store_true",
                    help="if absent, no files are written (safe default)")
    args = ap.parse_args()
    if not args.outdir:
        args.outdir = ""
    if not args.panel_path:
        args.panel_path = ""
    sys.exit(build(args))


if __name__ == "__main__":
    main()
