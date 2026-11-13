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
from src.views_context import render_view3  # noqa: E402
from licence_mix import render_licence_mix  # noqa: E402


shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load(path: str):
    return epoch_models.load_epoch_models(path), epoch_models.load_licence_check(path)


models, licence_check = load(str(HERE / "data" / "model_capability.csv"))

shell.story(1, " (second half: the licence fits the route)")
with st.container(key="licence_classes", border=True):
    st.subheader("3. How much capability can the bank run on its own servers, by licence class?",
                 anchor="view-3")

    @st.fragment  # a click inside View 3 re-runs only View 3
    def view_three():
        render_view3(models, licence_check)
        st.divider()
        render_licence_mix(models, licence_check)  # second chart of story 1b, same controls

    view_three()

shell.limitations()
