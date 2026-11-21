# Story 3: developers, what they disclose and what is reported (Views 1 and 2)

**Built by:** Yin, with Claude's help.  **Data snapshots:** AI Incident Database export of 16 Nov 2026 (latest incident 12 Nov 2026, latest model incident 29 Oct 2026), Stanford FMTI December 2025 edition, Epoch Capabilities Index file retrieved 20 Nov 2026 13:08 UTC.

**Status:** Views 1 and 2 are built and read only this folder's own data. Open items are listed under "Limitations" and "Checks". The data was refreshed on 20 Nov 2026 and the page text, counts and notebooks were updated to it. The chart names were changed on 18 Nov 2026 (see "Chart names").

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

**Story 3:** As a group enterprise architect, I want to see how openly each developer builds its models and how often it appears in reported incidents, so that I can tell the committee what is known and unknown about the developers we would rely on.

**Questions answered:**

- **View 1:** How much does each developer disclose about how it builds its models?
- **View 2:** How often does each developer appear in reported model incidents, and what went wrong?

**Framing:** Story 3 shows what public evidence exists about each developer and shows the gaps as gaps. It contains no benchmark data. The FMTI score is read as an indicator of disclosure practice and not as a score of the models in Story 1a View 1 and Story 1a View 2.

## The 11 developers

The page covers the 11 developers in scope: OpenAI, Anthropic, Google, Meta, xAI, Mistral AI, DeepSeek, Alibaba, Z.ai, Moonshot and MiniMax.

| Group | Developers | Count |
|---|---|---|
| Scored by FMTI | OpenAI, Anthropic, Google, Meta, xAI, Mistral AI, DeepSeek, Alibaba | 8 |
| Not scored by FMTI | Z.ai, Moonshot, MiniMax | 3 |
| Scored by FMTI, not one of the 11 | AI21 Labs, Amazon, IBM, Midjourney, Writer | 5 |

FMTI scores 13 companies in total (8 of the 11 and 5 others). View 1 shows light grey names for the five others and grey rows for the three unscored developers.

## Charts used

| View | Chart type | What it shows |
|---|---|---|
| 1 | Heatmap, 16 rows by 19 subdomains | Indicators disclosed by each company in each FMTI subdomain, with rows grouped by headquarters region and columns grouped by domain |
| 2 | Event timeline (dot strip plot) with an aligned monthly stacked bar on a shared time axis | Model incidents by developer and incident type, with Epoch model releases as triangles |

**Filters:** View 1 has headquarters region, domain, companies and subdomains. View 2 has a period slider (default 2020 to 2026), incident type, headquarters region, developers and a toggle for Epoch model releases.

**Chart names:** Until 17 Nov 2026 the charts were called View 1, 2, 3, 3b, 4, 4B, V3, 5a and 5b. On 18 Nov 2026 the charts of each story were numbered from 1 in page order. Story 1a has View 1 and View 2 (unchanged). Story 1b has View 1 (earlier View 3) and View 2 (earlier View 3b). Story 2 has View 1 (earlier View 4), View 2 (earlier View 4B) and View 3 (earlier V3, the proposal chart). Story 3 has View 1 (earlier View 5a) and View 2 (earlier View 5b). A chart of another story is named with its story, for example Story 2 View 1. File names (`view4b.py`, `v3_difference.py`, `DATA_DICTIONARY_4B.md`, `DATA_DICTIONARY_V3.md`) and the proposal chart ids (V1 to V7) are unchanged.

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Stanford Foundation Model Transparency Index, December 2025 edition | 100 yes-or-no indicators for 13 companies, each for the flagship model that the company selected as of May 2025 | Retrieved 20 Nov 2026 13:08 UTC from the repository `stanford-crfm/fmti` |
| AI Incident Database, weekly Excel export, sheet `Incidents` (Responsible AI Collaborative) | Incident date, title, alleged developer, MIT risk domain | Export of 16 Nov 2026, retrieved 20 Nov 2026 14:25 UTC. Model incidents from 23 Mar 2020 to 29 Oct 2026 are kept |
| MIT AI Risk Repository risk domains | Incident type for 252 of the 343 counted incidents | Labels as carried in the AI Incident Database export |
| Epoch Capabilities Index, file `eci_scores.csv` | Model release dates, capability index and the number of models of each developer | Retrieved 20 Nov 2026 13:08 UTC, 257 models released 24 Feb 2023 to 17 Nov 2026 |

**Files written by the group:**

- **Labels of 425 incidents:** `manual/aiid_incident_labels.csv`. Each of the 425 incidents that name one of the 11 developers is labelled as model incident or not.
- **Incident type of 91 incidents:** `manual/aiid_assigned_mit_domain.csv`. The group's reading for the incidents that MIT had not classified.
- **Company table:** `manual/fmti_companies.csv`. Headquarters, region, whether the company submitted its own report, the flagship model assessed and whether the company is one of the 11 developers.

**Data flow.** Three notebooks write to `processed/`, and four files are copied by hand into `data/`. Nothing is joined in a notebook.

| Notebook | Writes to `processed/` | Copied by hand into `data/` |
|---|---|---|
| `notebooks/fmti_scores/fmti_scores.ipynb` | `fmti_dec2025_scores_tidy.csv`, `fmti_companies.csv`, `data_currency.csv` | `fmti_dec2025_scores_tidy.csv`, `fmti_companies.csv` |
| `notebooks/aiid_model_incidents/aiid_model_incidents.ipynb` | `aiid_model_incidents_by_developer.csv`, `aiid_not_counted_incidents.csv`, `data_currency.csv` | `aiid_model_incidents_by_developer.csv` |
| `notebooks/eci_scores/eci_scores.ipynb` | `model_capability.csv`, `data_currency.csv` | `model_capability.csv` |

The files `incidents.csv` and `incident_developers.csv` in `data/` and the notebook `notebooks/aiid_incidents/` come from the earlier version of this page. Views 1 and 2 do not read them.

## What the page shows

**View 1. FMTI heatmap.**

- **Cell:** the indicators a company discloses in a subdomain, over the indicators in that subdomain.
- **Rows:** one row per company, grouped by headquarters region and sorted A to Z inside each group, so the order is not a ranking. The China group comes last.
- **Grey rows:** Z.ai, Moonshot and MiniMax close the China group. FMTI did not score them, so a grey row is a gap in the evidence.
- **Total score:** the official total out of 100 is not drawn in the chart. It is in the table under "Values behind the chart".

**View 2. Incident timeline.**

- **Counted:** 1,561 incidents since 2020, of which 425 name one of the 11 developers (403 in the developer field and 22 only in the implicated systems) and 343 are model incidents. The other 82 are platform products (61), operations cases (5) and cases that name a developer only as the place of a scam (16).
- **Dots:** one dot per incident and named developer, which gives 406 dots for 343 incidents. 33 incidents name more than one developer.
- **Incident type:** four types made from the MIT risk domains. By type: 150 wrong output or failure, 41 data and security, 83 misuse by others and 69 harm to users or society.
- **Triangles:** the release dates of Epoch models. The chart does not test whether releases cause incidents.

## Changes after A3P1

- **Replaced:** the A3P1 tab on developers in reported incidents (a stacked column chart by year above a ranking by developer) is replaced by Views 1 and 2.
- **Added:** the openness half of the story is now covered by View 1, and the incident half by View 2 with MIT risk domains and Epoch release dates.
- **Settled during the build:** Z.ai, Moonshot and MiniMax are kept as grey rows. The metric "Mean of the 13" and the total score column are removed from View 1. The incident type filter is the only control for type in View 2. Help icons sit next to their labels in the whole app.

## Refreshing the data

- **FMTI:** run `fmti_scores.ipynb` and copy the two files into `data/`. FMTI scores are fixed for one edition, so a new download changes nothing until a new edition is published.
- **AIID:** download a newer weekly export into `raw/`, update `retrieval_log.json`, run `aiid_model_incidents.ipynb` and copy the file into `data/`. The two manual label files must be extended for new incidents. The notebook stops and lists any incident that names one of the 11 developers and has no label, and any model incident that has no MIT class or assigned class. The counts typed in `src/views_story3.py` (constants at the top) must then be updated by hand.
- **Epoch:** with `REFRESH = False` the notebook reuses the file retrieved on 20 Nov 2026, so the data is as old as that date.

## Limitations

- **Disclosure, not practice (View 1):** an indicator counts when the company publishes the item. How well the company does it is not measured.
- **One flagship model per company (View 1):** the models are the flagships that the companies selected as of May 2025. Newer models are not covered.
- **Different evidence (View 1):** seven companies submitted their own reports and six did not. A zero for the six can mean that the item was not found.
- **Eight of 11 (View 1):** nothing in the page says how Z.ai, Moonshot or MiniMax compare, because FMTI does not score them.
- **Reports, not failures (View 2):** a count shows what was reported and not how often a model fails. Counts follow use and press attention as well as risk.
- **Language (View 2):** the database draws on English-language media, so the five developers based in China cannot be compared with those based in the United States.
- **Types set by the group (View 2):** 91 incidents had no MIT risk domain, 88 of them from 2025 and 2026. The group assigned the closest domain, with AI assistance in the reading. Anh checked the first 66 of the 91 types and a random sample of 30 of the first 400 of the 425 labels on 19 Nov 2026. The result is in `AI_PROVENANCE_MATRIX.csv`. The 25 labels and 25 types added with the export of 16 Nov 2026 followed the same method and definitions that Anh checked, and no second person checked them.
- **Export age (View 2):** the database adds incidents every week, so a later export holds more incidents than the export of 16 Nov 2026.
- **Developer as recorded (View 2):** naming a developer is not proof of fault.

## Restrictions

- **Stanford FMTI licence:** CC BY 4.0. The `LICENSE.md` in the repository ZIP retrieved on 20 Nov 2026 holds the text of Attribution 4.0 International and the README says that the data and visuals are licensed CC BY. Credit and a note of changes are given in the app.
- **AI Incident Database licence:** the group's notes record CC BY-SA 4.0. Snapshots page: [incidentdatabase.ai/research/snapshots](https://incidentdatabase.ai/research/snapshots/).
- **Epoch data licence:** Creative Commons Attribution. The page read does not state a version ([epoch.ai/data](https://epoch.ai/data)).
- **MIT AI Risk Repository:** the licence was not read for this page. The labels are used as carried in the AI Incident Database export.
- **Credit:** The group's reading of 91 incident types, the 425 incident labels (343 of them model incidents) and the grouping of incident types are the group's own work and must not be credited to the AI Incident Database, MIT or Epoch.
- **Not legal advice.** The page is descriptive only.

## Checks

| Check | Result |
|---|---|
| FMTI scores file, 100 indicators per company, summed against the published totals | All 13 match. Direct evidence for 7 companies (IBM, DeepSeek, Alibaba, xAI, Midjourney, Meta, Mistral). The other 6 rest on a news article and the paper's averages |
| FMTI domains, indicator order against the indicator file | 100 of 100 matched, Upstream 34, Model 30 and Downstream 36 in 19 subdomains |
| View 1 unit tests (pytest, cloud copy) | 4 passed. Row order, grey rows without values, 13 scored rows equal to the tidy file, no click order that breaks the page |
| Help icon gap in the browser, Stories 1a, 1b, 2 and 3 | 6 px between label and icon. Before the change it was 270 to 1426 px on sliders and multiselects |
| View 2 controls look | Developers and Incident type start within 1 to 2 px at three window widths |
| Page on the data of 20 Nov 2026: all four pages at 1366x768 in headless Chromium searched for the old dates and counts. 14 counts in the text (1,561, 343, 406, 33, 252, 91, 88, 101, 73, 204 and the four type counts) compared with `data/` by a script. Primary keys of the Story 3 data files tested. Empty Developers and Incident type selection | No old date or count found. All 14 counts match. All keys hold. Each empty selection shows "Choose at least one developer and one group" without an exception. Run on 20 Nov 2026 |
| Page at 1366x768 in headless Chromium, run on the local code (18 Nov 2026) | Document width 1366, charts 1174 px wide, no element beyond the window, so no horizontal scroll (rubric check 23) |
| Empty selections (`streamlit.testing`, 18 Nov 2026): no company or no subdomain in View 1, no developer or no incident type in View 2 | Each shows a "Choose at least one" message and raises no exception (rubric check 22). The period slider cannot give an empty period |
| Colour vision simulation (protan, deutan and tritan, 18 Nov 2026) of the colours of both views | Incident types: smallest colour difference 17.0 to 22.7 under colour vision deficiency, 53.6 in normal vision (CIE76). Domains 17.0 to 55.7. The heatmap steps keep their order by lightness and the smallest step difference is 15.6 to 24.2. No pair collapses and tritan is the lowest. Simulation only, not seen in a browser (rubric check 18) |
| Values readable without hovering (18 Nov 2026) | Partly met. View 1 shows the value in every heatmap cell. In View 2 the monthly totals are on the chart but the value of each incident dot shows on hover, and the values tables of both views sit in closed sections (rubric check 17) |

These checks were run by Claude.
