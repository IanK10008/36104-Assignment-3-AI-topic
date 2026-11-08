"""Story 2: how far accessible models trail the restricted US models, View 4.

Reads only this folder's own data (data/model_capability.csv). Runs inside app.py or on its own:
    streamlit run stories/2_gap_to_us_models/page.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))  # so that "src" is found when this file is run on its own

import streamlit as st  # noqa: E402

from src import epoch_models, shell  # noqa: E402
from src.views_context import render_view4  # noqa: E402


shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load(path: str):
    return epoch_models.load_epoch_models(path)


models = load(str(HERE / "data" / "model_capability.csv"))

shell.story(2, "")
with st.container(key="capability_gap", border=True):
    st.subheader("4. How far do accessible models trail the restricted US models, and is the gap shrinking?",
                 anchor="view-4")

    @st.fragment
    def view_four():
        render_view4(models)

    view_four()

shell.limitations()
