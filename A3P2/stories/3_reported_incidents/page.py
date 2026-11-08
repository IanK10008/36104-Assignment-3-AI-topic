"""Story 3: which developers appear in reported AI incidents, View 5.

Reads only this folder's own data: data/model_capability.csv (Epoch), data/incidents.csv and
data/incident_developers.csv (AI Incident Database). The tables are joined here, not in the notebooks.
Runs inside app.py or on its own:
    streamlit run stories/3_reported_incidents/page.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))  # so that "src" is found when this file is run on its own

import streamlit as st  # noqa: E402

from src import aiid, epoch_models, shell  # noqa: E402
from src.views_context import render_view5  # noqa: E402

# First year shown. A3P1 uses 2015 for the slider and 2012 for the top chart. Here both start in 2020: before
# 2020 the database has at most 50 incidents a year and 11 to 22 incidents naming a company, too few to compare
# developers. 2020 to 2022 are the years before ChatGPT (November 2022), shown as the baseline.
SLIDER_FIRST_YEAR = 2020
CHART_FIRST_YEAR = 2020

shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load(folder: str):
    models = epoch_models.load_epoch_models(f"{folder}/model_capability.csv")
    incidents, named = aiid.load_incidents(f"{folder}/incidents.csv", f"{folder}/incident_developers.csv")
    return models, incidents, named


models, incidents, incident_developers = load(str(HERE / "data"))

shell.story(3, "")
with st.container(key="reported_incidents", border=True):
    st.subheader("5. Which developers appear in reported AI incidents, and how often?", anchor="view-5")

    @st.fragment
    def view_five():
        render_view5(models, incidents, incident_developers, SLIDER_FIRST_YEAR, CHART_FIRST_YEAR)

    view_five()

shell.limitations()
