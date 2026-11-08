# Story 2: gap to the restricted US models (View 4)

**Owner:** Rida  **Data snapshot:** Epoch file retrieved 17 Oct 2026 22:27 UTC (18 Oct 2026 in Sydney)

**Status:** the gap chart is built and checked against the A3P1 app. The part of the story about independent benchmarks (V3) is not built.

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

**Not covered yet:** The clause "check whether independent benchmarks agree with developer claims" (chart V3). The benchmark file has no flag that separates developer-reported scores from independent runs.

**Question answered:** How far do accessible models trail the restricted US models, and is the gap shrinking?

**Acceptance criteria (from the proposal):** The app shows the best accessible model against the best model overall by release date, with the confidence interval, units and time range stated. It says that the data cannot predict when US access returns.

## Chart used

| Proposal chart | App view | Chart type | What it shows |
|---|---|---|---|
| V2 | View 4 | Step lines with a shaded gap | Best score so far for the restricted US models and for the accessible models, the gap between them and the months behind |

**Visual Vocabulary family:** change over time (as recorded in MEMORY.md section 8p).

## What the page shows (default settings, 7 Oct 2026)

| Date | Best restricted | Score | Best accessible | Score | Gap (points) | Months behind |
|---|---|---|---|---|---|---|
| 7 Oct 2026 | Claude Opus 5.5 | 166.8 | Kimi K3 | 157.4 | 9.4 | 7 |
| 7 Apr 2026 | GPT-5.4 Pro | 159 | GLM-5.1 | 150 | 9 | 8 |
| 7 Oct 2025 | GPT-5 Pro | 150.7 | DeepSeek-V3.2-Exp | 145 | 5.8 | 6 |
| 7 Oct 2024 | o1-mini | 135.8 | Qwen2.5-72B | 129 | 6.8 | 5 |

These values were read from the rendered page and match the A3P1 app.

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Epoch Capabilities Index, file `eci_scores.csv` | Release date, capability score and interval, developer, country, accessibility label | Retrieved 17 Oct 2026 22:27 UTC, models released 24 Feb 2023 to 7 Oct 2026 (277 models) |

**Data flow:** `notebooks/eci_scores/` downloads or reuses the raw file in `raw/`, writes `model_capability.csv` to `processed/`, and the file is copied by hand into `data/`. The page reads only `data/model_capability.csv`. The notebook is a copy of notebook 01 with the folder name, the manual folder and the output step changed.

## Limitations

- **Capability index:** Epoch's index leans to maths and reasoning, covers smaller and non-US models less well, and the 90% intervals of neighbouring models overlap.
- **Excluded models:** Models with no open weights and no stated country (17 older models) belong to neither side, so neither side can be claimed for them.
- **Prediction:** The data cannot show when US access returns or whether the gap keeps shrinking.
- **Different group definitions:** Epoch published its own open-weight lag figures (about 3 months in October 2025 and about 4 months in May 2026, as recorded in the A3P1 documentation and not re-checked here). The groups are defined differently, so the numbers should not be compared without saying so.

## Restrictions

- **Restricted and accessible:** Restricted means a US developer with no downloadable weights. Accessible means open weights from any country or a service from a developer outside the US. This is a rule and not a measurement.
- **Hong Kong availability:** The restriction is the premise of the story and was not measured.
- **Epoch data licence:** Creative Commons Attribution. The page read does not state a version, so the version is to be confirmed on the dataset page ([epoch.ai/data](https://epoch.ai/data)).

## Options for the part not built (V3)

Found on 5 Nov 2026 and recorded in the A3P1 documentation. Not re-checked here.

- **A.** Epoch self-reported against Epoch-run GPQA. Eight models.
- **B.** Developer-reported GPQA for 2026 accessible models against Epoch runs. This is the most usable option for the story.
- **C.** ECI evidence mix. A hand classification of 74 source names is needed.

## Checks

| Check | Result |
|---|---|
| The page table built from `model_capability.csv` against the same columns of `models.csv` in the A3P1 app | Identical values, types and row order (277 models) |
| Visible text of the View 4 page against the A3P1 tab 3, from the "User story" line down | No difference |
| Notebook run in a cloud copy, output compared with the original `model_capability.csv` | Same content (277 rows, 16 columns). Only the line endings differ between Windows and the cloud |
| Whole build from zero in a fresh virtual environment (`pip install -r requirements.txt -r requirements-notebook.txt`, Python 3.13): notebook run, `processed/model_capability.csv` copied by hand into `data/` | Same content as the earlier files (277 rows, 16 columns). Run on 9 Nov 2026 |
| Page run inside `app.py` and on its own (`streamlit run stories/<story>/page.py`), text from "User story" down compared with the A3P1 tab | No difference in both cases. Screenshot of the in-app page checked by eye |

These checks were run by Claude. Ian has not reviewed them yet.
