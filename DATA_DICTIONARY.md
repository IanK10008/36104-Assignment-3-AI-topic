# Data dictionary

This file describes every dataset that the pages of the app read from the `data/` folders of the four stories. It covers 16 file paths. Three of them are identical copies of one file, so the file has 14 sections. Appendix A lists the supporting files outside the `data/` folders.

**How the facts were collected.** Column types, ranges, row counts, time coverage and primary keys were read from the data files with pandas on 20 Nov 2026. A primary key was accepted only when the column set had no duplicate and no missing value. The file names were compared with the folders of the repository on 20 Nov 2026 and every one exists. Source, URL, licence and dates come only from the `docs.md` files, `DATA_DICTIONARY_V3.md` and `DATA_DICTIONARY_4B.md` in `stories/2_gap_to_us_models/`, the Sources lists in `src/views.py` and `src/views_story3.py` (shown by `src/shell.py`), the `data_currency.csv` and `retrieval_log.json` files of the notebooks, and the data files themselves. A fact that none of these states is written as "Not stated in the repository". The rows "Update frequency" and "Source type" were added on 21 Nov 2026 from the source pages: the Epoch AI Benchmarking Hub post of 7 Feb 2025, the AI Incident Database snapshots page, the 2025 Foundation Model Transparency Index paper and the LiteLLM contribution guide.

**Licence versions.** The `docs.md` files describe the Epoch AI licence as Creative Commons Attribution with the version not stated on the page read. The Sources list in `src/views.py` states CC BY 4.0. The two statements are given side by side below because the page read does not give the version.

**Notebooks.** The `docs.md` files name the notebooks that write each file. Every notebook named below is present in this copy of the repository, under `stories/<story>/notebooks/<notebook folder>/`. The dictionary describes the files and the notebook steps as the `docs.md` files record them. All notebooks were run with a fresh download on 20 Nov 2026 (UTC). The Story 2 Benchmarking Hub tables were rebuilt on 20 Nov 2026 from the downloaded ZIP after the capability file of Story 2 had changed.

**Copy step.** In every story the notebooks write to `processed/`. A member then copies the file into `data/` by hand. The notebooks never write to `data/`.

**Not legal advice.** The licence readings in this file and in the app are the group's reading. They are not legal advice.

---

## 1. Story 1a: `stories/1a_ranked_shortlist/data/model_capability.csv`

| Item | Value |
|---|---|
| Source organisation | Epoch AI (Epoch Capabilities Index, file `eci_scores.csv`) |
| URL | https://epoch.ai/benchmarks/eci (Sources list in `src/views.py`). Data licence page https://epoch.ai/data |
| Licence | Creative Commons Attribution, version not stated (`docs.md`). CC BY 4.0 (`src/views.py`) |
| Retrieval date | 20 Nov 2026 13:02 UTC (`notebooks/eci_scores/raw/retrieval_log.json` and `notebooks/eci_scores/processed/data_currency.csv`) |
| Update frequency | Epoch gives no update schedule. Its post of 7 Feb 2025 says the benchmarking database is updated more often than before. The file here is the snapshot of 20 Nov 2026 |
| Source type | Live source on epoch.ai, kept as a submitted snapshot (CSV and `retrieval_log.json` in `notebooks/eci_scores/raw/`) |
| Row count | 257 rows, 16 columns |
| Primary key | `model` (unique, no missing value). `display_name` is also unique |
| Time coverage | `release_date` 2023-02-24 to 2026-11-17 |
| Latest observation | Model released 2026-11-17 |
| Transform | `notebooks/eci_scores/eci_scores.ipynb` (copy of notebook 01) writes `processed/model_capability.csv`, which is copied by hand into `data/`. The md5 of the `processed/` file equals the md5 of the `data/` file (`62a74a58d048b0681e774a1822fe33c0`, checked 20 Nov 2026) |
| Note | This file has the same md5 as the copies used in Stories 1b, 2 and 3 (section 4) |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| model | text | model name used to match the sources | 257 unique |
| display_name | text | model name shown in the app | 257 unique |
| eci | float | Epoch Capabilities Index points | 48.59 to 174.17 |
| eci_ci_low | float | lower bound of Epoch's 90% interval, index points | 25.79 to 170.29, 2 missing |
| eci_ci_high | float | upper bound of Epoch's 90% interval, index points | 67.73 to 178.58, 2 missing |
| eci_rank | integer | rank by `eci`, 1 is highest | 1 to 257 |
| release_date | date (text, YYYY-MM-DD) | release date | 2023-02-24 to 2026-11-17 |
| organization | text | developer as given by Epoch | 29 values, 16 missing |
| organization_primary | text | first or main developer | 27 values, 16 missing |
| country | text | developer country | 5 values, 16 missing |
| is_china_based | boolean | developer based in China | True or False |
| epoch_accessibility | text | Epoch accessibility label | 7 values, for example "API access", "Open weights (unrestricted)" |
| epoch_accessibility_group | text | grouped accessibility label | 3 values, for example "Closed weights" |
| access_class_epoch | text | access class derived from Epoch's label | 4 values, for example `api_only` |
| licence_class_ours | text | the group's licence class | `api_only`, `not_reviewed`, `custom_threshold`, `mit`, `apache_2_0` |
| licence_basis | text | licence name, short reading and author-date citation read by the group | 5 values, 252 missing |

## 2. Story 1a: `stories/1a_ranked_shortlist/data/model_price.csv`

| Item | Value |
|---|---|
| Source organisation | BerriAI LiteLLM (community-maintained), file `model_prices_and_context_window.json` |
| URL | https://github.com/BerriAI/litellm |
| Licence | MIT, except the `enterprise/` directory, which has its own licence. The price JSON sits at the repository root (`docs.md`, checked 18 Oct 2026) |
| Retrieval date | 20 Nov 2026 13:03 UTC. The source file carries no date of its own (`notebooks/litellm_prices/raw/retrieval_log.json`) |
| Update frequency | No fixed schedule. The file on GitHub changes whenever a pull request adds or edits a model or a price. The file here is the snapshot of 20 Nov 2026 |
| Source type | Live source on GitHub, kept as a submitted snapshot (JSON and `retrieval_log.json` in `notebooks/litellm_prices/raw/`) |
| Row count | 6,929 rows, 18 columns |
| Primary key | `model_key` (unique, no missing value) |
| Time coverage | Current list prices at the retrieval date. The only date column is `deprecation_date`, 2025-06-16 to 2028-05-20 (1,246 rows filled) |
| Latest observation | Snapshot of 20 Nov 2026 13:03 UTC |
| Transform | `notebooks/litellm_prices/litellm_prices.ipynb` (copy of notebook 04) writes `processed/model_price.csv`, copied by hand into `data/`. The notebook drops 108 pointer entries (`alias_of`) and one routing block and stops on any other entry without a host (`docs.md`) |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| model_key | text | LiteLLM model key | 6,929 unique |
| litellm_provider | text | provider name | 157 values |
| key_prefix | text | prefix of the key | 143 values, 733 missing |
| model_stem | text | key without the prefix | 3,276 values |
| mode | text | model mode, for example `chat`, `embedding` | 19 values, 44 missing |
| input_usd_per_million | float | US dollars per million input tokens | 0 to 150, 2,010 missing |
| output_usd_per_million | float | US dollars per million output tokens | 0 to 600, 2,037 missing |
| cache_read_usd_per_million | float | US dollars per million cached input tokens | 0 to 29.99997, 4,751 missing |
| max_input_tokens | float | tokens | 0 to 10,485,760, 2,111 missing |
| max_output_tokens | float | tokens | 0 to 10,000,000, 2,509 missing |
| supports_function_calling | text (True or False) | flag | 3,214 missing |
| supports_vision | text (True or False) | flag | 3,609 missing |
| supports_reasoning | text (True or False) | flag | 4,508 missing |
| supports_prompt_caching | text (True or False) | flag | 5,149 missing |
| supported_regions | text | cloud region | 3 values, 6,914 missing |
| deprecation_date | date (text, YYYY-MM-DD) | date | 2025-06-16 to 2028-05-20, 5,683 missing |
| source_url | text | URL of the provider's price page | 1,334 missing |
| family | text | model family | 5 values, 5,241 missing |

## 3. Story 1a: `stories/1a_ranked_shortlist/data/lmarena_ratings.csv`

| Item | Value |
|---|---|
| Source organisation | LMArena (now Arena), text leaderboard |
| URL | https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset |
| Licence | CC BY 4.0 (`docs.md`, checked 18 Oct 2026) |
| Retrieval date | Downloaded 20 Nov 2026 13:04 UTC, leaderboard published 19 Nov 2026 (`notebooks/lmarena_leaderboard/raw/retrieval_log.json` and `processed/data_currency.csv`) |
| Update frequency | No fixed schedule found. LMArena publishes its leaderboard with a publish date. The file here holds the one published on 19 Nov 2026 |
| Source type | Live leaderboard, kept as a submitted snapshot (Parquet file and `retrieval_log.json` in `notebooks/lmarena_leaderboard/raw/`) |
| Row count | 11,291 rows, 12 columns |
| Primary key | `model_name` + `category` (unique, no missing value) |
| Time coverage | One snapshot. `leaderboard_publish_date` is 2026-11-19 in every row |
| Latest observation | Leaderboard of 2026-11-19 |
| Transform | `notebooks/lmarena_leaderboard/lmarena_leaderboard.ipynb` (copy of notebook 06) writes `processed/lmarena_ratings.csv`, copied by hand into `data/` |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| model_name | text | model name on the leaderboard | 426 values |
| organization | text | developer | 28 values, 1,103 missing |
| license | text | licence label on the leaderboard | 40 values, for example "Proprietary" |
| rating | float | LMArena rating points | 533.73 to 1,628.95 |
| rating_lower | float | lower bound of the rating interval, rating points | 508.98 to 1,596.40 |
| rating_upper | float | upper bound of the rating interval, rating points | 558.49 to 1,661.49 |
| variance | float | variance of the rating, as published | 1.47 to 1,384.97 |
| vote_count | float | votes | 58 to 194,909 |
| rank | float | rank in the category | 1 to 426 |
| category | text | leaderboard category | 29 values, for example `chinese` |
| leaderboard_publish_date | date (text, YYYY-MM-DD) | publication date | 2026-11-19 |
| is_overall | boolean | row of the overall category | True or False |

## 4. Stories 1b, 2 and 3: `model_capability.csv` (one file, three identical copies)

Paths: `stories/1b_licence_route/data/model_capability.csv`, `stories/2_gap_to_us_models/data/model_capability.csv` and `stories/3_reported_incidents/data/model_capability.csv`. The three copies have the same md5 (`62a74a58d048b0681e774a1822fe33c0`), which is also the md5 of the Story 1a file in section 1.

| Item | Value |
|---|---|
| Source organisation | Epoch AI (Epoch Capabilities Index, file `eci_scores.csv`) |
| URL | https://epoch.ai/benchmarks/eci (Sources list in `src/views.py`). Data licence page https://epoch.ai/data |
| Licence | Creative Commons Attribution, version not stated (`docs.md` of Stories 1b, 2 and 3). CC BY 4.0 (`src/views.py`) |
| Retrieval date | 20 Nov 2026 (Story 1b 13:04 UTC, Story 2 13:07 UTC and Story 3 13:08 UTC, from the `retrieval_log.json` of each `eci_scores` notebook) |
| Update frequency | Epoch gives no update schedule. Its post of 7 Feb 2025 says the benchmarking database is updated more often than before. The file here is the snapshot of 20 Nov 2026 (same file as section 1) |
| Source type | Live source on epoch.ai, kept as a submitted snapshot (CSV and `retrieval_log.json` in each story's `notebooks/eci_scores/raw/`) |
| Row count | 257 rows, 16 columns |
| Primary key | `model` (unique, no missing value). `display_name` is also unique |
| Time coverage | `release_date` 2023-02-24 to 2026-11-17 |
| Latest observation | Model released 2026-11-17 |
| Transform | `notebooks/eci_scores/eci_scores.ipynb` of each story writes `processed/model_capability.csv`, copied by hand into `data/` (`docs.md` of Stories 1b, 2 and 3). Story 1b records a rebuild from zero in a fresh virtual environment that gave the same content (277 rows, 16 columns, for the download of 17 Oct 2026) |
| Used by | Story 1b Views 1 and 2, Story 2 Views 1 to 3 (access group), Story 3 View 2 (model releases) |

The columns, types and units are the same as in section 1. The ranges differ as follows.

| Column | Range or note |
|---|---|
| model, display_name | 257 unique |
| eci | 48.59 to 174.17 |
| eci_ci_low | 25.79 to 170.29, 2 missing |
| eci_ci_high | 67.73 to 178.58, 2 missing |
| eci_rank | 1 to 257 |
| release_date | 2023-02-24 to 2026-11-17 |
| organization | 29 values, 16 missing |
| organization_primary | 27 values, 16 missing |
| country | 5 values, 16 missing |
| licence_basis | 5 values, 252 missing |
| licence_class_ours | the group's own reading, which must not be credited to Epoch (`docs.md` of Story 1b) |

## 5. Story 1b: `stories/1b_licence_route/data/licence_terms.json`

| Item | Value |
|---|---|
| Source organisation | The project group, with AI reading by Claude (`docs.md` of Story 1b). Written by hand from the licence notes file `licence_check_2024_2026_2026-11-18.md` and `licence_summary_2024_2026.csv` kept by the group, which sit outside this repository. The notes read the licence pages of the model developers on Hugging Face and GitHub |
| URL | One licence link per record in the field `url` |
| Licence | The licence of the file is Not stated in the repository. The model licences it describes are those of each developer |
| Retrieval date | Licences read 18 Nov 2026. The reading is AI work (Claude). The provenance matrix records Rida as reviewer of the reading (19 Nov 2026). It is not legal advice |
| Update frequency | None. The group wrote the file once from licence pages read on 18 Nov 2026 and has not updated it since |
| Source type | Group-made record built from public licence pages. It is not a download of an existing dataset |
| Row count | 51 records (JSON list), 15 fields per record, 6 cells per record |
| Primary key | `model` (51 unique values) |
| Time coverage | `release` 2024-02-20 to 2026-10-29 |
| Latest observation | Model released 2026-10-29 |
| Transform | No notebook. The file is written by hand from the notes. The model list is the union of the Epoch file of 12 Nov 2026 and the Epoch file of 17 Oct 2026. It keeps the models that Epoch labels restricted use, non-commercial or unknown, released 2024 to 2026 (`docs.md`). Against the Epoch file of 20 Nov 2026, 45 models with these labels are all covered, and six records are no longer in that file (Command R+, Llama 3.2 1B, Mistral Large 2 of Nov 2024, Gemma 3 12B, Gemma 3 4B and MiniMax-M2.7). `licence_terms.py` reads it for View 3 |

| Field | Type | Unit or values | Range or note |
|---|---|---|---|
| model | text | model name | 51 unique |
| group | text | developer group shown in the matrix | for example "Alibaba Qwen" |
| fam | text | licence family key | for example `tongyi` |
| year | integer | release year | 2024 to 2026 |
| release | date (text, YYYY-MM-DD) | release date | 2024-02-20 to 2026-10-29 |
| org | text | organisation, may be empty | text |
| e12 | text | Epoch label in the 12 Nov 2026 file | for example "Unknown" |
| e17 | text | Epoch label in the 17 Oct 2026 file | for example "Unknown" |
| licence | text | licence name and version | text |
| cells | list of 6 lists | [state, short text, evidence] for the six licence terms: commercial use, revenue or user threshold, hosting or MaaS, attribution or notice, use policy, output or derivative rule | states `ok` 126, `cond` 136, `unk` 24, `block` 11, `na` 9 |
| ev | text | evidence level | `full` 42, `part` 5, `assumed` 3, `na` 1 |
| conf | text | evidence sentence | for example "Read in full (LICENSE file)" |
| terms | list of text | full licence note | text |
| gap | text | difference between Epoch's label and the licence text | text |
| url | text | licence page | URL |

## 6. Story 2: `stories/2_gap_to_us_models/data/hub_scores_by_model.csv`

| Item | Value |
|---|---|
| Source organisation | Epoch AI Benchmarking Hub (`benchmark_data.zip`, 58 benchmark files and `benchmark_metadata.csv`) |
| URL | https://epoch.ai/data/benchmark_data.zip |
| Licence | CC BY 4.0, as stated on the Epoch benchmarking pages (`DATA_DICTIONARY_4B.md`). Epoch's pages add that data taken from external projects keeps its original licence (checked 21 Nov 2026) |
| Retrieval date | ZIP downloaded 20 Nov 2026 13:06:42 UTC (`notebooks/benchmark_hub/raw/retrieval_log.json`). Table extracted 2026-11-20T15:51:35Z (`hub_data_currency.csv`) |
| Update frequency | Epoch gives no update schedule. Its post of 7 Feb 2025 says the benchmarking database is updated more often than before. The ZIP here is the download of 20 Nov 2026 |
| Source type | Live source on epoch.ai, kept as a submitted snapshot (`benchmark_data.zip` and `retrieval_log.json` in `notebooks/benchmark_hub/raw/`) |
| Row count | 2,128 rows, 7 columns, 168 models, 57 benchmarks |
| Primary key | `model` + `benchmark` + `kind` (unique, no missing value) |
| Time coverage | `release_year` 2023 to 2026 |
| Latest observation | ZIP downloaded 20 Nov 2026. Latest release year 2026 |
| Transform | `notebooks/benchmark_hub/benchmark_hub.ipynb` reads the benchmark files, labels each row by kind of source, matches Hub versions to capability models (508 of 957 versions), keeps the highest score per model, benchmark and kind, runs checks and writes the file (`DATA_DICTIONARY_4B.md`) |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| model | text | model name as in `model_capability.csv` | 168 values |
| release_year | integer | year | 2023 to 2026 |
| access_group | text | `accessible` or `restricted` | 2 values |
| benchmark | text | benchmark name in the Hub | 57 values |
| kind | text | `epoch`, `third_party` or `developer` | 3 values |
| source | text | `Epoch run` or the source name given in the Hub | 69 values |
| score_pct | float | percent (0 to 100 scale) | 0 to 100 |

## 7. Story 2: `stories/2_gap_to_us_models/data/hub_model_coverage.csv`

| Item | Value |
|---|---|
| Source organisation | Derived from the Epoch AI Benchmarking Hub and the Epoch Capabilities Index file |
| URL | https://epoch.ai/data/benchmark_data.zip |
| Licence | CC BY 4.0 (`DATA_DICTIONARY_4B.md`). Data taken from external projects keeps its original licence, as in section 6 |
| Retrieval date | As section 6 |
| Update frequency | As section 6 |
| Source type | As section 6. This table is derived from the ZIP by the notebook |
| Row count | 10 rows, 4 columns |
| Primary key | `release_year` + `access_group` (unique, no missing value) |
| Time coverage | `release_year` 2023 to 2026 |
| Latest observation | Release year 2026 |
| Transform | Written by `notebooks/benchmark_hub/benchmark_hub.ipynb` |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| release_year | integer | year | 2023 to 2026 |
| access_group | text | `accessible`, `restricted` or `excluded` | 3 values |
| models_in_capability_file | integer | models | 6 to 46 |
| models_with_hub_scores | float (whole numbers) | models with at least one score | 0 to 43 |

## 8. Story 2: `stories/2_gap_to_us_models/data/hub_data_currency.csv`

| Item | Value |
|---|---|
| Source organisation | The notebook run (data stamp of the Hub extract) |
| URL | https://epoch.ai/data/benchmark_data.zip |
| Licence | CC BY 4.0 for the underlying Hub data (`DATA_DICTIONARY_4B.md`) |
| Retrieval date | `zip_retrieved_utc` 2026-11-20T13:06:42Z (download time of the ZIP), `zip_how` = reused |
| Update frequency | Not applicable. One row, written by the notebook each time it runs |
| Source type | Group-made log of the Hub download, written by `benchmark_hub.ipynb` |
| Row count | 1 row, 9 columns |
| Primary key | `dataset` (one row) |
| Time coverage | Not applicable (one stamp) |
| Latest observation | `extracted_utc` 2026-11-20T15:51:35Z |
| Transform | Written by `notebooks/benchmark_hub/benchmark_hub.ipynb` |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| dataset | text | dataset name | 1 value |
| extracted_utc | timestamp (text, ISO 8601 UTC) | time of the notebook run | 2026-11-20T15:51:35Z |
| zip_retrieved_utc | text | time the ZIP was downloaded | 2026-11-20T13:06:42Z |
| zip_how | text | `downloaded` or `reused` | `reused` |
| zip_sha256 | text | SHA-256 hash of the ZIP | 64 hex characters |
| scores | integer | score rows | 2,128 |
| models | integer | models | 168 |
| benchmarks | integer | benchmarks | 57 |
| note | text | note on the release year and access group | text |

## 9. Story 2: `stories/2_gap_to_us_models/data/gpqa_reported_vs_epoch.csv`

| Item | Value |
|---|---|
| Source organisation | Epoch AI, article "AI developers accurately report GPQA Diamond scores for recent models" (Jaeho Lee and Yafah Edelman), with the developer disclosures it cites |
| URL | https://epoch.ai/data-insights/self-reported-gpqa |
| Licence | Not verified for the comparison table of this web page. Reuse permission must be checked with Epoch before a repackaged dataset is published (`DATA_DICTIONARY_V3.md`) |
| Retrieval date | Transcribed by hand on 14 Nov 2026, with no retrieval log. Article of 19 Sep 2025 |
| Update frequency | None. The article is dated 19 Sep 2025 and the table was copied once on 14 Nov 2026 |
| Source type | Hand transcription of a table in a published article. A fixed snapshot |
| Row count | 8 rows, 12 columns |
| Primary key | `model` (unique, no missing value) |
| Time coverage | A selection of frontier models up to 2025. Not a time series. The file has no date column |
| Latest observation | Article of 19 Sep 2025 |
| Transform | Hand transcription of the article's table into `notebooks/eci_scores/raw/epoch_article_gpqa_table.csv`, with the same content in `data/`. `load_gpqa` in `v3_difference.py` checks the values and adds `access_group`, `difference_pp` and `in_band` when the page loads (`DATA_DICTIONARY_V3.md`) |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| model | text | model display name in the article | 8 unique |
| developer_reported_pct | float | % correct on GPQA Diamond | 48.6 to 87.5 |
| epoch_independent_pct | float | % correct on GPQA Diamond | 51.3 to 87.0 |
| epoch_standard_error_pp | float | percentage points | 2.0 to 3.2 |
| epoch_90ci_halfwidth_pp | float | percentage points (1.645 times the standard error) | 3.29 to 5.26 |
| developer_report_type | text | `developer_report` or `third_party_endorsed` | 2 values |
| source_page | text | URL of the article | 1 value |
| developer_source | text | URL of the developer page | 8 values |
| reference_model | text | Epoch's identifier of the model run | 8 values |
| notes | text | test setting or exception | 2 values, 6 missing |
| difference_pp | float | percentage points (developer-reported minus Epoch independent) | -2.7 to 2.8 |
| within_epoch_90ci | boolean | the difference lies inside Epoch's 90% interval | True in all 8 rows |

## 10. Story 3: `stories/3_reported_incidents/data/aiid_model_incidents_by_developer.csv`

| Item | Value |
|---|---|
| Source organisation | Responsible AI Collaborative, AI Incident Database (weekly Excel export, sheet `Incidents`). Risk domains from the MIT AI Risk Repository as carried in the export. Group labels in `notebooks/aiid_model_incidents/manual/aiid_incident_labels.csv` and `notebooks/aiid_model_incidents/manual/aiid_assigned_mit_domain.csv` (Appendix A) |
| URL | https://incidentdatabase.ai/research/snapshots/ (AIID) and https://airisk.mit.edu/ (MIT) |
| Licence | CC BY-SA 4.0 for the AIID collections, checked on the AIID terms of use on 21 Nov 2026. This file holds no report text. MIT AI Risk Repository licence not read (`docs.md`). The group labels are the group's own work |
| Retrieval date | Export of 16 Nov 2026, retrieved 20 Nov 2026 14:25 UTC (`notebooks/aiid_model_incidents/raw/retrieval_log.json`) |
| Update frequency | AIID publishes weekly snapshots of its database (incidentdatabase.ai/research/snapshots). The group's labels were added on 20 Nov 2026 to the export of 16 Nov 2026 |
| Source type | Derived from a snapshot of a live database (AIID export of 16 Nov 2026) and the group's incident labels |
| Row count | 406 rows (one per incident and named developer), 343 incidents, 14 columns |
| Primary key | `incident_id` + `developer` (unique, no missing value) |
| Time coverage | `date` 2020-03-23 to 2026-10-29 |
| Latest observation | Incident of 2026-10-29 |
| Transform | `notebooks/aiid_model_incidents/aiid_model_incidents.ipynb` writes `processed/aiid_model_incidents_by_developer.csv`, copied by hand into `data/` |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| incident_id | integer | AIID incident number | 85 to 1,828 |
| date | date (text, YYYY-MM-DD) | incident date | 2020-03-23 to 2026-10-29 |
| year | integer | year | 2020 to 2026 |
| developer | text | one of the 11 developers in scope | 9 values present |
| found_in | text | field where the developer was found | 2 values, for example "developer field" |
| title | text | incident title | 343 values |
| mit_risk_domain | text | MIT risk domain | 7 values, 99 missing |
| mit_risk_subdomain | text | MIT risk subdomain | 17 values, 99 missing |
| group_mit | text | incident type from the MIT domain | 5 values |
| report_count | integer | reports | 1 to 58 |
| assigned_domain | text | domain assigned by the group where MIT had none | 5 values, 307 missing |
| type_source | text | `MIT` or `Project group` | 2 values |
| domain_shown | text | domain shown in the app | 7 values |
| group | text | incident type shown in the app | "Wrong output or failure", "Harm to users or society", "Misuse by others", "Data and security" |

## 11. Story 3: `stories/3_reported_incidents/data/incidents.csv`

| Item | Value |
|---|---|
| Source organisation | Responsible AI Collaborative, AI Incident Database |
| URL | https://incidentdatabase.ai/research/snapshots/ |
| Licence | CC BY-SA 4.0 for the incidents collection, checked on the AIID terms of use on 21 Nov 2026. The report text field and user submissions are not under that licence and this file holds neither. The terms bar selling or commercially exploiting the site without permission |
| Retrieval date | Weekly export dated 16 Nov 2026, retrieved 20 Nov 2026 13:07 UTC and table extracted 13:07 UTC (`notebooks/aiid_incidents/raw/retrieval_log.json` and `processed/data_currency.csv`). The notebook `aiid_model_incidents` downloaded the same export at 14:25 UTC |
| Update frequency | AIID publishes weekly snapshots of its database (incidentdatabase.ai/research/snapshots). The file here uses the export dated 16 Nov 2026 |
| Source type | Snapshot of a live database (AIID weekly export of 16 Nov 2026, kept in `notebooks/aiid_incidents/raw/`) |
| Row count | 1,815 rows, 10 columns |
| Primary key | `incident_id` (unique, no missing value) |
| Time coverage | `date` 1983-09-26 to 2026-11-12 |
| Latest observation | Incident of 2026-11-12 |
| Transform | From the earlier version of the Story 3 page, notebook `notebooks/aiid_incidents/aiid_incidents.ipynb` (`docs.md`). Story 3 Views 1 and 2 do not read this file. `src/aiid.py` describes it |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| incident_id | integer | AIID incident number | 1 to 1,828 |
| date | date (text, YYYY-MM-DD) | incident date | 1983-09-26 to 2026-11-12 |
| year | integer | year | 1983 to 2026 |
| title | text | incident title | 1,815 unique |
| developer_raw | text | alleged developer as recorded | 755 values, 1 missing |
| deployer_raw | text | alleged deployer as recorded | 1,329 values, 3 missing |
| report_count | integer | reports | 0 to 58 |
| named_developers | text | named developers after cleaning | 40 values, 1,231 missing |
| is_generative_related | boolean | flag | True or False |
| has_named_developer | boolean | flag | True or False |

## 12. Story 3: `stories/3_reported_incidents/data/incident_developers.csv`

| Item | Value |
|---|---|
| Source organisation | Responsible AI Collaborative, AI Incident Database |
| URL | https://incidentdatabase.ai/research/snapshots/ |
| Licence | CC BY-SA 4.0 for the incidents collection, checked on the AIID terms of use on 21 Nov 2026. The report text field and user submissions are not under that licence and this file holds neither. The terms bar selling or commercially exploiting the site without permission |
| Retrieval date | Weekly export dated 16 Nov 2026, retrieved 20 Nov 2026 13:07 UTC and table extracted 13:07 UTC (`notebooks/aiid_incidents/raw/retrieval_log.json` and `processed/data_currency.csv`) |
| Update frequency | AIID publishes weekly snapshots of its database (incidentdatabase.ai/research/snapshots). The file here uses the export dated 16 Nov 2026 |
| Source type | Snapshot of a live database (AIID weekly export of 16 Nov 2026, kept in `notebooks/aiid_incidents/raw/`) |
| Row count | 3,305 rows, 8 columns |
| Primary key | `incident_id` + `developer_raw_entity` (unique, no missing value) |
| Time coverage | `date` 1983-09-26 to 2026-11-12 |
| Latest observation | Incident of 2026-11-12 |
| Transform | From the earlier version of the Story 3 page, notebook `notebooks/aiid_incidents/aiid_incidents.ipynb` (`docs.md`). Story 3 Views 1 and 2 do not read this file |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| incident_id | integer | AIID incident number | 1 to 1,828 |
| date | date (text, YYYY-MM-DD) | incident date | 1983-09-26 to 2026-11-12 |
| year | integer | year | 1983 to 2026 |
| developer_raw_entity | text | one developer name as recorded | 752 values |
| developer_clean | text | cleaned developer name | 731 values |
| entity_kind | text | `named_company`, `generic_category`, `other_entity`, `unknown` | 4 values |
| is_china_based | boolean | flag | True or False |
| genai_flag | boolean | flag | True or False |

## 13. Story 3: `stories/3_reported_incidents/data/fmti_companies.csv`

| Item | Value |
|---|---|
| Source organisation | The project group (`notebooks/fmti_scores/manual/fmti_companies.csv`), describing the companies of the Stanford Foundation Model Transparency Index (Stanford Center for Research on Foundation Models) |
| URL | https://crfm.stanford.edu/fmti/December-2025 and the repository `stanford-crfm/fmti` |
| Licence | Not stated in the repository for the group table. FMTI is CC BY as stated in the repository README, version not stated (`docs.md`) |
| Retrieval date | The date the group wrote the table is Not stated in the repository. The notebook copied it to `processed/` on 20 Nov 2026 13:08 UTC (`data_currency.csv`). The FMTI repository was retrieved 20 Nov 2026 13:08 UTC |
| Update frequency | None. The group wrote the table once. FMTI itself is annual |
| Source type | Group-made table of company details |
| Row count | 13 rows, 6 columns |
| Primary key | `company` (unique, no missing value) |
| Time coverage | FMTI December 2025 edition, flagship models selected as of May 2025. The file has no date column |
| Latest observation | December 2025 edition |
| Transform | `notebooks/fmti_scores/fmti_scores.ipynb` writes `processed/fmti_companies.csv` from the manual table, copied by hand into `data/` |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| company | text | company name | 13 unique |
| headquarters | text | country | Israel, China, USA, France |
| region | text | headquarters region | United States, China, Europe and Israel |
| self_submitted_report | text | `yes` or `no` | 2 values |
| flagship_model | text | model assessed by FMTI | 13 unique |
| in_bank_list | text | one of the 11 developers in scope, `yes` or `no` | 2 values |

## 14. Story 3: `stories/3_reported_incidents/data/fmti_dec2025_scores_tidy.csv`

| Item | Value |
|---|---|
| Source organisation | Stanford Center for Research on Foundation Models, Foundation Model Transparency Index, December 2025 (scores file `Dec2025_scores.csv`) |
| URL | https://crfm.stanford.edu/fmti/December-2025 and the repository `stanford-crfm/fmti` |
| Licence | CC BY 4.0. The `LICENSE.md` of the repository ZIP retrieved on 20 Nov 2026 holds the Attribution 4.0 International text, and the README says that the data and visuals are licensed CC BY |
| Retrieval date | 20 Nov 2026 13:08 UTC (`notebooks/fmti_scores/raw/retrieval_log.json`) |
| Update frequency | Annual. The December 2025 edition is the third edition of the Index, after 2023 and 2024 |
| Source type | Archived edition (December 2025) downloaded as `fmti-main.zip` from GitHub, kept in `notebooks/fmti_scores/raw/`. A fixed snapshot |
| Row count | 1,300 rows (100 indicators by 13 companies), 5 columns |
| Primary key | `Indicator` + `Developer` (unique, no missing value) |
| Time coverage | December 2025 edition, flagship models selected as of May 2025. The file has no date column |
| Latest observation | December 2025 edition |
| Transform | `notebooks/fmti_scores/fmti_scores.ipynb` writes `processed/fmti_dec2025_scores_tidy.csv`, copied by hand into `data/`. The sum per company matches the 13 published totals (`docs.md`) |

| Column | Type | Unit or values | Range or note |
|---|---|---|---|
| Indicator | text | FMTI indicator name | 100 values |
| Domain | text | `Upstream`, `Model`, `Downstream` | 3 values |
| Subdomain | text | FMTI subdomain | 19 values |
| Developer | text | company name | 13 values |
| Disclosed | integer | 1 = disclosed, 0 = not disclosed | 0 to 1 |

---

## Appendix A. Supporting files outside the `data/` folders

These files are not read by a page directly. They feed the files above or record how a file was matched. Row counts were read with pandas on 20 Nov 2026. The group's own work is credited to the group and not to any source.

| File | Rows, columns | Role |
|---|---|---|
| `stories/3_reported_incidents/notebooks/aiid_model_incidents/manual/aiid_incident_labels.csv` | 425, 4 | The group's label (model incident or not) for each of the 425 incidents that name one of the 11 developers. Fields `incident_id`, `label`, `label_detail`, `title` |
| `stories/3_reported_incidents/notebooks/aiid_model_incidents/manual/aiid_assigned_mit_domain.csv` | 91, 6 | The group's reading of the incident type of the 91 incidents that MIT had not classified, made with AI assistance. Fields `incident_id`, `date`, `title`, `assigned_domain`, `basis`, `comparable_MIT_classified_incidents` |
| `stories/3_reported_incidents/notebooks/aiid_model_incidents/processed/aiid_not_counted_incidents.csv` | 82, 6 | The 82 incidents that name a developer but are not counted as model incidents (platform products, operations cases and scam places) |
| `stories/3_reported_incidents/notebooks/fmti_scores/manual/fmti_companies.csv` | 13, 6 | Source of the data file in section 13 |
| `stories/2_gap_to_us_models/notebooks/benchmark_hub/manual/source_evidence_labels.csv` | 81, 7 | The label of each of the 81 named sources of the Benchmarking Hub (developer report, third party or Epoch run), set by Claude on 17 Nov 2026. The field `second_reviewer` is empty |
| `stories/2_gap_to_us_models/notebooks/benchmark_hub/processed/hub_name_matches.csv` | 508, 2 | Match of each Hub model version (`hub_model_version`) to a capability model (`capability_model`) |

The raw downloads (`raw/` folders of the notebooks) are the files as received, with a `retrieval_log.json` that records the address, time, size and SHA-256 hash where the download was made by the notebook.
