# Local Data-Folder Safety Audit - Tokyo-China Opportunity-Risk Project

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo: A Public-Data Analysis of Housing, Accessibility, Services, and Disaster
Exposure (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (.gitignore and local data-folder safety audit)

## A. Purpose

This note records the .gitignore and local data-folder safety checks performed
before any Tokyo-China official data acquisition. Its goal is to strengthen the
public-repository safety boundary so that future raw data, processed data, local
full text, temporary downloads, caches, credentials, PDFs, screenshots, and
large files cannot be accidentally committed to the public GitHub repository.

## B. Evidence boundary

- This is repository safety planning.
- It is NOT data acquisition.
- It is NOT analysis.
- It is NOT academic literature review.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No datasets or PDFs were downloaded.
- Current status remains: gap under verification.

## C. .gitignore audit result

- .gitignore existed: YES.
- .gitignore patched: YES (additive only; an appended "Tokyo-China data-
  acquisition safety" section; no existing rule or negation removed).
- Major categories now ignored:
  - A. Local raw/processed data: data/, data_raw/, data_processed/,
    data_interim/, data_external/, local_data/, downloads/, tmp_downloads/,
    scratch/, cache/
  - B. Literature/full-text: ref/, refs/, fulltext/, full_text/,
    local_fulltext/, literature_fulltext/, *.pdf
  - C. Office/manuscript: *.docx, *.doc, *.pptx, *.ppt, ~$*, TokyoProject.docx
  - D. Large geospatial/database: *.gpkg, *.shp, *.shx, *.dbf, *.prj, *.cpg,
    *.qpj, *.geojson, *.jsonl, *.sqlite, *.sqlite3, *.db, *.tif, *.tiff, *.vrt,
    *.zip, *.7z, *.rar
  - E. Credentials/environment: .env, .env.*, *.env, credentials/, secrets/,
    tokens/, *.key, *.pem, *.p12, *.json.credentials, *_credentials.json,
    *token*, *secret*, *appid*, *api_key*
  - F. Caches/temporary: __pycache__/, *.pyc, .ipynb_checkpoints/, .Rhistory,
    .RData, .DS_Store, Thumbs.db, *.log, *.tmp, *.bak, *.swp
  - G. Project raw-output folders: outputs/literature_discovery/,
    outputs/literature_verification/, outputs/tmp/, outputs/cache/, outputs/raw/
- outputs/claude_reports/ remains TRACKABLE (not ignored). Confirmed.
- outputs/literature_discovery/ and outputs/literature_verification/ remain
  IGNORED (now explicit). Confirmed via git check-ignore.

Note on already-tracked files: .gitignore does not untrack files already under
version control. The intentionally-tracked CSVs (literature_matrix.csv,
gap_verification_matrix.csv, and the force-added round02 matrices and metadata
control CSVs) and the Claude reports remain tracked and committable. The broad
patterns only affect NEW, untracked files.

## D. Local data-folder policy

Raw downloads should preferably be stored OUTSIDE the public repo until the user
explicitly approves another arrangement. Recommended local (outside-repo)
folders:

- E:\rsch\laborJapan_local_data\raw\
- E:\rsch\laborJapan_local_data\processed\
- E:\rsch\laborJapan_local_data\interim\
- E:\rsch\laborJapan_local_data\metadata\
- E:\rsch\laborJapan_local_fulltext\
- E:\rsch\laborJapan_local_temp\

## E. In-repo ignored folders

If the user later chooses in-repo local storage, use these ignored folders:

- data_raw/
- data_processed/
- data_interim/
- data_external/
- downloads/
- scratch/

These folders should remain ignored unless there is explicit user approval and
license clearance for the specific data placed in them.

## F. Tracked-file risk audit

Results of the git ls-files risk search (107 tracked files total):

- tracked PDFs found: 0
- tracked DOCX found: 0
- tracked data/geospatial/archive files found: 0 (no .shp/.gpkg/.zip/.7z/.rar/
  .tif/.sqlite/.db/.parquet under version control)
- tracked credential-like files found: 0
- tracked raw-output folders found: 0 (nothing tracked under
  outputs/literature_discovery/ or outputs/literature_verification/)
- high-risk tracked files requiring user decision: 0

One low-risk tracked file under data/: data/data_sources.md - a markdown
documentation file (a list of sources), NOT raw data. It remains tracked; the
new data/ ignore rule only affects new files added under data/ (verified:
data/newraw.txt, data/raw/x.tif are ignored while data/data_sources.md stays
trackable). No action required.

Sensitive keyword content scan (token, secret, api_key, appid, password,
CINII_APP_ID) over tracked files: all hits are non-secret references - the
env-variable NAME CINII_APP_ID in protocol notes and the harvest scripts (which
read it via os.environ.get(...) and do NOT hardcode any value), the word
"secret" inside this round's safety guidance, and "token" appearing in
literature matrices and uv.lock. No actual credential, API key, or password
value is committed. Result: PASS.

## G. Untracked sensitive-file audit

Before the patch, git status showed these untracked items, all of which were
left untouched and NOT staged: TokyoProject.docx, ref/,
outputs/literature_discovery/, outputs/literature_verification/. After the
patch these are now ignored (they no longer appear in git status). No data
folders, PDFs, DOCX, archives, or credential files were staged. The only staged
working-tree change relevant to tracking is .gitignore itself plus this audit
note and the Claude reports.

## H. Future acquisition safety rules

- No raw data should be committed by default.
- No PDFs or full text should be committed.
- No credentials or API keys should be written to the repo.
- Every future data download requires a decision-log entry
  (metadata/data_download_decision_log.csv).
- Every future downloaded file requires a metadata record
  (metadata/official_data_source_metadata_template.csv).
- A checksum (SHA-256) should be computed after download.
- Processing scripts may be committed, but raw data should remain ignored unless
  explicitly approved.
- Public-repo commit permission must be checked source by source.

## I. Recommended next repo task

Recommended next task: prepare a data acquisition approval package for the first
P1 source group, starting with the population-baseline sources (ISA / e-Stat).
It should list the exact tables to check manually, the decision-log rows to
approve (DDL_001, DDL_002, and the derived DDL_003), the metadata fields to fill,
and a clear statement that NO download occurs until the user approves.

Do not recommend immediate bulk download. Do not recommend writing the final
Introduction yet. Status remains: gap under verification.
