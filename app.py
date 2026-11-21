"""A3P2: Model Choice Explorer, one page per user story.

Run from this folder:  streamlit run app.py
Each page lives in its own story folder (stories/<story>/page.py) with its own data and notebook.
"""
from __future__ import annotations

import streamlit as st

from src import shell
from src.selection import keep_state

st.set_page_config(page_title="Model Choice Explorer", layout="wide")

# Keep every widget setting when a reader moves to another page and comes back
# (Streamlit drops the state of widgets that are not drawn on the current page).
keep_state()

shell.header()

PAGES = [
    st.Page("stories/1a_ranked_shortlist/page.py", title="1a · Shortlist: capability for the price",
            default=True),
    st.Page("stories/1b_licence_route/page.py", title="1b · Self-hosting: what the licence allows",
            url_path="licence"),
    st.Page("stories/2_gap_to_us_models/page.py", title="2 · Waiting for US access: the gap",
            url_path="gap"),
    st.Page("stories/3_reported_incidents/page.py", title="3 · Openness and reported incidents by developer",
            url_path="incidents"),
]
st.navigation(PAGES, position="top").run()
