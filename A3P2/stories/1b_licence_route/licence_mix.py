"""Story 1b, second chart (owner: Anh): the licence mix of open-weight releases by year.

View 3 (the dot strip) shows how much capability each licence class holds today. This chart adds the trend:
of the open-weight models released each year, how many may a bank self-host for commercial use under Epoch's label?
It reads the same table and View 3's developer-country control; it always shows every release year, because the
trend is the point of the chart. Counts come straight from data/model_capability.csv; nothing is hand-coded.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.views import GRID, INK, MUTED, PLOT_CONFIG
from src.views_context import WINDOW_ALL, view3_data

# Okabe-Ito colours, safe for the common colour vision deficiencies; every segment also carries a text label.
MIX_CLASSES = {
    "Open weights, unrestricted": ("Commercial self-hosting allowed", "#0072B2"),
    "Open weights, restricted use": ("Self-hosting after a legal review", "#E69F00"),
    "Open weights, non-commercial": ("No commercial use", "#999999"),
}
LATEST_RELEASE = pd.Timestamp("2026-10-07")
LATEST_SHORT = f"{LATEST_RELEASE.day} {LATEST_RELEASE:%b}"  # "7 Oct", built without the Unix-only day flag
LATEST_LONG = f"{LATEST_RELEASE.day} {LATEST_RELEASE:%B %Y}"
EMPTY_TEXT = "No open-weight models from the chosen developer countries, so there is no licence mix to show. Choose more countries above."


def mix_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Open-weight models per release year and licence class, with each class's share of the year."""
    open_w = frame.loc[frame["licence_class"].isin(MIX_CLASSES)]
    if open_w.empty:
        return pd.DataFrame(columns=["release_year", "licence_class", "models", "share"])
    counts = (open_w.groupby(["release_year", "licence_class"]).size()
              .unstack(fill_value=0).reindex(columns=list(MIX_CLASSES), fill_value=0))
    long = counts.stack().rename("models").reset_index()
    long["share"] = (long["models"] / long.groupby("release_year")["models"].transform("sum") * 100).round(1)
    return long


def _year_label(year: int) -> str:
    return f"{year}<br>(to {LATEST_SHORT})" if year == LATEST_RELEASE.year else str(year)


def chart_mix(table: pd.DataFrame) -> go.Figure:
    years = sorted(table["release_year"].unique())
    totals = table.groupby("release_year")["models"].sum()
    fig = go.Figure()
    for name, (meaning, colour) in MIX_CLASSES.items():
        part = table.loc[table["licence_class"] == name].set_index("release_year").reindex(years)
        text = [f"{int(n)} ({s:.0f}%)" if n > 0 else "" for n, s in zip(part["models"], part["share"])]
        fig.add_trace(go.Bar(
            x=[_year_label(y) for y in years], y=part["share"], name=f"{name}: {meaning.lower()}",
            marker={"color": colour, "line": {"color": "white", "width": 1.5}}, text=text,
            textposition="inside", insidetextanchor="middle", textfont={"size": 13, "color": "white"},
            customdata=part["models"], hovertemplate="%{x}: %{customdata} models, %{y:.1f}%<extra>" + name + "</extra>"))
    for y in years:
        fig.add_annotation(x=_year_label(y), y=100, text=f"{int(totals[y])} models", showarrow=False, yshift=12,
                           font={"size": 12, "color": INK})
    fig.update_layout(
        barmode="stack", height=430, margin={"l": 10, "r": 10, "t": 70, "b": 10},
        title={"text": "Licence mix of open-weight models released each year (share of the year's releases)",
               "font": {"size": 16, "color": INK}, "x": 0, "xanchor": "left"},
        plot_bgcolor="white", paper_bgcolor="white", font={"family": "Arial, sans-serif", "size": 13, "color": INK},
        legend={"orientation": "h", "yanchor": "top", "y": -0.18, "x": 0, "font": {"size": 12}},
        uniformtext={"minsize": 11, "mode": "hide"})
    fig.update_xaxes(title_text="Release year (Epoch release date)", showgrid=False)
    fig.update_yaxes(title_text="Share of open-weight models released (%)", range=[0, 108], gridcolor=GRID,
                     ticksuffix="%", dtick=25)
    return fig


def answer_text(table: pd.DataFrame) -> str:
    unres = table.loc[table["licence_class"] == "Open weights, unrestricted"].set_index("release_year")
    totals = table.groupby("release_year")["models"].sum()
    first, last = int(totals.index.min()), int(totals.index.max())
    if first == last or unres.empty:
        y = last
        return (f"**Reading for story 1b.** In {y}, {int(unres['models'].get(y, 0))} of {int(totals[y])} open-weight "
                f"models in this selection ({unres['share'].get(y, 0):.0f}%) carry Epoch's unrestricted label.")
    a, b = unres["share"].get(first, 0.0), unres["share"].get(last, 0.0)
    trend = "rose" if b > a + 5 else "fell" if b < a - 5 else "stayed about the same"
    text = (f"**Reading for story 1b.** The share of open-weight releases that Epoch labels unrestricted {trend}, "
            f"from {a:.0f}% in {first} ({int(unres['models'].get(first, 0))} of {int(totals[first])} models) to "
            f"{b:.0f}% in {last} ({int(unres['models'].get(last, 0))} of {int(totals[last])}"
            f"{', releases to 7 Oct' if last == LATEST_RELEASE.year else ''}). ")
    if b > a + 5:
        text += ("For the architect, the self-hosting route has widened: most new open-weight models can now go to the "
                 "legal team as candidates for commercial use, rather than being ruled out by their licence. ")
    text += "Epoch's label is not a legal reading, so each shortlisted licence still needs the bank's own review."
    return text


def render_licence_mix(models: pd.DataFrame, check: pd.DataFrame) -> None:
    """Second chart of story 1b. Uses View 3's developer-country control (key v3_countries). It always shows every
    release year, because a trend cut to the release window above (two years by default) would hide the change."""
    countries = st.session_state.get("v3_countries") or []
    frame = view3_data(models, check, WINDOW_ALL, countries)
    st.subheader("3b. Are the open-weight models released each year becoming easier to self-host?", anchor="view-3b")
    st.caption("Unit: share of the open-weight models released in each year (%), with the number of models in each "
               "segment. Licence class from Epoch AI's accessibility label. Uses the developer countries chosen above, "
               "and always every release year (Feb 2023 to 7 Oct 2026), since the trend needs all years.")
    if frame.empty:
        st.caption("No models match the filters above.")
        return
    table = mix_table(frame)
    if table.empty:
        st.info(EMPTY_TEXT)
        return
    st.plotly_chart(chart_mix(table), width="stretch", key="v3b_mix_chart", config=PLOT_CONFIG)
    st.caption("Each bar is one release year and adds up to 100% of that year's open-weight releases. The label in a "
               "segment is the number of models and its share; the number above a bar is the year's total. "
               f"{LATEST_RELEASE.year} covers releases to {LATEST_LONG} only.")
    st.markdown(answer_text(table))
    with st.expander("**Values behind this chart**"):
        wide = table.pivot(index="release_year", columns="licence_class", values="models").reindex(
            columns=list(MIX_CLASSES))
        wide["All open-weight"] = wide.sum(axis=1)
        wide["Unrestricted share (%)"] = (wide["Open weights, unrestricted"] / wide["All open-weight"] * 100).round(1)
        st.dataframe(wide.reset_index().rename(columns={"release_year": "Release year"}), hide_index=True,
                     key="v3b_mix_values")
    with st.expander("**Design decision for this chart** (task, form, rejected alternatives)"):
        st.markdown(
            "**Visual task:** show how the licence mix of new open-weight models has changed, so the architect can "
            "tell the committee whether the self-hosting route is widening or narrowing.\n\n"
            "**Form chosen:** a 100% stacked bar per release year (Visual Vocabulary: *part-to-whole*), with the "
            "count and share written in every segment so no value needs hovering.\n\n"
            "**Alternatives rejected:**\n\n"
            "1. **Stacked bars of counts.** The yearly totals differ (2026 is a part year), so the share that matters "
            "would have to be judged from bars of different heights.\n"
            "2. **One pie chart per year.** Angles across four pies are harder to compare than aligned bar segments.\n"
            "3. **A line of the unrestricted share only.** It hides the trade between restricted-use and "
            "non-commercial licences, which decides how much legal review the shortlist needs.")
    with st.expander("**What this chart cannot show**"):
        st.markdown(
            "- **Labels, not legal readings:** the classes are Epoch's labels. The group read only 5 licences; "
            "Epoch calls Kimi K3 non-commercial while its licence text allows commercial use under a revenue "
            "condition.\n"
            f"- **{LATEST_RELEASE.year} is a part year** (releases to {LATEST_SHORT}), so its total is lower "
            "and its share may still move.\n"
            "- **Only models Epoch has scored** are counted, not every open-weight model published.\n"
            "- **Counts are not quality:** a year with more unrestricted models does not mean better unrestricted "
            "models; the dot strip above shows capability.")
    st.caption("**Source:** Epoch AI, Epoch Capabilities Index (`eci_scores.csv`, CC BY), retrieved 17 Oct 2026; "
               f"latest model release in the file {LATEST_LONG}. Licence class from Epoch's accessibility label. "
               "Counts computed from `stories/1b_licence_route/data/model_capability.csv`.")
