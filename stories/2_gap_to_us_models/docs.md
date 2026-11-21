# Story 2: gap to the restricted US models (Views 1 to 3)

**Built by:** Rida (the initial Story 2 submission, including the first version of the GPQA chart that was View 3 before it was changed, see `v3_benchmark.py`). Yin (View 2 and the current View 3, with Claude's help, and a basic version of View 1 that was made first because Rida had also worked on View 1). The split of View 1 between the two is not certain.  **Data snapshot:** Epoch file retrieved 20 Nov 2026 13:07 UTC, Benchmarking Hub ZIP downloaded 20 Nov 2026 13:06 UTC

**Status:** View 1 (the gap chart) is built and was checked against the A3P1 app on the data of 17 Oct 2026. It was rebuilt on the data of 20 Nov 2026 (257 models in the capability file, see "Checks"). View 2 (who produced the benchmark scores) and View 3 (the difference between developer-reported and independent GPQA scores) are built as alternatives to the A3P1 version of the story. The charts of each story are numbered from 1 since 18 Nov 2026, see "Chart names" below.

## Persona, scenario, task and constraints

Source: Alternative Proposal (No Search ABC), section "Primary persona, scenario and three user stories".

**Persona:** group enterprise architect at an Asia-Pacific bank or insurer with operations in Hong Kong and other markets.

**Scenario:** The risk committee has asked for an approved list of AI models for staff and internal tools. The leading closed US models are not offered in Hong Kong. The committee wants an interim list within one to two weeks. The architect must choose between API services from outside the US and self-hosted open weights, and the committee will ask what capability is given up, what each route costs, and which models the bank may run itself.

**Task:** Produce an interim approved list. For each candidate model, say which route it uses (API or self-hosted), what its licence allows, how much capability it gives, and what it costs.

**Constraints (assumed in the proposal):**

- **Time:** One to two weeks. The list is interim, so each version is kept with its date and sources.
- **Organisation:** The committee needs reasons, not a single score.
- **Data:** Capability and licence class come from files, but data control is a proxy and availability by place is not measured.
- **Scope:** Regulator rules, the organisation's own tasks, hosting cost and security review are not covered.

## User story

**Story 2:** As a group enterprise architect, I want to measure how far the best accessible model trails the best model overall and check whether independent benchmarks agree with developer claims, so that I can judge whether waiting for US access is worth it.

**Covered in part:** The clause "check whether independent benchmarks agree with developer claims" (View 3, the proposal chart V3) is answered for one benchmark (GPQA Diamond) and seven models only. The capability file has no flag that separates developer-reported scores from independent runs.

**Question answered:** How far do accessible models trail the restricted US models, and is the gap shrinking?

**Acceptance criteria (from the proposal):** The app shows the best accessible model against the best model overall by release date, with the confidence interval, units and time range stated. It says that the data cannot predict when US access returns.

## Chart used

| Proposal chart | App view | Chart type | What it shows |
|---|---|---|---|
| V2 | View 1 | Step lines with a shaded gap | Best score so far for the restricted US models and for the accessible models, the gap between them and the months behind |
| none (added by the group) | View 2 | Two 100% stacked bars | Share of the benchmark scores behind the capability index by who produced them (Epoch AI, third party or developer), by release year and access group |
| V3 (rebuilt as a difference chart) | View 3 | Dot plot of differences with a band | Developer-reported minus Epoch's independent GPQA Diamond score for seven models, in percentage points, with Epoch's approximate 90% band around zero |

**Visual Vocabulary family:** change over time (Visual Vocabulary).

**Chart names:** Until 17 Nov 2026 the charts were called View 1, 2, 3, 3b, 4, 4B, V3, 5a and 5b. On 18 Nov 2026 the charts of each story were numbered from 1 in page order. Story 1a has View 1 and View 2 (unchanged). Story 1b has View 1 (earlier View 3) and View 2 (earlier View 3b). Story 2 has View 1 (earlier View 4), View 2 (earlier View 4B) and View 3 (earlier V3, the proposal chart). Story 3 has View 1 (earlier View 5a) and View 2 (earlier View 5b). A chart of another story is named with its story, for example Story 2 View 1. File names (`view4b.py`, `v3_difference.py`, `DATA_DICTIONARY_4B.md`, `DATA_DICTIONARY_V3.md`) and the proposal chart ids (V1 to V7) are unchanged.

## What the page shows (default settings, 17 Nov 2026)

| Date | Best restricted | Score | Best accessible | Score | Gap (points) | Months behind |
|---|---|---|---|---|---|---|
| 17 Nov 2026 | GPT-6.2 Astra | 174.2 | Kimi K3.1 Pro | 161.4 | 12.8 | 7 |
| 17 May 2026 | GPT-5.5 Pro | 162.8 | Kimi K2.6 | 151.6 | 11.2 | 6 |
| 17 Nov 2025 | GPT-5 Pro | 151.3 | Kimi K2 Thinking | 145.5 | 5.8 | 7 |
| 17 Nov 2024 | o1-mini | 135.3 | Llama 3.1-405B | 127.9 | 7.4 | 6 |

These values were read from the rendered page on 20 Nov 2026 (UTC) on the data of the Epoch file retrieved that day. The end date of the chart is the latest release date in the file.

## View 2 (alternative): who produced the benchmark scores behind the capability index

**Question answered:** Do the benchmark scores behind the capability index come from Epoch's own runs, from third parties or from reports published by developers, and has that mix changed since 2023?

**Chart:** Two vertical 100% stacked bar charts (Accessible and Restricted, same groups as View 1) by release year, or one combined chart. The page sits between View 1 and View 3 (moved above View 3 on 17 Nov 2026 at Yin's request) and does not change View 1 or View 3. Hovering over a segment shows its top three sources, one per line. Clicking a segment opens two sections under the chart. The first section is called after the segment and has two tables side by side (top benchmarks or sources, and models with the most scores, 8 rows visible and the rest by scroll bar). The second section is called "Look at model" and shows how the scores of one model are counted, in three columns by kind of source, inside a box with its own scroll bar. Two controls choose another model: a release year (All, 2023 to 2026) and a model list with a search box. The controls are preset by the clicked segment and by the selected row in the models table. Before a segment is clicked, nothing is shown under the chart except the five sections below. They open and close by clicking their titles: "How to read this chart", "Design decision for this view", "What this chart cannot show", "Values behind the chart" and "Filtered records (the rows behind this chart)" with a "Download filtered data (CSV)" button. The filtered records are the scores of the clicked segment, or all 2,128 scores when no segment is clicked. The sources are given once, in the block "Data, methods and limitations" at the end of the page.

**Counting rule:** One score is one model, one benchmark and one kind of source. Versions of a model (for example high, low and max effort) are merged and the highest score is kept. A benchmark with two kinds of source for the same model counts twice. A benchmark with no result is not counted. Percent is the scores of one kind divided by all scores in the bar, so models with more scores weigh more.

**Kinds of source:** "Run by Epoch AI" are rows from Epoch's own benchmark files. "Third party" are rows from leaderboards, websites or papers by a group that is not the developer, plus rows whose source the Hub does not state. "Developer-reported" are rows whose source is a technical report, model card, system card or announcement. Such a report can list scores for models of other developers, for example in comparison tables. The label of each named source is in `notebooks/benchmark_hub/manual/source_evidence_labels.csv` (81 sources, 58 of them in the 2,128 scores of the current file). The other 11 sources in the scores are rows whose source the Hub does not state, and they are counted as third party.

**Numbers (notebook run of 20 Nov 2026 on the ZIP downloaded that day):**

| Release year | Group | Models with scores | Scores | Benchmarks | Run by Epoch AI | Third party | Developer-reported |
|---|---|---|---|---|---|---|---|
| 2023 | Accessible | 21 of 27 | 182 | 12 | 0% | 9% | 91% |
| 2024 | Accessible | 18 of 30 | 139 | 24 | 17% | 32% | 51% |
| 2025 | Accessible | 14 of 27 | 90 | 24 | 31% | 69% | 0% |
| 2026 | Accessible | 36 of 42 | 392 | 34 | 47% | 53% | 0% |
| 2023 | Restricted | 1 of 7 | 8 | 8 | 0% | 0% | 100% |
| 2024 | Restricted | 11 of 23 | 127 | 32 | 32% | 53% | 15% |
| 2025 | Restricted | 24 of 39 | 391 | 39 | 37% | 62% | 1% |
| 2026 | Restricted | 43 of 46 | 799 | 39 | 46% | 54% | 0% |

Percentages are rounded. The numbers were read from `data/hub_scores_by_model.csv`. The table was rebuilt on 20 Nov 2026 because the first run after the download had read the capability file of an earlier date (data to 7 Oct 2026). The counts of the table were recomputed from `data/hub_scores_by_model.csv` by a separate script on 21 Nov 2026, and every share matches the table. The totals are 803 scores of 89 accessible models and 1,325 scores of 79 restricted models.

**Data flow:** `notebooks/benchmark_hub/benchmark_hub.ipynb` downloads `https://epoch.ai/data/benchmark_data.zip` (or reuses `raw/benchmark_data.zip`), reads the 58 benchmark files listed in `benchmark_metadata.csv` with the score column named there, labels each row, matches Hub model names to the capability file, applies the access group rule of View 1, keeps one score per model, benchmark and kind, runs checks that stop the run on failure and writes `processed/hub_scores_by_model.csv`, `hub_model_coverage.csv`, `hub_name_matches.csv` and `hub_data_currency.csv`. The first, second and fourth file are copied to `data/` by hand, like the files of the other notebooks. The page reads only `data/hub_scores_by_model.csv`, `data/hub_model_coverage.csv` and `data/hub_data_currency.csv`. The retrieval record is `raw/retrieval_log.json`. The ZIP in `raw/` was downloaded on 20 Nov 2026 at 13:06 UTC (`zip_retrieved_utc` in `hub_data_currency.csv`) and the tables were extracted from it at 15:51 UTC the same day. A run with `REFRESH = True` downloads it again and records the new time.

**Refresh rule:** If a source name is not in the label table, the run stops and lists it. A reader then adds a row with `developer_report` or `third_party` to the table. The matches in `processed/hub_name_matches.csv` are read again for new model names, and the access group counts are compared with View 1.

**Limitations:**

- **Matching:** 168 of the 241 accessible and restricted models in the capability file have at least one Hub score after name matching (508 of the 957 Hub model versions are matched to 184 capability models, and 168 of those are in the two groups). Some of the others may be matching misses and not missing scores.
- **Labels:** The labels of the 81 sources were set by one reader.
- **Coverage:** Some bars hold few models (Restricted 2023 has 1 model and 8 scores), so the shares in them are not stable.
- **Meaning of scores:** The chart shows who produced the scores, not how high they are. Scores of different benchmarks are not comparable, and some benchmarks measure progress or win rate and not answers correct.
- **Developer-reported:** The label does not mean that the developer reported a score for its own model in every case.

**Relation to View 3:** View 3 checks whether independent and publisher scores agree for one benchmark. View 2 shows how many of the scores behind the capability index come from each kind of source. It does not compare the two scores of one model, so the two views answer different parts of the same question. The same note is the last line of the View 2 block in the app.

## View 3 (alternative): difference chart (proposal chart V3)

**Question answered:** Do the GPQA Diamond scores that developers report agree with the scores Epoch AI measures itself, and is the gap different for the restricted and the accessible group?

**Based on:** Epoch AI, "AI developers accurately report GPQA Diamond scores for recent models" (19 September 2025, [epoch.ai/data-insights/self-reported-gpqa](https://epoch.ai/data-insights/self-reported-gpqa)). Epoch plots the two scores of each model next to each other. The alternative plots only their difference, which is the point of the chart, and adds the access groups of View 1. The first alternative was built on 17 Nov 2026 as a new module (`v3_difference.py`). The earlier module `v3_benchmark.py` stays in the folder unchanged and is no longer called by `page.py`.

**Chart:** One dot per model. The dot is the developer-reported score minus Epoch's independent score, in percentage points. The zero line means the two agree. A grey band shows Epoch's approximate 90% band (1.645 times its standard error) around zero. Dots are orange for the restricted group and blue for the accessible group, with the colours of View 1. The page opens with a "Based on" line and a "Message of this chart" line. The chart is followed by a note on the model that is not plotted and by three sections that open and close by clicking their titles ("How to read this chart", "Design decision for this view" and "What this chart cannot show") and by "Filtered records (the rows behind this chart)" with a "Download filtered data (CSV)" button, the same pattern as View 2. The records are the seven plotted models, so Mistral Large is not in the table or the CSV. The sources are given in the block "Data, methods and limitations" at the end of the page. There are no filters.

**Numbers (computed on 17 Nov 2026 from `data/gpqa_reported_vs_epoch.csv`):** Seven models with a developer-reported score. The differences in percentage points are GPT-5 +1.2, Claude Opus 4.1 +1.7, Gemini 2.5 Pro +1.6, Grok 4 +0.5 (restricted) and Llama 4 Maverick +2.8, Qwen 3 +0.4, DeepSeek R1 −0.2 (accessible). All seven lie inside Epoch's band. Six are above Epoch's score. All four restricted models are above it.

**Access group:** Each model is matched by name to a row of `data/model_capability.csv` (the match table is the `CAPABILITY_NAME` dictionary in `v3_difference.py`) and the rule of View 1 is applied (`access_group` in `src/context.py`). The load stops with an error if a model is missing or duplicated.

**Mistral Large 2407 is not plotted.** Mistral did not report a GPQA Diamond score. Epoch lists 48.6% from a third-party evaluation that Mistral's benchmark page endorses, against 51.3% measured by Epoch (−2.7 pp). The row is labelled 2407, while Epoch's run used 2411. The article text does not label which number belongs to which source, so the assignment of the two numbers to their sources could not be confirmed. The row is explained in a note under the chart and is left out of the chart and the counts. The earlier View 3 checkbox for this row and the model filter were removed.

**Limitations:** Seven models chosen by Epoch, one benchmark, a comparison published on 19 September 2025, and groups of four and three models that are too small to test a difference between them. The Epoch Benchmarking Hub holds no model with both an Epoch run and a developer-reported score on one benchmark (GPQA in the Hub has only Epoch-run rows), so the comparison cannot be extended from the Hub.

**Notes:** The data file has no retrieval log. `DATA_DICTIONARY_V3.md` was refreshed on 18 Nov 2026 and 21 Nov 2026 to describe the difference chart. The AI use for this chart is in `AI_PROVENANCE_MATRIX.csv`. `notebooks/eci_scores/build_v3_data.py` looks for its files in `notebooks/data/` and does not run from its present folder. The app does not call it.

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Epoch Capabilities Index, file `eci_scores.csv` | Release date, capability score and interval, developer, country, accessibility label | Retrieved 20 Nov 2026 13:07 UTC, models released 24 Feb 2023 to 17 Nov 2026 (257 models) |
| Epoch AI article "AI developers accurately report GPQA Diamond scores for recent models", file `gpqa_reported_vs_epoch.csv` | View 3 only: reported and independent GPQA Diamond scores of eight models | Article of 19 Sep 2025, scores transcribed by the group on 14 Nov 2026 (date as stated in the earlier View 3 caption) |
| Epoch AI Benchmarking Hub, file `benchmark_data.zip` (CC BY 4.0) | View 2 only: the benchmark scores behind the capability index, who produced each score | ZIP downloaded 20 Nov 2026 13:06 UTC, 2,128 scores of 168 models on 57 benchmarks |

**Data flow:** `notebooks/eci_scores/` downloads or reuses the raw file in `raw/`, writes `model_capability.csv` to `processed/`, and the file is copied by hand into `data/`. View 1 reads only `data/model_capability.csv`. View 3 reads `data/gpqa_reported_vs_epoch.csv` and uses `data/model_capability.csv` for the access group. View 2 also reads `data/hub_scores_by_model.csv`, `data/hub_model_coverage.csv` and `data/hub_data_currency.csv`, which come from `notebooks/benchmark_hub/` (see the View 2 section and `DATA_DICTIONARY_4B.md`). The benchmark_hub notebook follows the same rule: it writes to `processed/` and its three page files are copied into `data/` by hand. Run the eci_scores notebook of this story first, because benchmark_hub matches the Hub names against its `processed/model_capability.csv`. The notebook is a copy of notebook 01 with the folder name, the manual folder and the output step changed.

**Licence check at every refresh:** Every time the data is downloaded again, for each new open-weight model and each model that Epoch labels restricted use, non-commercial or unknown, open the LICENSE file on Hugging Face or GitHub and read it. Epoch's label and news pages do not replace it. Record the licence name, whether commercial use is allowed, the condition (revenue line, user line or Model-as-a-Service clause), whether internal use is exempt, whether Epoch's label agrees with the text, the link and the date read. Add the reading to `LICENCE_NOTES` in `src/views.py` and, for Story 1b, to `data/licence_terms.json`. Then check whether the accessible best model in View 1 rests on a restricted use or non-commercial licence, and say so in the page text if it does. View 1 counts every open-weight model as accessible whatever its licence.

## Limitations

- **Capability index:** Epoch's index leans to maths and reasoning, covers smaller and non-US models less well, and the 90% intervals of neighbouring models overlap.
- **Excluded models:** Models with no open weights and no stated country (16 older models) belong to neither side, so neither side can be claimed for them.
- **Prediction:** The data cannot show when US access returns or whether the gap keeps shrinking.
- **Different group definitions:** Epoch published its own open-weight lag figures (about 3 months in October 2025 and about 4 months in May 2026, as recorded in the A3P1 documentation and not re-checked here). The groups are defined differently, so the numbers should not be compared without saying so.

## Restrictions

- **Restricted and accessible:** Restricted means a US developer with no downloadable weights. Accessible means open weights from any country or a service from a developer outside the US. This is a rule and not a measurement.
- **Hong Kong availability:** The restriction is the premise of the story and was not measured.
- **Epoch data licence:** Creative Commons Attribution. The page read does not state a version ([epoch.ai/data](https://epoch.ai/data)).

## Options for the independent benchmark part (V3)

Found on 5 Nov 2026 and recorded in the A3P1 documentation. Not re-checked here. Status on 18 Nov 2026:

- **A.** Epoch self-reported against Epoch-run GPQA, eight models. Built as View 3, with the Mistral row left out of the chart.
- **B.** Developer-reported GPQA for 2026 accessible models against Epoch runs. Not built. The Epoch Benchmarking Hub holds no model with both an Epoch run and a developer-reported score on GPQA, so there is nothing to compare.
- **C.** ECI evidence mix. Built as View 2 from the Hub files, with the named sources labelled by one reader.

## Checks

The first five checks below compared the page with the A3P1 app on the data of 17 Oct 2026 (277 models) and on the notebook run of 9 Nov 2026. The data was refreshed on 20 Nov 2026 (257 models), so the numbers in those rows describe the earlier data. The rows after them describe the data of 20 Nov 2026. The A3P1 app was not run again on the new data.

| Check | Result |
|---|---|
| The page table built from `model_capability.csv` against the same columns of `models.csv` in the A3P1 app | Identical values, types and row order (277 models) |
| Visible text of the View 1 page against the A3P1 tab 3, from the "User story" line down | No difference |
| Notebook run in a cloud copy, output compared with the original `model_capability.csv` | Same content (277 rows, 16 columns). Only the line endings differ between Windows and the cloud |
| Whole build from zero in a fresh virtual environment (`pip install -r requirements.txt -r requirements-notebook.txt`, Python 3.13): notebook run, `processed/model_capability.csv` copied by hand into `data/` | Same content as the earlier files (277 rows, 16 columns). Run on 9 Nov 2026 |
| Page run inside `app.py` and on its own (`streamlit run stories/<story>/page.py`), text from "User story" down compared with the A3P1 tab | No difference in both cases. Screenshot of the in-app page checked by eye |
| Page on the data of 20 Nov 2026: all four pages at 1366x768 in headless Chromium searched for the old dates and counts, the Hub tables rebuilt after the capability file changed, the end date of View 1 read from the data | No old date or count found. Gap on 17 Nov 2026 is 12.8 points and 7 months. The Hub tables hold 2,128 scores of 168 models on 57 benchmarks. Run on 20 Nov 2026 |
| View 2 notebook run in a cloud copy, with checks that stop the run (unique score per model, benchmark and kind, scores between 0 and 100, shares sum to 100) | All checks passed. Run on 17 Nov 2026 |
| View 2 counts rebuilt from `data/hub_scores_by_model.csv` by a separate script (scores, models and shares of each kind for every release year and group, and the totals) | Every figure equals the table under "Numbers" (803 scores of 89 accessible models, 1,325 scores of 79 restricted models, 2,128 scores of 168 models on 57 benchmarks). Run on 21 Nov 2026 |
| View 2 tests (`tests/test_view4b.py`, 14 tests) and a Chrome run of the clicks, row selection, year and model choice and the sections under the chart | 14 passed, no JavaScript error. Run on 17 Nov 2026. The test files are kept outside the repository |
| View 3 difference chart tests (`tests/test_v3_difference.py`, 9 tests: eight rows and groups, differences against the CSV by hand, Mistral left out, counts and order, texts, records table and CSV text, figure shapes, bad data stops the load, page renders without filters and with a Filtered records section) and a Chrome run with the sections opened, a hover and the CSV download (7 rows, no Mistral) | 9 passed, no JavaScript error. Page run once inside `page.py` with no exception and the order View 1, View 2, View 3. Run on 18 Nov 2026. The test files are kept outside the repository |
| Renumbering of the chart names (18 Nov 2026): a script replaced the old names in the code, docs and README (numbers restart in every story), and the whole app was run with `streamlit.testing` (all four pages, no exception) | No exception on any of the four pages |

These checks were run by Claude.
