"""Story 1b (second half of user story 1): what the licence allows, View 3.

Reads only this folder's own data (data/model_capability.csv). Runs inside app.py or on its own:
    streamlit run stories/1b_licence_route/page.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))  # so that "src" is found when this file is run on its own
sys.path.insert(0, str(HERE))  # so that this story's own licence_mix.py is found

import streamlit as st  # noqa: E402

from src import epoch_models, shell  # noqa: E402
from src.selection import keep_state  # noqa: E402
from src.views_context import render_view3  # noqa: E402
from licence_mix import render_licence_mix  # noqa: E402
from licence_terms import render_licence_terms  # noqa: E402


shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load(path: str):
    return epoch_models.load_epoch_models(path), epoch_models.load_licence_check(path)


models, licence_check = load(str(HERE / "data" / "model_capability.csv"))

# Keep every widget setting when a view is closed and opened again (Streamlit drops state of unrendered widgets).
st.session_state.setdefault("show_1b_view1", True)
st.session_state.setdefault("show_1b_view2", True)
st.session_state.setdefault("show_1b_view3", True)

shell.story(1, " (second half: the licence fits the route)")


@st.fragment  # a click or a filter in Views 1 and 2 re-runs only these two views (View 2 reads the countries of View 1)
def views_one_and_two():
    keep_state()  # this fragment runs without app.py, so it keeps the settings of a switched-off view itself
    with st.container(key="licence_classes", border=True):
        head1, tog1 = st.columns([5, 1], vertical_alignment="center")
        head1.subheader("1. How much capability can the bank run on its own servers, by licence class?",
                        anchor="view-1")
        if tog1.toggle("Show view", key="show_1b_view1"):
            render_view3(models, licence_check)
    with st.container(key="licence_mix", border=True):
        head2, tog2 = st.columns([5, 1], vertical_alignment="center")
        head2.subheader("2. Are the open-weight models released each year becoming easier to self-host?",
                        anchor="view-2")
        if tog2.toggle("Show view", key="show_1b_view2"):
            render_licence_mix(models, licence_check)  # second chart of story 1b, same developer-country control


views_one_and_two()

with st.container(key="licence_terms", border=True):
    head3, tog3 = st.columns([5, 1], vertical_alignment="center")
    head3.subheader("3. Which licence term holds the condition?", anchor="view-3")
    if tog3.toggle("Show view", key="show_1b_view3"):
        render_licence_terms()  # third chart of story 1b, term by term, with its own filters

shell.limitations_1b()
