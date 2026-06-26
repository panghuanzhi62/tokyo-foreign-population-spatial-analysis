#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 02 targeted official-source discovery (Tokyo-China opportunity-risk project).

Standard-library only. Official Japanese government and quasi-official websites
generally do NOT expose a uniform search API, so this script uses the
conservative semi-automated approach permitted by the task:

  - it works from a CURATED list of KNOWN, stable official / quasi-official
    landing or catalogue pages relevant to the project domains and geographies;
  - it verifies each page with a single lightweight reachability request
    (HTTP status only; a few bytes are read to confirm the page responds);
  - it NEVER crawls a site, NEVER downloads a PDF or a dataset, NEVER uses
    browser automation, NEVER uses a paid API, and stores NO credentials.

Output is written to the local discovery folder and NEW rows are appended to
official_source_registry.csv. Academic literature is NOT added here; official
sources stay in the registry. This is source discovery, not a literature review
and not a research-gap claim. Current status: gap under verification.
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = ("TokyoChinaLitDiscovery/Round02 (official-source landing-page "
              "reachability check; metadata only; stdlib urllib)")
HTTP_TIMEOUT = 12  # seconds

REGISTRY_CSV_REL = Path("literature") / "02_matrices" / "official_source_registry.csv"

REGISTRY_COLUMNS = [
    "source_id", "institution", "source_title", "english_working_title",
    "year", "stable_url", "source_type", "geographic_coverage",
    "data_or_policy_domain", "relevance_to_tokyo_chinese_project",
    "use_in_analysis", "license_or_access_note", "verified_status", "notes",
]

# Catalogue/data-portal source types get verified_by_official_catalogue on 200.
CATALOGUE_TYPES = {
    "official_data_source", "official_open_data_catalogue",
}

# ---------------------------------------------------------------------------
# Curated official / quasi-official sources. Each is a real, stable landing or
# catalogue page. URLs are HTML landing/section pages (NOT PDFs/datasets).
# domain_group drives --max-per-domain and the coverage tally.
# ---------------------------------------------------------------------------
CANDIDATES = [
    # ---- population / nationality statistics ----
    {
        "domain_group": "population_statistics",
        "institution": "総務省統計局 / 政府統計の総合窓口 (Statistics Bureau of Japan / e-Stat)",
        "source_title": "政府統計の総合窓口 (e-Stat)",
        "english_working_title": "e-Stat: portal site of official statistics of Japan",
        "year": "NA", "stable_url": "https://www.e-stat.go.jp/",
        "source_type": "official_data_source",
        "geographic_coverage": "Japan (incl. Tokyo, by prefecture/municipality)",
        "data_or_policy_domain": "population statistics; foreign-resident counts; census; open data",
        "relevance": "primary portal for census and Basic Resident Register statistics, including foreign-resident population by nationality and municipality; baseline data source for the Tokyo-region population layer.",
        "use_in_analysis": "official_population_data",
    },
    {
        "domain_group": "population_statistics",
        "institution": "出入国在留管理庁 (Immigration Services Agency of Japan)",
        "source_title": "在留外国人統計 (旧 登録外国人統計)",
        "english_working_title": "Statistics on foreign residents (ISA)",
        "year": "NA",
        "stable_url": "https://www.moj.go.jp/isa/policies/statistics/toukei_ichiran_touroku.html",
        "source_type": "official_data_source",
        "geographic_coverage": "Japan (by nationality and prefecture/municipality)",
        "data_or_policy_domain": "foreign-resident population by nationality (incl. Chinese)",
        "relevance": "official foreign-resident counts by nationality and area; supports the Chinese-resident population baseline for Tokyo and surrounding prefectures.",
        "use_in_analysis": "official_population_data",
    },
    {
        "domain_group": "population_statistics",
        "institution": "総務省 (Ministry of Internal Affairs and Communications)",
        "source_title": "住民基本台帳に基づく人口、人口動態及び世帯数",
        "english_working_title": "Population based on the Basic Resident Register (incl. foreign residents)",
        "year": "NA",
        "stable_url": "https://www.soumu.go.jp/main_sosiki/jichi_gyousei/daityo/jinkou_jinkoudoutai-setaisuu.html",
        "source_type": "official_data_source",
        "geographic_coverage": "Japan (by municipality)",
        "data_or_policy_domain": "resident population incl. foreign residents by municipality",
        "relevance": "municipality-level resident population including foreign residents; supports municipal population denominators for the Tokyo region.",
        "use_in_analysis": "official_population_data",
    },
    {
        "domain_group": "population_statistics",
        "institution": "東京都総務局統計部 (Tokyo Metropolitan Government, Statistics Division)",
        "source_title": "東京都の統計 / 東京都の人口（推計）",
        "english_working_title": "Tokyo Statistics / Population of Tokyo (estimates)",
        "year": "NA", "stable_url": "https://www.toukei.metro.tokyo.lg.jp/",
        "source_type": "official_data_source",
        "geographic_coverage": "Tokyo Metropolis (by ward/municipality)",
        "data_or_policy_domain": "Tokyo population statistics incl. foreign residents",
        "relevance": "Tokyo Metropolitan Government statistics including ward/municipality population and foreign-resident figures; core Tokyo population layer.",
        "use_in_analysis": "official_population_data",
    },
    # ---- spatial / open data ----
    {
        "domain_group": "spatial_open_data",
        "institution": "国土交通省 (MLIT) 国土数値情報",
        "source_title": "国土数値情報ダウンロードサイト",
        "english_working_title": "National Land Numerical Information download site (MLIT)",
        "year": "NA", "stable_url": "https://nlftp.mlit.go.jp/ksj/",
        "source_type": "official_open_data_catalogue",
        "geographic_coverage": "Japan (national GIS layers; incl. Tokyo region)",
        "data_or_policy_domain": "spatial base data: boundaries, transit, land use, facilities, hazard",
        "relevance": "national GIS layers (administrative boundaries, railways/stations, land use, facilities, hazard zones) for constructing the accessibility and exposure layers of the analysis.",
        "use_in_analysis": "official_spatial_data",
    },
    {
        "domain_group": "spatial_open_data",
        "institution": "国土地理院 (Geospatial Information Authority of Japan, GSI)",
        "source_title": "地理院地図 / GSI Maps",
        "english_working_title": "GSI Maps (Geospatial Information Authority of Japan)",
        "year": "NA", "stable_url": "https://www.gsi.go.jp/",
        "source_type": "official_spatial_data",
        "geographic_coverage": "Japan (base maps; incl. Tokyo region)",
        "data_or_policy_domain": "national base maps and geospatial reference data",
        "relevance": "authoritative base maps and geospatial reference for the spatial analysis; basemap and geocoding context.",
        "use_in_analysis": "official_spatial_data",
    },
    # ---- housing ----
    {
        "domain_group": "housing",
        "institution": "東京都住宅政策本部 (Tokyo Metropolitan Government, Bureau of Housing Policy)",
        "source_title": "東京都住宅政策本部",
        "english_working_title": "Tokyo Metropolitan Government Bureau of Housing Policy",
        "year": "NA", "stable_url": "https://www.juutakuseisaku.metro.tokyo.lg.jp/",
        "source_type": "official_housing_context",
        "geographic_coverage": "Tokyo Metropolis",
        "data_or_policy_domain": "housing policy; public housing (Toei housing); housing consultation",
        "relevance": "Tokyo housing policy and public (Toei) housing context, including housing support and consultation relevant to the housing-constraint module.",
        "use_in_analysis": "housing_policy_context",
    },
    {
        "domain_group": "housing",
        "institution": "独立行政法人都市再生機構 (UR都市機構, Urban Renaissance Agency)",
        "source_title": "UR都市機構 (UR賃貸住宅)",
        "english_working_title": "Urban Renaissance Agency (UR rental housing)",
        "year": "NA", "stable_url": "https://www.ur-net.go.jp/",
        "source_type": "quasi_official_service_infrastructure",
        "geographic_coverage": "Japan (incl. Tokyo region public rental estates)",
        "data_or_policy_domain": "public rental housing; large housing estates",
        "relevance": "quasi-official public rental housing provider; large UR estates (e.g. in the Tokyo region) often house concentrations of foreign residents; housing-infrastructure context.",
        "use_in_analysis": "housing_policy_context",
    },
    {
        "domain_group": "housing",
        "institution": "東京都住宅供給公社 (JKK東京, Tokyo Metropolitan Housing Supply Corporation)",
        "source_title": "JKK東京 (東京都住宅供給公社)",
        "english_working_title": "JKK Tokyo (Tokyo Metropolitan Housing Supply Corporation)",
        "year": "NA", "stable_url": "https://www.to-kousya.or.jp/",
        "source_type": "quasi_official_service_infrastructure",
        "geographic_coverage": "Tokyo Metropolis",
        "data_or_policy_domain": "public/affordable rental housing supply and management",
        "relevance": "quasi-official Tokyo housing-supply body managing public/affordable rental housing; housing-access infrastructure context.",
        "use_in_analysis": "housing_policy_context",
    },
    # ---- disaster / risk ----
    {
        "domain_group": "disaster_risk",
        "institution": "東京都 (Tokyo Metropolitan Government)",
        "source_title": "東京都防災ホームページ",
        "english_working_title": "Tokyo Metropolitan Government Disaster Prevention website",
        "year": "NA", "stable_url": "https://www.bousai.metro.tokyo.lg.jp/",
        "source_type": "official_disaster_or_risk_context",
        "geographic_coverage": "Tokyo Metropolis",
        "data_or_policy_domain": "disaster prevention; evacuation; multilingual disaster information",
        "relevance": "Tokyo disaster-prevention portal including evacuation guidance and multilingual disaster information; disaster-exposure and risk-communication context.",
        "use_in_analysis": "disaster_or_risk_context",
    },
    {
        "domain_group": "disaster_risk",
        "institution": "国土交通省 (MLIT) / 国土地理院",
        "source_title": "ハザードマップポータルサイト",
        "english_working_title": "Hazard Map Portal Site (MLIT)",
        "year": "NA", "stable_url": "https://disaportal.gsi.go.jp/",
        "source_type": "official_open_data_catalogue",
        "geographic_coverage": "Japan (by municipality; incl. Tokyo region)",
        "data_or_policy_domain": "flood/earthquake/landslide hazard maps; risk exposure",
        "relevance": "national hazard-map portal (flood, earthquake, sediment) for constructing the disaster-exposure layer across Tokyo-region municipalities.",
        "use_in_analysis": "disaster_or_risk_context",
    },
    {
        "domain_group": "disaster_risk",
        "institution": "内閣府 (Cabinet Office, Disaster Management)",
        "source_title": "内閣府 防災情報のページ",
        "english_working_title": "Cabinet Office Disaster Management website",
        "year": "NA", "stable_url": "https://www.bousai.go.jp/",
        "source_type": "official_policy_context",
        "geographic_coverage": "Japan",
        "data_or_policy_domain": "national disaster-management policy and guidance",
        "relevance": "national disaster-management policy context, including guidance on foreign residents and vulnerable populations; risk-policy interpretation.",
        "use_in_analysis": "disaster_or_risk_context",
    },
    # ---- multilingual / administrative service ----
    {
        "domain_group": "multilingual_service",
        "institution": "公益財団法人東京都つながり創成財団 (Tokyo Metropolitan Foundation 'Tsunagari')",
        "source_title": "東京都つながり創成財団 / 東京都多言語生活情報",
        "english_working_title": "Tokyo Metropolitan Foundation Tsunagari / Tokyo multilingual living information",
        "year": "NA", "stable_url": "https://www.tsunagari-tokyo.jp/",
        "source_type": "quasi_official_service_infrastructure",
        "geographic_coverage": "Tokyo Metropolis",
        "data_or_policy_domain": "multilingual living information; foreign-resident support",
        "relevance": "Tokyo Metropolitan quasi-official foundation providing multilingual living information and foreign-resident support; core multilingual administrative-service infrastructure for Tokyo.",
        "use_in_analysis": "multilingual_administrative_context",
    },
    {
        "domain_group": "multilingual_service",
        "institution": "東京都国際交流委員会 (Tokyo International Communication Committee, TICC)",
        "source_title": "東京都国際交流委員会 (TICC)",
        "english_working_title": "Tokyo International Communication Committee (TICC)",
        "year": "NA", "stable_url": "https://www.tokyo-icc.jp/",
        "source_type": "quasi_official_service_infrastructure",
        "geographic_coverage": "Tokyo Metropolis",
        "data_or_policy_domain": "international exchange; multilingual/foreign-resident support",
        "relevance": "Tokyo international-exchange body providing foreign-resident information and support; multilingual administrative-service context for Tokyo.",
        "use_in_analysis": "multilingual_administrative_context",
    },
    {
        "domain_group": "multilingual_service",
        "institution": "出入国在留管理庁 (Immigration Services Agency of Japan)",
        "source_title": "外国人生活支援ポータルサイト",
        "english_working_title": "Support Portal for Foreign Residents (ISA)",
        "year": "NA",
        "stable_url": "https://www.moj.go.jp/isa/support/portal/index.html",
        "source_type": "official_service_context",
        "geographic_coverage": "Japan (multilingual)",
        "data_or_policy_domain": "multilingual administrative-service guidance for foreign residents",
        "relevance": "national multilingual portal of administrative-service guidance for foreign residents (living, work, disaster, health, education); service-access context.",
        "use_in_analysis": "multilingual_administrative_context",
    },
    {
        "domain_group": "multilingual_service",
        "institution": "一般財団法人自治体国際化協会 (CLAIR)",
        "source_title": "CLAIR 多文化共生ポータルサイト",
        "english_working_title": "CLAIR Multicultural Coexistence Portal",
        "year": "NA", "stable_url": "https://www.clair.or.jp/",
        "source_type": "quasi_official_service_infrastructure",
        "geographic_coverage": "Japan (nationwide local governments)",
        "data_or_policy_domain": "municipal multicultural coexistence; multilingual support resources",
        "relevance": "CLAIR's official portal of municipal multicultural-coexistence and multilingual resources; complements the CLAIR periodical record R02_NDL_OFF_002 with the live institutional portal.",
        "use_in_analysis": "multilingual_administrative_context",
    },
    # ---- health / welfare / education ----
    {
        "domain_group": "health_welfare_education",
        "institution": "文部科学省 (MEXT)",
        "source_title": "CLARINET 外国人児童生徒等の教育",
        "english_working_title": "CLARINET: education for foreign children and students (MEXT)",
        "year": "NA", "stable_url": "https://www.mext.go.jp/a_menu/shotou/clarinet/",
        "source_type": "official_health_welfare_education_context",
        "geographic_coverage": "Japan",
        "data_or_policy_domain": "education for foreign children; school enrolment support",
        "relevance": "national policy/resource hub for education of foreign children; education service-access context for foreign-resident families.",
        "use_in_analysis": "health_welfare_education_context",
    },
    {
        "domain_group": "health_welfare_education",
        "institution": "厚生労働省 (Ministry of Health, Labour and Welfare)",
        "source_title": "厚生労働省 (外国人の医療・福祉関連情報)",
        "english_working_title": "MHLW (foreign-resident health, welfare and labour information)",
        "year": "NA", "stable_url": "https://www.mhlw.go.jp/",
        "source_type": "official_health_welfare_education_context",
        "geographic_coverage": "Japan",
        "data_or_policy_domain": "health, welfare and labour policy incl. foreign residents",
        "relevance": "national health/welfare/labour ministry; foreign-resident medical-access and welfare policy context (specific sub-pages to confirm manually).",
        "use_in_analysis": "health_welfare_education_context",
    },
    # ---- prefectural / municipal ----
    {
        "domain_group": "municipal_prefectural",
        "institution": "埼玉県 (Saitama Prefecture)",
        "source_title": "埼玉県 多文化共生 / 外国人住民支援",
        "english_working_title": "Saitama Prefecture multicultural coexistence / foreign-resident support",
        "year": "NA", "stable_url": "https://www.pref.saitama.lg.jp/",
        "source_type": "municipal_context_source",
        "geographic_coverage": "Saitama Prefecture (Tokyo metropolitan region)",
        "data_or_policy_domain": "prefectural multicultural / foreign-resident support policy",
        "relevance": "Saitama prefectural portal (e.g. Kawaguchi/Warabi have notable Chinese-resident concentrations); municipal/prefectural service-context for the wider Tokyo region. Confirm specific multicultural page manually.",
        "use_in_analysis": "municipal_context_source",
    },
    {
        "domain_group": "municipal_prefectural",
        "institution": "千葉県 (Chiba Prefecture)",
        "source_title": "千葉県 多文化共生 / 外国人県民支援",
        "english_working_title": "Chiba Prefecture multicultural coexistence / foreign-resident support",
        "year": "NA", "stable_url": "https://www.pref.chiba.lg.jp/",
        "source_type": "municipal_context_source",
        "geographic_coverage": "Chiba Prefecture (Tokyo metropolitan region)",
        "data_or_policy_domain": "prefectural multicultural / foreign-resident support policy",
        "relevance": "Chiba prefectural portal for foreign-resident support; municipal/prefectural service-context for the wider Tokyo region. Confirm specific multicultural page manually.",
        "use_in_analysis": "municipal_context_source",
    },
    {
        "domain_group": "municipal_prefectural",
        "institution": "公益財団法人かながわ国際交流財団 (Kanagawa International Foundation, KIF)",
        "source_title": "かながわ国際交流財団 (KIF)",
        "english_working_title": "Kanagawa International Foundation (KIF)",
        "year": "NA", "stable_url": "https://www.kifjp.org/",
        "source_type": "quasi_official_service_infrastructure",
        "geographic_coverage": "Kanagawa Prefecture (Tokyo metropolitan region)",
        "data_or_policy_domain": "multilingual support; foreign-resident services; multicultural resources",
        "relevance": "Kanagawa quasi-official international foundation providing multilingual support and foreign-resident resources; service-infrastructure context for the Tokyo region.",
        "use_in_analysis": "multilingual_administrative_context",
    },
]


def build_arg_parser():
    p = argparse.ArgumentParser(
        description="Targeted official-source discovery (Tokyo-China project).")
    p.add_argument("--project-root", required=True,
                   help="Absolute path to the repository root.")
    p.add_argument("--run-id", default="round02_official_targeted",
                   help="Run identifier; controls output subfolder.")
    p.add_argument("--max-per-domain", type=int, default=10,
                   help="Max candidates verified per domain group.")
    p.add_argument("--sleep-seconds", type=float, default=1.5,
                   help="Polite delay between reachability checks.")
    return p


def check_url(url):
    """Single lightweight reachability check. Returns (status_code, note).

    Reads only a few bytes to confirm the page responds. No PDF/dataset is
    downloaded and no site is crawled.
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            resp.read(256)  # confirm the page responds; not a download
            return getattr(resp, "status", 200) or 200, ""
    except urllib.error.HTTPError as e:
        return e.code, "HTTP %s" % e.code
    except urllib.error.URLError as e:
        return None, "URLERROR %s" % getattr(e, "reason", e)
    except Exception as e:  # noqa: BLE001 - defensive
        return None, "ERROR %s" % e


def status_for(source_type, code):
    if code == 200:
        return ("verified_by_official_catalogue"
                if source_type in CATALOGUE_TYPES else "verified_by_official_page")
    if code is not None and 400 <= code < 600:
        return "partially_verified"
    return "hold_for_manual_check"


def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def read_existing_registry(path):
    ids, titles, urls, max_tgt = set(), set(), set(), 0
    if not path.exists():
        return ids, titles, urls, max_tgt
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid = (row.get("source_id") or "").strip()
            if sid:
                ids.add(sid)
                m = re.match(r"^R02_OFF_TGT_(\d+)$", sid)
                if m:
                    max_tgt = max(max_tgt, int(m.group(1)))
            titles.add(_norm(row.get("source_title")))
            urls.add(_norm(row.get("stable_url")))
    return ids, titles, urls, max_tgt


def main():
    args = build_arg_parser().parse_args()
    root = Path(args.project_root)
    out_dir = root / "outputs" / "literature_discovery" / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Apply per-domain cap.
    per_domain = {}
    selected = []
    for c in CANDIDATES:
        g = c["domain_group"]
        per_domain[g] = per_domain.get(g, 0) + 1
        if per_domain[g] <= args.max_per_domain:
            selected.append(c)

    registry_csv = root / REGISTRY_CSV_REL
    existing_ids, existing_titles, existing_urls, max_tgt = read_existing_registry(registry_csv)

    candidates = []
    for c in selected:
        code, note = check_url(c["stable_url"])
        vstatus = status_for(c["source_type"], code)
        check_note = ("reachability check: HTTP %s" % code) if code else ("reachability check: %s" % note)
        rec = dict(c)
        rec["http_status"] = code if code is not None else "unreachable"
        rec["verified_status"] = vstatus
        rec["check_note"] = check_note
        candidates.append(rec)
        time.sleep(max(0.0, args.sleep_seconds))

    # Build registry rows with cross-run dedup (by title and URL).
    appended = []
    n = max_tgt
    for rec in candidates:
        nt, nu = _norm(rec["source_title"]), _norm(rec["stable_url"])
        if nt in existing_titles or nu in existing_urls:
            continue
        n += 1
        sid = "R02_OFF_TGT_%03d" % n
        while sid in existing_ids:
            n += 1
            sid = "R02_OFF_TGT_%03d" % n
        existing_ids.add(sid)
        existing_titles.add(nt)
        existing_urls.add(nu)
        license_note = ("Official web page; not downloaded; access/license to "
                        "confirm manually")
        if rec["source_type"] in ("official_open_data_catalogue", "official_data_source",
                                  "official_spatial_data"):
            license_note = ("Official catalogue/data page; dataset NOT downloaded; "
                            "access/license and data usability to confirm manually")
        appended.append({
            "source_id": sid,
            "institution": rec["institution"],
            "source_title": rec["source_title"],
            "english_working_title": rec["english_working_title"],
            "year": rec["year"],
            "stable_url": rec["stable_url"],
            "source_type": rec["source_type"],
            "geographic_coverage": rec["geographic_coverage"],
            "data_or_policy_domain": rec["data_or_policy_domain"],
            "relevance_to_tokyo_chinese_project": rec["relevance"],
            "use_in_analysis": rec["use_in_analysis"],
            "license_or_access_note": license_note,
            "verified_status": rec["verified_status"],
            "notes": ("Targeted official-source search round02; domain=%s; %s; "
                      "PDF link recorded only if applicable, file not downloaded; "
                      "manual verification recommended."
                      % (rec["domain_group"], rec["check_note"])),
        })

    if appended:
        write_header = not registry_csv.exists()
        with registry_csv.open("a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=REGISTRY_COLUMNS, extrasaction="ignore")
            if write_header:
                w.writeheader()
            for row in appended:
                w.writerow(row)

    # Local discovery outputs (never staged) ------------------------------
    cand_csv = out_dir / "official_source_candidates.csv"
    cand_cols = ["domain_group", "http_status", "verified_status", "institution",
                 "source_title", "english_working_title", "stable_url",
                 "source_type", "geographic_coverage", "data_or_policy_domain",
                 "use_in_analysis"]
    with cand_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cand_cols, extrasaction="ignore")
        w.writeheader()
        for rec in candidates:
            w.writerow(rec)
    with (out_dir / "official_source_candidates.jsonl").open("w", encoding="utf-8",
                                                             newline="\n") as f:
        for rec in candidates:
            f.write(json.dumps(rec, ensure_ascii=True) + "\n")

    # Coverage summary ----------------------------------------------------
    by_domain = {}
    by_status = {}
    for rec in candidates:
        by_domain[rec["domain_group"]] = by_domain.get(rec["domain_group"], 0) + 1
        by_status[rec["verified_status"]] = by_status.get(rec["verified_status"], 0) + 1
    s = []
    s.append("# Targeted Official-Source Search Coverage Summary (Round 02)")
    s.append("")
    s.append("Run id: %s" % args.run_id)
    s.append("Approach: curated known official/quasi-official landing pages + "
             "single lightweight reachability check (no crawl, no PDF/dataset "
             "download, no browser automation).")
    s.append("Max per domain: %d" % args.max_per_domain)
    s.append("Candidates checked: %d" % len(candidates))
    s.append("Rows appended to official_source_registry.csv: %d" % len(appended))
    s.append("")
    s.append("## Candidates by domain group")
    for g in sorted(by_domain):
        s.append("- %s: %d" % (g, by_domain[g]))
    s.append("")
    s.append("## Candidates by verification status")
    for k in sorted(by_status):
        s.append("- %s: %d" % (k, by_status[k]))
    s.append("")
    s.append("## Per-candidate")
    for rec in candidates:
        s.append("- [%s] %s | %s | %s | %s" % (
            rec["verified_status"], rec["source_title"], rec["domain_group"],
            rec["stable_url"], rec["check_note"]))
    s.append("")
    s.append("NOTE: Official-source discovery only. No datasets/PDFs downloaded. "
             "Licensing and data usability require manual checking. This does NOT "
             "confirm the research gap. Status: gap under verification.")
    (out_dir / "official_source_coverage_summary.md").write_text(
        "\n".join(s) + "\n", encoding="utf-8", newline="\n")

    print("RUN COMPLETE")
    print("candidates_checked:", len(candidates))
    print("rows_appended:", len(appended))
    print("by_domain:", json.dumps(by_domain, ensure_ascii=True))
    print("by_status:", json.dumps(by_status, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
