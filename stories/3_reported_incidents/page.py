"""Story 3: how openly each developer builds its models and how often it appears in reported incidents.

View 1 (Stanford FMTI, December 2025) and View 2 (AI Incident Database model incidents with Epoch model
releases). Reads only this folder's own data: data/fmti_dec2025_scores_tidy.csv and data/fmti_companies.csv (FMTI),
data/aiid_model_incidents_by_developer.csv (AI Incident Database) and data/model_capability.csv (Epoch). Nothing is
joined in a notebook. Runs inside app.py or on its own:
    streamlit run stories/3_reported_incidents/page.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))  # so that "src" is found when this file is run on its own

import streamlit as st  # noqa: E402

from src import epoch_models, shell, views_story3  # noqa: E402
from src.selection import view_header  # noqa: E402

shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load_epoch(folder: str):
    return epoch_models.load_epoch_models(f"{folder}/model_capability.csv")


epoch = load_epoch(str(HERE / "data"))

shell.story(3, "")
with st.container(key="fmti_view", border=True):
    open_a = view_header("1. How openly does each developer build its models?", "show_3_view1", "view-1")

    @st.fragment
    def view_a():
        views_story3.render_fmti()

    if open_a:
        view_a()

with st.container(key="incident_view", border=True):
    open_b = view_header("2. How often does each developer appear in reported model incidents, and what went wrong?",
                         "show_3_view2", "view-2")

    @st.fragment
    def view_b():
        views_story3.render_incidents(epoch)

    if open_b:
        view_b()

shell.limitations_3()
