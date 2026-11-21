
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

import datetime as dt  # noqa: E402

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from src import context as cx  # noqa: E402
from src import epoch_models, shell, views_context  # noqa: E402
from src.selection import view_header  # noqa: E402
from src.views_context import render_view4  # noqa: E402
from v3_difference import render_v3_difference  # noqa: E402
from view4b import render_view4b  # noqa: E402


shell.standalone_page_config()


@st.cache_data(show_spinner=False)
def load(path: str):
    return epoch_models.load_epoch_models(path)


models = load(str(HERE / "data" / "model_capability.csv"))


def _label_rejected_draft(make):
    """Wrap the small rejected-draft chart of View 1 so that its axes and its two lines carry titles and names."""
    def labelled(frame):
        fig = make(frame)
        fig.data[0].name, fig.data[1].name = "Best model overall", "Best open-weight model"
        fig.update_layout(showlegend=True, height=270, margin={"l": 55, "r": 20, "t": 10, "b": 85},
                          legend={"orientation": "h", "x": 0, "y": -0.35})
        fig.update_xaxes(title_text="Release date")
        fig.update_yaxes(title_text="Capability (ECI points)")
        return fig
    return labelled


views_context.mini_rejected_v4 = _label_rejected_draft(views_context.mini_rejected_v4)


def answer_text_2(models: pd.DataFrame) -> str:
    """One-sentence reading of View 1 for the routes and the end date now selected (the widget values in session state,
    or the defaults of the view before the first change). Every number comes from the Epoch file through gap_summary()."""
    frame = views_context.view4_frame(models)
    lo, hi = frame["release_date"].min().date(), frame["release_date"].max().date()
    options = list(cx.ACCESS_OPTIONS)
    picked = [p for p in st.session_state.get("v4_access", options) if p in cx.ACCESS_OPTIONS]
    accessible = [cx.ACCESS_OPTIONS[p] for p in picked]
    saved = st.session_state.get("v4_dates")
    valid = (isinstance(saved, (tuple, list)) and len(saved) == 2 and all(isinstance(d, dt.date) for d in saved)
             and lo <= saved[0] < saved[1] <= hi)
    end = pd.Timestamp(saved[1] if valid else hi)
    now = cx.gap_summary(frame, accessible, end) if accessible else {}
    if not now:
        return ""
    before = cx.gap_summary(frame, accessible, end - pd.DateOffset(months=12))
    a, r, when = now["accessible"], now["restricted"], views_context._date(end)
    head = f"On {when}, the best accessible model ({a['model']}, {a['eci']:.1f} ECI points) "
    if now["gap"] <= 0:
        text = head + f"is level with or ahead of the best restricted US model ({r['model']}, {r['eci']:.1f}). "
    else:
        text = head + f"trails the best restricted US model ({r['model']}, {r['eci']:.1f}) by {now['gap']:.1f} points"
        if now["lag_months"] is not None:
            text += (f", and restricted models first reached that accessible score {now['lag_months']:.0f} months "
                     f"earlier, on {views_context._date(now['reached_on'])}")
        text += ". "
    if before:
        change = now["gap"] - before["gap"]
        verb = ("has not changed" if abs(change) < 0.05
                else f"has {'widened' if change > 0 else 'narrowed'} by {abs(change):.1f} points")
        text += f"Twelve months earlier the gap was {before['gap']:.1f} points, so it {verb}."
    return text.strip()


shell.story(2, "")

# V2 - Existing capability gap chart
with st.container(key="capability_gap", border=True):
    open_one = view_header("1. How far do accessible models trail the restricted US models, and is the gap shrinking?",
                           "show_2_view1", "view-1")

    @st.fragment
    def view_four():
        # render_view4 is locked, so the sentence is written right after its main chart by wrapping st.plotly_chart
        # for the duration of this call only. The result sits directly below the chart, above the gap table.
        original = st.plotly_chart

        def chart_then_reading(*args, **kwargs):
            result = original(*args, **kwargs)
            if kwargs.get("key") == "v4_chart":
                reading = answer_text_2(models)
                if reading:
                    st.markdown(reading)
            return result

        st.plotly_chart = chart_then_reading
        try:
            render_view4(models)
        finally:
            st.plotly_chart = original

    if open_one:
        view_four()


# View 2 (alternative) - who produced the benchmark scores behind the capability index
with st.container(key="view4b_alternative", border=True):
    render_view4b()


# View 3 (alternative, proposal chart V3) - difference between developer-reported and Epoch GPQA scores
with st.container(border=True):
    render_v3_difference()


shell.limitations_2()
