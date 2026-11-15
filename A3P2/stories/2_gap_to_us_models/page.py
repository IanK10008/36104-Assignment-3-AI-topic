
"""Story 2: Capability gap and independent benchmark comparison.

Runs inside app.py or on its own:
    streamlit run stories/2_gap_to_us_models/page.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Allow imports from the repository and Story 2 folder.
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE))

import streamlit as st  # noqa: E402

from src import epoch_models, shell  # noqa: E402
from src.views_context import render_view4  # noqa: E402
from v3_benchmark import render_v3  # noqa: E402


shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load(path: str):
    return epoch_models.load_epoch_models(path)


models = load(str(HERE / "data" / "model_capability.csv"))

shell.story(2, "")

# V2 - Existing capability gap chart
with st.container(key="capability_gap", border=True):
    st.subheader(
        "4. How far do accessible models trail the restricted US models, "
        "and is the gap shrinking?",
        anchor="view-4",
    )

    @st.fragment
    def view_four():
        render_view4(models)

    view_four()


# V3 - New independent benchmark comparison
with st.container(border=True):
    render_v3()


shell.limitations()
