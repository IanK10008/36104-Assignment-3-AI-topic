# Story 1a: ranked shortlist

**Owner:** Ian  **Data snapshot:** Epoch and LiteLLM retrieved 12 Nov 2026, LMArena leaderboard published 9 Nov 2026 (the earlier snapshot of 17 Oct 2026 was replaced on 13 Nov 2026)

**Status:** both views are built and were reviewed with Ian on 13 Nov 2026. The page started as a copy of the A3P1 app (Views 1 and 2) and has been changed since, as listed under "Changes after A3P1". Story 1a is a proposed split of user story 1 and the group has not agreed to it yet.

## Persona and scenario

**Persona:** group enterprise architect at an Asia-Pacific bank or insurer with operations in Hong Kong and other markets.

**Scenario:** The risk committee has asked for an approved list of AI models for staff and internal tools. The leading closed US models are not offered in Hong Kong. The committee wants an interim list within one to two weeks. The architect must choose between API services from outside the US and self-hosted open weights, and the committee will ask what capability is given up, what each route costs, and which models the bank may run itself.

**Task:** Produce an interim approved list. For each candidate model, say which route it uses (API or self-hosted), what its licence allows, how much capability it gives, and what it costs.

**Constraints (assumed, to validate with the group):**

- **Time:** One to two weeks. The list is interim, so each version is kept with its date and sources.
- **Organisation:** The committee needs reasons, not a single score.
- **Data:** Capability and licence class come from files, but data control is a proxy and availability by place is not measured.
- **Scope:** Regulator rules, the organisation's own tasks, hosting cost and security review are not covered.

**Source of this section:** GitHub, 01b Alternative Proposal (No Search ABC), "Primary persona, scenario and three user stories".

**Core question:** In regions where leading closed US models are restricted, which accessible AI model gives an organisation the most measured capability for its cost and self-hosting feasibility?

## User story

**Story 1 (full):** As a group enterprise architect, I want to pick a route (API or self-hosted) and shortlist the accessible models whose licence fits it, ranked with capability set against price, so that I can build an interim approved list the risk committee will accept.

**Story 1a (proposed split):** As a group enterprise architect, I want to rank the accessible models by capability, human preference and price, so that I can see which models are worth putting on the interim approved list.

## Charts used

| Proposal chart | App view | Chart type | What it shows |
|---|---|---|---|
| V4 | View 1 | Scatter plot with price frontier | Capability against price for each model with a price (LMArena is not used) |
| V1 | View 2 | Stacked bars | Weighted ranking from capability, human preference and low price |

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Epoch Capabilities Index, file `eci_scores.csv` | Capability (View 1 and View 2) | Retrieved 12 Nov 2026 19:04 UTC, models released 24 Feb 2023 to 9 Nov 2026 (256 models) |
| LiteLLM price file `model_prices_and_context_window.json` | Output price per million tokens (View 1 and View 2, 5,834 model rows, 188 of the 256 Epoch models have a price) | Retrieved 12 Nov 2026 19:12 UTC, the file carries no date of its own |
| LMArena leaderboard (text, latest split) | Human preference (View 2 only, 148 of the 256 Epoch models have a rating) | Downloaded 12 Nov 2026 19:08 UTC, published 9 Nov 2026 |

**Models covered:** at the default settings (released 2025 to 2026) View 1 plots 126 models with a price and 7 of them lie on the price frontier. View 2 ranks the 98 models that appear in all three sources (same name or same name plus a tag). 28 models have a price but no LMArena rating and are not ranked. The rule "same name only" leaves 44 models. The counts of the earlier snapshot of 17 Oct 2026 were 117, 10, 84, 33 and 44.

**Data flow.** There are three notebooks and three files in `data/`. They are kept apart and are not combined in any notebook.

| Notebook | Writes to `processed/` | Copied by hand into `data/` |
|---|---|---|
| `notebooks/eci_scores/eci_scores.ipynb` (copy of notebook 01) | `model_capability.csv` | `model_capability.csv` |
| `notebooks/litellm_prices/litellm_prices.ipynb` (copy of notebook 04) | `model_price.csv` | `model_price.csv` |
| `notebooks/lmarena_leaderboard/lmarena_leaderboard.ipynb` (copy of notebook 06) | `lmarena_ratings.csv` | `lmarena_ratings.csv` |

The combining is done when the page loads, in `load()` in `page.py`, with the A3P1 rules in `src/data.py`: (1) cut the slim columns from each file (all Epoch models, LiteLLM chat models with an output price, the overall LMArena text board), (2) match the three sources by model name and build one row per Epoch model, (3) validate the table. Nothing is written to the story folder. The result is a 256-row table. For the earlier snapshot of 17 Oct 2026 it was the same 277-row table as `models.csv` in the A3P1 app. The two views and the controls start from the A3P1 code (`src/views.py`, `src/analysis.py` and `src/controls_1a.py`, which is the controls code of A3P1 `app.py`) with the changes listed below.

All three notebooks have `REFRESH = False`, so they reuse the files in `raw/` and the data match A3P1. Set it to `True` to try a fresh download. The numbers will then change.

## What the page shows

- **View 1, capability against price:** each dot is one model with a LiteLLM price (126 at the defaults), the colour is the route, and the black step line is the price frontier (7 models at the defaults). Route pills filter the groups, and hiding a group also removes it from the frontier. Frontier models are labelled with their ECI and price and listed in "Values behind the chart". The view uses no LMArena data and shows no ranking.
- **View 2, weighted ranking:** one bar per model, split into weight × percentile for capability, human preference and low price. Criteria pills, route pills and the rank-position pills ("Models shown") control it. The weights are CRITIC by default (27/26/47 at the defaults) or custom sliders.
- **Detail panel:** a click on a bar opens two tabs, "Why it ranks here" (original value, percentile, weight and weighted points per criterion) and "Where each number comes from" (name, match, column and file per source). No model is opened by default, so that the page does not present one model as the winner.
- **First-place share:** the share of the 1,033 different slider weightings under which a model ranks first (Gemini 4 Carbon (High) 39% and GLM-5.3-Flash 25% at the defaults). Every weighting counts equally, so the figure shows robustness to the weights and is not a probability of being the best model.
- **Sections under each chart:** the same four expanders in both views, "How to read this chart", "What this chart cannot show", "Values behind the chart" and "Filtered records" (with the download). The sources are given once, in the block "Data, methods and limitations" at the end of the page.
- **Form chosen for View 2:** a sorted horizontal bar chart (Visual Vocabulary: ranking) with each bar split into its weighted parts (part-to-whole). The bars share one baseline, so lengths are compared accurately, long model names fit on the left, and the score is printed at the end of each bar. This rationale was a "Design decision" section in the app until 13 Nov 2026 and is kept here.

## Changes after A3P1

- **View 1 without LMArena:** every Epoch model with a usable price is plotted with solid dots (126 at the defaults). The hollow dots, the name-match select and the dot-type pills of the earlier version are removed.
- **Top of the page:** the green "Top of the ranking" box is removed. A block "Data behind this page" gives the four counts with their retrieval dates and says which source is used in which view.
- **View 2:** the weights and the number of ranked models sit side by side, "Models shown" sits on one line, the detail panel opens only after a click, and "How the score is calculated" and the "Design decision" section are removed.
- **Naming:** "Wins under any weighting" is now "First-place share". A model that ranks first under fewer than half a percent of the weightings is shown as "under 1%".
- **Units and rounding:** the LMArena rating is a whole number and the ECI has one decimal in text and hovers. Tables and downloads keep the original values, except the computed weighted score and first-place share (one decimal). Dates read D Mon YYYY.
- **Price frontier:** the explanation has an example (Qwen3.5-9B against Qwen3-14B) and the note that models on the line are not ranked against each other.
- **Page-end block:** Story 1a has its own "Data, methods and limitations" (`limitations_1a()` in `src/shell.py`) that lists only the sources and methods of its two views. Stories 1b, 2 and 3 keep the shared block.
- **Text style:** bold lead-ins are short noun phrases, the word after the colon is lower case unless it is a proper noun, and there are no semicolons.

## Refreshing the data

1. Run the three notebooks with `REFRESH = True`. Each writes its table to `processed/` by itself, with `data_currency.csv` and `raw/retrieval_log.json`.
2. Copy the three tables from `processed/` into `data/` by hand (the notebooks never write there).
3. Restart the app. The dates, the counts, the frontier example, the correlation and the ECI interval width in the page text follow the data (`src/snapshot.py`).
4. By hand: the licence marks for new models with a limit (`LICENCE_NOTES` in `src/views.py`) and the numbers in this file.

## Limitations

- **Capability index:** Epoch's index leans to maths and reasoning, covers smaller and non-US models less well, and the 90% intervals of neighbouring models overlap.
- **Human preference:** LMArena voters are self-selected and longer, well-formatted answers win more often.
- **Price:** list price per token is not the cost per task. This is a snapshot and not a quote.
- **Name matching:** models are matched across sources by name, and ambiguous versions are left out. Only View 2 depends on the LMArena match.
- **Relative percentiles:** percentile ranks depend on which models are in the comparison, so a small gap counts as much as a large one when it moves a model by one place.
- **Double counting:** capability and preference agree at about 0.85, so equal weight on both tilts the ranking towards quality. CRITIC lowers both weights.
- **Not covered:** hosting cost, security review, provider data handling and performance on the bank's own documents and languages.

## Restrictions

- **Restricted and accessible:** restricted means a US developer with no downloadable weights. Accessible means open weights from any country or a service from a developer outside the US. This is a rule and not a measurement.
- **Hong Kong availability:** the restriction is the premise of the story and was not measured.
- **Licence labels (open issue):** View 2 groups the three Epoch open-weight labels together (unrestricted, restricted use, non-commercial). Six of the 98 ranked models carry a licence limit at the default settings (GLM-5.3, MiniMax-M3, Mistral Large 4, Kimi K3.1 Pro, Kimi K3 and Mistral Medium 3.5). Epoch's label and the licence text differ for Kimi K3 and GLM-5.3.
- **Epoch definitions:** restricted use is a licence that limits things such as user counts or permitted purposes. Non-commercial is a licence that does not allow commercial use. A missing or unclear licence also counts as non-commercial. Source: [Epoch open models report, Table A1](https://epoch.ai/blog/open-models-report), as recorded in the group's licence check of 18 Oct 2026.

### Models with a licence limit at the default settings

Rank is the position among the 98 ranked models at the default settings of 12 Nov 2026 data.

#### MiniMax-M2.7 (Epoch label: non-commercial, no longer in the Epoch file since the download of 12 Nov 2026, so the app shows no mark for it)

- **Licence type:** non-commercial licence ([Hugging Face LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-M2.7/blob/main/LICENSE), [GitHub LICENSE](https://github.com/MiniMax-AI/MiniMax-M2.7/blob/main/LICENSE)).
- **Free use:** personal use (including self-hosted coding, applications and research), and non-commercial use by non-profits, academic institutions and researchers ([Hugging Face LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-M2.7/blob/main/LICENSE)).
- **Commercial use:** needs a separate prior written authorisation from MiniMax. Requests go to api@minimax.io with the subject "M2.7 licensing". No revenue threshold is stated ([GitHub LICENSE](https://github.com/MiniMax-AI/MiniMax-M2.7/blob/main/LICENSE)).
- **Notice:** commercial use must display "Built with MiniMax M2.7" on the related website, interface or documentation ([GitHub LICENSE](https://github.com/MiniMax-AI/MiniMax-M2.7/blob/main/LICENSE)).
- **Prohibited uses:** any military purpose, unlawful content, harm to minors, harmful false information and discrimination ([GitHub LICENSE](https://github.com/MiniMax-AI/MiniMax-M2.7/blob/main/LICENSE)).

#### MiniMax-M3 (rank 22, Epoch label: restricted use)

- **Licence type:** MiniMax Community License ([Hugging Face LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE)).
- **Notice:** a notice is always required, even at or below the revenue line (subject "M3 licensing - notice"), and "Built with MiniMax M3" must be displayed ([Hugging Face LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE)).
- **Revenue line:** a separate prior written authorisation is needed above US$20 million yearly revenue ([Hugging Face LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE)).
- **Prohibited uses:** military purposes are listed among the prohibited uses ([Hugging Face LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE)).

#### Kimi K3 (rank 48, Epoch label: non-commercial)

- **Licence type:** Kimi K3 License ([Hugging Face LICENSE](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE), [GitHub LICENSE](https://github.com/MoonshotAI/Kimi-K3/blob/main/LICENSE)).
- **Commercial use:** allowed. A separate agreement is needed only if Model-as-a-Service revenue exceeds US$20 million in any 12 months ([GitHub LICENSE](https://github.com/MoonshotAI/Kimi-K3/blob/main/LICENSE)).
- **Internal use:** exempt from the separate-agreement requirement ([GitHub LICENSE](https://github.com/MoonshotAI/Kimi-K3/blob/main/LICENSE)).
- **Mismatch:** Epoch labels the model non-commercial but the licence text allows commercial use with a revenue condition.

#### Mistral Medium 3.5 (rank 89, Epoch label: restricted use)

- **Licence type:** Modified MIT License ([Hugging Face LICENSE](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE), [Mistral model page](https://docs.mistral.ai/models/mistral-medium-3-5-26-04)).
- **Notice:** the attribution notice and the permission notice must be kept in all copies or substantial portions of the model ([Hugging Face LICENSE](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE)).
- **Revenue line:** rights are not granted if the company's global consolidated monthly revenue exceeded US$20 million in the preceding month. The line also covers derivatives ([Hugging Face LICENSE](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE)).
- **Above the line:** a commercial licence from Mistral AI is needed, or the hosted services can be used ([Hugging Face LICENSE](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE), [Mistral help article](https://help.mistral.ai/en/articles/347393-under-which-license-are-mistral-s-open-models-available)). The help article describes modified MIT licences in general and does not name Medium 3.5.

#### GLM-5.3 (rank 13, Epoch label: restricted use)

- **Licence type:** GLM-5.3 License ([Hugging Face LICENSE](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE)).
- **Free use:** including commercial use, with the copyright and permission notice kept ([Hugging Face LICENSE](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE)).
- **Revenue line:** a Model-as-a-Service business with revenue above US$10 billion in any 12 months must pass Z.AI's security review before commercial use. Model-as-a-Service means giving third parties inference or fine-tuning access, for example by API ([Hugging Face LICENSE](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE)).
- **Mismatch:** Epoch's label is stricter than the licence text for most users.

#### Mistral Large 4 (rank 26, Epoch label: restricted use)

- **Licence type:** Mistral Ecosystem Open-Weight License, a modified MIT licence ([Hugging Face LICENSE](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE)).
- **Condition:** a business that operates a Model-as-a-Service offering needs a separate commercial licence from Mistral before commercial use. No revenue threshold is stated ([Hugging Face LICENSE](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE)).
- **Exempt:** internal use and use through Mistral's official products.
- **Notice:** the copyright and permission notice is kept in all copies.

#### Kimi K3.1 Pro (rank 33, Epoch label: restricted use)

- **Licence type:** Kimi K3.1-Pro License ([Hugging Face LICENSE](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/main/LICENSE)).
- **Revenue line:** a Model-as-a-Service business with revenue above US$20 million in any 12 months needs a separate agreement with Moonshot AI ([Hugging Face LICENSE](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/main/LICENSE)).
- **Notice:** a commercial product with more than 100 million monthly users or more than US$20 million monthly revenue must display "Kimi K3.1-Pro" in its interface. Internal use is exempt.
- **Mismatch:** none found, Epoch's label and the licence text agree.

**How the readings were made:** MiniMax-M3 and Kimi K3 were read on 18 Oct 2026 in the group's licence check. MiniMax-M2.7, Mistral Medium 3.5, GLM-5.3, Mistral Large 4 and Kimi K3.1 Pro were read on 13 Nov 2026 on the licence pages with Claude's fetch tool, which returns the passages as paraphrase and short quotes. The content of the earlier notes was confirmed. The app links the licence pages and shows this reading in the hover. The full terms need checking by legal or procurement before any approval.

### Data licences

| Dataset | Licence | Link | Checked |
|---|---|---|---|
| LMArena leaderboard | CC BY 4.0 | [Hugging Face dataset](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset) | 18 Oct 2026 |
| LiteLLM price file | MIT, except the enterprise/ directory, which has its own licence. The price JSON sits at the repository root. | [LICENSE](https://github.com/BerriAI/litellm/blob/main/LICENSE) | 18 Oct 2026 |
| Epoch AI data | Creative Commons Attribution. The page read does not state a version, so the version is to be confirmed on each dataset page. | [epoch.ai/data](https://epoch.ai/data) | 18 Oct 2026 |

- **Not legal advice.** The licence classes are Epoch's labels and the group's own reading. A bank deploying any of these models should check the full licence text with its own counsel.

## Checks

**Checks of 13 Nov 2026 before the data refresh**, on the data of 17 Oct 2026 (Claude, each could have failed):

| Check | Result |
|---|---|
| Page run with AppTest at the defaults and with two criteria | No exception in both runs |
| Old wording ("Wins under any weighting", per-chart Sources footer, "Showing the model ranked first", "still to be re-read") searched in the page text | Not found |
| Counts at the defaults | 117 points in View 1 with 10 on the price frontier, 84 ranked in View 2, 33 priced without a rating, 44 with "same name only" |
| First-place share at the defaults | GLM-5.3-Flash 40%, Gemini 3.8 Flash (High) 23%, Gemini 4 Argon (High) 22%, gpt-oss-20b shown as "under 1%" |
| Claim "same name only changes the top pick" recomputed with capability at 80% | True: first place goes from Claude Opus 5.5 (84 models) to Qwen 3.8 Max (44 models) |
| Click on a bar opens the detail tabs | A real mouse click did not trigger the selection in headless Chromium. The selection event sent to the chart opened the tabs for GLM-5.3-Flash. A click in a normal browser is still to be tried |
| Licence pages of MiniMax-M2.7 and Mistral Medium 3.5 read again | Notes confirmed. The M2.7 notice and the military ban were added to the hover |
| Files written to D: | Modified time of each file compared before each write, no newer edit overwritten |

**Checks of 13 Nov 2026 after the data refresh** (Claude, each could have failed):

| Check | Result |
|---|---|
| Notebook `litellm_prices.ipynb` with the new LiteLLM file | It stopped at the validation (1.8% of entries without a host). Cause: 107 pointer entries (`alias_of`) and one routing block. The notebook now drops them, counts them and still stops for any other kind. Run in full in a cloud copy: 5,834 model entries, no problems |
| Page with the three new files | Stopped at two fixed values in `src/data.py` (latest release date 7 Oct 2026, 84 and 44 matches). The first is now a parsing guard and the second a plausibility check |
| Dates in the page text | Read from `data_currency.csv` and `retrieval_log.json` of the notebooks. A search of the page text finds no 17 Oct or 15 Oct date |
| Figures quoted in text | Correlation of capability with preference 0.79 (it was 0.85), typical ECI interval width 4 to 5 points (unchanged), frontier example chosen from the data (Qwen3.5-9B against Qwen3-8B) |
| AppTest at the defaults, with two criteria, with the rule "same name only" and with Open weights only | No exception in all runs |
| Licence marks | Three models with a limit had no mark (GLM-5.3, Mistral Large 4, Kimi K3.1 Pro). Marks added after reading the licence pages |

**Checks of 11 Nov 2026**, run before the changes above, on the data of 17 Oct 2026. They compared the page with the A3P1 app, so the text comparisons no longer apply. The data table and the LMArena rows are unchanged.

| Check | Result |
|---|---|
| The models table built by `load()` from the three files in `data/`, against `models.csv` of the A3P1 app (read with the A3P1 function `read_dataset`) | Exactly equal: values, column types and row order (277 rows, 24 columns) |
| The overall LMArena rows used by the detail panel, against `data/source/lmarena_overall.csv` of A3P1 | Equal (416 rows) |
| The `model_price.csv` and `lmarena_ratings.csv` written by the notebooks run in a cloud copy, against the files in the group's `Data` folder | Same content (4,206 and 11,033 rows). Only the line endings differ between Windows and the cloud |
| Page run inside `app.py` and on its own (`streamlit run stories/1a_ranked_shortlist/page.py`), text from "User story" down, against the A3P1 tab 1 | No difference in both cases (8,356 characters) |
| Same comparison after changing the Route and the Release window in both apps | No difference (8,343 characters) |

These checks were run by Claude on 11 Nov 2026. Ian has not reviewed them yet. Not compared: the charts pixel by pixel. One screenshot of the page was checked by eye.
