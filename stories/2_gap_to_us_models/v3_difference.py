"""Story 2, View 3 (alternative, the proposal chart V3): do developer-reported GPQA scores agree with Epoch's independent scores?

Reads data/gpqa_reported_vs_epoch.csv (the eight rows transcribed from Epoch AI's article of 19 September 2025)
and data/model_capability.csv (to give each model the same access group as View 1). Place this module next to
page.py and call render_v3_difference() from the page.

The chart draws one dot per model: the developer-reported score minus Epoch's independent score, in percentage
points. The grey band is Epoch's approximate 90% band around its own score. The one model without a developer
report (Mistral Large 2) is not plotted and is explained in a note under the chart.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import epoch_models
from src.context import access_group
from src.selection import view_header
from src.views_context import download_records
from src.views import GRID, INK, MUTED, ROUTE_COLOURS

HERE = Path(__file__).resolve().parent
GPQA_PATH = HERE / "data" / "gpqa_reported_vs_epoch.csv"
CAPABILITY_PATH = HERE / "data" / "model_capability.csv"
SOURCE = "https://epoch.ai/data-insights/self-reported-gpqa"
ARTICLE = "AI developers accurately report GPQA Diamond scores for recent models"

# Name of each GPQA model in data/model_capability.csv, used only to apply the access rule of View 1.
CAPABILITY_NAME = {
    "GPT-5": "GPT-5",
    "Opus 4.1": "Claude Opus 4.1",
    "DeepSeek R1": "DeepSeek-R1",
    "Llama 4 Maverick": "Llama 4 Maverick",
    "Grok 4": "Grok 4",
    "Gemini 2.5 Pro": "Gemini 2.5 Pro (Jun 2025)",
    "Qwen 3": "Qwen3-235B-A22B",
    "Mistral Large 2407": "Mistral Large 2 (Jul 2024)",
}
GROUPS = ["restricted", "accessible"]
GROUP_NAME = {
    "restricted": "Restricted (US developer, closed weights)",
    "accessible": "Accessible (open weights or non-US service)",
}
GROUP_COLOUR = {"restricted": ROUTE_COLOURS["Closed weights"], "accessible": ROUTE_COLOURS["Open weights"]}
BAND_COLOUR = "#dfe3e8"
ROW_HEIGHT = 64
BAND_HALF = 0.24  # half the height of a band, in rows


# --- Data ---------------------------------------------------------------------------------

def _signed(value: float) -> str:
    """Signed number with a true minus sign, one decimal."""
    return f"{value:+.1f}".replace("-", "−")


@st.cache_data(show_spinner=False)
def load_gpqa(path: str = str(GPQA_PATH), capability_path: str = str(CAPABILITY_PATH)) -> pd.DataFrame:
    """All eight rows with the difference, the band test and the access group of View 1."""
    df = pd.read_csv(path)
    for field in ("developer_reported_pct", "epoch_independent_pct", "epoch_standard_error_pp",
                  "epoch_90ci_halfwidth_pp"):
        df[field] = pd.to_numeric(df[field], errors="raise")
        if df[field].isna().any():
            raise ValueError(f"Missing value in {field}")
    if df["model"].duplicated().any():
        raise ValueError("Duplicate model names in the GPQA comparison")
    for field in ("developer_reported_pct", "epoch_independent_pct"):
        if not df[field].between(0, 100).all():
            raise ValueError(f"Invalid percentage in {field}")
    unknown = set(df["model"]) - set(CAPABILITY_NAME)
    if unknown:
        raise ValueError(f"No capability-file name for: {sorted(unknown)}")

    capability = epoch_models.load_epoch_models(capability_path)
    capability = capability.assign(group=access_group(capability)).set_index("model")["group"]
    names = df["model"].map(CAPABILITY_NAME)
    if not names.isin(capability.index).all() or capability.index.duplicated().any():
        raise ValueError("A GPQA model is missing or duplicated in the capability file")
    group = names.map(capability).map({"restricted": "restricted", "open": "accessible", "api": "accessible"})
    if group.isna().any():
        raise ValueError("A GPQA model has no access group")
    out = df.assign(access_group=group.to_numpy())
    out["difference_pp"] = out["developer_reported_pct"] - out["epoch_independent_pct"]
    out["in_band"] = out["difference_pp"].abs() <= out["epoch_90ci_halfwidth_pp"]
    return out


def split_rows(all_rows: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Developer-reported rows in plotting order (restricted first, largest difference first) and the others."""
    reported = all_rows[all_rows["developer_report_type"] == "developer_report"].copy()
    reported["order"] = reported["access_group"].map({g: i for i, g in enumerate(GROUPS)})
    reported = reported.sort_values(["order", "difference_pp"], ascending=[True, False]).reset_index(drop=True)
    return reported, all_rows[all_rows["developer_report_type"] != "developer_report"]


def records_table(df: pd.DataFrame) -> pd.DataFrame:
    """Rows behind the chart (the plotted models only), named for the reader and for the CSV download."""
    table = df[["model", "access_group", "developer_reported_pct", "epoch_independent_pct", "difference_pp",
                "epoch_90ci_halfwidth_pp", "in_band", "developer_source"]].copy()
    table["difference_pp"] = table["difference_pp"].round(1)
    table["access_group"] = table["access_group"].str.capitalize()
    return table.rename(columns={
        "model": "Model", "access_group": "Access group", "developer_reported_pct": "Reported (%)",
        "epoch_independent_pct": "Epoch (%)", "difference_pp": "Reported − Epoch (percentage points)",
        "epoch_90ci_halfwidth_pp": "Epoch band ± (percentage points)", "in_band": "Inside band",
        "developer_source": "Developer source"}).reset_index(drop=True)


# --- Text ---------------------------------------------------------------------------------

def summary_text(df: pd.DataFrame) -> str:
    n, within = len(df), int(df["in_band"].sum())
    above, below = int((df["difference_pp"] > 0).sum()), int((df["difference_pp"] < 0).sum())
    text = (f"**{within} of {n} reported scores lie inside Epoch's approximate 90% band.** "
            f"{above} {'is' if above == 1 else 'are'} above Epoch's score and {below} "
            f"{'is' if below == 1 else 'are'} below it. ")
    parts = []
    for group in GROUPS:
        part = df[df["access_group"] == group]
        if part.empty:
            continue
        parts.append(f"the {len(part)} {group} models range from {_signed(part['difference_pp'].min())} "
                     f"to {_signed(part['difference_pp'].max())} percentage points")
    if parts:
        text += "In the groups of View 1, " + " and ".join(parts) + ". "
    restricted = df[df["access_group"] == "restricted"]
    if len(restricted) and (restricted["difference_pp"] > 0).all():
        text += "Every restricted model reported a score above Epoch's. "
    counts = " and ".join(str(int((df["access_group"] == g).sum())) for g in GROUPS)
    text += (f"Groups of {counts} models are too small to test whether restricted developers report higher "
             "scores than accessible ones.")
    return text


def answer_sentence(df: pd.DataFrame) -> str:
    """One or two plain sentences on the plotted models. Empty when no model is plotted."""
    if df.empty:
        return ""
    top, low = df.loc[df["difference_pp"].idxmax()], df.loc[df["difference_pp"].idxmin()]
    text = (f"Across the {len(df)} plotted models, the median difference between the reported score and Epoch's score is "
            f"{_signed(float(df['difference_pp'].median()))} percentage points. ")
    if len(df) > 1 and top["model"] != low["model"]:
        text += (f"The largest positive difference is {_signed(float(top['difference_pp']))} percentage points for {top['model']} "
                 f"and the largest negative difference is {_signed(float(low['difference_pp']))} percentage points for {low['model']}.")
    else:
        text += f"The largest difference is {_signed(float(top['difference_pp']))} percentage points for {top['model']}."
    return text


def based_on_text() -> str:
    return (f"**Based on** the Epoch AI article “{ARTICLE}” ([Epoch AI, 2025]({SOURCE})). "
            "Epoch plots the two scores of each model next to each other. This view is a redesign as a diverging "
            "chart that shows only the gap between them, and it adds the access groups of View 1.")


def message_text(df: pd.DataFrame) -> str:
    n, within = len(df), int(df["in_band"].sum())
    inside = f"every one of the {n}" if within == n else f"{within} of the {n}"
    return ("**Message of this chart:** The gap between the GPQA score a developer reports and the score Epoch "
            f"measures itself is small, and {inside} lies within Epoch's measurement error. Published scores can "
            "therefore serve as a first screen for shortlisting. The chart does not show whether restricted and "
            "accessible developers report differently.")


def mistral_note(others: pd.DataFrame) -> str:
    if others.empty:
        return ""
    row = others.iloc[0]
    return (
        f"**{row['model'].rsplit(' ', 1)[0]} is not plotted.** The developer did not report a GPQA Diamond score. "
        f"Epoch lists {row['developer_reported_pct']:.1f}% from a third-party evaluation that the developer's own "
        f"benchmark page endorses, against {row['epoch_independent_pct']:.1f}% from Epoch "
        f"({_signed(row['difference_pp'])} percentage points). The row is labelled {row['model'].rsplit(' ', 1)[1]}, while Epoch's "
        f"run used {str(row['reference_model']).rsplit('-', 1)[1]}. It is unclear which of the "
        "two numbers belongs to which source, so this row is kept out of the chart and out of the counts above."
    )


# --- Chart --------------------------------------------------------------------------------

def build_figure(df: pd.DataFrame) -> go.Figure:
    n = len(df)
    reach = float(df["epoch_90ci_halfwidth_pp"].max()) + 0.8
    fig = go.Figure()
    for i, row in df.iterrows():
        half = float(row["epoch_90ci_halfwidth_pp"])
        fig.add_shape(type="rect", x0=-half, x1=half, y0=i - BAND_HALF, y1=i + BAND_HALF, xref="x", yref="y",
                      fillcolor=BAND_COLOUR, line={"width": 0}, layer="below")
    n_restricted = int((df["access_group"] == "restricted").sum())
    if 0 < n_restricted < n:
        fig.add_shape(type="line", x0=-reach, x1=reach, y0=n_restricted - 0.5, y1=n_restricted - 0.5,
                      xref="x", yref="y", line={"color": GRID, "width": 1, "dash": "dot"}, layer="below")
    fig.add_shape(type="line", x0=0, x1=0, y0=-0.6, y1=n - 0.4, xref="x", yref="y",
                  line={"color": INK, "width": 1.5}, layer="below")
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers", name="Epoch's approximate 90% band",
        marker={"size": 14, "symbol": "square", "color": BAND_COLOUR}, hoverinfo="skip"))
    for group in GROUPS:
        part = df[df["access_group"] == group]
        if part.empty:
            continue
        fig.add_trace(go.Scatter(
            x=part["difference_pp"], y=part["model"], mode="markers+text", name=GROUP_NAME[group],
            marker={"size": 14, "color": GROUP_COLOUR[group], "line": {"color": "white", "width": 1.5}},
            text=[_signed(v) for v in part["difference_pp"]], textposition="top center",
            textfont={"size": 12, "color": INK},
            customdata=[[f"{r:.1f}", f"{e:.1f}", _signed(d), f"{h:.1f}"] for r, e, d, h in zip(
                part["developer_reported_pct"], part["epoch_independent_pct"], part["difference_pp"],
                part["epoch_90ci_halfwidth_pp"])],
            hovertemplate=("<b>%{y}</b><br>Reported: %{customdata[0]}%<br>Epoch: %{customdata[1]}%<br>"
                           "Difference: %{customdata[2]} percentage points<br>Epoch band: \u00b1%{customdata[3]} percentage points"
                           f"<br>{GROUP_NAME[group]}<extra></extra>"),
        ))
    fig.update_layout(
        height=ROW_HEIGHT * n + 230, plot_bgcolor="white", paper_bgcolor="white",
        margin={"l": 10, "r": 20, "t": 50, "b": 110},
        font={"family": "Arial, sans-serif", "size": 12, "color": INK},
        hoverlabel={"bgcolor": "white", "font": {"size": 12, "color": INK}},
        legend={"orientation": "h", "x": 0.5, "xanchor": "center", "y": -0.22, "yanchor": "top"},
        xaxis={"range": [-reach, reach], "dtick": 1, "title": {"text": "Reported score minus Epoch's independent "
                                                              "score (percentage points)"},
               "zeroline": False, "gridcolor": GRID, "ticks": "outside"},
        yaxis={"type": "category", "autorange": "reversed", "categoryorder": "array", "categoryarray": df["model"].tolist(),
               "title": {"text": "Model"}, "showgrid": False, "automargin": True},
    )
    fig.update_xaxes(tickvals=list(range(-int(reach), int(reach) + 1)),
                     ticktext=[("0" if v == 0 else _signed(v)[:-2]) for v in range(-int(reach), int(reach) + 1)])
    fig.add_annotation(x=-0.15, y=1.0, xref="x", yref="paper", yshift=26, text="← Reported lower than Epoch",
                       showarrow=False, xanchor="right", font={"size": 12, "color": MUTED})
    fig.add_annotation(x=0.15, y=1.0, xref="x", yref="paper", yshift=26, text="Reported higher than Epoch →",
                       showarrow=False, xanchor="left", font={"size": 12, "color": MUTED})
    return fig


# --- Page ---------------------------------------------------------------------------------

def render_v3_difference() -> None:
    if not view_header("3. Do independent benchmark checks agree with published scores?", "show_2_view3", "view-3"):
        return
    try:
        all_rows = load_gpqa()
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"The benchmark comparison could not be loaded: {exc}")
        return
    df, others = split_rows(all_rows)
    st.markdown(based_on_text())
    st.markdown(message_text(df))
    st.caption(
        f"GPQA Diamond · {len(df)} models with a developer-reported score · a small selection of models "
        "and not a 2026 census"
    )
    st.markdown(summary_text(df))
    st.plotly_chart(build_figure(df), use_container_width=True, config={"displaylogo": False, "toImageButtonOptions": {"format": "png", "scale": 3}})
    sentence = answer_sentence(df)
    if sentence:
        st.markdown(sentence)
    note = mistral_note(others)
    if note:
        st.markdown(note)
    with st.expander("**How to read this chart**"):
        st.markdown(
            "- **One row per model:** the dot is the developer-reported score minus the score Epoch measured "
            "itself, in percentage points.\n"
            "- **Zero line:** the developer and Epoch agree exactly. A dot to the right means the developer "
            "reported the higher score.\n"
            "- **Grey band:** Epoch's approximate 90% band around its own score (1.645 times its standard error). "
            "A dot inside the band is a difference that Epoch's own measurement error can explain.\n"
            "- **Dot colour:** the access group of View 1. Restricted means a US developer without downloadable "
            "weights. Accessible means open weights, or a service from a developer outside the US. The group is "
            "a rule and not a measurement."
        )
    with st.expander("**Design decision for this view** (visual task and form chosen)"):
        st.markdown(
            "**Visual task:** Show whether the GPQA Diamond scores that developers report agree with the scores Epoch "
            "measures itself, and whether the gap differs for restricted and accessible models.\n\n"
            "**Form chosen:** A dot plot of differences (Visual Vocabulary: *deviation*) against a zero line, with "
            "Epoch's approximate 90% band in grey. Each dot is one model, coloured by access group as in View 1, so the "
            "size and the direction of each difference are read from one baseline."
        )
    with st.expander("**What this chart cannot show**"):
        st.markdown(
            "- **Few models:** Epoch chose these models. The groups hold "
            + " and ".join(str(int((df['access_group'] == g).sum())) for g in GROUPS)
            + " models, so the chart describes them and cannot test a difference between the groups.\n"
            "- **One benchmark:** GPQA Diamond only. Agreement here does not carry over to other benchmarks.\n"
            "- **Different settings:** prompts, test versions and model versions can differ between the developer "
            "and Epoch.\n"
            "- **Age:** the comparison was published on 19 September 2025. No 2026 cross-check is shown.\n"
            "- **No other source:** the Epoch Benchmarking Hub holds no model with both an Epoch run and a "
            "developer-reported score on the same benchmark, so the comparison cannot be extended from it.\n"
            "- **Other questions:** agreement says nothing about price, licence, safety or banking tasks. The "
            "capability index of View 1 and a GPQA percentage are different scales and must not be subtracted "
            "from each other."
        )
    download_records(records_table(df), "story2_v3d_records", "view_v3_gpqa_difference.csv",
                     "One row per plotted model. Scores are in percent and the difference is in percentage points. "
                     "Mistral Large is not included.")
    st.caption(
        "The grey band is Epoch's approximate 90% band, 1.645 times its reported standard error. "
        "Differences and access groups are calculated by the group."
    )
