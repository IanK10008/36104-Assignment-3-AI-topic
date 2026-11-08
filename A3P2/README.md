# A3P2: Model Choice Explorer, split by user story

A3P2 is the rebuild of the A3P1 app in one folder per user story. Each story has its own page, its own data folder, its own notebook and its own `docs.md`. Stories 1b, 2 and 3 are built. Story 1a comes later.

The app uses only the Epoch Capabilities Index file and, for Story 3, the AI Incident Database export. The LiteLLM and LMArena files are not used here.

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
  src/                        shared code, copied unchanged from A3P1 (+ shell.py, epoch_models.py)
  stories/
    1b_licence_route/         View 3: which open-weight models the bank may run itself
      page.py
      docs.md                 persona, task, sources, dates, limitations, licences
      data/                   the file the page reads (model_capability.csv)
      notebooks/eci_scores/   eci_scores.ipynb, raw/, processed/
    2_gap_to_us_models/       View 4: gap to the restricted US models
      (same layout)
    3_reported_incidents/     View 5: developers in reported AI incidents
      data/                   model_capability.csv (Epoch), incidents.csv, incident_developers.csv (AIID), kept apart
      notebooks/eci_scores/       Epoch notebook
      notebooks/aiid_incidents/   AI Incident Database notebook
```

## How data moves (the manual step)

1. Open the story's notebook (`stories/<story>/notebooks/eci_scores/eci_scores.ipynb`, and for Story 3 also `notebooks/aiid_incidents/aiid_incidents.ipynb`) and run all cells.
2. The notebook keeps the file it received in `raw/` and writes `model_capability.csv` and `data_currency.csv` to `processed/`.
3. **Copy the file the last cell names from `processed/` into the story's `data/` folder by hand.** The notebooks never write to `data/`. The eci_scores notebook gives `model_capability.csv`. The aiid_incidents notebook gives `incidents.csv` and `incident_developers.csv`. The page reads only the files in its own `data/`.

Story 3 has three files from two notebooks. They are not combined in a notebook. The page joins them when it loads (`src/aiid.py`, `src/context.py`).

Why by hand: a person checks the new file before the page uses it. The page never changes because a notebook ran by accident.

`REFRESH = False` in the notebook's set-up cell reuses the file already in `raw/` (Epoch retrieved 17 Oct 2026, AIID export of 12 Oct 2026), so the page matches A3P1. Set it to `True` to try a fresh download. The numbers on the page will then change and no longer match A3P1.

To run the notebooks: `pip install -r requirements-notebook.txt`, then open the notebook with Jupyter or VS Code, or from the command line:

```
jupyter nbconvert --to notebook --execute --inplace stories/1b_licence_route/notebooks/eci_scores/eci_scores.ipynb
```

## Status

| Story | Question | Page | Docs | Checked against A3P1 |
|---|---|---|---|---|
| 1a | Ranked shortlist (Views 1 and 2) | not started | not started | not applicable |
| 1b | How much capability can the bank run on its own servers, by licence class? (View 3) | built | draft | page text identical, data identical |
| 2 | How far do accessible models trail the restricted US models? (View 4) | built | draft | page text identical, data identical |
| 3 | Which developers appear in reported AI incidents, and how often? (View 5) | built, shows 2020 to 2026 | draft, lists open data issues | with A3P1 year settings: page text identical, tables identical. With 2020 start: differs only in the years shown |

Set aside for now: tests, shared data across stories, and the LiteLLM and LMArena files (needed by Story 1a only).

## Known differences from A3P1

- Top navigation instead of tabs. Each story is its own page.
- Story 3 starts in 2020 (A3P1: slider 2015, top chart 2012). `render_view5` in `src/views_context.py` has two new optional arguments for this. Their defaults are the A3P1 values.
- The page text is the A3P1 tab text without the sentence about four tabs.
- `src/` is a shared copy of the A3P1 code. Two changes: the optional years for `render_view5`, and the new `aiid.py`, `shell.py` and `epoch_models.py`. If one story needs a change, agree it with the group first because both pages use the same files.
- Owners in the `docs.md` files: Story 1b Anh, Story 2 Rida, Story 3 Yash.
- Story 1b is a proposed split of user story 1. The group has not agreed to it yet.
