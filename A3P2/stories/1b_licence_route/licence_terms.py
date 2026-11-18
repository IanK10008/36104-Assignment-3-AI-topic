"""Story 1b, View 3: what each restricted-use, non-commercial or unknown licence says, term by term.

View 1 (dot strip) and View 2 (licence mix by year, Anh) use Epoch's accessibility label. Epoch's label is a class, and
a class cannot say which condition the architect must check. This view opens the licences themselves: one row per model
that Epoch labels restricted use, non-commercial or unknown (released 2024 to 2026), one column per licence term.

Reading: 18 November 2026, AI reading with Ian as reviewer, not legal advice. The cells come from
data/licence_terms.json, which is written from the licence notes (licence_check_2024_2026_2026-11-18.md). Nothing is
hand-coded here.

Interaction: hover a cell for a short preview. Click a cell to pin its evidence in the card above the matrix. The card
stays until Close is pressed. The card also holds a collapsed Full note for the model.
"""
from __future__ import annotations

import json
import textwrap
import zlib
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.views import INK, MUTED, PLOT_CONFIG
from src.views_context import _layout, download_records, legend_html

HERE = Path(__file__).resolve().parent
READ_DATE = "18 November 2026"
COLUMNS = ["Epoch label", "Commercial use", "Revenue or user threshold", "Hosting or MaaS", "Attribution or notice",
           "Use policy", "Output or derivative rule"]
# state -> (fill, text colour, edge, meaning). Colour never carries the meaning alone: every cell also has its words.
STATES = {
    "ok": ("#E3F1E8", "#17513A", "#2F8F62", "No condition"),
    "cond": ("#FBEFD0", "#6B4A05", "#C98A10", "Condition applies"),
    "block": ("#F9DCD8", "#7A1F16", "#C4432F", "Blocked or needs a separate licence"),
    "unk": ("#D9DCE1", "#454B55", "#8A909B", "Assumed, not read or unclear (italic)"),
    "na": ("#F1F0EC", "#7B8089", "#C9C7BF", "Not applicable"),
    "epoch": ("#FFFFFF", INK, "#C9C7BF", "Epoch label, shown for comparison"),
}
EVIDENCE = {"full": "Read in full", "part": "Read in part", "assumed": "Assumed", "na": "Not a licence case"}
ROW_PX = 46
WRAP = 22

HOW_TO_READ = """
- **One row per model:** the 51 models released 2024 to 2026 whose Epoch label is restricted use, non-commercial or
  unknown. Rows are grouped by developer and ordered by release date.
- **First column is Epoch's label:** it is the label that Views 1 and 2 use. The other six columns are what the
  licence text says.
- **Cell colour:** green, no condition. Amber, a condition applies. Red, commercial use is blocked or needs a separate
  licence. Grey in italics, assumed or not read. Pale grey, not applicable.
- **Hover a cell:** a short preview. **Click a cell:** the evidence for that one term is pinned in the card above the
  matrix and stays there until Close.
- **Full note:** the card holds a collapsed Full note section. It opens inside the card and holds the licence text, key terms,
  the gap against the Epoch label and the source link.
- **Filters:** Epoch label, release year, evidence level and developer. Every option starts selected. Press an option to hide it, so that the matrix gets shorter.
"""

DESIGN_DECISION = """
**Visual task:** Show, for each model whose Epoch label hides a condition, which licence term holds the condition, so
that the architect knows what the legal team must read first.

**Form chosen:** An XY heatmap matrix (Visual Vocabulary: *correlation*, used here as a model-by-term grid) with the
condition written inside every cell. Views 1 and 2 stay at class level. This view sits below them because it answers
the next question, which licence term decides.

**Alternatives rejected:**

1. **Replacing View 2.** View 2 shows the trend across years. The matrix shows terms per model. They answer different
   questions.
2. **A stacked bar of terms.** A count of models per term hides which model carries which condition.
3. **A table of paragraphs.** Readers cannot scan which models share a condition.
4. **Colour only.** Colour alone fails for colour vision deficiency, so each cell also carries its words.
"""

LIMITS = f"""
- **Reading, not a legal opinion:** AI reading on {READ_DATE}. Ian is the reviewer and has not yet reviewed every
  cell. Legal or procurement must confirm before any approval.
- **Evidence levels differ:** 42 models were read in full from the licence file or page. Others were read in part,
  assumed or are not licence cases. The Evidence column and the italic grey cells mark them.
- **Hosted entries:** for hosted models only the vendor's API layer was read. The open-weight licence is assumed for
  the Qwen hosted entries and marked as assumed.
- **Not covered:** data handling, regions, security review and local law.
"""


@st.cache_data(show_spinner=False)
def load_terms(path: str) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _label(row: dict) -> str:
    return row.get("e12") or row.get("e17") or "No label"


def _wrap(text: str) -> str:
    return "<br>".join(textwrap.wrap(text, WRAP, break_long_words=False)[:3])


def _cell(row: dict, col: int) -> tuple[str, str, str]:
    """State, shown text and evidence sentence for one cell. Column 0 is Epoch's label with the gap as evidence."""
    if col == 0:
        return "epoch", _label(row), row["gap"]
    state, text, evidence = row["cells"][col - 1]
    return state, text, evidence


def _org(row: dict) -> str:
    return row.get("org") or "Not stated"


def _filter(rows: list[dict]) -> tuple[list[dict], bool]:
    labels = sorted({_label(r) for r in rows})
    years = sorted({str(r["year"]) for r in rows})
    levels = list(EVIDENCE)
    orgs = sorted({_org(r) for r in rows})
    with st.container(horizontal=True, vertical_alignment="center", gap="large"):  # Epoch label and year on one line
        st.markdown("**Epoch label:**", width=110)
        pick_l = st.pills("Epoch label", labels, selection_mode="multi", default=labels, key="lt_labels",
                          label_visibility="collapsed", width="content")
        st.markdown("**Release year:**", width=100)
        pick_y = st.pills("Release year", years, selection_mode="multi", default=years, key="lt_years",
                          label_visibility="collapsed", width="content")
    with st.container(horizontal=True, vertical_alignment="center", gap="small"):
        st.markdown("**Evidence:**", width=110)
        pick_e = st.pills("Evidence", levels, selection_mode="multi", default=levels, key="lt_evidence",
                          format_func=EVIDENCE.get, label_visibility="collapsed", width="content")
    pick_o = st.multiselect("Developers", orgs, default=orgs, key="lt_orgs",
                            help="Keep only the models from these developers. Fewer developers make the matrix shorter.")
    if not (pick_l and pick_y and pick_e and pick_o):
        return [], True
    keep = [r for r in rows if _label(r) in pick_l and str(r["year"]) in pick_y and r["ev"] in pick_e
            and _org(r) in pick_o]
    return keep, False


def chart_matrix(rows: list[dict], pinned: tuple[str, int] | None) -> go.Figure:
    n = len(rows)
    z = [[list(STATES).index(_cell(r, c)[0]) for c in range(len(COLUMNS))] for r in rows]
    text = []
    hover = []
    for r in rows:
        t_row, h_row = [], []
        for c in range(len(COLUMNS)):
            state, shown, evidence = _cell(r, c)
            t_row.append(f"<i>{_wrap(shown)}</i>" if state == "unk" else _wrap(shown))
            h_row.append(f"<b>{r['model']}</b><br><b>{COLUMNS[c]}: {shown}</b><br><b>{STATES[state][3]}</b><br><br>"
                         f"{_wrap_hover(evidence)}<br><br><i>Click to pin the evidence above the matrix</i>")
        text.append(t_row)
        hover.append(h_row)
    keys = list(STATES)
    colourscale = []
    for i, k in enumerate(keys):
        lo, hi = i / len(keys), (i + 1) / len(keys)
        colourscale += [[lo, STATES[k][0]], [hi, STATES[k][0]]]
    fig = go.Figure(go.Heatmap(
        z=z, x=list(range(len(COLUMNS))), y=list(range(n)), zmin=-0.5, zmax=len(keys) - 0.5, colorscale=colourscale,
        showscale=False, text=text, texttemplate="%{text}", textfont={"size": 11, "color": INK},
        hoverinfo="skip", xgap=3, ygap=3))
    # Plotly does not report a click on a heatmap cell to Streamlit, so an invisible point at each cell centre takes the
    # hover and the click. The heatmap draws the cells and the points draw nothing.
    xs = [c for _ in rows for c in range(len(COLUMNS))]
    ys = [i for i, _ in enumerate(rows) for _ in range(len(COLUMNS))]
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers", marker={"size": 30, "symbol": "square", "opacity": 0.0},
        selected={"marker": {"opacity": 0.0}}, unselected={"marker": {"opacity": 0.0}},
        customdata=[[i, c] for i in range(len(rows)) for c in range(len(COLUMNS))],
        hovertext=[h for h_row in hover for h in h_row], hovertemplate="%{hovertext}<extra></extra>"))
    fig.update_layout(clickmode="event+select", hoverdistance=90, dragmode=False,
                      hoverlabel={"align": "left", "bgcolor": "white", "font": {"size": 12, "color": INK}})
    ticks = [f"<b>{r['model']}</b><br><span style='color:{MUTED}'>{r['group']} | {r['release']}</span>" for r in rows]
    _layout(fig, 90 + ROW_PX * max(n, 1), "", "", f"lt|{n}", {"l": 250, "r": 20, "t": 60, "b": 20})
    fig.update_xaxes(side="top", tickvals=list(range(len(COLUMNS))), ticktext=[_wrap(c) for c in COLUMNS],
                     showgrid=False, ticks="", range=[-0.5, len(COLUMNS) - 0.5], fixedrange=True)
    fig.update_yaxes(tickvals=list(range(n)), ticktext=ticks, range=[n - 0.5, -0.5], showgrid=False, ticks="",
                     fixedrange=True)
    if pinned:
        for i, r in enumerate(rows):
            if r["model"] == pinned[0]:
                fig.add_shape(type="rect", x0=pinned[1] - 0.5, x1=pinned[1] + 0.5, y0=i - 0.5, y1=i + 0.5,
                              line={"color": INK, "width": 3}, fillcolor="rgba(0,0,0,0)")
    return fig


def _wrap_hover(text: str, width: int = 60) -> str:
    return "<br>".join(textwrap.wrap(text, width)[:5])


def _note(row: dict) -> None:
    st.markdown(f"**Licence text:** {row['licence']}")
    st.markdown("**Key terms:**\n" + "\n".join(f"- {t}" for t in row["terms"]))
    st.markdown(f"**Gap between the Epoch label and the licence text:** {row['gap']}")
    st.markdown(f"**Source and confidence:** {row['conf']}. Read {READ_DATE}.")
    if row.get("url"):
        st.markdown(f"[Open the licence source]({row['url']})")


def _card(rows_all: list[dict], pinned: tuple[str, int] | None, nonce_key: str) -> None:
    """The pinned card is kept short because it stays on screen while the reader scrolls the matrix."""
    if not pinned:
        st.caption("Click a cell to pin its evidence here. The card stays until Close is pressed.")
        return
    row = next((r for r in rows_all if r["model"] == pinned[0]), None)
    if row is None:
        return
    state, shown, evidence = _cell(row, pinned[1])
    with st.container(border=True, key="lt_card"):
        head, close = st.columns([8, 1], vertical_alignment="center")
        head.markdown(f"**{row['model']}** | {COLUMNS[pinned[1]]}: **{shown}** "
                      f"<span style='color:{MUTED};font-size:0.85rem'>({STATES[state][3]})</span>",
                      unsafe_allow_html=True)
        if close.button("Close", width="stretch"):
            st.session_state["lt_pin"] = None
            st.session_state[nonce_key] = st.session_state.get(nonce_key, 0) + 1
            st.rerun(scope="fragment")
        st.markdown(evidence)
        link = f" [Open the source]({row['url']})" if row.get("url") else ""
        st.caption(f"{row['org'] or 'Developer not named'} | released {row['release']} | Epoch label: {_label(row)} | "
                   f"Evidence: {EVIDENCE[row['ev']]}, read {READ_DATE}.{link}")
        with st.expander(f"**Full note for {row['model']}**"):
            _note(row)


@st.fragment  # a click or a filter change re-runs only this view, not the two views above it
def render_licence_terms() -> None:
    rows_all = load_terms(str(HERE / "data" / "licence_terms.json"))
    st.caption(f"Unit: one row per model, one column per licence term. Epoch's label next to what the licence text says, "
               f"read on {READ_DATE}. {len(rows_all)} models released 2024 to 2026 that Epoch labels restricted use, "
               "non-commercial or unknown.")
    rows, none = _filter(rows_all)
    if none:
        st.warning("Select at least one option in each filter.")
    else:
        blocked = sum(1 for r in rows if r["cells"][0][0] == "block")
        thr = sum(1 for r in rows if r["cells"][1][0] in ("cond", "block"))
        full = sum(1 for r in rows if r["ev"] == "full")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Models shown", f"{len(rows)} of {len(rows_all)}")
        m2.metric("Commercial use blocked", f"{blocked}", help="Commercial use is blocked or needs a separate licence.")
        m3.metric("Revenue or user threshold", f"{thr}", help="A revenue or user limit applies, or commercial use is blocked.")
        m4.metric("Read in full", f"{full}", help="Read from the licence file or page in full.")
    nonce_key = "lt_nonce"
    st.html("<style>div:has(> .st-key-lt_slot){position:sticky;top:3.75rem;z-index:20;background:white;max-height:62vh;overflow-y:auto}</style>")
    if none or not rows:
        with st.container(key="lt_slot"):
            _card(rows_all, None, nonce_key)
        legend_html([(v[0], v[3], "square") for k, v in STATES.items() if k != "epoch"])
        return
    chart_key = f"lt_{st.session_state.get(nonce_key, 0)}_{zlib.crc32('|'.join(r['model'] for r in rows).encode()) % 100000}_chart"
    # The selection of the chart is already in session state when this run starts, so the pinned cell is known before
    # the figure is drawn. One run per click, with no second run to outline the cell.
    hits = []
    try:
        for p in st.session_state[chart_key]["selection"]["points"]:
            custom = p.get("customdata") or []
            if len(custom) == 2 and 0 <= int(custom[0]) < len(rows):
                hits.append((rows[int(custom[0])]["model"], int(custom[1])))
    except (KeyError, TypeError):  # no selection yet
        hits = []
    last = st.session_state.get("lt_last_hit")
    new_hits = [h for h in hits if h != last]  # Plotly may keep the earlier point selected, so the new one is the point that differs
    hit = new_hits[0] if new_hits else (last if last in hits else None)
    st.session_state["lt_last_hit"] = hit
    if new_hits:
        st.session_state["lt_pin"] = list(hit)
    pinned = st.session_state.get("lt_pin")
    pinned = tuple(pinned) if pinned else None
    with st.container(key="lt_slot"):
        _card(rows_all, pinned, nonce_key)
    legend_html([(v[0], v[3], "square") for k, v in STATES.items() if k != "epoch"])  # directly above the matrix
    st.plotly_chart(chart_matrix(rows, pinned), width="content", key=chart_key, config=PLOT_CONFIG,
                    on_select="rerun", selection_mode="points")
    with st.expander("**How to read this matrix**"):
        st.markdown(HOW_TO_READ)
    with st.expander("**Design decision for this view** (task, form, rejected alternatives)"):
        st.markdown(DESIGN_DECISION)
    with st.expander("**What this matrix cannot show**"):
        st.markdown(LIMITS)
    records = pd.DataFrame([{
        "Model (Epoch name)": r["model"], "Release date": r["release"], "Developer": r["org"] or "Not stated",
        "Epoch label": _label(r), **{COLUMNS[i + 1]: r["cells"][i][1] for i in range(6)},
        "Evidence level": EVIDENCE[r["ev"]], "Licence": r["licence"], "Gap against the Epoch label": r["gap"],
        "Source": r.get("url") or ""} for r in rows])
    download_records(records, "lt", "view3_licence_terms_records.csv",
                     "One row per model with the text of each licence term, the evidence level and the source link.")
    st.caption("Sources:\n\n- **Epoch AI accessibility labels**, from the Epoch capability files of 12 Nov 2026 and 17 Oct 2026 "
               "(the models are the union of the two files).\n- **Licence files and pages**, opened by Claude on "
               f"{READ_DATE}. The link for each model is in its full note.")
    st.caption(f"Latest observation: {READ_DATE} (licence reading)")
