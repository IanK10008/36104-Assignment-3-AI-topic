"""The controls of Views 1 and 2 (Story 1a), copied word for word from app.py of the A3P1 app.

A3P1 builds these controls with module-level variables (``models``, ``developers``). Here the same code sits
inside ``build(models)`` so the story page can pass its own table. Nothing in the logic or the wording changes.
"""
from __future__ import annotations

import streamlit as st

from src import analysis as an
from src import data, snapshot


def build(models):
    """Return ``(controls_block, all_three_recent, overview)`` for this table of models."""
    all_three_recent = models.loc[(models["release_year"] >= 2025)
                                  & models["match_status"].isin([data.ALL_SAME, data.ALL_TAG])]
    developers = sorted(an.developer_name(models).unique())


    def _saved(key: str, options: list, default):
        """Value kept in the browser session, or the default if it is missing or no longer one of the options
        (for example, left over from an older version of the page)."""
        value = st.session_state.get(key, default)
        if value not in options:
            value = default
            st.session_state[key] = default
        return value


    def window_text(name: str) -> str:
        """Window name, with the first date written out for the rolling windows (they follow the data refresh)."""
        spec = an.WINDOWS[name]
        if isinstance(spec, tuple):
            start = an.window_start(models, spec)
            return f"{name}, from {start.day} {start:%b %Y}"
        return name


    def overview() -> None:
        """The data behind the page: how many models each source holds, and which view uses which source.
        It sits above View 1 because it describes the whole page, and View 1 itself uses only Epoch and LiteLLM."""
        st.subheader("Data behind this page")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Epoch: capability score", f"{len(models)}",
                  help="Models in the Epoch file with a capability score (ECI). Released "
                       f"{snapshot.get('epoch_first')} to {snapshot.get('epoch_last')}, "
                       f"Epoch file retrieved {snapshot.get('epoch_retrieved')}.")
        m2.metric("LiteLLM: list price", f"{models['output_price_usd_per_million'].notna().sum()}",
                  help=f"Models with a LiteLLM list price. The price file was retrieved {snapshot.get('litellm_retrieved')}, and the price used is "
                       "the median list price per million output tokens across the provider rows of one model.")
        m3.metric("LMArena: rating", f"{models['arena_rating'].notna().sum()}",
                  help=f"Models with an LMArena rating. The text leaderboard snapshot was published {snapshot.get('lmarena_published')}. Ratings "
                       "come from people's votes between pairs of answers, and a model needs a name match to count here.")
        m4.metric("In all three, 2025-2026", f"{len(all_three_recent)}",
                  help="Released in 2025 or 2026 and found in Epoch, LiteLLM and LMArena. Same name, or same name plus a "
                       "tag such as (High).")
        st.info(
            "**How to read this page.** Three public sources measure different things:\n\n"
            "- **Capability:** Epoch Capabilities Index (ECI), benchmark-based, from Epoch AI. Used in View 1 and View 2.\n"
            "- **List price:** US dollars per million output tokens, from LiteLLM. Used in View 1 and View 2.\n"
            "- **Human preference:** votes on LMArena. Used in View 2 only.\n\n"
            "View 1 plots capability against price. View 2 combines the three into one ranking. Where intervals "
            "overlap, read models as roughly equal, not better or worse.")


    def controls_block(prefix: str, settings=None) -> tuple:
        """The controls of one view. View 1 and View 2 each have their own copy
        (keys start with ``prefix``), so each can be set differently. Returns the selected data for that view."""
        if prefix:
            settings = settings if settings is not None else st.container()
        else:
            settings = st.container()
            with settings:
                st.markdown("#### Controls for this view")
        k = lambda name: prefix + name
        year = an.WINDOWS[_saved(k("window"), list(an.WINDOWS), list(an.WINDOWS)[0])]
        route = an.ROUTE_CHOICES[_saved(k("route"), list(an.ROUTE_CHOICES), list(an.ROUTE_CHOICES)[0])]
        _saved(k("match_rule"), list(an.MATCH_RULES), list(an.MATCH_RULES)[0])
        st.session_state.setdefault(k("developers"), developers)
        devs = [d for d in st.session_state[k("developers")] if d in developers]
        st.session_state[k("developers")] = devs
        base = an.filter_models(models, year, route, devs)
        rule_counts = {n: len(an.three_source(base, v)) for n, v in an.MATCH_RULES.items()} if prefix else {}
        window_counts = {n: len(an.filter_models(models, y, route, devs)) for n, y in an.WINDOWS.items()}
        route_counts = {n: len(an.filter_models(models, year, r, devs)) for n, r in an.ROUTE_CHOICES.items()}

        with settings:
            c1, c2, c3 = st.columns([1, 1.2, 1.6]) if prefix else (*st.columns([1, 1.2]), None)
            window_label = c1.selectbox("Release window", list(an.WINDOWS), key=k("window"),
                                        format_func=lambda x: window_text(x) + f" ({window_counts[x]} models)")
            route_label = c2.selectbox("Route", list(an.ROUTE_CHOICES), key=k("route"),
                                       format_func=lambda x: f"{x} ({route_counts[x]} models)")
            rule_label = list(an.MATCH_RULES)[0]  # View 1 uses Epoch and LiteLLM only, so it has no name-match rule
            if prefix:
                rule_label = c3.selectbox("Which name matches count as \"in all three sources\"", list(an.MATCH_RULES),
                                          key=k("match_rule"), format_func=lambda x: f"{rule_counts[x]} models: {x}",
                                          help="Same name: identical in all three files. Plus a tag: LMArena adds a setting such "
                                               "as \"(High)\" to the same model. Unclear versions and \"-max\" entries are "
                                               "always left out. The number in each option is how many models it gives for the "
                                               "current window, route and developers.")
            chosen = st.multiselect("Developers", developers, key=k("developers"),
                                    help="Remove developers to compare a subset. An empty selection shows a message.")

            window = an.filter_models(models, an.WINDOWS[window_label], an.ROUTE_CHOICES[route_label], chosen)
            points = an.price_points(window)
            three = an.three_source(window, an.MATCH_RULES[rule_label]) if prefix else points.iloc[0:0]
            pct = an.percentiles(three) if not three.empty else three
            st.caption(f"Selected: {len(window)} Epoch models · {len(points)} with a usable price"
                       + (f" · {len(three)} in all three sources" if prefix else ""))

        # The weights are drawn inside the view; the ranking here reads them from the saved state.
        if not three.empty:
            criteria = list(an.CRITERIA)
            if prefix:  # View 2 can leave a criterion out of its ranking
                picked = st.session_state.get(k("criteria"), list(an.CRITERIA))
                criteria = [c for c in an.CRITERIA if c in picked] or list(an.CRITERIA)
            # View 1 has no weight controls, so its one-line answer always uses CRITIC weights (the View 2 default)
            if not prefix or st.session_state.get(k("weight_method"), "CRITIC (data-driven)").startswith("CRITIC"):
                w = an.critic_weights(pct, criteria)
            else:
                w = an.normalise({c: st.session_state.get(k(f"w_{c}"), 5) if c in criteria else 0 for c in an.CRITERIA})
            ranked = an.score(three, pct, w)
            tags = [an.effort_tag(m, l) for m, l in zip(ranked["model"], ranked["lmarena_match"])]
            ranked["label"] = [f"{m} ({t})" if t else m for m, t in zip(ranked["model"], tags)]
        else:
            ranked = three
        return window_label, rule_label, points, three, pct, ranked
    return controls_block, all_three_recent, overview
