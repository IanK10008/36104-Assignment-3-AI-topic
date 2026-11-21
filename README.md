# 36104 DVN 2026 A3P2: Model Choice Explorer, split by user story

## Group Detail

**Group number**: 6

**Member**: Anh Quyen Hoang, Rida Mehboob, Yin Kao and Yash Vikas Patil

## Question, persona and user stories

**Question:** In regions where leading closed US models are restricted, which accessible AI model gives an organisation the most measured capability for its cost and self-hosting feasibility?

The question is arguable: the same data could support a different answer. A reader who weights capability alone would pick a closed model through an outside API. A reader who weights licence freedom would pick an unrestricted open-weight model that scores lower. A reader who weights developer transparency could rule out the strongest models.

**Persona:** group enterprise architect at an Asia-Pacific bank or insurer with operations in Hong Kong and other markets. **Decision:** which accessible models go on an interim approved list for staff and internal tools, by route (API or self-hosted), with capability set against price.

**User stories:**

1. As a group enterprise architect, I want to pick a route (API or self-hosted) and shortlist the accessible models whose licence fits it, ranked with capability set against price, so that I can build an interim approved list the risk committee will accept. (Story 1a, ranked shortlist. Story 1b, what the licence allows.)
2. As a group enterprise architect, I want to measure how far the best accessible model trails the best model overall and check whether independent benchmarks agree with developer claims, so that I can judge whether waiting for US access is worth it. (Story 2.)
3. As a group enterprise architect, I want to see how openly each developer builds its models and how often it appears in reported incidents, so that I can tell the committee what is known and unknown about the developers we would rely on. (Story 3.)

A3P2 is the app, built in one folder per user story. Each story has its own page, its own data folder, its own notebook and its own `docs.md`. Stories 1a, 1b, 2 and 3 are built.

The app uses the Epoch Capabilities Index file in every story. Story 1a also uses the LiteLLM price file and the LMArena leaderboard file, Story 3 uses the AI Incident Database export, and Story 2 View 2 uses the Epoch Benchmarking Hub ZIP.

## Quick start

```
python -m venv .venv
.venv\Scripts\activate          (Windows)   or   source .venv/bin/activate   (Mac, Linux)
pip install -r requirements.txt
streamlit run app.py
```

The packages are pinned: numpy 2.4.6, pandas 3.0.5, plotly 7.1.0, streamlit 1.63.0. The app was run on Python 3.13.

## Run the app again (environment already installed)

Use this when the `.venv` folder already exists and the packages are installed. Nothing needs to be installed again.

**Step 1, open a terminal in the repository folder:** In Windows, open PowerShell or Command Prompt and change to the folder that holds `app.py`.

```
cd path\to\repository-folder
```

**Step 2, activate the environment:** Use the line that matches the terminal. Copy only the command and not the text beside it.

Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```
.venv\Scripts\activate.bat
```

Mac, Linux:

```
source .venv/bin/activate
```

The prompt then starts with `(.venv)`.

**If PowerShell says that running scripts is disabled:** Run the next line once in the same window and then activate again. It only changes that one window and nothing on the computer.

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Another way is to skip the activation and use the one-line route under Step 4.

**Step 3, start the app:**

```
streamlit run app.py
```

The browser opens at `http://localhost:8501`. If it does not open, copy that address into the browser.

**Step 4, start without activating (any terminal):** The same result comes from one line that calls the environment's Python directly.

```
.venv\Scripts\python.exe -m streamlit run app.py
```

**Step 5, stop the app:** Press `Ctrl + C` in the terminal. Close the browser tab afterwards.

**After any code change:** Stop the app with `Ctrl + C`, then run `streamlit run app.py` again. The Streamlit cache can keep old data or old code when only the browser page is refreshed.

**Port already in use:** Start the app on another port with `streamlit run app.py --server.port 8502`.

To run one story alone, from this folder:

```
streamlit run stories/1a_ranked_shortlist/page.py
streamlit run stories/1b_licence_route/page.py
streamlit run stories/2_gap_to_us_models/page.py
streamlit run stories/3_reported_incidents/page.py
```

## Folder map

This map lists every file and folder pushed to GitHub. Nothing else is in the repository. `.venv/`, `__pycache__/` and `*.pyc` are never pushed.

```
(repository root)
  README.md
  AI_PROVENANCE_MATRIX.csv    AI provenance matrix: each AI use, the member who reviewed it and the check
  DATA_AND_AI_DISCLOSURE.md   data sources, licences and AI tools used
  DATA_DICTIONARY.md          every dataset: source, URL, licence, columns, units, primary key, time coverage, latest observation, transform
  requirements.txt            packages for the app
  requirements-notebook.txt   extra packages for the notebooks
  .gitignore                  files that git does not track (virtual environments, caches)
  app.py                      multipage app (top navigation, one page per story)
  .streamlit/config.toml
  src/                        shared code used by the pages (shell.py, epoch_models.py, aiid.py, controls_1a.py, views_story3.py and others)
  stories/
    1a_ranked_shortlist/      Views 1 and 2: capability for the price, ranked shortlist
      page.py                 also builds the models table from the three files below
      docs.md
      data/                   model_capability.csv (Epoch), model_price.csv (LiteLLM), lmarena_ratings.csv (LMArena), kept apart
      notebooks/eci_scores/       Epoch notebook, raw/, processed/
      notebooks/litellm_prices/   LiteLLM notebook, raw/, processed/
      notebooks/lmarena_leaderboard/   LMArena notebook, raw/, processed/
    1b_licence_route/         Story 1b Views 1 to 3: which open-weight models the bank may run itself, how that mix changes by year, and which licence term holds the condition
      page.py
      licence_mix.py          View 2, called from page.py
      licence_terms.py        View 3, called from page.py
      docs.md                 persona, task, sources, dates, limitations, licences
      data/                   the files the page reads (model_capability.csv, and licence_terms.json for View 3)
      notebooks/eci_scores/   eci_scores.ipynb, raw/, processed/
    2_gap_to_us_models/       Story 2 Views 1 to 3: gap to the restricted US models, who produced the benchmark scores, and whether independent and published GPQA scores agree
      page.py
      docs.md
      view4b.py               Story 2 View 2, called from page.py
      v3_difference.py        Story 2 View 3 (the difference chart of the proposal chart V3), called from page.py
      data/                   model_capability.csv, hub_scores_by_model.csv, hub_model_coverage.csv, hub_data_currency.csv (Epoch Benchmarking Hub), gpqa_reported_vs_epoch.csv
      notebooks/eci_scores/   eci_scores.ipynb, raw/, processed/, build_v3_data.py
      notebooks/benchmark_hub/   benchmark_hub.ipynb (downloads or reuses the Hub ZIP), manual/, raw/, processed/
      DATA_DICTIONARY_4B.md   data dictionary of the Story 2 View 2 files
      DATA_DICTIONARY_V3.md   data dictionary of the GPQA file of Story 2 View 3
      v3_benchmark.py         first GPQA chart, not used by the page (kept for credit)
    3_reported_incidents/     Story 3 Views 1 and 2: how openly each developer builds its models, and how often it appears in reported incidents
      page.py
      docs.md
      data/                   model_capability.csv (Epoch), incidents.csv, incident_developers.csv (AIID), aiid_model_incidents_by_developer.csv, fmti_dec2025_scores_tidy.csv, fmti_companies.csv
      notebooks/eci_scores/       Epoch notebook, raw/, processed/
      notebooks/aiid_incidents/   AI Incident Database notebook, raw/, processed/
      notebooks/aiid_model_incidents/   notebook, manual/ (the incident labels), raw/, processed/
      notebooks/fmti_scores/      Foundation Model Transparency Index notebook, manual/, raw/, processed/
```

## How data moves (the manual step)

1. Open the story's notebook (`stories/<story>/notebooks/eci_scores/eci_scores.ipynb`; Story 1a also has `litellm_prices` and `lmarena_leaderboard`, Story 2 also has `benchmark_hub`, Story 3 also has `aiid_incidents`, `aiid_model_incidents` and `fmti_scores`) and run all cells. All notebooks have the same structure.
2. The notebook keeps the file it received in `raw/` and writes `model_capability.csv` and `data_currency.csv` to `processed/`.
3. **Copy the file the last cell names from `processed/` into the story's `data/` folder by hand.** The notebooks never write to `data/`. The eci_scores notebook gives `model_capability.csv`. The litellm_prices notebook gives `model_price.csv`, the lmarena_leaderboard notebook gives `lmarena_ratings.csv`, the aiid_incidents notebook gives `incidents.csv` and `incident_developers.csv`, the aiid_model_incidents notebook gives `aiid_model_incidents_by_developer.csv`, the fmti_scores notebook gives `fmti_dec2025_scores_tidy.csv` and `fmti_companies.csv`, and the benchmark_hub notebook of Story 2 View 2 gives `hub_scores_by_model.csv`, `hub_model_coverage.csv` and `hub_data_currency.csv`. The page reads only the files in its own `data/`. Run the eci_scores notebook of Story 2 before benchmark_hub, because benchmark_hub matches the Hub names against its output.

Story 1a has three files from three notebooks and Story 3 has three files from two notebooks. They are not combined in a notebook. The page combines them when it loads: Story 1a in `load()` in `page.py` with the rules in `src/data.py` (cut the slim columns, match by model name, validate), and Story 3 in `src/aiid.py` and `src/context.py`.

Why by hand: a person checks the new file before the page uses it. The page never changes because a notebook ran by accident.

Every notebook ships with `REFRESH = True` in its set-up cell. The notebook first tries a fresh download and falls back to the file already in `raw/` (or in `manual/`) if the download fails. `REFRESH = False` reuses the file already in `raw/` and gives the same tables as the files now in `data/`. The files in `raw/` were retrieved on 20 Nov 2026 (UTC), from `raw/retrieval_log.json`: the Epoch capability file in all four stories, LiteLLM, LMArena (leaderboard published 19 Nov 2026), the AIID export file of 16 Nov 2026, the FMTI repository and the Epoch Benchmarking Hub ZIP. The notebooks read the newest file in `raw/`. After a fresh download the numbers on the page can change.

To run the notebooks: `pip install -r requirements-notebook.txt`, then open the notebook with Jupyter or VS Code, or from the command line:

```
jupyter nbconvert --to notebook --execute --inplace stories/1b_licence_route/notebooks/eci_scores/eci_scores.ipynb
```

## Chart names

The charts of each story are numbered from 1 in page order. A chart of another story is named with its story, for example Story 2 View 1.

| Story | View | Chart                                                                             |
| ----- | ---- | --------------------------------------------------------------------------------- |
| 1a    | 1    | Cost against capability (scatter plot with price frontier)                        |
| 1a    | 2    | Ranked options (weighted stacked bars)                                            |
| 1b    | 1    | Capability by licence class (dot strip)                                           |
| 1b    | 2    | Licence mix of open-weight releases by year, 2024 to 2026 (100% stacked bars)     |
| 1b    | 3    | Which licence term holds the condition (matrix of models by licence term)         |
| 2     | 1    | Capability gap between restricted and accessible models (step lines)              |
| 2     | 2    | Who produced the benchmark scores behind the capability index (100% stacked bars) |
| 2     | 3    | Developer-reported against independent GPQA scores (difference chart)             |
| 3     | 1    | How openly each developer builds its models (FMTI heatmap)                        |
| 3     | 2    | Reported model incidents by developer (event timeline)                            |

## Status

| Story | Question                                                                                                             | Page                      | Docs    |
| ----- | -------------------------------------------------------------------------------------------------------------------- | ------------------------- | ------- |
| 1a    | Ranked shortlist (Views 1 and 2)                                                                                     | built                     | written |
| 1b    | How much capability can the bank run on its own servers, by licence class? (Views 1 to 3)                            | built                     | written |
| 2     | How far do accessible models trail the restricted US models? (Views 1 to 3)                                          | built                     | written |
| 3     | How openly does each developer build its models, and how often does it appear in reported incidents? (Views 1 and 2) | built, shows 2020 to 2026 | written |

Set aside for now: tests and shared data across stories (each story has its own copy of the files it reads).

## Notes

- Line endings: the CSV files in the `data/` folders have CRLF line endings, except the three `hub_*` files of Story 2 and `licence_terms.json`, which have LF. The content is the same whichever ending a file has.
- `src/` is shared by the pages. If one story needs a change in it, agree the change with the group first.
- Who built what is in the "Built by" line of each `docs.md`: Story 1a Yin. Story 1b Yin (View 1, View 3, later changes to View 2) and Anh (first version of View 2). Story 2 Rida (initial submission, including the first GPQA chart) and Yin (View 2, the current View 3, and a basic version of View 1 that was made first because Rida had also worked on it, so the split of View 1 is not certain). Story 3 Yin, with Anh checking the incident labels.
- Stories 1a and 1b are the two halves of user story 1.
