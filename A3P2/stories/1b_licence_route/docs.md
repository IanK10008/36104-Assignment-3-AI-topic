# Story 1b: licence and route (View 3)

**Owner:** Anh  **Data snapshot:** Epoch file retrieved 17 Oct 2026 22:27 UTC (18 Oct 2026 in Sydney)

**Status:** page built and checked against the A3P1 app. View 3b (licence mix by year) added by Anh on 13 Nov 2026. Story 1b is a proposed split of user story 1 and the group has not agreed to it yet.

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

**Story 1 (full):** As a group enterprise architect, I want to pick a route (API or self-hosted) and shortlist the accessible models whose licence fits it, ranked with capability set against price, so that I can build an interim approved list the risk committee will accept.

**Story 1b (proposed split):** As a group enterprise architect, I want to see which open-weight models the bank may run on its own servers under their licences, so that I can choose between self-hosting and an outside API with the risk committee.

**Question answered:** How much capability can the bank run on its own servers, by licence class?

## Chart used

| Proposal chart | App view | Chart type | What it shows |
|---|---|---|---|
| V7 | View 3 | Dot strip | Each model as a dot by licence class, with the best model of each class labelled and the best model of any kind marked |
| new (Anh) | View 3b | 100% stacked bar | Licence mix of the open-weight models released each year: unrestricted, restricted use, non-commercial, with the count and share in every segment |

**Visual Vocabulary family:** View 3, distribution (as recorded in MEMORY.md section 8p). View 3b, part-to-whole.

## View 3b: licence mix by release year (added by Anh, 13 Nov 2026)

**Why it was added:** View 3 shows how much capability each licence class holds today, but not whether the self-hosting route is widening. The committee's question "which models may the bank run itself?" depends on the licences of new releases as well as on today's best model. View 3b also ties story 1b to the rise of AI: it shows a change over time in what the bank is allowed to do.

**Finding (all developer countries, all years):** the share of open-weight releases that Epoch labels unrestricted rose from 36% in 2023 (11 of 31) to 76% in 2025 (25 of 33) and 79% in 2026 (22 of 28, releases to 7 Oct). Restricted-use licences fell from 14 of 31 to 4 of 28. For China-based developers alone: 0 of 11 in 2023 to 18 of 22 in 2026.

**Controls:** the chart uses View 3's "Developer based in" control. It ignores the release window on purpose and always shows every year, because the default window (2025 to 2026) would cut the trend to two bars. An empty country selection, or countries with no open-weight models, shows a message instead of the chart.

**Code:** `licence_mix.py` in this folder (counts from `data/model_capability.csv`, no new data file), called from `page.py` inside View 3's fragment. Nothing in the shared `src/` folder was changed.

**Design decision:** visual task, how the licence mix of new open-weight models changed. Form chosen, 100% stacked bar per year with the count and share written in each segment (no hovering needed), Okabe-Ito colours. Rejected: stacked counts (2026 is a part year, so totals differ), one pie per year (angles across pies are hard to compare), a line of the unrestricted share only (hides the trade between restricted-use and non-commercial licences).

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Epoch Capabilities Index, file `eci_scores.csv` | Capability, release date, developer, country, Epoch accessibility label | Retrieved 17 Oct 2026 22:27 UTC, models released 24 Feb 2023 to 7 Oct 2026 (277 models) |
| The group's licence readings, written in the eci_scores notebook | Five licences read against the licence pages | Read 18 Oct 2026 |

**Data flow:** `notebooks/eci_scores/` downloads or reuses the raw file in `raw/`, writes `model_capability.csv` to `processed/`, and the file is copied by hand into `data/`. The page reads only `data/model_capability.csv`. The notebook is a copy of notebook 01 with the folder name, the manual folder and the output step changed.

## Licences read by the group (shown in the chart on hover)

| Model | Licence found | Link | Read on |
|---|---|---|---|
| Kimi K3 | Kimi K3 License. A separate agreement is needed above US$20 million Model-as-a-Service revenue in 12 months. Internal use is exempt. | [Hugging Face](https://huggingface.co/moonshotai/Kimi-K3), [GitHub](https://github.com/MoonshotAI/Kimi-K3/blob/main/LICENSE) | 18 Oct 2026 |
| DeepSeek V4 Pro 0813 | MIT License. The page covers the V4-Pro family and the 0813 release needs to be confirmed. | [Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | 18 Oct 2026 |
| Qwen 3.8 27B | Apache License 2.0. Whether Epoch's Qwen 3.8 27B is the same release needs to be confirmed. | [Hugging Face](https://huggingface.co/Qwen) | 18 Oct 2026 |
| MiniMax-M3 | MiniMax Community License. A notice is always required. A separate authorisation is needed above US$20 million yearly revenue. Military use is prohibited. | [Hugging Face](https://huggingface.co/MiniMaxAI/MiniMax-M3) | 18 Oct 2026 |
| GLM-5 | Field "License: mit" on the model page. No further licence document, per a team member's check of the repository. | [Hugging Face](https://huggingface.co/zai-org/GLM-5) | 18 Oct 2026 |

## Licence classes and Epoch's definitions

Epoch's accessibility label is read as what it allows a bank to do. **Restricted use** is a licence that limits things such as user counts or permitted purposes. **Non-commercial** is a licence that does not allow commercial use. A missing or unclear licence also counts as non-commercial. Source: [Epoch open models report, Table A1](https://epoch.ai/blog/open-models-report), as recorded in the group's licence check of 18 Oct 2026.

## Limitations

- **Licence label:** Epoch's label can disagree with the licence text. Epoch labels Kimi K3 non-commercial, but the licence text allows commercial use with a revenue condition.
- **Coverage of readings:** Only five licences were read. Every other open-weight model keeps Epoch's label.
- **View 3b, part year:** 2026 covers releases to 7 Oct 2026 only, so its total is lower and its share may still move. Counts cover only models Epoch has scored.
- **Capability index:** Epoch's index leans to maths and reasoning, covers smaller and non-US models less well, and the 90% intervals of neighbouring models overlap.
- **Not covered:** Licence terms beyond "open weights", provider data handling, security review, hosting cost and performance on the bank's own documents.
- **Not legal advice.** A bank deploying any of these models should check the full licence text with its own counsel.

## Restrictions

- **Epoch data licence:** Creative Commons Attribution. The page read does not state a version, so the version is to be confirmed on the dataset page ([epoch.ai/data](https://epoch.ai/data)).
- **Credit:** The licence column `licence_class_ours` is the group's own reading and must not be credited to Epoch.

## Checks

| Check | Result |
|---|---|
| The page table built from `model_capability.csv` against the same columns of `models.csv` in the A3P1 app | Identical values, types and row order (277 models) |
| Visible text of the View 3 page against the A3P1 tab 2, from the "User story" line down | No difference |
| Notebook run in a cloud copy, output compared with the original `model_capability.csv` | Same content (277 rows, 16 columns). Only the line endings differ between Windows and the cloud |
| Whole build from zero in a fresh virtual environment (`pip install -r requirements.txt -r requirements-notebook.txt`, Python 3.13): notebook run, `processed/model_capability.csv` copied by hand into `data/` | Same content as the earlier files (277 rows, 16 columns). Run on 9 Nov 2026 |
| Page run inside `app.py` and on its own (`streamlit run stories/<story>/page.py`), text from "User story" down compared with the A3P1 tab | No difference in both cases. Screenshot of the in-app page checked by eye |

| View 3b counts against the data file by hand (Anh, to do before commit): in `data/model_capability.csv`, open-weight rows released in 2023 = 31, of which `epoch_accessibility` = "Open weights (unrestricted)" = 11; in 2026 = 28, of which 22 | Must match the chart labels 11 (36%) and 22 (79%) |
| View 3b in the app (`streamlit.testing`, 13 Nov 2026): default page, China only, "Not stated" only (no open-weight models), empty selection; whole app with all four pages | No errors; the empty and no-open-weight states show their messages |

These checks were run by Claude. Ian has not reviewed them yet.
