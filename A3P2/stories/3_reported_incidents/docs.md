# Story 3: developers, what they disclose and what is reported (Views 5a and 5b)

**Built by:** Ian, with Claude's help.  **Data snapshots:** AI Incident Database export of 12 Oct 2026 (latest incident 3 Oct 2026), Stanford FMTI December 2025 edition, Epoch Capabilities Index file retrieved 17 Oct 2026 22:27 UTC.

**Status:** Views 5a and 5b are built and read only this folder's own data. Open items are listed under "Limitations" and "Checks". The Story 3 notebooks and the app files were last changed on 14 to 16 Nov 2026.

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

**Questions answered:**

- **View 5a:** How much does each developer disclose about how it builds its models?
- **View 5b:** How often does each developer appear in reported model incidents, and what went wrong?

**Framing:** Story 3 shows what public evidence exists about each developer and shows the gaps as gaps. It contains no benchmark data. The FMTI score is read as an indicator of disclosure practice and not as a score of the models in View 1 and View 2.

## The 11 developers

The page covers the 11 developers in scope: OpenAI, Anthropic, Google, Meta, xAI, Mistral AI, DeepSeek, Alibaba, Z.ai, Moonshot and MiniMax.

| Group | Developers | Count |
|---|---|---|
| Scored by FMTI | OpenAI, Anthropic, Google, Meta, xAI, Mistral AI, DeepSeek, Alibaba | 8 |
| Not scored by FMTI | Z.ai, Moonshot, MiniMax | 3 |
| Scored by FMTI, not one of the 11 | AI21 Labs, Amazon, IBM, Midjourney, Writer | 5 |

FMTI scores 13 companies in total (8 of the 11 and 5 others). View 5a shows light grey names for the five others and grey rows for the three unscored developers.

## Charts used

| View | Chart type | What it shows |
|---|---|---|
| 5a | Heatmap, 16 rows by 19 subdomains | Indicators disclosed by each company in each FMTI subdomain, with rows grouped by headquarters region and columns grouped by domain |
| 5b | Event timeline (dot strip plot) with an aligned monthly stacked bar on a shared time axis | Model incidents by developer and incident type, with Epoch model releases as triangles |

**Filters:** 5a has headquarters region, domain, companies and subdomains. 5b has a period slider (default 2020 to 2026), incident type, headquarters region, developers and a toggle for Epoch model releases.

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Stanford Foundation Model Transparency Index, December 2025 edition | 100 yes-or-no indicators for 13 companies, flagship models assessed in May 2025 | Retrieved 17 Oct 2026 22:51 UTC from the repository `stanford-crfm/fmti` |
| AI Incident Database, weekly Excel export, sheet `Incidents` (Responsible AI Collaborative) | Incident date, title, alleged developer, MIT risk domain | Export of 12 Oct 2026, retrieved 17 Oct 2026 23:10 UTC. Incidents from 23 Mar 2020 to 3 Oct 2026 are kept |
| MIT AI Risk Repository risk domains | Incident type for 252 of the 318 counted incidents | Labels as carried in the AI Incident Database export |
| Epoch Capabilities Index, file `eci_scores.csv` | Model release dates, capability index and the number of models of each developer | Retrieved 17 Oct 2026 22:27 UTC, 277 models released 24 Feb 2023 to 7 Oct 2026 |

**Files written by the group:**

- **Labels of 400 incidents:** `manual/aiid_incident_labels_400.csv`. Each of the 400 incidents that name one of the 11 developers is labelled as model incident or not.
- **Incident type of 66 incidents:** `manual/aiid_66_assigned_mit_domain.csv`. The group's reading for the incidents that MIT had not classified.
- **Company table:** `manual/fmti_companies.csv`. Headquarters, region, whether the company submitted its own report, the flagship model assessed and whether the company is one of the 11 developers.

**Data flow.** Three notebooks write to `processed/`, and four files are copied by hand into `data/`. Nothing is joined in a notebook.

| Notebook | Writes to `processed/` | Copied by hand into `data/` |
|---|---|---|
| `notebooks/fmti_scores/fmti_scores.ipynb` | `fmti_dec2025_scores_tidy.csv`, `fmti_companies.csv`, `data_currency.csv` | `fmti_dec2025_scores_tidy.csv`, `fmti_companies.csv` |
| `notebooks/aiid_model_incidents/aiid_model_incidents.ipynb` | `aiid_model_incidents_by_developer.csv`, `aiid_not_counted_incidents.csv`, `data_currency.csv` | `aiid_model_incidents_by_developer.csv` |
| `notebooks/eci_scores/eci_scores.ipynb` | `model_capability.csv`, `data_currency.csv` | `model_capability.csv` |

The files `incidents.csv` and `incident_developers.csv` in `data/` and the notebook `notebooks/aiid_incidents/` come from the earlier version of this page. Views 5a and 5b do not read them.

## What the page shows

**View 5a. FMTI heatmap.**

- **Cell:** the indicators a company discloses in a subdomain, over the indicators in that subdomain.
- **Rows:** one row per company, grouped by headquarters region and sorted A to Z inside each group, so the order is not a ranking. The China group comes last.
- **Grey rows:** Z.ai, Moonshot and MiniMax close the China group. FMTI did not score them, so a grey row is a gap in the evidence.
- **Total score:** the official total out of 100 is not drawn in the chart. It is in the table under "Values behind the chart".

**View 5b. Incident timeline.**

- **Counted:** 1,481 incidents since 2020, of which 400 name one of the 11 developers and 318 are model incidents. The other 82 are platform products (61), operations cases (5) and cases that name a developer only as the place of a scam (16).
- **Dots:** one dot per incident and named developer, which gives 377 dots for 318 incidents.
- **Incident type:** four types made from the MIT risk domains. By type: 137 wrong output or failure, 38 data and security, 78 misuse by others and 65 harm to users or society.
- **Triangles:** the release dates of Epoch models. The chart does not test whether releases cause incidents.

## Changes after A3P1

- **Replaced:** the A3P1 tab on developers in reported incidents (a stacked column chart by year above a ranking by developer) is replaced by Views 5a and 5b.
- **Added:** the openness half of the story is now covered by View 5a, and the incident half by View 5b with MIT risk domains and Epoch release dates.
- **Settled during the build:** Z.ai, Moonshot and MiniMax are kept as grey rows. The metric "Mean of the 13" and the total score column are removed from 5a. The incident type filter is the only control for type in 5b. Help icons sit next to their labels in the whole app.

## Refreshing the data

- **FMTI:** run `fmti_scores.ipynb` and copy the two files into `data/`. FMTI scores are fixed for one edition, so a new download changes nothing until a new edition is published.
- **AIID:** download a newer weekly export into `raw/`, update `retrieval_log.json`, run `aiid_model_incidents.ipynb` and copy the file into `data/`. The two manual label files must be extended for new incidents.
- **Epoch:** with `REFRESH = False` the notebook reuses the file retrieved on 17 Oct 2026, so the data is as old as that date.

## Limitations

- **Disclosure, not practice (5a):** an indicator counts when the company publishes the item. How well the company does it is not measured.
- **One flagship model per company (5a):** the assessed models are those of May 2025. Newer models are not covered.
- **Different evidence (5a):** seven companies submitted their own reports and six did not. A zero for the six can mean that the item was not found.
- **Eight of 11 (5a):** nothing in the page says how Z.ai, Moonshot or MiniMax compare, because FMTI does not score them.
- **Reports, not failures (5b):** a count shows what was reported and not how often a model fails. Counts follow use and press attention as well as risk.
- **Language (5b):** the database draws on English-language media, so the five developers based in China cannot be compared with those based in the United States.
- **Types set by the group (5b):** 66 incidents had no MIT risk domain, mostly from 2025 and 2026. The group assigned the closest domain, with AI assistance in the reading. A second group member has not yet checked these types or the 400 labels.
- **Export age (5b):** a newer weekly export exists and has not been used.
- **Developer as recorded (5b):** naming a developer is not proof of fault.

## Restrictions

- **Stanford FMTI licence:** CC BY, as stated in the repository README. Credit and a note of changes are given in the app. The licence text is to be read again on the repository before the final submission.
- **AI Incident Database licence:** the group's notes record CC BY-SA 4.0. The licence is to be confirmed on the snapshots page ([incidentdatabase.ai/research/snapshots](https://incidentdatabase.ai/research/snapshots/)) before the final submission. The share-alike condition for the group's labelled CSV files in a public repository is still open.
- **Epoch data licence:** Creative Commons Attribution. The page read does not state a version, so the version is to be confirmed on the dataset page ([epoch.ai/data](https://epoch.ai/data)).
- **MIT AI Risk Repository:** the licence was not read for this page. The labels are used as carried in the AI Incident Database export.
- **Credit:** The group's reading of 66 incident types, the 400 model incident labels and the grouping of incident types are the group's own work and must not be credited to the AI Incident Database, MIT or Epoch.
- **Not legal advice.** The page is descriptive only.

## Checks

| Check | Result |
|---|---|
| FMTI scores file, 100 indicators per company, summed against the published totals | All 13 match. Direct evidence for 7 companies (IBM, DeepSeek, Alibaba, xAI, Midjourney, Meta, Mistral). The other 6 rest on a news article and the paper's averages |
| FMTI domains, indicator order against the indicator file | 100 of 100 matched, Upstream 34, Model 30 and Downstream 36 in 19 subdomains |
| 5a unit tests (pytest, cloud copy) | 4 passed. Row order, grey rows without values, 13 scored rows equal to the tidy file, no click order that breaks the page |
| Help icon gap in the browser, Stories 1a, 1b, 2 and 3 | 6 px between label and icon. Before the change it was 270 to 1426 px on sliders and multiselects |
| 5b controls look | Developers and Incident type start within 1 to 2 px at three window widths |

**Not yet checked:** the look of the grey rows, the 5a hover and the colourbar title spacing in a browser, the second group member's check of the 66 types and 400 labels, and a full run of the three notebooks on Ian's computer.

These checks were run by Claude. Ian has not reviewed them yet.
