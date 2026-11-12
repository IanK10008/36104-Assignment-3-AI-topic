"""Story 1a: ranked shortlist, capability for the price (Views 1 and 2).

Reads only this folder's own data: data/model_capability.csv (Epoch), data/model_price.csv (LiteLLM) and
data/lmarena_ratings.csv (LMArena). The three files are kept apart. The workflow that assembles the models
table (cut the slim columns, match models by name, validate) runs in load() below, with the A3P1 rules in
src/data.py. The two views and their controls are the A3P1 code. Runs inside app.py or on its own:
    streamlit run stories/1a_ranked_shortlist/page.py
"""
from __future__ import annotations

import io
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))  # so that "src" is found when this file is run on its own

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from src import analysis as an  # noqa: E402
from src import controls_1a, data, shell, snapshot  # noqa: E402
from src.views import LICENCE_NOTES, render_view1, render_view2  # noqa: E402

shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load(folder: str):
    """Assemble the models table from the three source files in the story's data folder.

    1. Cut the slim columns from each file (Epoch: all models; LiteLLM: chat models with an output price;
       LMArena: the overall text board). The extracts go to a temporary folder that is deleted at once.
    2. Match the three sources by model name and build one row per Epoch model (data.build_models).
    3. Validate the table, then read it back the way the A3P1 app reads models.csv, which fixes the column
       types (dates, whole numbers). The result is the same table as models.csv in A3P1.
    Nothing is written to the story folder. Returns the models table and the overall LMArena rows, which the
    detail panel of View 2 uses to list every setting of a model.
    """
    with tempfile.TemporaryDirectory() as tmp:
        data.extract_sources(Path(folder), Path(tmp))
        sources = data.read_sources(Path(tmp))
        arena_all = pd.read_csv(Path(tmp) / data.SOURCE_FILES["lmarena"].name)
    built = data.build_models(sources)
    data.validate(built)
    return data.read_dataset(io.StringIO(built.to_csv(index=False))), arena_all


models, arena_all = load(str(HERE / "data"))
snapshot.load(HERE, models)  # dates and figures quoted in the page text come from the data, not from typed text
controls_block, all_three_recent, overview = controls_1a.build(models)

# Keep every widget setting when a view is closed and opened again (Streamlit drops state of unrendered widgets).
st.session_state.setdefault("show_view1", True)
st.session_state.setdefault("show_view2", True)

shell.story(1, "")
overview()  # the data behind the page, above both views
with st.container(key="cost_capability", border=True):
    head1, tog1 = st.columns([5, 1], vertical_alignment="center")
    head1.subheader("1. Which models give the most capability for the price?", anchor="view-1")
    open1 = tog1.toggle("Show view", key="show_view1")

    @st.fragment  # a click inside View 1 re-runs only View 1
    def view_one():
        w_label, r_label, points, three, pct, ranked = controls_block("")
        render_view1(models, points, ranked, pct if not three.empty else three, w_label)

    if open1:
        view_one()

with st.container(key="ranked_options", border=True):
    head2, tog2 = st.columns([5, 1], vertical_alignment="center")
    head2.subheader("2. Which models rank highest once capability, preference and price are weighed together?",
                    anchor="view-2")
    open2 = tog2.toggle("Show view", key="show_view2")

    @st.fragment  # a click inside View 2 re-runs only View 2, so the chart updates faster
    def view_two():
        summary_slot = st.container()
        advanced = st.expander("Advanced settings: release window, route, name matching, developers, weights")
        w_label2, r_label2, points2, three2, pct2, ranked2 = controls_block("v2_", advanced)
        render_view2(ranked2, pct2, r_label2, arena_all, list(an.CRITERIA), advanced, summary_slot, points=points2)

    if open2:
        view_two()

shell.limitations_1a([m for m in LICENCE_NOTES if m in set(models["model"])])
