 ee

# A3P2: Model Choice Explorer, split by user story

A3P2 is the rebuild of the A3P1 app in one folder per user story. Each story has its own page, its own data folder, its own notebook and its own `docs.md`. Stories 1a, 1b, 2 and 3 are built.

The app uses the Epoch Capabilities Index file in every story. Story 1a also uses the LiteLLM price file and the LMArena leaderboard file, Story 3 uses the AI Incident Database export, and Story 2 View 2 uses the Epoch Benchmarking Hub ZIP.

## Quick start

```
python -m venv .venv
.venv\Scripts\activate          (Windows)   or   source .venv/bin/activate   (Mac, Linux)
pip install -r requirements.txt
streamlit run app.py
```

The packages are pinned: numpy 2.4.6, pandas 3.0.5, plotly 7.1.0, streamlit 1.63.0. The A3P1 app was tested with Python 3.11.9. A3P2 was also run on Python 3.13.

To run one story alone, from this folder:

```
streamlit run stories/1a_ranked_shortlist/page.py
streamlit run stories/1b_licence_route/page.py
streamlit run stories/2_gap_to_us_models/page.py
streamlit run stories/3_reported_incidents/page.py
```

## Folder map

```
A3P2/
  README.md
  requirements.txt            packages for the app
  requirements-notebook.txt   extra packages for the notebooks
  app.py                      multipage app (top navigation, one page per story)
  .streamlit/config.toml
  src/                        shared code, copied unchanged from A3P1 (+ shell.py, epoch_models.py, aiid.py, controls_1a.py, views_story3.py)
  stories/
    1a_ranked_shortlist/      Views 1 and 2: capability for the price, ranked shortlist
      page.py                 also builds the models table from the three files below
      docs.md
      data/                   model_capability.csv (Epoch), model_price.csv (LiteLLM), lmarena_ratings.csv (LMArena), kept apart
      notebooks/eci_scores/       Epoch notebook
      notebooks/litellm_prices/   LiteLLM notebook
      notebooks/lmarena_leaderboard/   LMArena notebook
    1b_licence_route/         Story 1b Views 1 and 2: which open-weight models the bank may run itself, and how that mix changes by year
      page.py
      docs.md                 persona, task, sources, dates, limitations, licences
      data/                   the file the page reads (model_capability.csv)
      notebooks/eci_scores/   eci_scores.ipynb, raw/, processed/
    2_gap_to_us_models/       Story 2 Views 1 to 3: gap to the restricted US models, who produced the benchmark scores, and whether independent and published GPQA scores agree
      (same layout, plus the files below)
      view4b.py               Story 2 View 2, called from page.py
      v3_difference.py        Story 2 View 3 (the difference chart of the proposal chart V3), called from page.py
      data/                   also hub_scores_by_model.csv, hub_model_coverage.csv, hub_data_currency.csv (Epoch Benchmarking Hub)
      notebooks/benchmark_hub/   benchmark_hub.ipynb (downloads or reuses the Hub ZIP), manual/, raw/, processed/
      DATA_DICTIONARY_4B.md   columns, source, transform and limitations of the Story 2 View 2 files
    3_reported_incidents/     Story 3 Views 1 and 2: how openly each developer builds its models, and how often it appears in reported incidents
      data/                   model_capability.csv (Epoch), incidents.csv, incident_developers.csv (AIID), kept apart
      notebooks/eci_scores/       Epoch notebook
      notebooks/aiid_incidents/   AI Incident Database notebook
```

## How data moves (the manual step)

1. Open the story's notebook (`stories/<story>/notebooks/eci_scores/eci_scores.ipynb`; Story 1a also has `litellm_prices` and `lmarena_leaderboard`, Story 3 also has `aiid_incidents`) and run all cells.
2. The notebook keeps the file it received in `raw/` and writes `model_capability.csv` and `data_currency.csv` to `processed/`.
3. **Copy the file the last cell names from `processed/` into the story's `data/` folder by hand.** The notebooks never write to `data/`. The eci_scores notebook gives `model_capability.csv`. The litellm_prices notebook gives `model_price.csv`, the lmarena_leaderboard notebook gives `lmarena_ratings.csv`, and the aiid_incidents notebook gives `incidents.csv` and `incident_developers.csv`. The page reads only the files in its own `data/`. Exception: the `benchmark_hub` notebook of Story 2 View 2 copies its three page files into `data/` itself when `COPY_TO_APP = True`, and its first run needs `REFRESH = True` on a computer that can reach epoch.ai to record the download time.

Story 1a has three files from three notebooks and Story 3 has three files from two notebooks. They are not combined in a notebook. The page combines them when it loads: Story 1a in `load()` in `page.py` with the A3P1 rules in `src/data.py` (cut the slim columns, match by model name, validate), and Story 3 in `src/aiid.py` and `src/context.py`.

Why by hand: a person checks the new file before the page uses it. The page never changes because a notebook ran by accident.

`REFRESH = False` in the notebook's set-up cell reuses the file already in `raw/` (Epoch and LiteLLM retrieved 17 Oct 2026, LMArena published 15 Oct 2026, AIID export of 12 Oct 2026), so the page matches A3P1. Set it to `True` to try a fresh download. The numbers on the page will then change and no longer match A3P1.

To run the notebooks: `pip install -r requirements-notebook.txt`, then open the notebook with Jupyter or VS Code, or from the command line:

```
jupyter nbconvert --to notebook --execute --inplace stories/1b_licence_route/notebooks/eci_scores/eci_scores.ipynb
```

## Chart names

The charts of each story are numbered from 1 in page order (changed on 18 Nov 2026). A chart of another story is named with its story, for example Story 2 View 1.

| Story | View | Chart | Earlier name |
|---|---|---|---|
| 1a | 1 | Cost against capability (scatter plot with price frontier) | View 1 |
| 1a | 2 | Ranked options (weighted stacked bars) | View 2 |
| 1b | 1 | Capability by licence class (dot strip) | View 3 |
| 1b | 2 | Licence mix of open-weight releases by year (100% stacked bars) | View 3b |
| 2 | 1 | Capability gap between restricted and accessible models (step lines) | View 4 |
| 2 | 2 | Who produced the benchmark scores behind the capability index (100% stacked bars) | View 4B |
| 2 | 3 | Developer-reported against independent GPQA scores (difference chart) | V3 |
| 3 | 1 | How openly each developer builds its models (FMTI heatmap) | View 5a |
| 3 | 2 | Reported model incidents by developer (event timeline) | View 5b |

## Status

| Story | Question                                                                            | Page                      | Docs                          | Checked against A3P1                                                                                             |
| ----- | ----------------------------------------------------------------------------------- | ------------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1a    | Ranked shortlist (Views 1 and 2)                                                    | built                     | draft                         | page text identical, models table identical to A3P1 `models.csv`                                               |
| 1b    | How much capability can the bank run on its own servers, by licence class? (Views 1 and 2) | built                     | draft                         | View 1: page text identical, data identical. View 2 is new and has no A3P1 version |
| 2     | How far do accessible models trail the restricted US models? (Views 1 to 3)                 | built                     | draft                         | View 1: page text identical, data identical. Views 2 and 3 are new and have no A3P1 version |
| 3     | How openly does each developer build its models, and how often does it appear in reported incidents? (Views 1 and 2) | built, shows 2020 to 2026 | draft, lists open items | Views 1 and 2 replace the A3P1 incident chart, so there is no A3P1 page to compare |

Set aside for now: tests and shared data across stories (each story has its own copy of the files it reads).

## Known differences from A3P1

- Top navigation instead of tabs. Each story is its own page.
- Story 3 no longer uses the A3P1 incident chart. Story 3 Views 1 and 2 are new and sit in `src/views_story3.py`. `render_view5` in `src/views_context.py`, with its two optional arguments, is not called by any page.
- Story 1a: Views 1 and 2 are the A3P1 code. The controls are `src/controls_1a.py`, which is the controls block of A3P1 `app.py` moved into a function with no change to its lines. The A3P1 app reads a ready-made `models.csv`. Here `page.py` builds the same table from the three files in `data/`, so the table is equal to `models.csv`.
- The data files copied by the notebooks have LF line endings. The group's `Data` folder has CRLF. The content is the same.
- The page text is the A3P1 tab text without the sentence about four tabs.
- `src/` is a shared copy of the A3P1 code. Changes: the optional years for `render_view5`, and the new `aiid.py`, `shell.py`, `epoch_models.py`, `controls_1a.py` and `views_story3.py`. If one story needs a change, agree it with the group first because both pages use the same files.
- Owners in the `docs.md` files: Story 1a Ian, Story 1b Anh, Story 2 Rida (Story 2 Views 2 and 3 were built later by Ian with Claude's help), Story 3 Ian with Claude's help (to be confirmed by the group, as in its `docs.md`).
- Stories 1a and 1b are a proposed split of user story 1. The group has not agreed to it yet.
