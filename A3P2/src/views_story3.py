"""Views 1 and 2 of Story 3 of the Model Choice Explorer.

View A shows what each developer discloses about how it builds its models (Stanford FMTI, December 2025).
View B shows how often the eleven developers appear in model incidents of the AI Incident Database, grouped by
MIT risk domain, with the FMTI score and the Epoch model count beside each developer.
The style follows the other views of the Model Choice Explorer (Plotly, white ground, Okabe-Ito colours).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.views import CHART_W, GRID, INK, MUTED, PLOT_CONFIG, SOURCES
from src.views_context import ZOOM_NOTE, _layout, _set_default, download_records

# Sources of this story only. A copy, so that the source list of the other stories is not changed.
SOURCES_3 = {k: SOURCES[k] for k in ("aiid", "epoch")}
SOURCES_3["fmti"] = (
    "Foundation Model Transparency Index, December 2025 (scores file Dec2025_scores.csv)",
    "Stanford Center for Research on Foundation Models", "https://crfm.stanford.edu/fmti/December-2025",
    "edition of December 2025, flagship models assessed in May 2025, CC BY (scores file in github.com/stanford-crfm/fmti)")
SOURCES_3["mit"] = ("Risk domains and subdomains of the AI Risk Repository", "MIT", "https://airisk.mit.edu/",
                    "labels as carried in the AI Incident Database export of 12 Oct 2026")


def footer_3(source_keys: list[str], latest: str) -> None:
    """Same layout as footer() in src/views.py, with the sources of this story."""
    lines = "\n".join(f"- **{SOURCES_3[k][0]}**, {SOURCES_3[k][1]}, [{SOURCES_3[k][2]}]({SOURCES_3[k][2]}), {SOURCES_3[k][3]}"
                      for k in source_keys)
    st.caption(f"Sources:\n\n{lines}")
    st.caption(f"Latest observation: {latest}")



DOMAIN_COLOURS = {"Upstream": "#0072B2", "Model": "#E69F00", "Downstream": "#009E73"}
GROUP_ORDER = ["Wrong output or failure", "Data and security", "Misuse by others", "Harm to users or society"]
GROUP_COLOURS = {"Wrong output or failure": "#0072B2", "Data and security": "#009E73", "Misuse by others": "#D55E00",
                 "Harm to users or society": "#CC79A7"}
ELEVEN = ["OpenAI", "Anthropic", "Google", "Meta", "xAI", "Mistral AI", "DeepSeek", "Alibaba", "Z.ai (Zhipu)",
          "Moonshot", "MiniMax"]
UNSCORED = [("MiniMax", "China"), ("Moonshot", "China"), ("Z.ai", "China")]  # one of the 11 developers, not scored by FMTI
FMTI_NAME = {"Mistral AI": "Mistral", "Z.ai (Zhipu)": "Z.ai", "Moonshot": "Moonshot", "MiniMax": "MiniMax"}
EPOCH_ORG = {"OpenAI": ["OpenAI"], "Anthropic": ["Anthropic"], "Google": ["Google DeepMind", "Google"],
             "Meta": ["Meta AI"], "xAI": ["xAI"], "Mistral AI": ["Mistral AI"], "DeepSeek": ["DeepSeek"],
             "Alibaba": ["Alibaba"], "Z.ai (Zhipu)": ["Z.ai (Zhipu AI)"], "Moonshot": ["Moonshot"],
             "MiniMax": ["MiniMax"]}
US_DEVS = ["OpenAI", "Anthropic", "Google", "Meta", "xAI"]
EU_DEVS = ["Mistral AI"]
CN_DEVS = ["DeepSeek", "Alibaba", "Z.ai (Zhipu)", "Moonshot", "MiniMax"]
HERE = Path(__file__).resolve().parents[1] / "stories" / "3_reported_incidents" / "data"
REGIONS = ["All regions", "United States", "China", "Europe and Israel"]
REGION_PICK = ["United States", "China", "Europe and Israel"]
REGION_RANK = {r: i for i, r in enumerate(REGION_PICK)}
A_REGION_RANK = {"United States": 0, "Europe and Israel": 1, "China": 2}  # row order of 8: China is the last group
DOMAINS = ["Upstream", "Model", "Downstream"]
DEV_REGION = {**{d: "United States" for d in US_DEVS}, **{d: "Europe and Israel" for d in EU_DEVS},
              **{d: "China" for d in CN_DEVS}}
SUBDOMAIN_ORDER = ["Data Acquisition", "Data Processing", "Data Properties", "Compute", "Methods",
                   "Other Resources", "Model Information", "Model Access", "Capabilities", "Risks",
                   "Model Mitigations", "Release", "Usage Data", "Impact", "Post-deployment Monitoring",
                   "Model Behavior Policy", "Downstream Mitigations", "Acceptable Use Policy", "Accountability"]


@st.cache_data(show_spinner=False)
def load_fmti():
    scores = pd.read_csv(HERE / "fmti_dec2025_scores_tidy.csv")
    companies = pd.read_csv(HERE / "fmti_companies.csv")
    return scores, companies


@st.cache_data(show_spinner=False)
def load_incidents():
    return pd.read_csv(HERE / "aiid_model_incidents_by_developer.csv")


def _legend_3(items: list[tuple[str, str, str]]) -> None:
    """Legend line above a chart, as views_context.legend_html with two more marks (diamond and triangle)."""
    marks = {
        "dot": "width:11px;height:11px;border-radius:50%;background:{c}",
        "diamond": "width:9px;height:9px;transform:rotate(45deg);background:{c};margin-left:1px",
        "triangle": "width:0;height:0;border-left:6px solid transparent;border-right:6px solid transparent;"
                    "border-bottom:10px solid {c}",
    }
    spans = " ".join(f"<span style='white-space:nowrap;margin-right:18px'><span style='display:inline-block;"
                     f"{marks[m].format(c=c)};margin-right:6px;vertical-align:-1px'></span>{label}</span>"
                     for c, label, m in items)
    st.markdown(f"<div style='font-size:0.9rem;color:{MUTED}'>{spans}</div>", unsafe_allow_html=True)


def _label(name: str, in_list: bool) -> str:
    """Row name: black and bold for one of the 11 developers, light grey for any other company."""
    return f'<b><span style="color:#111827">{name}</span></b>' if in_list else f'<span style="color:#8a929b">{name}</span>'


def _region_groups(regions: list[str]) -> list[tuple[str, int, int]]:
    """Consecutive runs of the same region as (region, first row, last row)."""
    out, start = [], 0
    for i in range(1, len(regions) + 1):
        if i == len(regions) or regions[i] != regions[start]:
            out.append((regions[start], start, i - 1))
            start = i
    return out


def _add_region_groups(fig: go.Figure, groups: list[tuple[str, int, int]], plot_w: int, left: int, yref: str,
                       row=None) -> None:
    """Region name left of the row names and a dark line between two regions."""
    for k, (name, a, b) in enumerate(groups):
        fig.add_annotation(xref="paper", yref=yref, x=-(left - 20) / plot_w, y=(a + b) / 2, text=f"<b>{name}</b>",
                           showarrow=False, xanchor="left", font={"size": 12, "color": MUTED})
        if k:
            fig.add_shape(type="line", xref="paper", yref=yref, x0=-(left - 10) / plot_w, x1=1, y0=a - 0.5, y1=a - 0.5,
                          line={"color": "#6b7280", "width": 1.5})


# --------------------------------------------------------------------------- #
# View A: FMTI
# --------------------------------------------------------------------------- #
A_HOW = """
- **Cells:** each cell is one company and one subdomain.
  - *Text:* the number of indicators the company discloses, over the number of indicators in the subdomain.
  - *Colour:* the same share, from light (little disclosed) to dark blue (all disclosed).
  - *Light cell:* the information is not public. It does not mean that the company handles the topic badly.
- **Columns:** the 19 subdomains follow the order of the FMTI paper and are grouped by the coloured bars underneath.
  - *Upstream* (34 indicators): what goes into a model, such as data, labour and compute.
  - *Model* (30 indicators): the model itself and its release.
  - *Downstream* (36 indicators): use after release, such as monitoring and accountability.
  - *Example:* averaged over the 13 companies, Data Properties is the lightest column (15% of its indicators
    disclosed) and Downstream Mitigations the darkest (75%).
- **Rows:** one row per company, grouped by headquarters region as given in Table 1 of the FMTI paper and sorted A to Z
  inside each group, so the order is not a ranking.
  - *Bold names:* the 11 developers.
  - *Example:* in Data Acquisition IBM discloses 12 of 12 indicators, Meta 4 of 12 and OpenAI 1 of 12. One company can
    be open on one topic and closed on another, which a single total score hides.
- **Hover:** a tick marks each indicator of the subdomain that the company discloses, and a cross marks each one it
  does not.
  - *All indicators:* the table under "Values behind the chart" lists the 100 indicators, with the number of the 13
    companies that disclose each.
- **Total score:** the official score out of 100 is in the same table.
- **Grey rows:** Z.ai, Moonshot and MiniMax are among the 11 developers, but FMTI did not score them.
  - *Meaning:* a grey row is a gap in the evidence. It does not show that the developer is open or closed.
  - *Position:* the rows close the China group, which is the last group of the chart. They are shown whenever China is chosen, because the three developers are based in China.
"""
A_LIMITS = """
- **Disclosure, not practice:** an indicator counts when the company publishes the item.
  - *Not measured:* how well the company does it. A company that lists its data sources in full can still use poor data.
- **One model per company:** the assessed model is the flagship of May 2025.
  - *Examples:* o3, Claude 4, Gemini 2.5, DeepSeek-R1 and Qwen 3.
  - *Consequence:* newer models are not covered, so a company that has become more open since then still shows its
    earlier picture.
- **Different evidence:** the researchers used two kinds of evidence.
  - *Seven companies* submitted their own reports: AI21 Labs, Amazon, Google, IBM, Meta, OpenAI and Writer.
  - *Six companies* did not: Alibaba, Anthropic, DeepSeek, Midjourney, Mistral and xAI. The researchers collected
    public information about them, partly with an AI agent that they checked by hand.
  - *Consequence:* a zero for these six can mean that the item was not found, so zeros of the two groups are not fully
    comparable.
- **Thirteen companies:** only these have a score.
  - *Consequence:* the comparison covers eight of the 11 developers. Nothing here says how Z.ai,
    Moonshot or MiniMax compare.
- **Edition of December 2025:** no later edition was found.
  - *Domains:* the scores file has no domain column, so domain and subdomain follow the indicator order in the paper.
"""


def render_fmti() -> None:
    scores, companies = load_fmti()
    companies = companies.assign(scored=True)
    sub_dom = scores.drop_duplicates("Subdomain").set_index("Subdomain")["Domain"].to_dict()
    st.caption("Unit: indicators disclosed, out of 100. One row per company, flagship model of May 2025.")
    _set_default("a_region", REGION_PICK, REGION_PICK)
    _set_default("a_domain", DOMAINS, DOMAINS)
    c1, c2 = st.columns([1.3, 1.3])
    with c1:
        regions = st.pills("Headquarters region", REGION_PICK, selection_mode="multi", key="a_region",
                           help="Headquarters as given in Table 1 of the FMTI paper. Choose one or several. "
                                "Nothing chosen shows all regions.") or REGION_PICK
    with c2:
        domains = st.pills("Domain", DOMAINS, selection_mode="multi", key="a_domain",
                           help="Upstream: before training. Model: the model and its release. Downstream: use after "
                                "release. Choose one or several. Nothing chosen shows all domains.") or DOMAINS
    pool = companies.loc[companies["region"].isin(regions)].copy()
    pool["r"] = pool["region"].map(A_REGION_RANK)
    pool = pool.sort_values(["r", "company"], key=lambda c: c if pd.api.types.is_numeric_dtype(c) else c.str.lower())
    names = list(pool["company"])
    if st.session_state.get("a_pool_sig") != tuple(names):
        st.session_state["a_companies"], st.session_state["a_pool_sig"] = list(names), tuple(names)
    chosen = st.multiselect("Companies", names, key="a_companies",
                            help="The thirteen companies scored by FMTI. Remove a company with its cross.")
    dom_subs = [x for x in SUBDOMAIN_ORDER if sub_dom[x] in domains]
    if st.session_state.get("a_subs_sig") != tuple(dom_subs):
        st.session_state["a_subs"], st.session_state["a_subs_sig"] = list(dom_subs), tuple(dom_subs)
    subs = st.multiselect("Subdomains", dom_subs, key="a_subs",
                          help="The columns of the heatmap, 19 in total. Remove a subdomain with its cross to take its "
                               "column out of the chart.")
    shown = pool.loc[pool["company"].isin(chosen)]
    if shown.empty or not subs:
        st.info("Choose at least one company and one subdomain.")
        return
    s = scores.loc[scores["Developer"].isin(shown["company"]) & scores["Subdomain"].isin(subs)]
    dom = scores.groupby(["Developer", "Domain"])["Disclosed"].sum().unstack(fill_value=0)
    dom["Total"] = dom.sum(axis=1)
    table = shown.merge(dom, left_on="company", right_index=True, how="left").reset_index(drop=True)
    scored_ours = int(table.loc[table["in_bank_list"] == "yes", "company"].nunique())
    m1, m2, _ = st.columns(3)
    m1.metric("Companies shown", f"{len(table)}")
    off_list = sorted(companies.loc[companies["in_bank_list"] == "no", "company"])
    m2.metric("... of the 11 developers", f"{scored_ours}",
              help="**Scored:** eight of the 11 developers are scored by FMTI.\n\n"
                   "**Not scored:** Z.ai, Moonshot and MiniMax. They appear as grey rows.\n\n"
                   f"**Scored but not one of the 11 developers:** {', '.join(off_list[:-1])} and {off_list[-1]}.")
    grey = [u for u in UNSCORED if u[1] in regions]
    st.caption(f"{len(subs)} of 19 subdomains shown. " + ZOOM_NOTE)
    st.markdown("**Share of indicators disclosed, by company and subdomain**")
    _names_key(off_list, [n for n, _ in grey])
    st.plotly_chart(chart_heat(table, s, sub_dom, grey), width="content", key="a_heat", config=PLOT_CONFIG)
    values = table[["company", "headquarters", "Upstream", "Model", "Downstream", "Total",
                    "self_submitted_report", "flagship_model"]].copy()
    with st.expander("**How to read this chart**"):
        st.markdown(A_HOW)
    with st.expander("**What this chart cannot show**"):
        st.markdown(A_LIMITS)
    with st.expander("**Values behind the chart** (the companies shown, with their original scores)"):
        st.caption("Disclosed indicators per domain and in total. The total counts all 100 indicators, whichever "
                   "subdomains are shown in the chart.")
        st.dataframe(values.rename(columns={"company": "Company", "headquarters": "Headquarters",
                                            "Total": "Total (of 100)", "self_submitted_report": "Own report submitted",
                                            "flagship_model": "Flagship model assessed"}),
                     hide_index=True, key="a_values")
        st.markdown("**The 100 indicators**")
        st.caption("Each indicator is one yes or no question defined by the FMTI researchers. The last column is the number "
                   "of the 13 companies that disclose it.")
        ind = (scores.groupby(["Domain", "Subdomain", "Indicator"], sort=False)["Disclosed"].sum().reset_index()
               .assign(o=lambda f: f["Domain"].map({d: k for k, d in enumerate(DOMAINS)}),
                       so=lambda f: f["Subdomain"].map({x: k for k, x in enumerate(SUBDOMAIN_ORDER)}))
               .sort_values(["o", "so"], kind="stable").drop(columns=["o", "so"]))
        st.dataframe(ind.rename(columns={"Disclosed": "Companies disclosing (of 13)"}), hide_index=True, key="a_indicators")
    records = s.rename(columns={"Developer": "Company", "Disclosed": "Disclosed (1 yes, 0 no)"})
    download_records(records, "a", "view_fmti_indicators.csv",
                     "One row per company and indicator. The domain and subdomain columns follow the paper's indicator order.")
    footer_3(["fmti"], "edition of December 2025, flagship models assessed in May 2025")


def _names_key(off_list: list[str], unscored: list[str]) -> None:
    """Key of the row names, directly above the heatmap. Each line names the companies it covers."""
    def join(names: list[str]) -> str:
        names = sorted(names, key=str.lower)
        return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    lines = ["<div><b style='color:#111827'>Bold black name:</b> one of the 11 developers, scored by "
             "FMTI.</div>",
             f"<div><span style='color:#8a929b'><b>Light grey name:</b></span> scored by FMTI but not one of the 11 developers "
             f"({join(off_list)}).</div>"]
    if unscored:
        lines.append("<div><span style='display:inline-block;width:26px;height:10px;background:#e5e7eb;margin-right:6px'>"
                     "</span><b>Grey bar:</b> one of the 11 developers, not scored by FMTI "
                     f"({join(unscored)}).</div>")
    st.markdown(f"<div style='font-size:0.9rem;color:{MUTED};line-height:1.6;margin:0.2rem 0 0.4rem 0'>"
                + "".join(lines) + "</div>", unsafe_allow_html=True)


HEAT_L, HEAT_R, HEAT_T, HEAT_B = 250, 20, 20, 215


def chart_heat(table: pd.DataFrame, s: pd.DataFrame, sub_dom: dict, unscored: list[tuple[str, str]] = ()) -> go.Figure:
    subs = [x for x in SUBDOMAIN_ORDER if x in set(s["Subdomain"])]
    agg = s.groupby(["Developer", "Subdomain"])["Disclosed"].agg(["sum", "count"])
    n_per_sub = agg.groupby(level=1)["count"].max()
    by_cell = {k: g for k, g in s.groupby(["Developer", "Subdomain"], sort=False)}
    # one entry per row: label, region, values, cell text, hover text, and the name when the row is a grey gap
    rows = []
    for c, i, r in zip(table["company"], table["in_bank_list"], table["region"]):
        rows.append({"label": _label(c, i == "yes"), "region": r, "grey": None,
                     "z": [agg.loc[(c, x), "sum"] / agg.loc[(c, x), "count"] for x in subs],
                     "text": [f"{int(agg.loc[(c, x), 'sum'])}/{int(agg.loc[(c, x), 'count'])}" for x in subs],
                     "detail": [f"<b>{c}</b>, {x} ({sub_dom[x]})<br>Disclosed: <b>{int(agg.loc[(c, x), 'sum'])} of "
                                f"{int(agg.loc[(c, x), 'count'])}</b> indicators<br>"
                                + "<br>".join(("\u2713 " if v else "\u2717 ") + ind
                                              for ind, v in zip(by_cell[(c, x)]["Indicator"], by_cell[(c, x)]["Disclosed"]))
                                for x in subs]})
    for name, hq in unscored:
        rows.append({"label": _label(name, True), "region": hq, "grey": name, "z": [None] * len(subs),
                     "text": [""] * len(subs),
                     "detail": [f"<b>{name}</b><br>Not scored by FMTI<br>The December 2025 edition of the Index does "
                                "not assess this developer."] * len(subs)})
    rows.sort(key=lambda e: A_REGION_RANK[e["region"]])  # stable: scored companies stay ahead of grey rows
    labels = [e["label"] for e in rows]
    fig = go.Figure(go.Heatmap(z=[e["z"] for e in rows], x=subs, y=labels, text=[e["text"] for e in rows],
                               texttemplate="%{text}", zmin=0, zmax=1,
                               colorscale=[[0, "#cde2fb"], [0.35, "#6da7ec"], [0.7, "#2a78d6"], [1, "#0d366b"]],
                               xgap=2, ygap=2, hoverongaps=True, customdata=[e["detail"] for e in rows],
                               hovertemplate="%{customdata}<extra></extra>",
                               colorbar={"title": "Share of indicators<br>disclosed<br> ", "thickness": 12, "len": 0.6, "tickformat": ".0%"}))
    n = len(rows)
    height = 34 * n + HEAT_T + HEAT_B
    plot_w, plot_h = CHART_W - HEAT_L - HEAT_R, height - HEAT_T - HEAT_B
    _layout(fig, height, "", "", f"a-heat|{n}|{len(subs)}", {"l": HEAT_L, "r": HEAT_R, "t": HEAT_T, "b": HEAT_B})
    fig.update_layout(hoverlabel={"align": "left"})  # left-align the hover text
    fig.update_xaxes(tickangle=-45, showgrid=False, side="bottom")
    fig.update_yaxes(autorange="reversed", showgrid=False, ticks="", tickfont={"size": 13})
    for k, e in enumerate(rows):
        if e["grey"]:
            fig.add_shape(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=k - 0.46, y1=k + 0.46,
                          fillcolor="#e5e7eb", line={"width": 0}, layer="below")
            fig.add_annotation(xref="paper", yref="y", x=0.5, y=k, text="Not scored by FMTI", showarrow=False,
                               font={"size": 12, "color": MUTED})
    _add_region_groups(fig, _region_groups([e["region"] for e in rows]), plot_w, HEAT_L, "y")
    # domain bars under the column names, and a white gap between two domains
    doms = [sub_dom[x] for x in subs]
    y_bar = -150 / plot_h
    for d in DOMAINS:
        idx = [k for k, v in enumerate(doms) if v == d]
        if not idx:
            continue
        x0, x1 = idx[0] - 0.45, idx[-1] + 0.45
        fig.add_shape(type="line", xref="x", yref="paper", x0=x0, x1=x1, y0=y_bar, y1=y_bar,
                      line={"color": DOMAIN_COLOURS[d], "width": 7})
        n_ind = int(sum(n_per_sub[subs[k]] for k in idx))
        fig.add_annotation(xref="x", yref="paper", x=(x0 + x1) / 2, y=y_bar - 10 / plot_h, yanchor="top", showarrow=False,
                           text=f"<b>{d}</b> ({n_ind} indicators)", font={"size": 12, "color": INK})
    for k in range(1, len(subs)):
        if doms[k] != doms[k - 1]:
            fig.add_shape(type="line", xref="x", yref="paper", x0=k - 0.5, x1=k - 0.5, y0=0, y1=1, layer="above",
                          line={"color": "white", "width": 6})
    return fig


# --------------------------------------------------------------------------- #
# View B: model incidents on a timeline, by developer, with Epoch model releases
# --------------------------------------------------------------------------- #
B_HOW = """
- **Top strip:** each bar is the number of model incidents reported in a month.
  - *Counting:* an incident that names two developers is counted once.
  - *Colour:* the incident type of each incident in the month.
  - *Number above a bar:* the total of a month with 10 incidents or more, so a busy month can be found before the lanes
    are read.
- **Lanes:** one lane per developer, grouped by headquarters region.
  - *Dot:* one incident on its incident date, coloured by incident type as in the strip above.
  - *Height:* dots on the same date are nudged up or down so that they do not hide each other, so the height inside a
    lane carries no meaning.
- **Incident type:** the MIT risk domains grouped into four types.
  - *Wrong output or failure:* misinformation and AI system failures.
  - *Data and security:* privacy and security.
  - *Misuse by others:* malicious actors and misuse.
  - *Harm to users or society:* discrimination and toxicity, human-computer interaction, and socioeconomic and
    environmental harm.
- **Source of the type:** MIT set the type for 252 of the 318 incidents.
  - *Circle:* the type was set by MIT.
  - *Diamond:* MIT had not classified the incident, so the project group manually assigned the closest MIT risk
    domain. This applies to 66 incidents.
- **Triangles:** a grey triangle at the bottom of a lane is a model release in the Epoch list, with its capability
  index in the hover.
  - *Use:* it shows when the developer shipped a model, so a reader can see whether incidents cluster after releases.
  - *Not tested:* the chart does not test whether releases cause incidents.
- **Selection:** hover on a dot to read the incident.
  - *Click or box:* click a dot or drag a box to list the incidents inside it in the table under the chart.
  - *Zoom:* choose the magnifier in the toolbar first, then drag a box.
- **Empty lane:** no report was found for the developer in the period.
  - *Not evidence of safety:* the database holds only incidents that someone reported.
"""
B_LIMITS = """
- **Reports, not failures:** the AI Incident Database collects incidents that volunteers and editors found in the media.
  - *Consequence:* a count shows what was reported and not how often a model fails.
  - *Example:* OpenAI's 190 incidents follow its wide use and press attention as well as its risk.
- **Small and zero counts:** Moonshot and MiniMax have no incident and Z.ai has one.
  - *Language:* the database draws on English-language media, so incidents in other languages, including Chinese, are
    under-counted.
  - *Consequence:* the five developers based in China cannot be compared with those based in the United States.
- **Model incidents only:** 82 of the 400 incidents that name one of the eleven developers are not counted.
  - *Platform products:* 61 incidents, such as feeds, ads and moderation.
  - *Operations:* 5 incidents, such as hardware or workforce.
  - *Venue only:* 16 incidents that name Meta or Google only as the place where a scam appeared.
  - *Labels:* all 82 are labelled in the group's working files.
- **Developer as recorded:** the database names the developer.
  - *Fault:* naming a developer is not proof of fault.
  - *Dots:* 31 of the 318 incidents name more than one developer, so the chart has 377 dots.
- **Types set by the project group:** 66 incidents had no MIT risk domain, 63 of them from 2025 and 2026, because
  classification lags behind new incidents.
  - *Method:* for these 66 incidents only, the project group assigned the closest MIT risk domain manually, with AI
    assistance in the reading. The reading used the incident title and description and the developer, deployer and
    implicated-system fields, and followed how MIT classified similar incidents.
  - *Other incidents:* the types of the other 252 incidents are MIT's own.
  - *Status:* these types are the group's judgement and not an MIT classification. A second group member has not yet
    checked them.
  - *Consequence:* they make up 48 of the 76 incidents of 2026, so the recent months rest mostly on this judgement.
- **Epoch triangles:** the Epoch list has 277 models and 229 of them belong to the eleven developers.
  - *Consequence:* the triangles are not all the models a developer has released.
- **Export of 12 Oct 2026:** a newer weekly export exists and has not been used.
"""


def render_incidents(epoch: pd.DataFrame) -> None:
    inc = load_incidents()
    st.caption("Unit: number of model incidents reported in the AI Incident Database. One dot is one incident and one "
               "developer.")
    years = list(range(2020, 2027))
    _set_default("b_developers", ELEVEN, ELEVEN)
    _set_default("b_groups", GROUP_ORDER, GROUP_ORDER)
    _set_default("b_epoch", True)
    _set_default("b_region", REGION_PICK, REGION_PICK)
    funnel()
    c1, c2, c3 = st.columns([1.05, 2.4, 0.75])
    with c1:
        from_year, to_year = st.select_slider("Period (years)", years, value=(2020, 2026), key="b_period",
                                              help="First and last year of the timeline. All counts below use this "
                                                   "period.")
    with c2:
        groups = st.multiselect("Incident type", GROUP_ORDER, key="b_groups",
                                help="Groups of the MIT risk domain. For 66 incidents that MIT has not classified, the "
                                     "project group assigned the domain after reading the incident.")

    with c3:
        # A label line like the other two controls, so that the toggle sits level with the slider and the box.
        st.markdown("<div style='font-size:0.875rem;margin-bottom:0.45rem'>Show on the chart</div>",
                    unsafe_allow_html=True,
                    help="**Epoch model releases:** grey triangles at the bottom of each lane, one for each model release "
                         "in the Epoch list.")
        show_epoch = st.toggle("Epoch model releases", key="b_epoch")
    c4, c5 = st.columns([1.05, 3.2])  # c5 starts where the Incident type box above starts
    with c4:
        regions = st.pills("Headquarters region", REGION_PICK, selection_mode="multi", key="b_region",
                           help="United States: OpenAI, Anthropic, Google, Meta, xAI. China: DeepSeek, Alibaba, Z.ai, "
                                "Moonshot, MiniMax. Europe and Israel: Mistral AI. Choose one or several. Nothing "
                                "chosen shows all regions.") or REGION_PICK
    with c5:
        developers = st.multiselect("Developers", ELEVEN, key="b_developers",
                                    help="Choose one or several of the 11 developers. A developer "
                                         "with no incident keeps an empty lane.")
    in_region = [d for d in ELEVEN if DEV_REGION[d] in regions]
    developers = [d for d in developers if d in in_region]
    if not developers or not groups:
        st.info("Choose at least one developer and one group.")
        return
    inc["shown_group"] = inc["group"]
    inc["when"] = pd.to_datetime(inc["date"])
    period = inc.loc[inc["year"].between(from_year, to_year) & inc["developer"].isin(developers)
                     & inc["shown_group"].isin(groups)]
    n_inc = period["incident_id"].nunique()
    m1, m2, m3 = st.columns(3)
    m1.metric("Model incidents counted (all years)", f"{inc['incident_id'].nunique()}",
              help="318 incidents since 2020 after leaving out platform products, operations and mentions as a venue only.")
    m2.metric(f"... shown, {from_year} to {'3 Oct 2026' if to_year == 2026 else to_year}", f"{n_inc}")
    m3.metric("... shown, with a type assigned by the project group",
              f"{period.loc[period['type_source'] == 'Project group', 'incident_id'].nunique()}",
              help="**Source of the type:** MIT has not classified these incidents, mostly from 2025 and 2026. The project "
                   "group assigned the closest MIT risk domain after reading the incident.")
    _legend_3([(GROUP_COLOURS[g], g, "dot") for g in GROUP_ORDER]
              + [("#5b6470", "Diamond: type assigned by the project group", "diamond")]
              + ([("#8c8c8c", "Triangle: model release (Epoch)", "triangle")] if show_epoch else []))
    st.markdown("**Model incidents by month, and one dot per incident for each developer**")
    st.caption("Hover on a dot to read the incident. Click a dot or drag a box to list the incidents inside it below the "
               "chart. To zoom, first choose the magnifier in the chart toolbar (top right), then drag a box. "
               "Double-click resets.")
    fig = chart_timeline(period, developers, epoch if show_epoch else None, from_year, to_year)
    event = st.plotly_chart(fig, width="content", key="b_timeline", on_select="rerun",
                            selection_mode=("points", "box"), config=_CONFIG)
    picked = []
    try:
        picked = [int(next(iter(p["customdata"].values())) if isinstance(p["customdata"], dict) else p["customdata"][0])
                  for p in event.selection.points if p.get("customdata")]
    except (AttributeError, KeyError, TypeError):
        picked = []
    shown_cols = ["incident_id", "date", "developer", "shown_group", "domain_shown", "type_source", "title"]
    names = {"incident_id": "Incident ID", "date": "Incident date", "developer": "Developer", "shown_group": "Group",
             "domain_shown": "MIT risk domain", "type_source": "Source of the type", "title": "Title"}
    if picked:
        sel = period.loc[period["incident_id"].isin(picked)].drop_duplicates(["incident_id", "developer"])
        by_group = sel.drop_duplicates("incident_id")["shown_group"].value_counts()
        st.markdown(f"**{sel['incident_id'].nunique()} incidents in the selection**")
        st.caption("By group: " + ", ".join(f"{n} {g.lower()}" for g, n in by_group.items()) + ".")
        st.dataframe(sel[shown_cols].sort_values("date").rename(columns=names), hide_index=True, key="b_picked")
    else:
        st.caption("No dot selected. The incidents behind a selection are listed here.")
    epoch_n = {d: int(epoch["organization"].isin(EPOCH_ORG[d]).sum()) for d in ELEVEN}
    rows = []
    for d in developers:
        p = period.loc[period["developer"] == d]
        rows.append({"Developer": d, "Incidents": p["incident_id"].nunique(),
                     **{g: int((p["shown_group"] == g).sum()) for g in GROUP_ORDER},
                     "Models in the Epoch list": epoch_n[d]})
    with st.expander("**How to read this chart**"):
        st.markdown(B_HOW)
    with st.expander("**What this chart cannot show**"):
        st.markdown(B_LIMITS)
    with st.expander("**Values behind the chart** (incidents per developer and incident type, with Epoch models)"):
        st.caption("Incidents in the period shown, one row per developer. An incident that names two developers is "
                   "counted for both. The last column is the number of models of the developer in the Epoch list.")
        st.dataframe(pd.DataFrame(rows).sort_values("Incidents", ascending=False), hide_index=True, key="b_values")
    records = period[["incident_id", "date", "developer", "found_in", "domain_shown", "mit_risk_subdomain",
                      "shown_group", "type_source", "title"]].sort_values(["date", "incident_id"], ascending=[False, True])
    records = records.rename(columns={**names, "found_in": "Found in", "mit_risk_subdomain": "MIT risk subdomain"})
    download_records(records, "b", "view_model_incidents.csv",
                     "One row per incident and named developer, so an incident naming two developers appears twice.")
    footer_3(["aiid", "mit", "epoch"], "3 Oct 2026 (latest incident date), export of 12 Oct 2026, "
           "7 Oct 2026 (latest Epoch release date)")


_CONFIG = {**PLOT_CONFIG, "modeBarButtonsToRemove": ["lasso2d"]}


def funnel() -> None:
    steps = [("Incidents reported since 2020", 1481, "#B0B6BD"),
             ("... naming one of the eleven developers", 400, "#56B4E9"),
             ("... model incidents, counted here", 318, "#0072B2")]
    fig = go.Figure(go.Bar(y=[s[0] for s in steps], x=[s[1] for s in steps], orientation="h",
                           marker_color=[s[2] for s in steps], text=[f"{s[1]:,}" for s in steps],
                           textposition="outside", hoverinfo="skip"))
    fig.update_layout(width=CHART_W, height=150, plot_bgcolor="white", paper_bgcolor="white", showlegend=False,
                      margin={"l": 270, "r": 40, "t": 10, "b": 10}, font={"family": "Arial, sans-serif", "size": 12, "color": INK})
    fig.update_yaxes(autorange="reversed", showgrid=False, ticks="")
    fig.update_xaxes(visible=False, range=[0, 1700])
    st.markdown("**Which incidents are counted**")
    st.plotly_chart(fig, width="content", key="b_funnel", config={"displayModeBar": False})
    st.caption("The 82 incidents not counted (400 minus 318) are 61 platform products such as feeds, ads and moderation, "
               "5 operations cases and 16 that name a developer only as the place where a scam appeared.")


def _wrap(text: str, width: int = 70) -> str:
    import textwrap
    return "<br>".join(textwrap.wrap(str(text), width))


TL_L = 260


def chart_timeline(period: pd.DataFrame, developers: list[str], epoch, from_year: int, to_year: int) -> go.Figure:
    from plotly.subplots import make_subplots
    lanes = sorted([d for d in ELEVEN if d in developers], key=lambda d: REGION_RANK[DEV_REGION[d]])
    pos = {d: i for i, d in enumerate(lanes)}
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.16, 0.84], vertical_spacing=0.04)
    # monthly strip, each incident once
    uniq = period.drop_duplicates("incident_id").assign(month=lambda f: f["when"].dt.to_period("M").dt.to_timestamp())
    monthly = uniq.groupby(["month", "shown_group"])["incident_id"].nunique().unstack(fill_value=0)
    for g in GROUP_ORDER:
        if g in monthly:
            fig.add_trace(go.Bar(x=monthly.index, y=monthly[g], marker_color=GROUP_COLOURS[g], name=g,
                                 width=86400000 * 24, hovertemplate="%{x|%b %Y}: %{y} " + g.lower() + "<extra></extra>"),
                          row=1, col=1)
    tot = monthly.sum(axis=1)
    peaks = tot[tot >= 10]
    if len(peaks):
        fig.add_trace(go.Scatter(x=peaks.index, y=peaks.values, mode="text", text=[str(int(v)) for v in peaks.values],
                                 textposition="top center", textfont={"size": 11, "color": INK}, hoverinfo="skip",
                                 showlegend=False), row=1, col=1)
    # one dot per incident and developer
    d = period.sort_values(["developer", "when", "incident_id"]).copy()
    d["k"] = d.groupby("developer").cumcount()
    d["y"] = d["developer"].map(pos) + ((d["k"] % 5) - 2) * 0.13
    for g in GROUP_ORDER:
        s = d.loc[d["shown_group"] == g]
        if s.empty:
            continue
        for src in ("MIT", "Project group"):
            s2 = s.loc[s["type_source"] == src]
            if s2.empty:
                continue
            hover = [f"<b>{_wrap(t_, 50)}</b><br>{dev}, {dt:%d %b %Y}, Incident #{i}<br>Incident type: <b>{g}</b>"
                     + ("" if src == "MIT" else "<br>Type assigned by: <b>project group</b>")
                     for t_, dt, i, dev in zip(s2["title"], s2["when"], s2["incident_id"], s2["developer"])]
            fig.add_trace(go.Scatter(x=s2["when"], y=s2["y"], mode="markers", name=g,
                                     customdata=s2[["incident_id"]].values,
                                     marker={"size": 10 if src == "MIT" else 11, "color": GROUP_COLOURS[g],
                                             "symbol": "circle" if src == "MIT" else "diamond",
                                             "line": {"color": "white", "width": 1.2}},
                                     hovertext=hover, hoverinfo="text", showlegend=False), row=2, col=1)
    if epoch is not None:
        rel = epoch.copy()
        rel["dev"] = rel["organization"].map({o: dv for dv, os_ in EPOCH_ORG.items() for o in os_})
        rel = rel.loc[rel["dev"].isin(lanes) & rel["release_year"].between(from_year, to_year)]
        fig.add_trace(go.Scatter(x=rel["release_date"], y=rel["dev"].map(pos) + 0.45, mode="markers",
                                 marker={"symbol": "triangle-up", "size": 7, "color": "#8c8c8c"}, showlegend=False,
                                 hovertext=[f"<b>{m}</b><br>released {dt:%d %b %Y} (Epoch)<br>"
                                            + (f"Epoch Capabilities Index {e:.0f} (90% interval {lo:.0f} to {hi:.0f})"
                                               if pd.notna(e) and pd.notna(lo) and pd.notna(hi)
                                               else (f"Epoch Capabilities Index {e:.0f}" if pd.notna(e)
                                                     else "Epoch Capabilities Index not available"))
                                            for m, dt, e, lo, hi in zip(rel["model"], rel["release_date"], rel["eci"],
                                                                        rel["eci_ci_low"], rel["eci_ci_high"])],
                                 hoverinfo="text"), row=2, col=1)
    for i in range(len(lanes) + 1):
        fig.add_hline(y=i - 0.5, line_color=GRID, line_width=1, row=2, col=1)
    labels = list(lanes)
    fig.update_layout(width=CHART_W, height=46 * len(lanes) + 260, plot_bgcolor="white", paper_bgcolor="white",
                      margin={"l": TL_L, "r": 30, "t": 20, "b": 50}, showlegend=False, barmode="stack", dragmode="select",
                      font={"family": "Arial, sans-serif", "size": 12, "color": INK},
                      hoverlabel={"bgcolor": "white", "align": "left", "font": {"size": 12, "color": INK}},
                      uirevision=f"b|{from_year}|{to_year}|{len(lanes)}")
    fig.update_yaxes(title_text="Incidents per month", showgrid=True, gridcolor=GRID, range=[0, max(float(tot.max()) * 1.2, 5)],
                     row=1, col=1)
    _add_region_groups(fig, _region_groups([DEV_REGION[d] for d in lanes]), CHART_W - TL_L - 30, TL_L, "y2")
    fig.update_yaxes(tickvals=list(range(len(lanes))), ticktext=labels, autorange="reversed", showgrid=False, zeroline=False,
                     range=[len(lanes) - 0.4, -0.6], row=2, col=1)
    fig.update_xaxes(showgrid=True, gridcolor=GRID, range=[f"{from_year}-01-01", "2026-11-05" if to_year == 2026 else f"{to_year}-12-31"], row=2, col=1)
    fig.update_xaxes(showgrid=True, gridcolor=GRID, row=1, col=1)
    return fig
