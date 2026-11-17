# Story 2: gap to the restricted US models (Views 1 to 3)

**Owner:** Rida  **Data snapshot:** Epoch file retrieved 17 Oct 2026 22:27 UTC (18 Oct 2026 in Sydney)

**Status:** View 1 (the gap chart) is built and checked against the A3P1 app. View 2 (who produced the benchmark scores) and View 3 (the difference between developer-reported and independent GPQA scores) are built as alternatives to the A3P1 version of the story. The charts of each story are numbered from 1 since 18 Nov 2026, see "Chart names" below.

## Persona, scenario, task and constraints

Source: [Alternative Proposal (No Search ABC), section "Primary persona, scenario and three user stories"](https://github.com/IanK10008/36104-Assignment-3-AI-topic/blob/main/Hedging%20Region%20AI%20Model%20Selection%20and%20Data%20Risk/01b%20Alternative%20Proposal%20(No%20Search%20ABC)/Alternative%20Proposal%20(No%20Search%20ABC)%20(English).md).

**Persona:** group enterprise architect at an Asia-Pacific bank or insurer with operations in Hong Kong and other markets.

**Scenario:** The risk committee has asked for an approved list of AI models for staff and internal tools. The leading closed US models are not offered in Hong Kong. The committee wants an interim list within one to two weeks. The architect must choose between API services from outside the US and self-hosted open weights, and the committee will ask what capability is given up, what each route costs, and which models the bank may run itself.

**Task:** Produce an interim approved list. For each candidate model, say which route it uses (API or self-hosted), what its licence allows, how much capability it gives, and what it costs.

**Constraints (assumed, to validate with the group):**

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

**Visual Vocabulary family:** change over time (as recorded in MEMORY.md section 8p).

**Chart names:** Until 17 Nov 2026 the charts were called View 1, 2, 3, 3b, 4, 4B, V3, 5a and 5b. On 18 Nov 2026 the charts of each story were numbered from 1 in page order. Story 1a has View 1 and View 2 (unchanged). Story 1b has View 1 (earlier View 3) and View 2 (earlier View 3b). Story 2 has View 1 (earlier View 4), View 2 (earlier View 4B) and View 3 (earlier V3, the proposal chart). Story 3 has View 1 (earlier View 5a) and View 2 (earlier View 5b). A chart of another story is named with its story, for example Story 2 View 1. File names (`view4b.py`, `v3_difference.py`, `DATA_DICTIONARY_4B.md`, `DATA_DICTIONARY_V3.md`, `PROVENANCE_V3_DRAFT.md`) and the proposal chart ids (V1 to V7) are unchanged. MEMORY.md sections up to 8al and the earlier decision logs use the old names.

## What the page shows (default settings, 7 Oct 2026)

| Date | Best restricted | Score | Best accessible | Score | Gap (points) | Months behind |
|---|---|---|---|---|---|---|
| 7 Oct 2026 | Claude Opus 5.5 | 166.8 | Kimi K3 | 157.4 | 9.4 | 7 |
| 7 Apr 2026 | GPT-5.4 Pro | 159 | GLM-5.1 | 150 | 9 | 8 |
| 7 Oct 2025 | GPT-5 Pro | 150.7 | DeepSeek-V3.2-Exp | 145 | 5.8 | 6 |
| 7 Oct 2024 | o1-mini | 135.8 | Qwen2.5-72B | 129 | 6.8 | 5 |

These values were read from the rendered page and match the A3P1 app.

## View 2 (alternative): who produced the benchmark scores behind the capability index

**Question answered:** Do the benchmark scores behind the capability index come from Epoch's own runs, from third parties or from reports published by developers, and has that mix changed since 2023?

**Chart:** Two vertical 100% stacked bar charts (Accessible and Restricted, same groups as View 1) by release year, or one combined chart. The page sits between View 1 and View 3 (moved above View 3 on 17 Nov 2026 at Ian's request) and does not change View 1 or View 3. Hovering over a segment shows its top three sources, one per line. Clicking a segment opens two sections under the chart. Each section opens and closes by clicking its title. The first section has two tables side by side (top benchmarks or sources, and models with the most scores, 8 rows visible and the rest by scroll bar). The second section is called "Look at model". It shows how the scores of one model are counted, in three columns by kind of source, inside a box with its own scroll bar. Two controls choose another model: a release year (All, 2023 to 2026) and a model list with a search box. The controls are preset by the clicked segment and by the selected row in the models table. Before a segment is clicked, nothing is shown under the chart except the four sections below. The four sections follow the pattern of Story 3 and open and close by clicking their titles: "How to read this chart", "What this chart cannot show", "Values behind the chart" and "Filtered records (the rows behind this chart)" with the same "Download filtered data (CSV)" button. The filtered records are the scores of the clicked segment, or all 2,093 scores when no segment is clicked. The data source line stays visible under the sections.

**Counting rule:** One score is one model, one benchmark and one kind of source. Versions of a model (for example high, low and max effort) are merged and the highest score is kept. A benchmark with two kinds of source for the same model counts twice. A benchmark with no result is not counted. Percent is the scores of one kind divided by all scores in the bar, so models with more scores weigh more.

**Kinds of source:** "Run by Epoch AI" are rows from Epoch's own benchmark files. "Third party" are rows from leaderboards, websites or papers by a group that is not the developer, plus rows whose source the Hub does not state. "Developer-reported" are rows whose source is a technical report, model card, system card or announcement. Such a report can list scores for models of other developers, for example in comparison tables. The label of each of the 81 named sources is in `notebooks/benchmark_hub/manual/source_evidence_labels.csv`.

**Numbers (notebook run of 17 Nov 2026 on the ZIP dated 16 Nov 2026):**

| Release year | Group | Models with scores | Scores | Benchmarks | Run by Epoch AI | Third party | Developer-reported |
|---|---|---|---|---|---|---|---|
| 2023 | Accessible | 23 of 31 | 191 | 15 | 3% | 9% | 88% |
| 2024 | Accessible | 21 of 37 | 151 | 24 | 21% | 32% | 47% |
| 2025 | Accessible | 16 of 36 | 96 | 24 | 34% | 66% | 0% |
| 2026 | Accessible | 36 of 40 | 385 | 33 | 48% | 52% | 0% |
| 2023 | Restricted | 2 of 9 | 13 | 12 | 15% | 23% | 62% |
| 2024 | Restricted | 11 of 25 | 127 | 32 | 32% | 53% | 15% |
| 2025 | Restricted | 24 of 39 | 391 | 39 | 37% | 62% | 1% |
| 2026 | Restricted | 41 of 43 | 739 | 39 | 45% | 55% | 0% |

Percentages are rounded. The numbers were read from `data/hub_scores_by_model.csv`. A second implementation of the counting that used only the 415 Hub model versions matched in the first cloud run gave 191, 151, 96 and 361 scores for Accessible and 13, 127, 381 and 605 for Restricted in 2023 to 2026. The current run matches 77 more Hub versions (other effort levels such as xhigh, none and unknown, and a few chat or instruct variants), so the 2025 and 2026 figures are higher than those first figures. The 2023 and 2024 figures did not change.

**Data flow:** `notebooks/benchmark_hub/benchmark_hub.ipynb` downloads `https://epoch.ai/data/benchmark_data.zip` (or reuses `raw/benchmark_data.zip`), reads the 58 benchmark files listed in `benchmark_metadata.csv` with the score column named there, labels each row, matches Hub model names to the capability file, applies the access group rule of View 1, keeps one score per model, benchmark and kind, runs checks that stop the run on failure and writes `processed/hub_scores_by_model.csv`, `hub_model_coverage.csv`, `hub_name_matches.csv` and `hub_data_currency.csv`. With `COPY_TO_APP = True` the first, second and fourth file are copied to `data/`. The page reads only `data/hub_scores_by_model.csv`, `data/hub_model_coverage.csv` and `data/hub_data_currency.csv`. The retrieval record is `raw/retrieval_log.json`. The ZIP in this folder was supplied by hand on 16 Nov 2026 and the download time was not recorded, so the first run on the group's computer should set `REFRESH = True` to download it again and record the time.

**Refresh rule:** If a source name is not in the label table, the run stops and lists it. A reader then adds a row with `developer_report` or `third_party` to the table. The matches in `processed/hub_name_matches.csv` are read again for new model names, and the access group counts are compared with View 1.

**Limitations:**

- **Matching:** 174 of the 260 accessible and restricted models in the capability file have at least one Hub score after name matching. Some of the others may be matching misses and not missing scores. The match list has not been reviewed by a second person.
- **Labels:** The labels of the 81 sources were set by one reader and have not been reviewed by a second person.
- **Coverage:** Some bars hold few models (Restricted 2023 has 2 models and 13 scores), so the shares in them are not stable.
- **Meaning of scores:** The chart shows who produced the scores, not how high they are. Scores of different benchmarks are not comparable, and some benchmarks measure progress or win rate and not answers correct.
- **Developer-reported:** The label does not mean that the developer reported a score for its own model in every case.

**Relation to View 3:** View 3 checks whether independent and publisher scores agree for one benchmark. View 2 shows how many of the scores behind the capability index come from each kind of source. It does not compare the two scores of one model, so the two views answer different parts of the same question. The same note is the last line of the View 2 block in the app.

## View 3 (alternative): difference chart (proposal chart V3)

**Question answered:** Do the GPQA Diamond scores that developers report agree with the scores Epoch AI measures itself, and is the gap different for the restricted and the accessible group?

**Based on:** Epoch AI, "AI developers accurately report GPQA Diamond scores for recent models" (19 September 2025, [epoch.ai/data-insights/self-reported-gpqa](https://epoch.ai/data-insights/self-reported-gpqa)). Epoch plots the two scores of each model next to each other. The alternative plots only their difference, which is the point of the chart, and adds the access groups of View 1. The first alternative was built on 17 Nov 2026 as a new module (`v3_difference.py`). The earlier module `v3_benchmark.py` stays in the folder unchanged and is no longer called by `page.py`.

**Chart:** One dot per model. The dot is the developer-reported score minus Epoch's independent score, in percentage points. The zero line means the two agree. A grey band shows Epoch's approximate 90% band (1.645 times its standard error) around zero. Dots are orange for the restricted group and blue for the accessible group, with the colours of View 1. The page opens with a "Based on" line and a "Message of this chart" line. The chart is followed by a note on the model that is not plotted and by two sections that open and close by clicking their titles ("How to read this chart" and "What this chart cannot show") and by "Filtered records (the rows behind this chart)" with a "Download filtered data (CSV)" button, the same pattern as View 2. The records are the seven plotted models, so Mistral Large is not in the table or the CSV. The source line stays visible. There are no filters.

**Numbers (computed on 17 Nov 2026 from `data/gpqa_reported_vs_epoch.csv`):** Seven models with a developer-reported score. The differences in percentage points are GPT-5 +1.2, Claude Opus 4.1 +1.7, Gemini 2.5 Pro +1.6, Grok 4 +0.5 (restricted) and Llama 4 Maverick +2.8, Qwen 3 +0.4, DeepSeek R1 −0.2 (accessible). All seven lie inside Epoch's band. Six are above Epoch's score. All four restricted models are above it.

**Access group:** Each model is matched by name to a row of `data/model_capability.csv` (the match table is the `CAPABILITY_NAME` dictionary in `v3_difference.py`) and the rule of View 1 is applied (`access_group` in `src/context.py`). The load stops with an error if a model is missing or duplicated.

**Mistral Large 2407 is not plotted.** Mistral did not report a GPQA Diamond score. Epoch lists 48.6% from a third-party evaluation that Mistral's benchmark page endorses, against 51.3% measured by Epoch (−2.7 pp). The row is labelled 2407, while Epoch's run used 2411. The assignment of the two numbers to their sources has not been checked against Epoch's chart, because the article text does not label them. The row is explained in a note under the chart and is left out of the chart and the counts. The earlier View 3 checkbox for this row and the model filter were removed.

**Limitations:** Seven models chosen by Epoch, one benchmark, a comparison published on 19 September 2025, and groups of four and three models that are too small to test a difference between them. The Epoch Benchmarking Hub holds no model with both an Epoch run and a developer-reported score on one benchmark (GPQA in the Hub has only Epoch-run rows), so the comparison cannot be extended from the Hub.

**Not yet done:** A second member checks the eight transcribed rows against Epoch's article. The data file has no retrieval log. Ian has not reviewed the wording of the "Message of this chart" line, which Claude wrote. `DATA_DICTIONARY_V3.md` and `PROVENANCE_V3_DRAFT.md` were refreshed on 18 Nov 2026 to describe the difference chart. `notebooks/eci_scores/build_v3_data.py` looks for its files in `notebooks/data/` and does not run from its present folder. The app does not call it.

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Epoch Capabilities Index, file `eci_scores.csv` | Release date, capability score and interval, developer, country, accessibility label | Retrieved 17 Oct 2026 22:27 UTC, models released 24 Feb 2023 to 7 Oct 2026 (277 models) |
| Epoch AI article "AI developers accurately report GPQA Diamond scores for recent models", file `gpqa_reported_vs_epoch.csv` | View 3 only: reported and independent GPQA Diamond scores of eight models | Article of 19 Sep 2025, scores transcribed by the group on 14 Nov 2026 (date as stated in the earlier View 3 caption) |
| Epoch AI Benchmarking Hub, file `benchmark_data.zip` (CC BY 4.0) | View 2 only: the benchmark scores behind the capability index, who produced each score | ZIP dated 16 Nov 2026 (download time not recorded), 2,093 scores of 174 models on 57 benchmarks |

**Data flow:** `notebooks/eci_scores/` downloads or reuses the raw file in `raw/`, writes `model_capability.csv` to `processed/`, and the file is copied by hand into `data/`. View 1 reads only `data/model_capability.csv`. View 3 reads `data/gpqa_reported_vs_epoch.csv` and uses `data/model_capability.csv` for the access group. View 2 also reads `data/hub_scores_by_model.csv`, `data/hub_model_coverage.csv` and `data/hub_data_currency.csv`, which come from `notebooks/benchmark_hub/` (see the View 2 section and `DATA_DICTIONARY_4B.md`). One difference from the other notebooks: the benchmark_hub notebook copies its three page files into `data/` itself when `COPY_TO_APP = True`. The notebook is a copy of notebook 01 with the folder name, the manual folder and the output step changed.

**Licence check at every refresh:** Every time the data is downloaded again, for each new open-weight model and each model that Epoch labels restricted use, non-commercial or unknown, open the LICENSE file on Hugging Face or GitHub and read it. Epoch's label and news pages do not replace it. Record the licence name, whether commercial use is allowed, the condition (revenue line, user line or Model-as-a-Service clause), whether internal use is exempt, whether Epoch's label agrees with the text, the link and the date read. Add the reading to `licence_check.csv`. Then check whether the accessible best model in View 1 rests on a restricted use or non-commercial licence, and say so in the page text if it does. View 1 counts every open-weight model as accessible whatever its licence.

## Limitations

- **Capability index:** Epoch's index leans to maths and reasoning, covers smaller and non-US models less well, and the 90% intervals of neighbouring models overlap.
- **Excluded models:** Models with no open weights and no stated country (17 older models) belong to neither side, so neither side can be claimed for them.
- **Prediction:** The data cannot show when US access returns or whether the gap keeps shrinking.
- **Different group definitions:** Epoch published its own open-weight lag figures (about 3 months in October 2025 and about 4 months in May 2026, as recorded in the A3P1 documentation and not re-checked here). The groups are defined differently, so the numbers should not be compared without saying so.

## Restrictions

- **Restricted and accessible:** Restricted means a US developer with no downloadable weights. Accessible means open weights from any country or a service from a developer outside the US. This is a rule and not a measurement.
- **Hong Kong availability:** The restriction is the premise of the story and was not measured.
- **Epoch data licence:** Creative Commons Attribution. The page read does not state a version, so the version is to be confirmed on the dataset page ([epoch.ai/data](https://epoch.ai/data)).

## Options for the independent benchmark part (V3)

Found on 5 Nov 2026 and recorded in the A3P1 documentation. Not re-checked here. Status on 18 Nov 2026:

- **A.** Epoch self-reported against Epoch-run GPQA, eight models. Built as View 3, with the Mistral row left out of the chart.
- **B.** Developer-reported GPQA for 2026 accessible models against Epoch runs. Not built. The Epoch Benchmarking Hub holds no model with both an Epoch run and a developer-reported score on GPQA, so there is nothing to compare.
- **C.** ECI evidence mix. Built as View 2 from the Hub files, with 81 named sources labelled by one reader.

## Checks

| Check | Result |
|---|---|
| The page table built from `model_capability.csv` against the same columns of `models.csv` in the A3P1 app | Identical values, types and row order (277 models) |
| Visible text of the View 1 page against the A3P1 tab 3, from the "User story" line down | No difference |
| Notebook run in a cloud copy, output compared with the original `model_capability.csv` | Same content (277 rows, 16 columns). Only the line endings differ between Windows and the cloud |
| Whole build from zero in a fresh virtual environment (`pip install -r requirements.txt -r requirements-notebook.txt`, Python 3.13): notebook run, `processed/model_capability.csv` copied by hand into `data/` | Same content as the earlier files (277 rows, 16 columns). Run on 9 Nov 2026 |
| Page run inside `app.py` and on its own (`streamlit run stories/<story>/page.py`), text from "User story" down compared with the A3P1 tab | No difference in both cases. Screenshot of the in-app page checked by eye |
| View 2 notebook run in a cloud copy, with checks that stop the run (unique score per model, benchmark and kind, scores between 0 and 100, shares sum to 100) | All checks passed. Run on 17 Nov 2026 |
| View 2 counts rebuilt by a second implementation that used only the 415 Hub versions matched in the first run | Matched the first run exactly (Accessible 191, 151, 96, 361 and Restricted 13, 127, 381, 605 for 2023 to 2026). The final matching adds 77 versions, so 2025 and 2026 are higher |
| View 2 tests (`tests/test_view4b.py`, 14 tests) and a Chrome run of the clicks, row selection, year and model choice and the four sections | 14 passed, no JavaScript error. Run on 17 Nov 2026 |
| View 3 difference chart tests (`tests/test_v3_difference.py`, 9 tests: eight rows and groups, differences against the CSV by hand, Mistral left out, counts and order, texts, records table and CSV text, figure shapes, bad data stops the load, page renders without filters and with a Filtered records section) and a Chrome run with the sections opened, a hover and the CSV download (7 rows, no Mistral) | 9 passed, no JavaScript error. Page run once inside `page.py` with no exception and the order View 1, View 2, View 3. Run on 18 Nov 2026 |

| Renumbering of the chart names (18 Nov 2026): a script replaced the old names in the code, docs and README (numbers restart in every story), and the whole app was run with `streamlit.testing` (all four pages, no exception) | See MEMORY.md section 8am for the result and the list of changed files |

These checks were run by Claude. Ian has not reviewed them yet.
