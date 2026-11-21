# View 2 data dictionary

**Files:** `data/hub_scores_by_model.csv` (page input), `data/hub_model_coverage.csv` (page input), `data/hub_data_currency.csv` (data stamp). They are written by `notebooks/benchmark_hub/benchmark_hub.ipynb` from the Epoch Benchmarking Hub ZIP.

**Primary source:** https://epoch.ai/data/benchmark_data.zip (Epoch AI Benchmarking Hub, 58 benchmark files with scores and `benchmark_metadata.csv`). **Licence:** Creative Commons Attribution 4.0 (CC BY 4.0), as stated on the Epoch benchmarking pages. **Retrieved:** the ZIP in `notebooks/benchmark_hub/raw/` was downloaded on 20 Nov 2026 at 13:06 UTC. The time, size and sha256 are in `raw/retrieval_log.json`. **Release year and access group:** from `data/model_capability.csv` (Epoch Capabilities Index, retrieved 20 Nov 2026), using the group rule of View 1.

## data/hub_scores_by_model.csv (2,128 rows, 168 models, 57 benchmarks)

**Primary key:** `model` + `benchmark` + `kind` (unique, no duplicates).

| Column | Meaning | Unit |
|---|---|---|
| model | Model name as in `model_capability.csv` | text |
| release_year | Release year of the model in the capability file | year (2023 to 2026) |
| access_group | accessible (open weights or non-US service) or restricted (US developer, closed weights). Excluded models have no score rows | category |
| benchmark | Benchmark name in the Hub | text |
| kind | Who produced the score: `epoch` (file of Epoch's own runs), `third_party` (leaderboard, website or paper by a group that is not the developer, and rows whose source the Hub does not state), `developer` (technical report, model card, system card or announcement) | category |
| source | `Epoch run` for Epoch rows, otherwise the source name or address given in the Hub | text |
| score_pct | Score on a 0 to 100 scale. The Hub stores 0 to 1 and three benchmarks with scale 0.01 are converted | % |

## data/hub_model_coverage.csv

One row per release year and access group. Columns: `release_year`, `access_group`, `models_in_capability_file` (all models of the group and year), `models_with_hub_scores` (models with at least one score row).

## data/hub_data_currency.csv

One row. Columns: `dataset`, `extracted_utc` (time of the notebook run), `zip_retrieved_utc`, `zip_how` (downloaded or reused), `zip_sha256`, `scores`, `models`, `benchmarks`, `note`. The page prints `zip_retrieved_utc` in the section "How to read this chart" (line "Data age").

## Files in the notebook folder

| File | Content |
|---|---|
| `manual/source_evidence_labels.csv` | One row per named source (81): `source`, `source_key`, `evidence_type` (developer_report 40, third_party 41), `rows_in_hub_nov_2026`, `our_reading` (set by Claude on 17 Nov 2026), `second_reviewer` (empty, no second reader), `rule` |
| `processed/hub_name_matches.csv` | The 508 Hub model versions matched to a capability model: `hub_model_version`, `capability_model` |
| `raw/benchmark_data.zip`, `raw/retrieval_log.json` | The ZIP as received and its retrieval record |
| `processed/` | The four CSV files the notebook writes. Copies of three of them are in `data/` |

## Transform

1. Read the 58 benchmark files listed in `benchmark_metadata.csv`, using the score column named there, and convert scale 0.01 scores.
2. Label each row: a file name with no `_external` is `epoch`. Rows of external files take their kind from `source_evidence_labels.csv`, and rows with no stated source are `third_party`. The notebook stops if a source name is missing from the label table.
3. Match Hub model versions to capability models by a normalised key (lower case, effort and date suffixes and punctuation removed). Only a unique match is kept (508 of 957 versions, 0 ambiguous).
4. Merge versions of a model and keep the highest score for each model, benchmark and kind.
5. Run the checks (unique key, score range 0 to 100, shares per bar sum to 100) and write the files.

## Limitations

- **Review:** the 81 labels and the 508 name matches were set by one reader, with no second check.
- **Coverage:** 168 of the 241 accessible and restricted models have at least one score. Some of the others may be matching misses.
- **Meaning of `developer`:** a report can list scores for models of other developers, for example in comparison tables, so the label does not always mean a developer reported its own model.
- **Scores:** some benchmarks measure progress, win rate or pass rate, so scores of different benchmarks are not comparable.
