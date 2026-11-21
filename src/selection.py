"""Selection of a multiselect whose options change with other controls."""
from __future__ import annotations

import streamlit as st


def keep_selection(key: str, options: list) -> None:
    """Set the selection of the multiselect ``key`` before it is drawn.

    An entry that the reader removed stays removed when the options change and come back. An entry that was not
    offered before (for example a region switched on again) starts selected. Nothing is reset to the full list."""
    shown = st.session_state.get(key + "_shown")
    removed = set(st.session_state.get(key + "_removed", ()))
    current = st.session_state.get(key)
    if shown is not None and isinstance(current, list):
        removed = (removed - set(current)) | (set(shown) - set(current))
    st.session_state[key + "_removed"] = removed
    st.session_state[key + "_shown"] = list(options)
    st.session_state[key] = [o for o in options if o not in removed]


def view_header(title: str, key: str, anchor: str) -> bool:
    """Heading of a view with a "Show view" switch at the right, as on the Story 1a and 1b pages.

    The switch only hides the view. The settings of its controls are kept (see app.py)."""
    st.session_state.setdefault(key, True)
    head, tog = st.columns([5, 1], vertical_alignment="center")
    head.subheader(title, anchor=anchor)
    return tog.toggle("Show view", key=key)


# Charts and tables that report a click are output widgets. Streamlit does not allow a value to be set for them.
_OUTPUT_KEYS = ("a_heat", "a_indicators", "b_funnel", "b_picked", "b_timeline", "story2_4b_chart")


def _is_output_widget(key: str) -> bool:
    if key.endswith(("_download", "_table", "_chart", "_values")) or key.startswith(_OUTPUT_KEYS):
        return True
    try:  # a chart or table that reports a selection holds a mapping with a "selection" entry, so a new one is found too
        return "selection" in st.session_state[key]
    except (TypeError, KeyError):
        return False


def keep_state() -> None:
    """Keep the value of every widget that is not drawn in this run (a view that is switched off).

    Streamlit drops the state of widgets that are not drawn. app.py does this at the start of each full run. A
    fragment runs without app.py, so a fragment that holds a "Show view" switch calls this too."""
    for key in list(st.session_state):
        if not _is_output_widget(key):
            st.session_state[key] = st.session_state[key]
