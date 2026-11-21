# View 3 data dictionary (proposal chart V3)

**Files:** `data/gpqa_reported_vs_epoch.csv` is the file the page reads (eight rows, twelve columns). `notebooks/eci_scores/raw/epoch_article_gpqa_table.csv` is the versioned transcription with the first ten columns. `notebooks/eci_scores/processed/gpqa_reported_vs_epoch.csv` is the transcription plus the two computed columns `difference_pp` and `within_epoch_90ci`, and it is identical to the file in `data/`. `data/model_capability.csv` is read only to give each model an access group. The page is `v3_difference.py`, called from `page.py`.

**Primary source:** https://epoch.ai/data-insights/self-reported-gpqa (Jaeho Lee and Yafah Edelman, 19 September 2025), including the model-developer disclosures it cites. **Last observation:** a selection of frontier models up to 2025. It is not a time series. **Transcribed:** 14 November 2026, by hand, with no retrieval log. **Licence:** not verified for the comparison table of this web page. Attribution is given, and the reuse permission was not confirmed with Epoch. It is not the same as the licence of the separate capability index dataset.

**Primary key:** `model` (unique display name, eight rows).

| Column | Meaning | Unit |
|---|---|---|
| model | Model display name used by Epoch's article | text |
| developer_reported_pct | Score published by the developer, or the third-party score that the developer endorses | % correct on GPQA Diamond |
| epoch_independent_pct | Score that Epoch AI measured itself | % correct on GPQA Diamond |
| epoch_standard_error_pp | Standard error of Epoch's estimate | percentage points |
| epoch_90ci_halfwidth_pp | Half width of Epoch's approximate 90% interval (1.645 times the standard error) | percentage points |
| developer_report_type | `developer_report` (seven rows) or `third_party_endorsed` (Mistral Large 2407) | category |
| source_page | Epoch article that holds the comparison | URL |
| developer_source | Page of the developer for the published score or the endorsement | URL |
| reference_model | Epoch's identifier of the model it ran | text |
| notes | Test setting or exception, for example no extended thinking | text |
| difference_pp | `developer_reported_pct` minus `epoch_independent_pct`, rounded to two decimals. Written by `build_v3_data.py`. The page calculates the difference again when it loads | percentage points |
| within_epoch_90ci | True when the absolute difference is not larger than `epoch_90ci_halfwidth_pp`. Written by `build_v3_data.py` | yes or no |

**Columns added when the page loads (`load_gpqa` in `v3_difference.py`, the page does not use the two computed columns of the file):**

| Column | Meaning | Unit |
|---|---|---|
| access_group | `restricted` (US developer, no downloadable weights) or `accessible` (open weights, or a service from a developer outside the US). The model is matched by name to `data/model_capability.csv` with the `CAPABILITY_NAME` dictionary and the rule of View 1 (`access_group` in `src/context.py`). The load stops with an error if a model is missing or duplicated | category |
| difference_pp | `developer_reported_pct` minus `epoch_independent_pct`, not rounded | percentage points |
| in_band | True when the absolute difference is not larger than `epoch_90ci_halfwidth_pp` | yes or no |

**Transform:** Eight rows are transcribed by hand from the table of Epoch's article. The page checks that the four numeric columns hold numbers, that the two percentages lie between 0 and 100 and that no model name repeats. It then computes the three columns above. No aggregation, imputation, scoring or automatic download is done. The page plots the seven rows with `developer_report`. The row with `third_party_endorsed` is explained in a note under the chart and is not plotted, not counted and not in the records table or the CSV download. `notebooks/eci_scores/build_v3_data.py` writes the processed file, but it looks for its files in `notebooks/data/` and does not run from its present folder. The app does not call it.

**Limitations:** A selection of models by Epoch, one benchmark (GPQA Diamond), a comparison of 19 September 2025, seven models in two groups of four and three, and test settings that may differ between the developer and Epoch. The Mistral row has two points that could not be settled: the article text does not say which of 48.6 and 51.3 comes from which source, and the row is labelled 2407 while Epoch's run used 2411. The eight rows were compared with the article by one reader only.
