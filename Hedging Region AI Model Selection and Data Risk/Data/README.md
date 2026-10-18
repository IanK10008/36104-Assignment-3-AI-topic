# Data: Q1 dataset notebooks

Seven datasets feed Q1 (notebooks 01 to 07), and three optional ones add context (08, 09 and 10) (which AI models matter where leading closed US models are restricted). Each has its own folder with one notebook, the files the notebook downloaded (`raw/`) and the tables it built (`processed/`).
Q1 相關的 7 個資料集，每個資料夾各有一支 notebook、自動下載的原始檔（`raw/`）和整理後的表（`processed/`）。

Every notebook has the same layout: purpose, source links and authorisation, table structure, set up, acquire, inspect, transform, validate, save, data currency, run time and limits, references.
Style follows the Assignment 2 Part C notebook template and `a3_p2_attention_app/notebooks/01_data_extraction.ipynb`.

| Folder | Dataset | Output tables | Kind | Expected run time |
|---|---|---|---|---|
| `01_epoch_eci_scores` | Epoch Capabilities Index | `model_capability.csv` | download, 1 CSV | under 10 s |
| `02_search_a_provider_data_handling` | Search A, provider data handling | `provider_data_handling.csv` | hand-built, 12 rows | under 2 s |
| `03_search_c_provider_availability` | Search C, provider availability | `provider_availability.csv` | hand-built, 28 rows | under 2 s |
| `04_litellm_prices` | LiteLLM price JSON | `model_price.csv` | download, 2.9 MB | under 20 s |
| `05_search_b_jurisdiction_rules` | Search B, jurisdiction rules | `jurisdiction_rules.csv`, `jurisdiction_sources.csv`, `financial_regulator_pages.csv` | hand-built | under 2 s |
| `06_lmarena_leaderboard` | LMArena text leaderboard | `lmarena_ratings.csv` | download from Hugging Face | 5 to 30 s |
| `07_epoch_benchmark_scores` | Epoch per-benchmark CSVs | `benchmark_scores.csv`, `benchmark_catalogue.csv`, `benchmark_model_metadata.csv` | download, 2.4 MB ZIP | under 30 s |
| `08_fmti_transparency` | Stanford FMTI, December 2025 (Q5 context) | `fmti_indicator_scores.csv`, `fmti_company_scores.csv`, `fmti_indicators.csv` | GitHub ZIP, about 15 MB, or the saved `Data/raw/manual/fmti-main.zip` | under 30 s |
| `10_aiid_incidents` | AI Incident Database weekly export (Q6) | `incidents.csv`, `incident_developers.csv`, `incidents_by_developer_year.csv` | download, 2.6 MB Excel, or the saved file in `raw/manual/` | under 30 s |
| `09_epoch_ai_models` | Epoch AI models table (Q2 compute and cost context) | `ai_models.csv`, `ai_models_columns.csv` | download, 1 CSV. Save by hand into `raw/epoch/` if blocked | under 20 s |

Notebooks 01 to 07 together run in about **one to two minutes**. The three hand-built datasets (02, 03, 05) took reading time rather than code time, and their rows come from `04 Searches A B C`.

Every folder also gets `processed/data_currency.csv`: the day the notebook ran, the dates the data covers, the snapshot note, the source's start note and its update frequency.
每個資料夾都會輸出 `processed/data_currency.csv`，記錄抽取日、資料涵蓋日期、來源起始與更新頻率。

## To run

1. Python 3.10 or newer with `pandas`, `requests`, `pyarrow` and `jupyter` (or VS Code). `pip install pandas requests pyarrow jupyter`
2. Open a notebook and choose Run All. Start with 01, then 02 to 10 in any order. Notebooks 02 and 03 run a join test against 01 if 01 has been run.
3. If a download is blocked, see `raw/README.md` for the manual route.

## Not built yet

- The model crosswalk (`model_crosswalk.csv`) that maps names across Epoch (01, 07), LiteLLM (04), LMArena (06) and Search A (02). It is the biggest Q1 risk.
- Not built by decision: Wikimedia pageviews (struck), the PCPD PDFs (read by hand, no table). Notebook 09 was tested only on a made-up table, so its first real run is the real test.
- Open items: MAS general terms (address https://www.mas.gov.sg/terms-of-use is recorded but its text is still unread, our tool could not load it), Epoch Creative Commons version (closed for the benchmarking data, 2026-10-18: https://epoch.ai/benchmarks/about states CC BY 4.0, the ECI chart page still to be checked), (closed on 2026-10-18: the regulator-page addresses in notebook 05 were checked by a team member, and both PCPD PDFs are CC BY 4.0 with addresses recorded), and MiniMax is missing from Search A.

## Updating

Every notebook has an "At a glance" table near the top (links, licence, authorisation, download size, timing) and a "How to update" section before the run-time section. Short version:

- Automatic: 01, 04, 06 and 07 download fresh data every time you run them.
- By hand: 02, 03 and 05 have nothing to download. Re-read the pages listed in each notebook and edit the records.
- If a download is blocked, save the file by hand into `raw/<source>/` using the link and file name in that notebook. The notebook uses the newer of the saved copy and its own earlier download.
- Check `raw/retrieval_log.json` (`how` says `downloaded` or `copied from manual folder`) and `processed/data_currency.csv` after every update.
