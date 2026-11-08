# Story 3: developers in reported AI incidents (View 5)

**Owner:** Yash  **Data snapshot:** AI Incident Database export of 12 Oct 2026 (latest incident 3 Oct 2026). Epoch file retrieved 17 Oct 2026 22:27 UTC.

**Status:** page built and checked against the A3P1 app. Only the incident half of the story is covered. The openness half (V5) is not built. Open data problems are listed below under "Open issues for the team". Please read them before anyone changes the chart.

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

**Story 3:** As a group enterprise architect, I want to see how openly each developer builds its models and how often it appears in reported incidents, so that I can tell the committee what is known and unknown about the developers we would rely on.

**Not covered yet:** The clause "how openly each developer builds its models" (chart V5). The page shows it in grey and says so under "What these charts cannot show".

**Question answered:** Which developers appear in reported AI incidents, and how often?

## Chart used

| Proposal chart | App view | Chart type | What it shows |
|---|---|---|---|
| V8 | View 5 | Stacked columns by year, above a sorted bar chart by developer | Incidents per year, and incidents naming each developer in the chosen period, each split into generative AI and other AI |

**Visual Vocabulary families:** change over time (top chart) and ranking (lower chart), as recorded in MEMORY.md section 8p.

## Years shown

This page starts in **2020**. A3P1 starts the slider in 2015 and the top chart in 2012. The reason is the counts in the AI Incident Database export of 12 Oct 2026:

| Years | Incidents a year | Generative AI by the notebook rule | Incidents naming a company, whole period |
|---|---|---|---|
| 2015 to 2019 | 24 to 50 | 0 to 3 | 89 in five years |
| 2020 to 2022 | 80 to 109 | 5 to 16 | |
| 2023 | 179 | 79 | |
| 2024 | 308 | 177 | |
| 2025 | 457 | 359 | |
| 2026 (to 3 Oct) | 257 | 195 | 459 for 2020 to 2026 |

Before 2020 there are too few incidents, and too few that name a company, to compare developers. 2020 to 2022 are kept as the years before ChatGPT (November 2022), so the jump from 2023 is visible against a baseline. The default start year of the lower chart stays at 2022, as in A3P1. To change the range, edit `SLIDER_FIRST_YEAR` and `CHART_FIRST_YEAR` at the top of `page.py`. The start year is a team decision.

One point for the team to weigh: Epoch lists only models released from 24 Feb 2023, so the column "Models in the Epoch list" does not cover the earlier years of the incident counts.

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| AI Incident Database, weekly Excel export, sheet `Incidents` (Responsible AI Collaborative) | Incident date, title, alleged developer text | Export of 12 Oct 2026, 1,734 incidents, latest incident 3 Oct 2026 |
| Epoch Capabilities Index, file `eci_scores.csv` | Number of models and best capability score for each developer | Retrieved 17 Oct 2026 22:27 UTC, models released 24 Feb 2023 to 7 Oct 2026 (277 models) |

**Data flow.** There are two notebooks and three files in `data/`. They are kept apart and are not combined in any notebook.

| Notebook | Writes to `processed/` | Copied by hand into `data/` |
|---|---|---|
| `notebooks/aiid_incidents/aiid_incidents.ipynb` (copy of notebook 10) | `incidents.csv`, `incident_developers.csv` (and two summary tables and `data_currency.csv`, not used by the page) | `incidents.csv`, `incident_developers.csv` |
| `notebooks/eci_scores/eci_scores.ipynb` (copy of notebook 01) | `model_capability.csv`, `data_currency.csv` | `model_capability.csv` |

The combining is done when the page loads (`src/aiid.py` and `src/context.py`):

1. `incident_developers.csv` is cut to the rows marked `named_company`, repeated rows for the same incident and company are removed, and five columns are kept. This gives the same table that A3P1 reads from `aiid_incident_developers.csv`.
2. The table is joined to `incidents.csv` by incident number (date, title and the generative flag are added).
3. The developer names are matched to Epoch's `organization` with the dictionary `EPOCH_NAMES` in `src/context.py`. This gives each company's number of Epoch models and best capability score.

## Open issues for the team

These were found while building A3P1 and A3P2 and are not fixed. None is decided. They are written here so the team can decide.

### 1. Epoch and AIID company names do not all match

- AIID names 16 companies. 11 have models in Epoch's `organization` field. **Tesla, ByteDance, Apple, Baidu and Tencent have no models in the Epoch list**, so the table shows 0 models (and a blank score) for them. 0 reads as "has no models", which is wrong. A label such as "not in the Epoch list" would be clearer.
- Names are matched through a short dictionary (`EPOCH_NAMES`): Google with Google DeepMind, Meta with Meta AI, Microsoft with Microsoft Research, Mistral with Mistral AI, Z.ai with Z.ai (Zhipu AI). Any other spelling is matched only when it is identical.
- **17 Epoch models have a blank organization.** They count for no developer. Nobody has checked whether some of them belong to a company in the list.
- AIID names deployers and developers of any AI system, while Epoch counts language models. A count of incidents and a count of models are not the same kind of thing. Companies with no incident are not shown.

### 2. The generative-AI flag has known errors

- Notebook 10 sets `is_generative_related` from the developer text only, with a keyword list and a named list (OpenAI, Anthropic, xAI, Mistral, DeepSeek, Moonshot, MiniMax, Z.ai). **Every OpenAI incident is flagged generative (190 of 190 rows), for example a video-game reinforcement-learning incident.** At the default settings OpenAI shows 176 incidents, all generative, Anthropic 39 of 39 and xAI 34 of 34.
- A second flag built from the export's `Implicated Systems` keywords (list written by Claude, not validated) disagrees on 180 incidents: 736 flagged by both, 118 only by the current rule, 62 only by the second rule and 818 by neither. The 62 include a Stable Diffusion bias case, an Air Canada chatbot and state deepfake campaigns, where the developer field names a government or an airline.
- Proposal, not decided: flag an incident if either signal fires, review a sample of 30 to 50 of the 180 disagreements to estimate the error rate, state that rate in the limitations and drop the rule that treats every OpenAI incident as generative. No perfect truth exists because AIID entries are alleged and editor written.
- The 2020 bar shows 16 generative incidents against 5 in 2021. The 16 are mostly GPT-3 and deepfake cases (and one chatbot in Korea), so the jump looks real and is not a flag error. This was read from the titles by Claude, not sampled by the team.

### 3. Most incidents name no company

- Only 557 of the 1,734 incidents name a company the notebook recognises. At the default settings (2022 to 2026) 394 of 1,310 incidents name a selected developer, which is 30%.
- The export has an `Implicated Systems` column that names the system (for example ChatGPT 103, Claude 25, Grok 24, Gemini 22, Meta AI 19). It is filled for 1,185 of 1,734 incidents (the data dictionary says all of them). It also holds generic terms (Deepfake Technology 418, Large Language Models 155, Social Media Platforms 139). The names are mostly products and not versions, so they match Epoch models only at the model-family level.
- A page based on specific systems instead of companies may answer the committee's question better. This is a design choice for the team.

### 4. Other limits that are already in the app

- Counts show exposure (how widely a product is used and how much English-language media covers it) and not risk. Companies based in China are under-counted, so they cannot be compared with US companies.
- 2026 is a partial year. Severity and harm are not compared. Developer is as alleged.
- The values table gives Streamlit a column that mixes numbers and blanks. Streamlit converts it with a warning in the log and the table shows correctly. A3P1 does the same.

## Please look for other data sources

The team is free to use other sources to answer the Story 3 question, with the same chart or a different one. The AI Incident Database is not required. A source is acceptable if it meets these conditions:

- **Public:** anyone can open or download it without a paid account.
- **Licensed for our use:** the licence allows reuse for a university project, and the licence text and version are written in the notebook with the date it was read.
- **Dated:** the notebook records when it was downloaded and what period it covers.
- **Complexity:** say in the notebook how much work it takes to clean (a download and a join, or hand classification of text).

Starting points, none of them checked for licence or coverage by Claude yet:

- AIAAIC repository and OECD AI Incidents Monitor (AIM). Both are blocked from the cloud environment and need a run on a local computer, as recorded in the A3P1 documentation.
- The AI Incident Database itself has other fields that A3P2 does not use: the MIT risk-domain labels (about 84% of recent incidents with a named developer, assigned by an AI model, so they need a caveat) and the `Implicated Systems` column described above.
- For the openness half (V5): the Foundation Model Transparency Index covers 13 developers (December 2025 edition), the FLI AI Safety Index grades 8 companies (December 2025), and Epoch publishes per-developer disclosure of parameters, compute and dataset size. Known is not the same as disclosed, so wording matters.
- Any other public list of AI incidents, AI safety reports or model cards with a licence that allows reuse. Say what each one measures. A count of reports follows media attention, and a transparency score follows what a developer chooses to publish.

For each new source, please write down: the link, the licence and the date it was read, the period covered, what one row means, and how developers or models would be matched to Epoch.

## Restrictions

- **AI Incident Database licence:** not re-read by Claude for this page. A3P1 lists the source in the app footer with the publisher and link. The licence of the export is to be confirmed on the snapshots page ([incidentdatabase.ai/research/snapshots](https://incidentdatabase.ai/research/snapshots/)) before the final submission.
- **Epoch data licence:** Creative Commons Attribution. The page read does not state a version, so the version is to be confirmed on the dataset page ([epoch.ai/data](https://epoch.ai/data)).
- **Credit:** The columns `is_generative_related` and `is_china_based` are the group's own rules and must not be credited to the AI Incident Database or to Epoch.
- **Not legal advice.** The page is descriptive only.

## Checks

| Check | Result |
|---|---|
| The notebook's two tables, cut and cleaned by `src/aiid.py`, against the A3P1 files `aiid_incidents.csv` and `aiid_incident_developers.csv` (after the same bool conversion and join) | Identical (1,734 incidents, 639 incident and company rows) |
| Page with the A3P1 year settings (slider from 2015, chart from 2012), text from "User story" down, against the A3P1 tab 4 | No difference |
| Page with this story's settings (from 2020), against the A3P1 tab 4 | Differences only in the slider's first year and the year labels of the top chart (2012 to 2019 are gone) |
| Notebook `aiid_incidents` run in a cloud copy on the export of 12 Oct 2026 (`REFRESH = False`) | No error. The output tables are the ones above |
| Whole build from zero in a fresh virtual environment (Python 3.13, both requirements files): both notebooks run, three files copied by hand into `data/` | Same content as the earlier files. Run on 9 Nov 2026 |
| Page run inside `app.py` and on its own, text from "User story" down | Same text in both |

These checks were run by Claude. Ian has not reviewed them yet.
