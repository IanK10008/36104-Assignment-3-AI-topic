# Story 1b: licence and route (Views 1, 2 and 3)

**Owner:** Anh  **Data snapshot:** Epoch file retrieved 17 Oct 2026 22:27 UTC (18 Oct 2026 in Sydney)

**Status:** page built and checked against the A3P1 app. View 2 (licence mix by year) added by Anh on 13 Nov 2026, restyled to Ian's layout and palette on 15 to 17 Nov 2026. Story 1b is a proposed split of user story 1 and the group has not agreed to it yet. The chart names were changed on 18 Nov 2026 (see "Chart names"). On 18 Nov 2026 View 3 (licence terms matrix) was added, View 2 was changed to start at 2024 and each view got its own bordered block with a "Show view" switch, as in Story 1a.

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

**Questions answered:** View 1, how much capability can the bank run on its own servers, by licence class? View 2, are the open-weight models released each year becoming easier to self-host? View 3, which licence term holds the condition?

## Chart used

| Proposal chart | App view | Chart type | What it shows |
|---|---|---|---|
| V7 | View 1 | Dot strip | Each model as a dot by licence class, with the best model of each class labelled and the best model of any kind marked |
| new (Anh) | View 2 | Horizontal 100% stacked bar | Licence mix of the open-weight models released each year (2024 to 2026): unrestricted, restricted use, non-commercial, with the number of models in every segment |
| new (Ian, 18 Nov 2026) | View 3 | Matrix heatmap with the condition written in every cell | One row per model that Epoch labels restricted use, non-commercial or unknown (released 2024 to 2026), one column per licence term, with the evidence of each cell on hover and on click |

**Visual Vocabulary family:** View 1, distribution (as recorded in MEMORY.md section 8p). View 2, part-to-whole. View 3, correlation (used as a model-by-term grid).

**Chart names:** Until 17 Nov 2026 the charts were called View 1, 2, 3, 3b, 4, 4B, V3, 5a and 5b. On 18 Nov 2026 the charts of each story were numbered from 1 in page order. Story 1a has View 1 and View 2 (unchanged). Story 1b has View 1 (earlier View 3), View 2 (earlier View 3b) and View 3 (new on 18 Nov 2026, the licence terms matrix). Story 2 has View 1 (earlier View 4), View 2 (earlier View 4B) and View 3 (earlier V3, the proposal chart). Story 3 has View 1 (earlier View 5a) and View 2 (earlier View 5b). A chart of another story is named with its story, for example Story 2 View 1. File names (`view4b.py`, `v3_difference.py`, `DATA_DICTIONARY_4B.md`, `DATA_DICTIONARY_V3.md`, `PROVENANCE_V3_DRAFT.md`) and the proposal chart ids (V1 to V7) are unchanged. MEMORY.md sections up to 8al and the earlier decision logs use the old names.

## View 2: licence mix by release year (added by Anh, 13 Nov 2026)

**Rationale (why it was added):**

1. **A gap in story 1b.** View 1 is a snapshot: how much capability each licence class holds today. The architect is also deciding whether the bank should build a self-hosting route at all (servers, a licence-review step), which only pays off if self-hostable models keep coming. That needs the trend in the licences of new releases, which View 1 cannot show.
2. **It ties story 1b to the rise of AI.** The brief asks about the rise of AI; View 2 is a change over time in what the bank is allowed to do with new models.
3. **It widens the chart families.** It adds *part-to-whole* to the app (check 14), next to correlation and ranking (1a), distribution (View 1), change over time (story 2) and the incident charts (story 3).
4. **No new data and no shared code.** It counts rows of the same `data/model_capability.csv` as View 1 and uses View 1's country filter, so every number traces to the data package (check 7).

**Finding (all developer countries, 2024 to 2026):** the share of open-weight releases that Epoch labels unrestricted rose from 40% in 2024 (14 of 35) to 76% in 2025 (25 of 33) and 79% in 2026 (22 of 28, releases to 7 Oct), a rise of 39 points. Restricted-use licences fell from 18 of 35 to 4 of 28. For China-based developers alone: 7 of 9 in 2024 to 18 of 22 in 2026. The chart holds 96 open-weight models.

**2023 left out (Ian, 18 Nov 2026):** the first version showed 2023 as well (31 open-weight models, 11 unrestricted). Ian asked for the 2023 bar to be dropped, so the chart starts at 2024. The constant `FIRST_YEAR = 2024` in `licence_mix.py` sets the first year. The filter applies to the chart, the three metrics, the values table and the CSV download.

**Controls:** the chart uses View 1's "Developer based in" control. It ignores the release window on purpose and always shows every year from 2024, because the default window (2025 to 2026) would cut the trend to two bars. An empty country selection, or countries with no open-weight models, shows a message instead of the chart.

**Layout and colours (Ian's view pattern, updated 17 Nov 2026 after Ian's style note):** subheading as a question, unit caption, three metrics (unrestricted share in the first and last year, number of models), "Selected" line with the zoom note, HTML legend above the chart, fixed-width Plotly chart (1200 px, Arial, Ian's `_layout`) with no title inside it, answer text, visible values table, then how to read, design decision, limits, filtered records with the CSV download and the shared sources footer. Open weights keep View 1's blue (#0072B2); the three licence classes are three steps of that blue (#0072B2, #56B4E9, #D6E9F6), darkest for the most permissive. Checked in a browser at 1366x768 on 15 Nov 2026: every segment label readable, no horizontal scrolling.

**50% line and percentages in the segments removed (Ian, 18 Nov 2026):** the dashed 50% line, its label and its legend entry were deleted, and the segments now show the absolute number of models only. The axis stays a share of the year (0 to 100%) so that the bars stay comparable. The metrics, the answer sentence and the hover still give percentages.

**Code:** `licence_mix.py` in this folder (counts from `data/model_capability.csv`, no new data file), called from `page.py` in the same fragment as View 1, because View 2 reads View 1's country control. Nothing in the shared `src/` folder was changed for View 2. Anh's heading line was moved from `licence_mix.py` to `page.py` on 18 Nov 2026 (same words) so that the heading and the "Show view" switch share one row.

**Design decision:** visual task, how the licence mix of new open-weight models changed. Form chosen, a horizontal 100% stacked bar per year with the number of models written in each segment (no hovering needed), in three steps of View 1's open-weight blue because the classes are ordered. Rejected: the first draft, vertical bars in blue, orange and grey with the legend under the chart (its orange read as "closed", close to the colour of closed models in View 1 and Story 2 View 1, and the unrelated colours hid that the classes are ordered; shown small in the app's design-decision section), stacked counts (2026 is a part year, so totals differ), one pie per year (angles across pies are hard to compare), a line of the unrestricted share only (hides the trade between restricted-use and non-commercial licences).

## View 3: licence terms matrix (added by Ian with Claude, 18 Nov 2026)

**Question answered:** Which licence term holds the condition?

**Rationale:** Views 1 and 2 use Epoch's accessibility label, which is a class. A class cannot say which condition the architect must check first. View 3 opens the licences themselves. Each row is one model that Epoch labels restricted use, non-commercial or unknown (released 2024 to 2026, 51 models). Each column is one licence term: Epoch label (for comparison), commercial use, revenue or user threshold, hosting or Model-as-a-Service, attribution or notice, use policy, and output or derivative rule.

**Data:** `data/licence_terms.json` (51 records, written from the licence notes in `Hedging Region AI Model Selection and Data Risk\licence_check_2024_2026_2026-11-18.md`). The model list is the union of the Story 1a file (12 Nov 2026) and the Story 1b file (17 Oct 2026), so a model that only one file holds is still listed. Each cell holds a state, a short label and the evidence. States: no condition, condition applies, blocked or needs a separate licence, assumed or not read, not applicable. Evidence levels: read in full 42, read in part 5, assumed 3, not a licence case 1. The reading is AI work (Claude) on 18 Nov 2026. Ian is the reviewer and has not yet reviewed every cell. It is not legal advice.

**Interaction:** hover a cell for a short preview with the evidence. Click a cell to pin its evidence in a card above the matrix. The card stays while the page scrolls, holds the evidence level, the source link and a collapsed Full note for the model, and closes with the Close button. Filters: Epoch label, release year and evidence level (multi-select pills) and developer (multi-select box). Every option starts selected, and pressing an option hides it so that the matrix gets shorter. If a filter has no option selected, a message asks for at least one. Below the matrix come three sections (how to read, design decision, what this matrix cannot show) and "Filtered records" with a CSV download.

**Speed:** the view runs in its own Streamlit fragment, so a click re-runs only this view. The selection is read from session state before the chart is drawn, so one click causes one re-run (about 0.2 to 0.5 s in the cloud test, not yet timed on Ian's computer).

**Code:** `licence_terms.py` in this folder, called from `page.py`. It draws a Plotly heatmap for the cells and an invisible scatter layer on top, because Streamlit receives no selection from a heatmap click. It uses `st.plotly_chart(on_select="rerun")`.

**Design decision:** visual task, show which licence term holds the condition so that the legal team knows what to read first. Form chosen, a matrix with the condition written inside every cell. Rejected: replacing View 2 (it shows a trend over years, the matrix shows terms per model), a stacked bar of terms (hides which model carries which condition), a table of paragraphs (readers cannot scan which models share a condition) and colour alone (fails for colour vision deficiency, so each cell also carries its words).

**Open:** the order of the rows (release date or A to Z) is not decided, and the help text still says "grouped by developer and ordered by release date", which is not what the matrix does. Ian has not yet chosen.

## Data sources and dates

| Source | Used for | Date |
|---|---|---|
| Epoch Capabilities Index, file `eci_scores.csv` | Capability, release date, developer, country, Epoch accessibility label | Retrieved 17 Oct 2026 22:27 UTC, models released 24 Feb 2023 to 7 Oct 2026 (277 models) |
| The group's licence readings, written in the eci_scores notebook | Five licences read against the licence pages (Views 1 and 2 hover) | Read 18 Oct 2026 |
| Licence check of 51 models, `licence_check_2024_2026_2026-11-18.md` and `licence_summary_2024_2026.csv` in the Hedging Region folder, copied into `data/licence_terms.json` | Cells of View 3 | Read 18 Nov 2026 (AI reading, Ian reviewer) |
| Epoch file of the Story 1a stream, `eci_scores.csv` | Used only to list the models of View 3 (union with the 17 Oct file) | Retrieved 12 Nov 2026 19:04 UTC, models to 9 Nov 2026 |

**Data flow:** `notebooks/eci_scores/` downloads or reuses the raw file in `raw/`, writes `model_capability.csv` to `processed/`, and the file is copied by hand into `data/`. The page reads only `data/model_capability.csv`. The notebook is a copy of notebook 01 with the folder name, the manual folder and the output step changed.

**Licence check at every refresh:** Every time the data is downloaded again, for each new open-weight model and each model that Epoch labels restricted use, non-commercial or unknown, open the LICENSE file on Hugging Face or GitHub and read it. Epoch's label and news pages do not replace it. Record the licence name, whether commercial use is allowed, the condition (revenue line, user line or Model-as-a-Service clause), whether internal use is exempt, whether Epoch's label agrees with the text, the link and the date read. Add the reading to `licence_check.csv`.

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
- **Coverage of readings:** In Views 1 and 2 only five licences were read and every other open-weight model keeps Epoch's label. View 3 covers the 51 models that Epoch labels restricted use, non-commercial or unknown, released 2024 to 2026. Models that Epoch labels unrestricted were not read in View 3.
- **View 3, evidence levels differ:** 42 models were read in full, 5 in part, 3 assumed and 1 is not a licence case. Hosted entries (the Qwen hosted models) assume the open-weight licence. Acceptable use policies were read only for Gemma, Llama 3.2, Falcon 2 and Command R+. One reader (Claude) did the reading and no second member has checked it.
- **View 3, two Epoch files:** the model list joins the 12 Nov 2026 and the 17 Oct 2026 downloads. 30 models are in the 17 Oct file only and 9 in the 12 Nov file only (see `epoch_snapshot_difference_story1a_vs_1b_2026-11-18.md`).
- **View 2, part year:** 2026 covers releases to 7 Oct 2026 only, so its total is lower and its share may still move. Counts cover only models Epoch has scored.
- **Review notes of 18 Nov 2026 (open, not yet decided by the group):** The counts in View 2 were recomputed from `data/model_capability.csv` and agree with the totals in this file. Six points came out of the review. On 18 Nov 2026 Ian dropped 2023 from View 2, so the rounding error and the 2023 figures below no longer show in the chart. They stay here as the record of the review.
  - **Rounding:** 11 of 31 is 35.48%, which is 35%. The chart label, the metric and this file show 36% because the share is rounded to 35.5 first and then to a whole number. The shares for 2025 (76%) and 2026 (79%) are correct.
  - **Kimi K3:** The chart counts it as non-commercial, as Epoch labels it, while the group's reading of the licence allows commercial use with a revenue condition. It is also the best open-weight model of 2026.
  - **Wording:** The legend and hover say "Commercial self-hosting allowed" for Epoch's unrestricted label, while the group read only five licences.
  - **Composition:** The rise of the unrestricted share follows who releases open-weight models. China-based developers made 11 of 31 open-weight releases in 2023 and 22 of 28 in 2026, and their unrestricted releases rose from 0 to 18. The default view with all countries does not show this.
  - **Share is not capability:** The bar counts models, including 2023 models that an approved list would not use. For the top quarter of the capability index the unrestricted share is 22 of 27 in 2026 (threshold 141.4), so the conclusion holds there, but the chart does not show it.
  - **Fit to the story:** Story 1b asks which open-weight models the bank may run on its own servers. View 2 shows a trend in a share and does not name models. The group has not decided whether View 2 stays.
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
| Visible text of the View 1 page against the A3P1 tab 2, from the "User story" line down | No difference |
| Notebook run in a cloud copy, output compared with the original `model_capability.csv` | Same content (277 rows, 16 columns). Only the line endings differ between Windows and the cloud |
| Whole build from zero in a fresh virtual environment (`pip install -r requirements.txt -r requirements-notebook.txt`, Python 3.13): notebook run, `processed/model_capability.csv` copied by hand into `data/` | Same content as the earlier files (277 rows, 16 columns). Run on 9 Nov 2026 |
| Page run inside `app.py` and on its own (`streamlit run stories/<story>/page.py`), text from "User story" down compared with the A3P1 tab | No difference in both cases. Screenshot of the in-app page checked by eye |
| View 2 counts against the data file by hand (Anh, to do before commit): in `data/model_capability.csv`, open-weight rows released in 2024 = 35, of which `epoch_accessibility` = "Open weights (unrestricted)" = 14; in 2026 = 28, of which 22 | Must match the chart labels 14 (40%) and 22 (79%). Until 18 Nov 2026 the row used 2023 (31 and 11, label 11 (36%), a double rounding of 35.48%) |
| View 2 without the 50% line (cloud browser, 18 Nov 2026) | No dashed line, label or legend entry. Segments read 14, 18, 3 (2024), 25, 8 (2025), 22, 4, 2 (2026). No exception |
| View 2 in the app (`streamlit.testing`, 13 and 15 Nov 2026): default page, China only, "Not stated" only (no open-weight models), empty selection; whole app with all four pages | No errors; the empty and no-open-weight states show their messages |
| View 2 in a browser at 1366x768 (15 Nov 2026) | Every segment label readable without hovering, no horizontal scrolling, values table visible |
| View 2 colour check (17 Nov 2026): the chart screenshot run through protanopia, deuteranopia and tritanopia simulations (Machado et al. 2009) | The three shades stay distinct in all three (lightness about 46, 70 and 91 in normal vision; 44 to 49, 68 to 73 and 91 to 92 when simulated), and every segment also carries its count and share as text |
| View 2 filter response (`streamlit.testing`, 17 Nov 2026) | Changing "Developer based in" re-runs the view in 0.1 to 0.2 s |
| View 2 counts recomputed by Claude from `data/model_capability.csv` (18 Nov 2026): open-weight models per release year as non-commercial, restricted use and unrestricted | 2023: 6, 14, 11 (31). 2024: 3, 18, 14 (35). 2025: 0, 8, 25 (33). 2026: 2, 4, 22 (28). Unrestricted shares 35.48%, 40.0%, 75.76% and 78.57%. The totals 31, 28, 22 and 11 agree with this file. The 36% for 2023 is a double rounding, so the check row above that requires the label "11 (36%)" repeats the error |
| View 2 without 2023 (cloud, 18 Nov 2026): counts recomputed from `data/model_capability.csv` with the app's own loader | 2024: 3, 18, 14 (35). 2025: 0, 8, 25 (33). 2026: 2, 4, 22 (28). 96 models. Shares 40%, 76%, 79%, rise 39 points. China only: unrestricted 7 of 9, 18 of 21 and 18 of 22. Screenshot: three bars, metrics and text agree |
| View 1 hover (cloud browser, 18 Nov 2026): hover on the best model of a class | Every line starts at the left edge of the box. Only View 1 was changed (`src/views_context.py`, one line) |
| View 3 in the app (`streamlit.testing` and a browser, 18 Nov 2026): 30 random operations (click, Close, filters, Full note), six switches of the three "Show view" toggles, the Developers filter down to 11 rows | No exception. Three headings 1, 2 and 3 and three bordered blocks found. Not run in Ian's own `.venv`, not timed on Ian's computer |

These checks were run by Claude. Ian has not reviewed them yet.
