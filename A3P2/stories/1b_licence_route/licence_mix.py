"""Story 1b, View 3b (owner: Anh): the licence mix of open-weight releases by year.

View 3 (the dot strip) shows how much capability each licence class holds today. View 3b adds the trend: of the
open-weight models released each year, how many may a bank self-host for commercial use under Epoch's label?

Layout and colours follow Ian's views in src/views_context.py: unit caption, metrics, "Selected" line, HTML legend
above the chart, fixed-width Plotly chart with no title inside it, visible values table, then how to read, design
decision, limits, filtered records with a CSV download, and the shared sources footer. Open weights stay in View 3's
blue (#0072B2); the three licence classes are steps of that one blue, darkest for the most permissive.

It reads the same table and View 3's developer-country control, and always shows every release year, because the
trend is the point of the chart. Counts come straight from data/model_capability.csv; nothing is hand-coded.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.views import INK, MUTED, PLOT_CONFIG, footer
from src.views_context import (OPEN, WINDOW_ALL, ZOOM_NOTE, _layout, download_records, legend_html,
                               view3_data)

# One hue (View 3's open-weight blue) in three steps, darkest = most permissive. Lightness alone separates the steps,
# so they survive every colour vision deficiency; each segment also carries its count and share as text.
MIX_CLASSES = {
    "Open weights, unrestricted": ("Commercial self-hosting allowed", OPEN, "white"),
    "Open weights, restricted use": ("Self-hosting after a legal review", "#56B4E9", INK),
    "Open weights, non-commercial": ("No commercial use", "#D6E9F6", INK),
}
LIGHT_EDGE = "#8DB6D6"  # outline for the palest step, so it stays visible against the white background
LATEST_RELEASE = pd.Timestamp("2026-10-07")
LATEST_SHORT = f"{LATEST_RELEASE.day} {LATEST_RELEASE:%b}"  # "7 Oct", built without the Unix-only day flag
LATEST_LONG = f"{LATEST_RELEASE.day} {LATEST_RELEASE:%B %Y}"
EMPTY_TEXT = ("No open-weight models from the chosen developer countries, so there is no licence mix to show. "
              "Choose more countries above.")

HOW_TO_READ = f"""
- **One row per release year,** from 2023 at the top to 2026 at the bottom. Each row is all the open-weight models
  Epoch scored that were released in that year, shown as 100%. The number under the year is that total.
- **Three shades of the open-weight blue:** darkest, the licence allows commercial self-hosting (Epoch: unrestricted);
  middle, it can be self-hosted after a legal review (restricted use); palest, it cannot be used for the bank's
  business (non-commercial). Each segment shows the number of models and its share of the year.
- **Read the dark segment down the rows:** a longer dark segment means more of that year's new open-weight models
  could go to the legal team as self-hosting candidates.
- **The dashed line marks 50%:** a dark segment that reaches past it means most of that year's releases carry an
  unrestricted label.
- **{LATEST_RELEASE.year} is a part year,** releases to {LATEST_SHORT} only, so its total is smaller.
- **The filter above changes the rows:** "Developer based in" keeps only models from those countries. The release
  window above does not apply here, because the chart needs every year to show the change.
"""

DESIGN_DECISION = """
**Why this view was added (story 1b):** View 3 is a snapshot: how much capability each licence class holds today.
The architect is also deciding whether the bank should build a self-hosting route at all, which only pays off if
self-hostable models keep coming. View 3b answers that with the trend: of each year's new open-weight models, how many
may the bank run for its business. It also shows a change over time, which ties story 1b to the rise of AI.

**Visual task:** Show how the licence mix of new open-weight models has changed, so the architect can tell the
committee whether the self-hosting route is widening or narrowing.

**Form chosen:** A horizontal 100% stacked bar per release year (Visual Vocabulary: *part-to-whole*), with the count
and share written in every segment, so no value needs hovering. The three classes are steps of View 3's open-weight
blue, darkest for the most permissive, because the classes are ordered (from "allowed" to "not allowed") and every
model here is open-weight. Rows read top to bottom in time, with the year's total under each label, as in View 3.

**Alternatives rejected:**

1. **Vertical 100% bars in blue, orange and grey (the first draft, shown small below).**
   - **Orange read as "closed":** it is close to the closed-model colour of Views 3 and 4, so the restricted-use
     segment looked like a closed model, yet every model here is open-weight.
   - **Unrelated colours hid the order:** blue, orange and grey say "three kinds", not "allowed, review needed, not
     allowed", which is the order the architect reads.
   - **The legend sat under the chart:** colours had to be matched across the page; the legend now sits above, as in
     every other view.
2. **Stacked bars of counts.** The yearly totals differ (2026 is a part year), so the share that matters would have
   to be judged from bars of different lengths.
3. **One pie chart per year.** Angles across four pies are harder to compare than aligned bar segments.
4. **A line of the unrestricted share only.** It hides the trade between restricted-use and non-commercial licences,
   which decides how much legal review the shortlist needs.
"""

LIMITS = f"""
- **Labels, not legal readings:** the classes are Epoch's labels. The group read only 5 licences; Epoch calls Kimi K3
  non-commercial while its licence text allows commercial use under a revenue condition.
- **{LATEST_RELEASE.year} is a part year** (releases to {LATEST_SHORT}), so its total is lower and its share may
  still move.
- **Only models Epoch has scored** are counted, not every open-weight model published.
- **Counts are not quality:** a year with more unrestricted models does not mean better unrestricted models; the dot
  strip above shows capability.
- **Self-hosting needs more than a licence:** hardware, running cost and a security review are not measured.
"""


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


def _segment_label(n: int, share: float) -> str:
    """Count and share inside a segment; only the count when the segment is too narrow for both."""
    if n == 0:
        return ""
    return f"{n} ({share:.0f}%)" if share >= 7 else f"{n}"


def chart_mix(table: pd.DataFrame, revision: str) -> go.Figure:
    years = sorted(table["release_year"].unique())
    totals = table.groupby("release_year")["models"].sum()
    fig = go.Figure()
    for name, (meaning, fill, text_colour) in MIX_CLASSES.items():
        part = table.loc[table["licence_class"] == name].set_index("release_year").reindex(years)
        edge = LIGHT_EDGE if fill == MIX_CLASSES["Open weights, non-commercial"][1] else "white"
        fig.add_trace(go.Bar(
            y=list(range(len(years))), x=part["share"], orientation="h", name=name,
            marker={"color": fill, "line": {"color": edge, "width": 1.5}},
            text=[_segment_label(int(n), s) for n, s in zip(part["models"], part["share"])],
            textposition="inside", insidetextanchor="middle", textangle=0,
            textfont={"size": 12, "color": text_colour}, customdata=part["models"],
            hovertemplate=f"<b>{name}</b><br>{meaning}<br>%{{customdata}} models, %{{x:.1f}}% of the year"
                          "<extra></extra>"))
    fig.add_shape(type="line", x0=50, x1=50, y0=-0.55, y1=len(years) - 0.45,
                  line={"color": MUTED, "width": 1.3, "dash": "dash"}, layer="above")
    fig.add_annotation(x=50, y=1, yref="paper", yanchor="bottom", xanchor="left", xshift=4, showarrow=False,
                       text="50% of the year's releases", font={"size": 11, "color": MUTED})
    ticks = []
    for y in years:
        tick = f"<b>{y}</b><br><span style='color:{MUTED}'>{int(totals[y])} models</span>"
        if y == LATEST_RELEASE.year:
            tick += f"<br><span style='color:{MUTED}'>to {LATEST_SHORT}</span>"
        ticks.append(tick)
    _layout(fig, 110 + 85 * len(years), "Share of the year's open-weight releases (%)", "", revision,
            {"l": 120, "r": 30, "t": 40, "b": 60})
    fig.update_layout(barmode="stack", bargap=0.35, uniformtext={"minsize": 11, "mode": "show"})
    fig.update_xaxes(range=[0, 100], ticksuffix="%", dtick=25)
    fig.update_yaxes(tickvals=list(range(len(years))), ticktext=ticks, range=[len(years) - 0.5, -0.6],
                     showgrid=False, ticks="")
    return fig


def mini_rejected_v3b(table: pd.DataFrame) -> go.Figure:
    """Small copy of the first draft: vertical 100% bars in blue, orange and grey, legend under the chart."""
    years = sorted(table["release_year"].unique())
    fig = go.Figure()
    for name, colour in zip(MIX_CLASSES, ["#0072B2", "#E69F00", "#999999"]):
        part = table.loc[table["licence_class"] == name].set_index("release_year").reindex(years)
        fig.add_trace(go.Bar(x=[str(y) for y in years], y=part["share"], name=name.split(", ")[1].capitalize(),
                             marker_color=colour, hoverinfo="skip"))
    fig.update_layout(barmode="stack", width=560, height=260, margin={"l": 50, "r": 20, "t": 10, "b": 70},
                      plot_bgcolor="white", font={"family": "Arial, sans-serif", "size": 11, "color": INK},
                      legend={"orientation": "h", "y": -0.25, "x": 0})
    fig.update_yaxes(range=[0, 100], ticksuffix="%", gridcolor="#e6e8eb")
    return fig


def _shares(table: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    unres = table.loc[table["licence_class"] == "Open weights, unrestricted"].set_index("release_year")
    return unres, table.groupby("release_year")["models"].sum()


def answer_text(table: pd.DataFrame) -> str:
    unres, totals = _shares(table)
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
            f"{f', releases to {LATEST_SHORT}' if last == LATEST_RELEASE.year else ''}). ")
    if b > a + 5:
        text += ("For the architect, the self-hosting route has widened: most new open-weight models can now go to the "
                 "legal team as candidates for commercial use, rather than being ruled out by their licence. ")
    text += "Epoch's label is not a legal reading, so each shortlisted licence still needs the bank's own review."
    return text


def render_licence_mix(models: pd.DataFrame, check: pd.DataFrame) -> None:
    """View 3b. Uses View 3's developer-country control (key v3_countries). It always shows every release year,
    because a trend cut to the release window above (two years by default) would hide the change."""
    countries = st.session_state.get("v3_countries") or []
    frame = view3_data(models, check, WINDOW_ALL, countries)
    st.subheader("3b. Are the open-weight models released each year becoming easier to self-host?", anchor="view-3b")
    st.caption("Unit: share of the open-weight models released in each year (%), with the number of models. Licence "
               "class from Epoch AI's accessibility label. Uses the developer countries chosen above and always "
               f"every release year (24 Feb 2023 to {LATEST_LONG}), since the trend needs all years.")
    if frame.empty:
        st.info("No models match the filters above. Choose at least one country.")
        footer(["epoch"], f"{LATEST_LONG} (latest Epoch release date)")
        return
    table = mix_table(frame)
    if table.empty:
        st.info(EMPTY_TEXT)
        footer(["epoch"], f"{LATEST_LONG} (latest Epoch release date)")
        return

    unres, totals = _shares(table)
    first, last = int(totals.index.min()), int(totals.index.max())
    a, b = unres["share"].get(first, 0.0), unres["share"].get(last, 0.0)
    last_label = f"{last} (to {LATEST_SHORT})" if last == LATEST_RELEASE.year else str(last)
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Unrestricted share, {first}", f"{a:.0f}%",
              help=f"{int(unres['models'].get(first, 0))} of {int(totals[first])} open-weight models released in "
                   f"{first}.")
    m2.metric(f"Unrestricted share, {last_label}", f"{b:.0f}%",
              delta=f"{b - a:+.0f} points since {first}" if last != first else None,
              help=f"{int(unres['models'].get(last, 0))} of {int(totals[last])} open-weight models released in {last}.")
    m3.metric("Open-weight models in the chart", f"{int(totals.sum())}",
              help="Unrestricted, restricted use and non-commercial together, every release year.")
    st.caption(f"Selected: {int(totals.sum())} open-weight models released {first} to {last_label}, developers based "
               f"in {', '.join(countries)}. " + ZOOM_NOTE)
    legend_html([(fill, f"{name.split(', ')[1].capitalize()}: {meaning.lower()}", "square")
                 for name, (meaning, fill, _) in MIX_CLASSES.items()] + [(MUTED, "50% of the year's releases", "line")])
    revision = f"v3b|{','.join(sorted(countries))}"
    st.plotly_chart(chart_mix(table, revision), width="content", key="v3b_mix_chart", config=PLOT_CONFIG)
    st.markdown(answer_text(table))

    wide = table.pivot(index="release_year", columns="licence_class", values="models").reindex(
        columns=list(MIX_CLASSES))
    wide.columns = ["Unrestricted", "Restricted use", "Non-commercial"]
    wide["All open-weight"] = wide.sum(axis=1)
    wide["Unrestricted share (%)"] = (wide["Unrestricted"] / wide["All open-weight"] * 100).round(1)
    st.caption("Open-weight models released each year, by licence class (number of models)")
    st.dataframe(wide.reset_index().rename(columns={"release_year": "Release year"}), hide_index=True,
                 key="v3b_mix_values")
    with st.expander("**How to read this chart**"):
        st.markdown(HOW_TO_READ)
    with st.expander("**Design decision for this view** (task, form, rejected alternatives)"):
        st.markdown(DESIGN_DECISION)
        st.caption("The rejected first draft, drawn from the same selection:")
        st.plotly_chart(mini_rejected_v3b(table), width="content", key="v3b_rejected_chart",
                        config={"displayModeBar": False})
    with st.expander("**What this chart cannot show**"):
        st.markdown(LIMITS)
    open_w = frame.loc[frame["licence_class"].isin(MIX_CLASSES)].sort_values(["release_year", "licence_class", "model"])
    records = open_w[["model", "release_date", "release_year", "organization", "country", "epoch_accessibility",
                      "licence_class"]].assign(release_date=lambda t: t["release_date"].astype(str).str[:10])
    records = records.rename(columns={
        "model": "Model (Epoch name)", "release_date": "Release date", "release_year": "Release year",
        "organization": "Developer", "country": "Developer country", "epoch_accessibility": "Epoch label",
        "licence_class": "Licence class"})
    download_records(records, "v3b", "view3b_licence_mix_records.csv",
                     "Open-weight models only, every release year, from the developer countries chosen above.")
    footer(["epoch"], f"{LATEST_LONG} (latest Epoch release date)")
