"""Views 3 to 5 of the Model Choice Explorer, one per tab after the shortlist.

- View 3 (user story 1, second half): capability by licence class, i.e. what the bank may run on its own servers.
- View 4 (user story 2): the capability gap between the restricted US models and the accessible ones over time.
- View 5 (user story 3): reported AI incidents by year and by developer.

Each view follows the pattern of Views 1 and 2: title, unit, controls above the chart, chart with the zoom toolbar,
values table, how to read, design decision with the rejected alternatives, limits, filtered records with a CSV
download, sources and the latest observation.
"""

from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import analysis as an
from src import context as cx
from src.views import (CHART_W, DOWNLOAD_LABEL, GRID, INK, MUTED, PLOT_CONFIG, ROUTE_COLOURS, footer)

OPEN, CLOSED, OTHER = ROUTE_COLOURS["Open weights"], ROUTE_COLOURS["Closed weights"], ROUTE_COLOURS["Other or unknown"]
GENERATIVE, NON_GENERATIVE = "#CC79A7", "#B0B6BD"  # Okabe-Ito reddish purple, and a light grey for "other"
CLASS_COLOURS = {"Open weights, unrestricted": OPEN, "Open weights, restricted use": OPEN,
                 "Open weights, non-commercial": OPEN, "API or hosted only": CLOSED,
                 "Unknown or not released": OTHER}
ZOOM_NOTE = "Chart toolbar (top right): drag a box to zoom, use pan, + / - or Autoscale, double-click resets."


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #
def _layout(fig: go.Figure, height: int, x_title: str, y_title: str, revision: str, margin: dict) -> None:
    fig.update_layout(width=CHART_W, height=height, plot_bgcolor="white", paper_bgcolor="white", margin=margin,
                      showlegend=False, uirevision=revision,
                      font={"family": "Arial, sans-serif", "size": 12, "color": INK},
                      hoverlabel={"bgcolor": "white", "font": {"size": 12, "color": INK}})
    fig.update_xaxes(title_text=x_title, showgrid=True, gridcolor=GRID, zeroline=False, linecolor="#9aa1a9",
                     ticks="outside")
    fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor=GRID, zeroline=False, linecolor="#9aa1a9",
                     ticks="outside")


def legend_html(items: list[tuple[str, str, str]]) -> None:
    """Legend line above a chart. Each item is (colour, label, mark) with mark dot, ring, line or band."""
    marks = {
        "dot": "width:11px;height:11px;border-radius:50%;background:{c}",
        "ring": "width:9px;height:9px;border-radius:50%;border:2px solid {c};background:white",
        "line": "width:22px;height:3px;background:{c};vertical-align:3px",
        "band": "width:22px;height:11px;background:{c};opacity:0.35",
        "square": "width:11px;height:11px;background:{c}",
        "shade": "width:22px;height:11px;background:rgba(31,35,40,0.07);border:1px solid #c4c9cf",
    }
    spans = " ".join(f"<span style='white-space:nowrap;margin-right:18px'><span style='display:inline-block;"
                     f"{marks[m].format(c=c)};margin-right:6px;vertical-align:-1px'></span>{label}</span>"
                     for c, label, m in items)
    st.markdown(f"<div style='font-size:0.9rem;color:{MUTED}'>{spans}</div>", unsafe_allow_html=True)


def download_records(table: pd.DataFrame, key: str, file_name: str, note: str) -> None:
    with st.expander("**Filtered records** (the rows behind this chart)"):
        st.caption(f"{len(table):,} rows match the current selection. {note} The CSV download holds the same rows.")
        st.dataframe(table, hide_index=True, height=min(35 * (len(table) + 1) + 3, 390), key=f"{key}_table")
    st.download_button(DOWNLOAD_LABEL, data=table.to_csv(index=False).encode("utf-8"), file_name=file_name,
                       mime="text/csv", key=f"{key}_download")


def _set_default(key: str, value, options: list | None = None) -> None:
    """Start value of a widget, kept in the session. A stale value from an older page version falls back."""
    current = st.session_state.get(key, value)
    if options is not None:
        if isinstance(value, list):
            current = [v for v in current if v in options] if isinstance(current, list) else value
        elif current not in options:
            current = value
    st.session_state[key] = current


def _date(value) -> str:
    return f"{pd.Timestamp(value).day} {pd.Timestamp(value):%b %Y}"


# --------------------------------------------------------------------------- #
# View 3: capability by licence class
# --------------------------------------------------------------------------- #
WINDOW_ALL = "All releases, Feb 2023 to Oct 2026"

V3_HOW = """
- **One row per licence class:** the classes come from Epoch AI's accessibility label, written as what it means for a
  bank that wants to run the model on its own servers. The rows run from "can be self-hosted" at the top to
  "cannot" at the bottom.
- **One dot per model:** further right means a higher capability score. Dots are spread up and down inside a row only
  so that they do not cover each other, and the vertical position inside a row carries no meaning.
- **The large dot in each row:** the best model in that class, with its name and score and a whisker for its 90%
  interval. Where whiskers of two classes overlap, read the two best models as roughly equal.
- **The dashed line:** the best model of any kind in the selection. The distance from a row's best dot to the line is
  the capability given up by staying in that class.
- **Dots with a dark ring:** the five open-weight models whose licence text the group read by hand on 18 Oct 2026.
  Hovering shows the group's reading next to Epoch's label.
"""

V3_LIMITS = """
- **Epoch's label is not a legal reading:** only 5 of the 127 open-weight licences were read by the group. Epoch
  calls Kimi K3 non-commercial, while the licence text read on 18 Oct 2026 allows commercial use with a separate
  agreement above US$20 million of model-as-a-service revenue. The chart keeps Epoch's label and shows the group's
  reading beside it. Neither is legal advice, and any use must be checked by the bank's legal team.
- **Self-hosting needs more than a licence:** hardware, the cost of running the model and a security review are not
  measured.
- **Developer country is where the developer is based,** not where the model may be used. Availability in Hong Kong
  is the premise of the story and is not measured.
- **Capability is one score:** the Epoch Capabilities Index leans to maths and reasoning, and usefulness for the
  bank's own tasks is not measured.
"""

V3_DECISION = """
**Visual task:** Show how much capability is left in each licence class, and how many models each class offers, so
the architect can say which models the bank may run on its own servers and what that choice costs in capability.

**Form chosen:** A dot strip plot by class (Visual Vocabulary: *distribution*), with the best model of each class
labelled and its 90% interval drawn. Every model is visible, so the depth of choice in a class is read together with
its best score.

**Alternatives rejected:**

1. **A bar for the best model of each class (the first draft, shown small below).**
   - **One number per class hides the depth of choice:** a class with 72 models and a class with 11 models look the
     same, yet the committee needs to know how many options remain if the first choice fails a review.
   - **The axis had to start at 100 to show any difference:** a bar that does not start at zero exaggerates the gap.
     With a zero baseline, 157.4 and 155.3 look identical, so the bar form cannot carry the message at all.
   - **The classes overlapped:** "open weights, any licence" contained "open weights, unrestricted", so the bars
     were not separate groups and could not be compared fairly.
   - **The gaps were inside the intervals:** the three open-weight bars differed by about 2 points while each 90%
     interval spans about 5, which the bars hid.
2. **A map of where the models come from.** Only six countries appear, two of them hold 237 of 277 models, and a
   map would suggest that the page measures where a model may be used, which it does not.
3. **A table only.** Good for looking up one model, which the values table below still does, but it hides the spread
   of each class.
"""


def view3_data(models: pd.DataFrame, check: pd.DataFrame, window: str, countries: list[str]) -> pd.DataFrame:
    frame = cx.with_licence(models, check)
    if window != WINDOW_ALL:
        frame = an.filter_models(frame, an.WINDOWS[window], None, list(an.developer_name(frame).unique()))
    return frame.loc[frame["country_group"].isin(countries)].reset_index(drop=True)


def chart_view3(frame: pd.DataFrame, revision: str) -> go.Figure:
    classes = list(cx.LICENCE_CLASSES)
    counts = frame["licence_class"].value_counts()
    best = cx.best_per_class(frame)
    overall = frame.sort_values("eci").iloc[-1]
    fig = go.Figure()
    for i, name in enumerate(classes):
        part = frame.loc[frame["licence_class"] == name].sort_values("eci").reset_index(drop=True)
        part = part.loc[~part["model"].isin(best["model"])].reset_index(drop=True)  # the best is drawn on its own
        if part.empty:
            continue
        jitter = ((np.arange(len(part)) * 0.618) % 1 - 0.5) * 0.56  # fixed spread, the same on every run
        hover = [f"<b>{r.model}</b><br>{r.organization if isinstance(r.organization, str) else 'Developer not stated'}"
                 f" · {r.country_group}<br>Capability {r.eci:.1f} (90% interval {r.eci_ci_low:.1f} to "
                 f"{r.eci_ci_high:.1f})<br>Released {_date(r.release_date)}<br>Epoch label: {r.epoch_accessibility}"
                 + (f"<br><b>Group's reading:</b> {r.our_reading}" if isinstance(r.our_reading, str) else "")
                 for r in part.itertuples()]
        checked = part["our_reading"].notna().to_numpy()
        fig.add_trace(go.Scatter(
            x=part["eci"], y=i + jitter, mode="markers", hovertext=hover, hoverinfo="text",
            marker={"size": np.where(checked, 11, 8), "color": CLASS_COLOURS[name],
                    "opacity": np.where(checked, 1.0, 0.5).tolist(),
                    "line": {"color": np.where(checked, INK, "white").tolist(),
                             "width": np.where(checked, 2, 0.5).tolist()}}))
    for row in best.itertuples():
        i = classes.index(row.licence_class)
        read = isinstance(row.our_reading, str)
        hover = (f"<b>Best in class: {row.model}</b><br>"
                 f"{row.organization if isinstance(row.organization, str) else 'Developer not stated'} · "
                 f"{row.country_group}<br>Capability {row.eci:.1f} (90% interval {row.eci_ci_low:.1f} to "
                 f"{row.eci_ci_high:.1f})<br>Released {_date(row.release_date)}<br>Epoch label: "
                 f"{row.epoch_accessibility}" + (f"<br><b>Group's reading:</b> {row.our_reading}" if read else "")
                 + f"<br>{row.n_in_class} models in this class")
        fig.add_trace(go.Scatter(
            x=[row.eci], y=[i], mode="markers", hovertext=[hover], hoverinfo="text",
            error_x={"type": "data", "symmetric": False, "array": [row.eci_ci_high - row.eci],
                     "arrayminus": [row.eci - row.eci_ci_low], "color": INK, "thickness": 1.3, "width": 5},
            marker={"size": 15, "color": CLASS_COLOURS[row.licence_class],
                    "line": {"color": INK if read else "white", "width": 2.5 if read else 2}}))
        differs = read and row.licence_class == "Open weights, non-commercial"
        note = "<br><span style='font-size:11px'>licence text read: commercial use allowed</span>" if differs else ""
        fig.add_annotation(x=row.eci_ci_high, y=i, text=f"<b>{row.model}</b> {row.eci:.1f}{note}", showarrow=False,
                           xanchor="left", align="left", xshift=8, font={"size": 12, "color": INK},
                           bgcolor="rgba(255,255,255,0.9)", borderpad=1)
    fig.add_shape(type="line", x0=overall["eci"], x1=overall["eci"], y0=-0.55, y1=len(classes) - 0.45,
                  line={"color": MUTED, "width": 1.3, "dash": "dash"}, layer="below")
    fig.add_annotation(x=overall["eci"], y=1, yref="paper", yanchor="bottom", xanchor="right", xshift=-4,
                       showarrow=False, text=f"Best model of any kind: {overall['model']} {overall['eci']:.1f}",
                       font={"size": 11, "color": MUTED})
    ticks = [f"<b>{name}</b><br><span style='color:{MUTED}'>{cx.LICENCE_CLASSES[name][0]}</span>"
             f"<br><span style='color:{MUTED}'>{int(counts.get(name, 0))} models</span>" for name in classes]
    _layout(fig, 620, "Capability score (Epoch Capabilities Index points)", "", revision,
            {"l": 330, "r": 30, "t": 45, "b": 60})
    lo, hi = frame["eci"].min(), max(frame["eci_ci_high"].max(), overall["eci"])
    fig.update_xaxes(range=[lo - 3, hi + 26])
    fig.update_yaxes(tickvals=list(range(len(classes))), ticktext=ticks, range=[len(classes) - 0.5, -0.6],
                     showgrid=False, ticks="")
    return fig


def mini_rejected_v3(frame: pd.DataFrame) -> go.Figure:
    """Small copy of the first draft: best model per class as bars on an axis that starts at 100."""
    rows = [("Closed API only", frame.loc[frame["epoch_accessibility"] == "API access"]),
            ("Open weights, any licence", frame.loc[frame["route"] == "Open weights"]),
            ("Open weights, unrestricted", frame.loc[frame["epoch_accessibility"] == "Open weights (unrestricted)"])]
    rows = [(n, p.sort_values("eci").iloc[-1]) for n, p in rows if not p.empty]
    fig = go.Figure(go.Bar(y=[n for n, _ in rows], x=[r["eci"] for _, r in rows], orientation="h",
                           marker_color=[CLOSED, OPEN, OPEN], hoverinfo="skip",
                           text=[f"{r['eci']:.1f}" for _, r in rows], textposition="inside"))
    fig.update_layout(width=560, height=220, margin={"l": 170, "r": 20, "t": 10, "b": 40}, plot_bgcolor="white",
                      font={"family": "Arial, sans-serif", "size": 11, "color": INK}, showlegend=False)
    fig.update_xaxes(range=[100, 175], gridcolor=GRID, title_text="Axis starts at 100, not 0")
    fig.update_yaxes(autorange="reversed")
    return fig


def render_view3(models: pd.DataFrame, check: pd.DataFrame) -> None:
    st.caption("Unit: capability in Epoch Capabilities Index points. Licence class from Epoch AI's accessibility "
               "label, with the group's own reading of five licences shown on hover.")
    windows = list(an.WINDOWS) + [WINDOW_ALL]
    _set_default("v3_window", windows[0], windows)
    _set_default("v3_countries", cx.COUNTRY_GROUPS, cx.COUNTRY_GROUPS)
    every = cx.with_licence(models, check)
    counts = {w: len(view3_data(models, check, w, cx.COUNTRY_GROUPS)) for w in windows}
    c1, c2 = st.columns([1, 2])
    window = c1.selectbox("Release window", windows, key="v3_window",
                          format_func=lambda w: f"{w} ({counts[w]} models)")
    present = [g for g in cx.COUNTRY_GROUPS if (every["country_group"] == g).any()]
    with c2:
        countries = st.pills("Developer based in", present, selection_mode="multi", key="v3_countries",
                             help="Some organisations prefer or avoid models from developers in particular countries. "
                                  "This is where the developer is based, not where the model may be used.")
    frame = view3_data(models, check, window, countries or [])
    if frame.empty:
        st.info("No models match these filters. Choose at least one country or a wider release window.")
        download_records(frame[[]], "v3", "view3_licence_classes.csv", "")
        footer(["epoch", "licence"], "7 Oct 2026 (latest Epoch release date), licences read 18 Oct 2026")
        return
    best = cx.best_per_class(frame).set_index("licence_class")
    overall = frame.sort_values("eci").iloc[-1]
    n_open = int((frame["route"] == "Open weights").sum())
    m1, m2, m3 = st.columns(3)
    if "Open weights, unrestricted" in best.index:
        top = best.loc["Open weights, unrestricted"]
        m1.metric("Best model the bank may self-host (Epoch: unrestricted)", f"{top['eci']:.1f}",
                  help=f"{top['model']} ({top['organization']}), released {_date(top['release_date'])}.")
        m2.metric("Capability given up against the best model of any kind", f"{overall['eci'] - top['eci']:.1f} points",
                  help=f"Best model of any kind in the selection: {overall['model']} {overall['eci']:.1f}. "
                       "Compare with the 90% intervals before calling the gap real.")
    else:
        m1.metric("Best model the bank may self-host (Epoch: unrestricted)", "none in this selection")
        m2.metric("Capability given up against the best model of any kind", "not available")
    m3.metric("Open-weight models in the selection", f"{n_open}",
              help="Unrestricted, restricted use and non-commercial together.")
    st.caption(f"Selected: {len(frame)} models, released {window}, "
               f"developers based in {', '.join(countries)}. " + ZOOM_NOTE)
    legend_html([(OPEN, "Open weights", "dot"), (CLOSED, "API or hosted only", "dot"),
                 (OTHER, "Unknown or not released", "dot"), (INK, "Licence text read by the group", "ring"),
                 (MUTED, "Best model of any kind", "line")])
    revision = f"v3|{window}|{','.join(sorted(countries))}"
    st.plotly_chart(chart_view3(frame, revision), width="content", key="v3_chart", config=PLOT_CONFIG)

    table = best.reset_index()[["licence_class", "model", "organization", "country_group", "eci", "eci_ci_low",
                                "eci_ci_high", "release_date", "n_in_class", "epoch_accessibility"]]
    table = table.assign(release_date=table["release_date"].astype(str).str[:10]).round(1)
    st.caption("Best model in each licence class")
    st.dataframe(table.rename(columns={
        "licence_class": "Licence class", "model": "Best model", "organization": "Developer",
        "country_group": "Developer based in", "eci": "Capability (points)", "eci_ci_low": "90% low",
        "eci_ci_high": "90% high", "release_date": "Release date", "n_in_class": "Models in class",
        "epoch_accessibility": "Epoch label"}), hide_index=True, key="v3_values")
    checked = frame.loc[frame["our_reading"].notna(), ["model", "epoch_accessibility", "our_reading", "licence_basis"]]
    if not checked.empty:
        with st.expander(f"**Licences read by the group** ({len(checked)} in this selection, read 18 Oct 2026)"):
            st.dataframe(checked.rename(columns={"model": "Model", "epoch_accessibility": "Epoch label",
                                                 "our_reading": "Group's reading",
                                                 "licence_basis": "Licence page and notes"}),
                         hide_index=True, key="v3_checked")
    with st.expander("**How to read this chart**"):
        st.markdown(V3_HOW)
    with st.expander("**Design decision for this view** (task, form, rejected alternatives)"):
        st.markdown(V3_DECISION)
        st.caption("The rejected first draft, drawn from the same selection:")
        st.plotly_chart(mini_rejected_v3(frame), width="content", key="v3_rejected_chart",
                        config={"displayModeBar": False})
    with st.expander("**What this chart cannot show**"):
        st.markdown(V3_LIMITS)
    records = frame[["model", "release_date", "organization", "country", "epoch_accessibility", "licence_class",
                     "eci", "eci_ci_low", "eci_ci_high", "licence_class_ours", "licence_basis"]]
    records = records.rename(columns={
        "model": "Model (Epoch name)", "release_date": "Release date", "organization": "Developer",
        "country": "Developer country", "epoch_accessibility": "Epoch label", "licence_class": "Licence class",
        "eci": "Capability (ECI points)", "eci_ci_low": "ECI 90% low", "eci_ci_high": "ECI 90% high",
        "licence_class_ours": "Group's licence class", "licence_basis": "Licence page and notes"})
    download_records(records, "v3", "view3_licence_classes.csv", "Licence class from Epoch's label.")
    footer(["epoch", "licence"], "7 Oct 2026 (latest Epoch release date), licences read 18 Oct 2026")


# --------------------------------------------------------------------------- #
# View 4: capability gap over time
# --------------------------------------------------------------------------- #
V4_HOW = """
- **Orange step line:** the best restricted model released so far, that is a model from a US developer whose weights
  cannot be downloaded (the leading closed US models of the question). It steps up only when a new best appears.
- **Dark step line:** the best accessible model released so far, from the groups chosen above (open weights from any
  country, and services from developers outside the US).
- **Shaded band:** the capability given up by using accessible models only. A narrowing band means the gap is
  shrinking.
- **Dotted line and "months behind":** how long ago the restricted models first reached the level of today's best
  accessible model. This is easier to judge than points, because the scale rises every year.
- **Dots:** every model, filled for restricted and open-weight models, hollow for services from outside the US.
  Hover for the name, developer and 90% interval.
"""

V4_LIMITS = """
- **The data cannot predict when US access returns,** or whether the gap will keep shrinking. It describes the past.
- **The gap is close to the size of the intervals:** the best models' 90% intervals span about 5 to 7 points, so a gap
  under about 5 points should be read as roughly level.
- **"Restricted" is a rule, not a measurement:** every US model without downloadable weights counts as restricted,
  and every non-US service as accessible. Availability in Hong Kong is the premise of the story and is not measured.
- **17 older models with no country and no open weights are left out,** because neither side can be claimed for them.
- **Release date is Epoch's date** for the model's public release, and the comparison holds only for the models
  Epoch has scored.
- **The second half of user story 2** (independent against developer-reported benchmark scores) is not shown. The
  benchmark files do not say which scores the developers reported themselves, so the comparison cannot be made
  without a hand-built source map.
"""

V4_DECISION = """
**Visual task:** Show how far the best accessible model trails the best restricted US model, and whether the gap is
shrinking, so the architect can tell the committee whether waiting for US access is worth it.

**Form chosen:** Two step lines over release date (Visual Vocabulary: *change over time*), with the gap shaded and
every model shown as a faint dot. The step shape is honest about how the best score changes: it jumps when a new
model is released and stays flat in between.

**Alternatives rejected:**

1. **Best open weights against the best model overall (the first draft, shown small below).**
   - **It compared the wrong groups:** "best overall" also contains accessible models, so whenever an accessible
     model leads, the gap disappears by definition. "Open weights" leaves out the non-US services the bank can use.
   - **Points alone do not answer "how long to wait":** the scale rises every year, so 9 points meant more in 2023
     than in 2026. The months-behind line was added for this reason.
2. **The average score of each group per quarter.** Averages mix small and large models, and the committee chooses
   from the best available models, not the average one.
3. **Today's gap only (a dumbbell of two scores).** Simple, but it cannot show whether the gap is shrinking, which is
   the second half of the question.
"""


def view4_frame(models: pd.DataFrame) -> pd.DataFrame:
    return models.assign(access=cx.access_group(models), release_date=pd.to_datetime(models["release_date"]))


def chart_view4(frame: pd.DataFrame, accessible: list[str], start: pd.Timestamp, end: pd.Timestamp,
                summary: dict, revision: str) -> go.Figure:
    restricted = frame.loc[frame["access"] == "restricted"]
    access = frame.loc[frame["access"].isin(accessible)]
    first = max(restricted["release_date"].min(), access["release_date"].min())
    dates = pd.DatetimeIndex(sorted(set(frame.loc[frame["release_date"].between(first, end), "release_date"])
                                    | {end}))
    r_line, a_line = cx.frontier(restricted, dates), cx.frontier(access, dates)
    shown = dates >= start
    fig = go.Figure()
    styles = {"restricted": ("circle", CLOSED, "Restricted (US developer, no downloadable weights)"),
              "open": ("circle", OPEN, "Accessible: open weights"),
              "api": ("circle-open", None, "Accessible: service from a developer outside the US")}
    dots = frame.loc[frame["access"].isin(["restricted"] + accessible) & frame["release_date"].between(start, end)]
    for group, (symbol, colour, name) in styles.items():
        part = dots.loc[dots["access"] == group]
        if part.empty:
            continue
        colours = colour or [ROUTE_COLOURS.get(r, OTHER) for r in part["route"]]
        hover = [f"<b>{r.model}</b><br>{r.organization if isinstance(r.organization, str) else 'Developer not stated'}"
                 f" · {r.country if isinstance(r.country, str) else 'country not stated'}<br>{name}<br>"
                 f"Capability {r.eci:.1f} (90% interval {r.eci_ci_low:.1f} to {r.eci_ci_high:.1f})<br>"
                 f"Released {_date(r.release_date)}" for r in part.itertuples()]
        fig.add_trace(go.Scatter(x=part["release_date"], y=part["eci"], mode="markers", hovertext=hover,
                                 hoverinfo="text", marker={"symbol": symbol, "size": 7, "color": colours,
                                                           "opacity": 0.35, "line": {"width": 1.5}}))
    x = dates[shown]
    fig.add_trace(go.Scatter(x=x, y=r_line["best"][shown], mode="lines", line={"color": CLOSED, "width": 2.5,
                                                                                "shape": "hv"},
                             hovertext=[f"Best restricted so far: {m} {b:.1f}" for m, b in
                                        zip(r_line["model"][shown], r_line["best"][shown])], hoverinfo="text"))
    fig.add_trace(go.Scatter(x=x, y=a_line["best"][shown], mode="lines", line={"color": INK, "width": 2.5,
                                                                                "shape": "hv"},
                             fill="tonexty", fillcolor="rgba(213,94,0,0.10)",
                             hovertext=[f"Best accessible so far: {m} {b:.1f}" for m, b in
                                        zip(a_line["model"][shown], a_line["best"][shown])], hoverinfo="text"))
    if summary:
        r, a = summary["restricted"], summary["accessible"]
        apart = r["eci"] - a["eci"]
        lift = 9 if abs(apart) < 4 else 0  # keep the two end labels apart when the lines nearly meet
        fig.add_annotation(x=end, y=r["eci"], text=f"Best restricted: <b>{r['model']}</b> {r['eci']:.1f}",
                           showarrow=False, xanchor="left", xshift=10, yshift=lift if apart >= 0 else -lift,
                           font={"size": 12, "color": CLOSED})
        fig.add_annotation(x=end, y=a["eci"], text=f"Best accessible: <b>{a['model']}</b> {a['eci']:.1f}",
                           showarrow=False, xanchor="left", xshift=10, yshift=-lift if apart >= 0 else lift,
                           font={"size": 12, "color": INK})
        if summary["reached_on"] is not None and summary["lag_months"] and summary["lag_months"] >= 0.5:
            fig.add_shape(type="line", x0=summary["reached_on"], x1=end, y0=a["eci"], y1=a["eci"],
                          line={"color": INK, "width": 1.3, "dash": "dot"})
            mid = summary["reached_on"] + (end - summary["reached_on"]) / 2
            # the text sits in the empty space below the lines, with an arrow to the dotted line, so it covers no data
            fig.add_annotation(x=mid, y=a["eci"], ax=0, ay=110, showarrow=True, arrowhead=0, arrowwidth=1,
                               arrowcolor=MUTED, yanchor="top", font={"size": 11, "color": INK},
                               text=f"<b>{summary['lag_months']:.0f} months behind:</b> restricted models reached "
                                    f"{a['eci']:.1f}<br>on {_date(summary['reached_on'])} ({summary['reached_by']})",
                               bgcolor="rgba(255,255,255,0.9)", borderpad=2)
    _layout(fig, 620, "Release date", "Capability score (Epoch Capabilities Index points)", revision,
            {"l": 70, "r": 290, "t": 45, "b": 60})
    pad = pd.Timedelta(days=12)
    fig.update_xaxes(range=[start - pad, end + pad])
    return fig


def mini_rejected_v4(frame: pd.DataFrame) -> go.Figure:
    dates = pd.DatetimeIndex(sorted(set(frame["release_date"])))
    every = cx.frontier(frame, dates)
    open_w = cx.frontier(frame.loc[frame["route"] == "Open weights"], dates)
    fig = go.Figure([go.Scatter(x=dates, y=every["best"], mode="lines", line={"color": CLOSED, "shape": "hv"}),
                     go.Scatter(x=dates, y=open_w["best"], mode="lines", line={"color": OPEN, "shape": "hv"})])
    fig.update_layout(width=560, height=220, margin={"l": 40, "r": 20, "t": 10, "b": 30}, plot_bgcolor="white",
                      font={"family": "Arial, sans-serif", "size": 11, "color": INK}, showlegend=False)
    fig.update_xaxes(gridcolor=GRID)
    fig.update_yaxes(gridcolor=GRID)
    return fig


def render_view4(models: pd.DataFrame) -> None:
    st.caption("Unit: capability in Epoch Capabilities Index points, by release date. Gap in points and in months.")
    frame = view4_frame(models)
    options = list(cx.ACCESS_OPTIONS)
    _set_default("v4_access", options, options)
    lo, hi = frame["release_date"].min().date(), cx.DATA_END.date()
    saved = st.session_state.get("v4_dates")
    valid = (isinstance(saved, (tuple, list)) and len(saved) == 2
             and all(isinstance(d, dt.date) for d in saved) and lo <= saved[0] < saved[1] <= hi)
    if not valid:
        st.session_state["v4_dates"] = (lo, hi)
    c1, c2 = st.columns([1, 1.4])
    with c1:
        picked = st.pills("Accessible models include", options, selection_mode="multi", key="v4_access",
                          help="**Open weights:** the bank downloads the model and runs it itself.\n\n"
                               "**Non-US API or hosted services:** models without downloadable weights from developers "
                               "outside the US, for example Alibaba's Qwen Max. Leaving one out shows the gap for "
                               "the other route only.")
    with c2:
        start_d, end_d = st.slider("Release dates shown", min_value=lo, max_value=hi, key="v4_dates",
                                   format="D MMM YYYY",
                                   help="The lines always count every earlier model, so moving the start only "
                                        "changes the part drawn. The gap and lag below are measured at the end date.")
    accessible = [cx.ACCESS_OPTIONS[p] for p in (picked or [])]
    if not accessible:
        st.info("No accessible models are selected. Choose at least one route above.")
        download_records(frame.iloc[0:0][["model"]], "v4", "view4_capability_gap.csv", "")
        footer(["epoch"], "7 Oct 2026 (latest Epoch release date in the file)")
        return
    start, end = pd.Timestamp(start_d), pd.Timestamp(end_d)
    now = cx.gap_summary(frame, accessible, end)
    before = cx.gap_summary(frame, accessible, end - pd.DateOffset(months=12))
    m1, m2, m3, m4 = st.columns(4)
    if now:
        m1.metric(f"Gap on {_date(end)}", f"{now['gap']:.1f} points",
                  delta=f"{now['gap'] - before['gap']:+.1f} in 12 months" if before else None, delta_color="inverse",
                  help=f"{now['restricted']['model']} {now['restricted']['eci']:.1f} against "
                       f"{now['accessible']['model']} {now['accessible']['eci']:.1f}. The 90% intervals "
                       + ("overlap, so the two may be level." if now["intervals_overlap"] else "do not overlap."))
        lag = now["lag_months"]
        m2.metric("Months behind", f"{lag:.0f}" if lag is not None else "not behind",
                  delta=(f"{lag - before['lag_months']:+.0f} in 12 months"
                         if before and before.get("lag_months") is not None and lag is not None else None),
                  delta_color="inverse",
                  help=(f"Restricted models first reached {now['accessible']['eci']:.1f} with {now['reached_by']} on "
                        f"{_date(now['reached_on'])}." if lag is not None else "The best accessible model is level "
                        "with or ahead of the restricted models."))
        m3.metric("Best accessible model", now["accessible"]["model"],
                  help=f"{now['accessible']['organization']}, {now['accessible']['route'].lower()}, released "
                       f"{_date(now['accessible']['release_date'])}.")
        m4.metric("Best restricted model", now["restricted"]["model"],
                  help=f"{now['restricted']['organization']}, released {_date(now['restricted']['release_date'])}.")
    shown = frame.loc[frame["access"].isin(["restricted"] + accessible) & frame["release_date"].between(start, end)]
    st.caption(f"Selected: {len(shown)} models released {_date(start)} to {_date(end)} "
               f"({int((shown['access'] == 'restricted').sum())} restricted, "
               f"{int(shown['access'].isin(accessible).sum())} accessible). " + ZOOM_NOTE)
    items = [(CLOSED, "Best restricted US model so far", "line"), (INK, "Best accessible model so far", "line"),
             (CLOSED, "Gap", "band"), (CLOSED, "Restricted model", "dot")]
    if "open" in accessible:
        items.append((OPEN, "Open-weight model", "dot"))
    if "api" in accessible:
        items.append((CLOSED, "Non-US service (hollow)", "ring"))
    legend_html(items)
    revision = f"v4|{','.join(accessible)}|{start_d}|{end_d}"
    st.plotly_chart(chart_view4(frame, accessible, start, end, now, revision), width="content", key="v4_chart",
                    config=PLOT_CONFIG)

    rows = []
    for months in (0, 6, 12, 24):
        at = end - pd.DateOffset(months=months)
        s = cx.gap_summary(frame, accessible, at)
        if s:
            rows.append({"Date": _date(at), "Best restricted": s["restricted"]["model"],
                         "Restricted score": round(s["restricted"]["eci"], 1),
                         "Best accessible": s["accessible"]["model"],
                         "Accessible score": round(s["accessible"]["eci"], 1), "Gap (points)": round(s["gap"], 1),
                         "Months behind": round(s["lag_months"]) if s["lag_months"] is not None else None})
    st.caption("Gap at the end date and 6, 12 and 24 months earlier")
    st.dataframe(pd.DataFrame(rows), hide_index=True, key="v4_values")
    with st.expander("**How to read this chart**"):
        st.markdown(V4_HOW)
    with st.expander("**Design decision for this view** (task, form, rejected alternatives)"):
        st.markdown(V4_DECISION)
        st.caption("The rejected first draft: orange = best model overall, blue = best open-weight model.")
        st.plotly_chart(mini_rejected_v4(frame), width="content", key="v4_rejected_chart",
                        config={"displayModeBar": False})
    with st.expander("**What this chart cannot show**"):
        st.markdown(V4_LIMITS)
    names = {"restricted": "Restricted", "open": "Accessible: open weights", "api": "Accessible: non-US service"}
    records = shown.assign(access=shown["access"].map(names), release_date=shown["release_date"].dt.date)
    records = records[["model", "release_date", "organization", "country", "route", "access", "eci", "eci_ci_low",
                       "eci_ci_high"]].rename(columns={
        "model": "Model (Epoch name)", "release_date": "Release date", "organization": "Developer",
        "country": "Developer country", "route": "Route", "access": "Group in this view",
        "eci": "Capability (ECI points)", "eci_ci_low": "ECI 90% low", "eci_ci_high": "ECI 90% high"})
    download_records(records, "v4", "view4_capability_gap.csv",
                     "Models drawn as dots in the date range. The lines also count earlier models.")
    footer(["epoch"], "7 Oct 2026 (latest Epoch release date in the file)")


# --------------------------------------------------------------------------- #
# View 5: reported incidents
# --------------------------------------------------------------------------- #
V5_HOW = """
- **Top chart:** AI incidents reported per year in the AI Incident Database, split into incidents involving
  generative AI (purple) and other AI such as face recognition, self-driving cars or recommendation systems (grey).
  The shaded years are the period counted in the lower chart. 2026 runs only to 3 October.
- **Lower chart:** how many incidents in that period name each company as the developer, with the same split. The
  number at the end of a bar is the total. "· China" marks a company based in China.
- **One incident can name several companies,** so the bars add up to more than the number of incidents.
- **Read the counts as exposure, not as risk:** reports follow how widely a product is used and how much English-language
  media covers it, so the most used products appear most often.
"""

V5_LIMITS = """
- **Descriptive only, not causal:** a higher count does not show that a developer's models are less safe, and the
  page gives no legal advice.
- **"Developer" is as alleged by the reporters** and is not proven. Severity and actual harm are not compared.
- **English-language media:** incidents in other languages, including Chinese, are under-counted, so companies based
  in China appear rarely and cannot be compared with US companies.
- **Usage is not measured:** there is no count of users, so incidents cannot be expressed per user.
- **2026 is a partial year** (export of 12 Oct 2026, latest incident 3 Oct 2026), and recent incidents are added as
  reports appear.
- **The transparency half of user story 3** (how openly each developer builds its models) is not shown. The Stanford
  Foundation Model Transparency Index covers only 13 companies, 9 of them in the Epoch list, and dates from December
  2025, so it is kept as a note rather than a chart.
"""

V5_DECISION = """
**Visual task:** Show how often each developer the bank might rely on appears in reported AI incidents, and how the
number of reports has changed, so the architect can tell the committee what is known and what is not.

**Form chosen:** A stacked column chart by year (Visual Vocabulary: *change over time*) above a sorted bar chart by
developer (*ranking*), both split into generative and other AI with the same two colours. The year chart gives the
context (reports have grown fast since 2023), and the bar chart answers the question for the chosen period.

**Alternatives rejected:**

1. **Transparency against capability with incidents as bubble size (the first draft).** Only 9 developers appear in
   all three sources, the transparency scores date from December 2025 while capability runs to October 2026, and
   the three measures are unrelated. The chart invited readers to see a relation that 9 points cannot support.
2. **One line per developer per year (shown small below).** With 16 companies and small yearly counts, the lines
   cross and jump, and the noise hides the main point that a few widely used products dominate the reports.
3. **A ranking framed as a risk league table.** Counts follow usage and media attention, so calling the top bar the
   riskiest developer would mislead.
4. **A map of incidents.** The export has no location field, and English-language reporting would make any map a
   map of media coverage.
"""


def chart_years(years: pd.DataFrame, from_year: int, kind: str, revision: str) -> go.Figure:
    fig = go.Figure()
    last = int(years["year"].max())
    if kind == cx.INCIDENT_KINDS[0]:
        fig.add_trace(go.Bar(x=years["year"], y=years["other"], marker_color=NON_GENERATIVE,
                             hovertemplate="%{x}: %{y} other AI incidents<extra></extra>"))
    fig.add_trace(go.Bar(x=years["year"], y=years["generative"], marker_color=GENERATIVE,
                         hovertemplate="%{x}: %{y} generative AI incidents<extra></extra>"))
    fig.add_trace(go.Scatter(x=years["year"], y=years["total"], mode="text", text=years["total"],
                             textposition="top center", textfont={"size": 11, "color": INK}, hoverinfo="skip"))
    fig.add_vrect(x0=from_year - 0.5, x1=last + 0.5, fillcolor=INK, opacity=0.06, line_width=0, layer="below")
    _layout(fig, 380, "", "Incidents reported", revision, {"l": 70, "r": 30, "t": 45, "b": 50})
    fig.update_layout(barmode="stack", bargap=0.25)
    ticks = list(years["year"])
    fig.update_xaxes(tickvals=ticks, ticktext=[f"{y}<br>(to 3 Oct)" if y == last else str(y) for y in ticks],
                     showgrid=False)
    fig.update_yaxes(range=[0, years["total"].max() * 1.12])
    return fig


def chart_developers(table: pd.DataFrame, kind: str, revision: str) -> go.Figure:
    labels = [f"{d} · China" if c else d for d, c in zip(table["developer_clean"], table["is_china_based"])]
    hover = [f"<b>{d}</b><br>{n} incidents ({g} generative AI, {o} other)<br>"
             + (f"{m} models in the Epoch list, best score {b:.1f}" if m else "No model in the Epoch list")
             for d, n, g, o, m, b in zip(table["developer_clean"], table["incidents"], table["generative"],
                                         table["other"], table["epoch_models"], table["best_eci"])]
    fig = go.Figure()
    if kind == cx.INCIDENT_KINDS[0]:
        fig.add_trace(go.Bar(y=labels, x=table["generative"], orientation="h", marker_color=GENERATIVE,
                             hovertext=hover, hoverinfo="text"))
        fig.add_trace(go.Bar(y=labels, x=table["other"], orientation="h", marker_color=NON_GENERATIVE,
                             hovertext=hover, hoverinfo="text"))
    else:
        fig.add_trace(go.Bar(y=labels, x=table["generative"], orientation="h", marker_color=GENERATIVE,
                             hovertext=hover, hoverinfo="text"))
    fig.add_trace(go.Scatter(y=labels, x=table["incidents"], mode="text", text=[f"  {n}" for n in table["incidents"]],
                             textposition="middle right", textfont={"size": 12, "color": INK}, hoverinfo="skip"))
    _layout(fig, 34 * len(table) + 120, "Incidents naming the company as developer", "", revision,
            {"l": 160, "r": 40, "t": 45, "b": 50})
    fig.update_layout(barmode="stack", bargap=0.3)
    fig.update_yaxes(autorange="reversed", showgrid=False, ticks="")
    fig.update_xaxes(range=[0, table["incidents"].max() * 1.1 + 2])
    return fig


def mini_rejected_v5(named: pd.DataFrame, from_year: int, developers: list[str]) -> go.Figure:
    rows = named.loc[(named["year"] >= from_year) & named["developer_clean"].isin(developers)]
    counts = rows.groupby(["developer_clean", "year"])["incident_id"].nunique().unstack(fill_value=0)
    palette = [OPEN, CLOSED, "#009E73", GENERATIVE, "#E69F00", "#56B4E9", OTHER]
    fig = go.Figure([go.Scatter(x=counts.columns, y=counts.loc[d], mode="lines",
                                line={"color": palette[i % len(palette)], "width": 1.5})
                     for i, d in enumerate(counts.index)])
    fig.update_layout(width=560, height=220, margin={"l": 40, "r": 20, "t": 10, "b": 30}, plot_bgcolor="white",
                      font={"family": "Arial, sans-serif", "size": 11, "color": INK}, showlegend=False)
    fig.update_xaxes(gridcolor=GRID, dtick=1)
    fig.update_yaxes(gridcolor=GRID)
    return fig


def render_view5(models: pd.DataFrame, incidents: pd.DataFrame, named: pd.DataFrame, first_year: int = 2015,
                 chart_first_year: int = 2012) -> None:
    """first_year: earliest start year in the slider. chart_first_year: first year of the top chart.
    The defaults are the A3P1 values; a story page may pass later years."""
    st.caption("Unit: number of incidents reported in the AI Incident Database (one incident can name several "
               "companies).")
    companies = sorted(named["developer_clean"].unique())
    years = list(range(first_year, int(incidents["year"].max()) + 1))
    _set_default("v5_kind", cx.INCIDENT_KINDS[0], cx.INCIDENT_KINDS)
    _set_default("v5_from", 2022, years)
    _set_default("v5_developers", companies, companies)
    c1, c2 = st.columns([1, 1.6])
    with c1:
        kind = st.pills("Incidents counted", cx.INCIDENT_KINDS, selection_mode="single", key="v5_kind",
                        help="Generative AI only keeps incidents the database tags as involving generative AI "
                             "(chatbots, image and video generators).") or cx.INCIDENT_KINDS[0]
    with c2:
        from_year = st.select_slider("Count incidents from", years, key="v5_from",
                                     help="Start year of the period counted in the lower chart, to the latest "
                                          "incident (3 Oct 2026).")
    developers = st.multiselect("Developers", companies, key="v5_developers",
                                help="Companies the AI Incident Database names as developers. Remove some to compare "
                                     "a few. An empty selection shows a message.")
    table = cx.per_developer(named, models, kind, from_year, developers)
    if table.empty:
        st.info("No incidents match these filters. Choose at least one developer or an earlier start year.")
        download_records(named.iloc[0:0][["incident_id"]], "v5", "view5_incidents.csv", "")
        footer(["aiid"], f"{cx.AIID_LATEST} (latest incident date), export of {cx.AIID_EXPORT}")
        return
    period = incidents.loc[incidents["year"] >= from_year]
    if kind == cx.INCIDENT_KINDS[1]:
        period = period.loc[period["is_generative_related"]]
    rows = cx.filter_named(named, kind, from_year, developers)
    naming = rows["incident_id"].nunique()
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Incidents {from_year} to 2026", f"{len(period):,}",
              help=f"{int(period['is_generative_related'].sum()):,} involve generative AI.")
    m2.metric("... naming a selected developer", f"{naming:,}",
              help=f"{naming / len(period) * 100:.0f}% of the incidents in the period. Most incidents name other "
                   "companies or deployers." if len(period) else None)
    china = rows.loc[rows["is_china_based"], "incident_id"].nunique()
    m3.metric("... naming a company based in China", f"{china:,}",
              help="Reports come mainly from English-language media, so this count is low by construction.")
    st.caption(f"Selected: {kind}, {from_year} to 3 Oct 2026, {len(table)} of {len(companies)} companies with "
               "at least one incident. " + ZOOM_NOTE)
    items = [(GENERATIVE, "Generative AI", "square")]
    if kind == cx.INCIDENT_KINDS[0]:
        items.append((NON_GENERATIVE, "Other AI (for example face recognition, self-driving)", "square"))
    items.append((INK, "Shaded years: the period counted in the lower chart", "shade"))
    legend_html(items)
    revision = f"v5|{kind}|{from_year}|{','.join(sorted(developers))}"
    st.markdown("**Incidents reported per year** (all companies and deployers)")
    st.plotly_chart(chart_years(cx.per_year(incidents, kind, chart_first_year), from_year, kind, revision), width="content",
                    key="v5_years_chart", config=PLOT_CONFIG)
    st.markdown(f"**Incidents naming each developer, {from_year} to 2026**")
    st.plotly_chart(chart_developers(table, kind, revision), width="content", key="v5_chart", config=PLOT_CONFIG)
    shown = table.assign(best_eci=table["best_eci"].round(1).astype(object).where(table["best_eci"].notna(), ""))[["developer_clean", "incidents", "generative", "other",
                                                               "is_china_based", "epoch_models", "best_eci"]]
    st.dataframe(shown.rename(columns={"developer_clean": "Developer", "incidents": "Incidents",
                                       "generative": "Generative AI", "other": "Other AI",
                                       "is_china_based": "Based in China", "epoch_models": "Models in the Epoch list",
                                       "best_eci": "Best capability score"}), hide_index=True, key="v5_values")
    with st.expander("**How to read these charts**"):
        st.markdown(V5_HOW)
    with st.expander("**Design decision for this view** (task, form, rejected alternatives)"):
        st.markdown(V5_DECISION)
        st.caption("Rejected alternative 2: one line per developer per year, same filters.")
        st.plotly_chart(mini_rejected_v5(named, from_year, developers), width="content", key="v5_rejected_chart",
                        config={"displayModeBar": False})
    with st.expander("**What these charts cannot show**"):
        st.markdown(V5_LIMITS)
    records = rows[["incident_id", "date", "year", "developer_clean", "is_china_based", "is_generative_related",
                    "title"]].sort_values(["date", "incident_id"], ascending=[False, True])
    records = records.rename(columns={"incident_id": "Incident ID", "date": "Incident date", "year": "Year",
                                      "developer_clean": "Developer (as alleged)", "is_china_based": "Based in China",
                                      "is_generative_related": "Generative AI", "title": "Title"})
    download_records(records, "v5", "view5_incidents.csv",
                     "One row per incident and named developer, so an incident naming two companies appears twice.")
    footer(["aiid"], f"{cx.AIID_LATEST} (latest incident date), export of {cx.AIID_EXPORT}")
