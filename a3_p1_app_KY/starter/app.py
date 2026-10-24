from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.views import render_population_view


ROOT = Path(__file__).resolve().parent
SAMPLE = ROOT / "data" / "sample.csv"
PROCESSED = ROOT / "data" / "processed.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    frame = pd.read_csv(path, parse_dates=["date"])
    return frame.sort_values(["country", "date"]).reset_index(drop=True)


def data_path() -> Path:
    sample_mode = os.getenv("DASHBOARD_SAMPLE_MODE", "0") == "1"
    if sample_mode or not PROCESSED.exists():
        return SAMPLE
    return PROCESSED


st.set_page_config(page_title="Population change", layout="wide")
st.title("Population change in Australia and New Zealand")
st.write(
    "**Question:** How did the populations of Australia and New Zealand change "
    "from 2019 to 2023?"
)
st.caption("Audience: interested non-specialists comparing population change.")
data = load_data(str(data_path()))

with st.container(key="population_trend"):
    render_population_view(data)

with st.expander("Data and limitations"):
    st.markdown(
        "**Source:** World Development Indicators: Population, total "
        "(SP.POP.TOTL), published by the World Bank."
    )
    st.markdown(
        "The indicator is an annual estimate assembled from national statistical "
        "offices, the United Nations Population Division and World Bank metadata. "
        "The latest year in this submitted snapshot is 2023. Values may be revised."
    )
    st.markdown(
        "[World Bank API](https://api.worldbank.org/v2/country/"
        "AUS;NZL/indicator/SP.POP.TOTL?format=json)"
    )
