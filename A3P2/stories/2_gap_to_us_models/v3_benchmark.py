"""Story 2 V3: compare reported GPQA Diamond accuracy with Epoch's independent evaluations.

Place this module alongside stories/2_gap_to_us_models/page.py and its CSV inside
stories/2_gap_to_us_models/data/. Call render_v3() from the existing page.
"""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent / "notebooks" / "eci_scores" / "processed" / "gpqa_reported_vs_epoch.csv"
SOURCE = "https://epoch.ai/data-insights/self-reported-gpqa"


def load_gpqa(path=DATA_PATH):
    df = pd.read_csv(path)
    numeric = ["developer_reported_pct", "epoch_independent_pct", "epoch_standard_error_pp", "epoch_90ci_halfwidth_pp"]
    for field in numeric:
        df[field] = pd.to_numeric(df[field], errors="raise")
    if df.model.duplicated().any():
        raise ValueError("Duplicate benchmark model names")
    for field in ("developer_reported_pct", "epoch_independent_pct"):
        if not df[field].between(0, 100).all():
            raise ValueError(f"Invalid percentage in {field}")
    df["difference_pp"] = df["developer_reported_pct"] - df["epoch_independent_pct"]
    df["in_epoch_90ci"] = df["difference_pp"].abs() <= df["epoch_90ci_halfwidth_pp"]
    return df


def render_v3():
    st.subheader("V3 · Do independent benchmark checks agree with published scores?")
    st.caption("GPQA Diamond accuracy (%) • Epoch AI comparison published 19 September 2025 • Selected models, not a 2026 census")
    try:
        all_data = load_gpqa()
    except (OSError, ValueError) as exc:
        st.error(f"Benchmark comparison data could not be loaded: {exc}")
        return

    include_third_party = st.checkbox(
        "Include Mistral's endorsed third-party result (not developer self-reported)", value=False,
        key="story2_include_3p"
    )
    available = all_data if include_third_party else all_data[all_data["developer_report_type"] == "developer_report"]
    choices = available["model"].tolist()
    selected = st.multiselect("Models to compare", choices, default=choices, key="story2_gpqa_model_filter")
    display = available[available["model"].isin(selected)].copy().sort_values("epoch_independent_pct")
    if display.empty:
        st.info("Select one or more models to see the independent benchmark comparison.")
        return

    within = int(display["in_epoch_90ci"].sum())
    st.write(
        f"**{within} of {len(display)} selected scores** lie inside Epoch's approximate 90% uncertainty bands "
        "around its independent GPQA estimates. Differences are not necessarily evidence of inaccurate reporting."
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=display["epoch_independent_pct"], y=display["model"], mode="markers",
        name="Epoch independent", marker=dict(size=11, color="#176b87"),
        error_x=dict(type="data", array=display["epoch_90ci_halfwidth_pp"], visible=True, color="#176b87"),
        text=[f"{x:.1f}%" for x in display["epoch_independent_pct"]],
        textposition="bottom center",
        customdata=display[["developer_reported_pct"]].to_numpy(),
        hovertemplate="%{y}<br>Epoch: %{x:.1f}%<br>Reported: %{customdata[0]:.1f}%<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=display["developer_reported_pct"], y=display["model"], mode="markers+text",
        name="Developer reported" if not include_third_party else "Reported / third-party endorsed",
        marker=dict(size=11, color="#d17823", symbol="diamond"),
        text=[f"{x:.1f}%" for x in display["developer_reported_pct"]], textposition="top center",
        hovertemplate="%{y}<br>Reported: %{x:.1f}%<extra></extra>"
    ))
    fig.update_layout(
        title="Published GPQA results versus independent GPQA evaluations",
        xaxis_title="GPQA Diamond accuracy (%)", yaxis_title="Model",
        legend_title="Measurement", height=max(440, 65 * len(display) + 190),
        margin=dict(l=15, r=30, t=60, b=35),
    )
    fig.update_xaxes(range=[max(0, min(display["epoch_independent_pct"].min(), display["developer_reported_pct"].min()) - 10), 100])
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Exact values and differences (percentage points)"):
        st.dataframe(display[["model", "developer_reported_pct", "epoch_independent_pct", "difference_pp", "epoch_90ci_halfwidth_pp", "in_epoch_90ci"]].rename(columns={
            "model": "Model", "developer_reported_pct": "Reported (%)",
            "epoch_independent_pct": "Epoch independent (%)", "difference_pp": "Reported − Epoch (pp)",
            "epoch_90ci_halfwidth_pp": "Epoch approx. 90% half-width (pp)", "in_epoch_90ci": "Reported within band"
        }), hide_index=True)
    st.markdown(
        "**Interpretation for the risk committee:** The selected developer-reported GPQA values are broadly "
        "consistent with independent Epoch measurements on this single benchmark. This supports cross-checking "
        "claims before shortlisting models, but does not prove safety, price, local availability, licence rights, "
        "or performance on banking tasks. The V2 capability score and V3 GPQA percentage are different scales "
        "and must not be directly subtracted or compared."
    )
    st.caption(
        "Limitations: Epoch's curated 2025 sample covers seven developer-reported scores; an optional eighth is "
        "third-party endorsed rather than developer-reported. Uncertainty bands approximate ±1.645 × Epoch's "
        "reported standard error. Prompt settings, test versions and model selection may differ. No 2026 "
        "independent cross-check is established by this dataset. "
        "Source: " + SOURCE + " • Published 19 Sep 2025 • Snapshot transcribed 14 Nov 2026."
    )
