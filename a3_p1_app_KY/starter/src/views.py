from __future__ import annotations

import pandas as pd
import streamlit as st


def render_population_view(data: pd.DataFrame) -> None:
    st.header("Population trend")
    st.caption("Unit: people")
    st.caption(f"Latest observation: {data['date'].max().date().isoformat()}")

    available = sorted(data["country"].unique())
    countries = st.multiselect(
        "Countries",
        available,
        default=available,
        key="country_filter",
    )
    st.write(f"Selected: {', '.join(countries) if countries else 'none'}")

    filtered = data.loc[data["country"].isin(countries)].copy()

    if filtered.empty:
        st.info("No observations match the selected filters.")
    else:
        latest = filtered.sort_values("date").groupby("country", as_index=False).tail(1)
        columns = st.columns(len(latest))
        for column, record in zip(columns, latest.itertuples(index=False), strict=True):
            column.metric(record.country, f"{record.population:,.0f} people")

        chart_data = filtered.pivot(index="date", columns="country", values="population")
        st.line_chart(chart_data, y_label="Population (people)", x_label="Year")

    st.caption(
        "Source: World Development Indicators: Population, total (SP.POP.TOTL), "
        "World Bank."
    )
    st.download_button(
        "Download filtered data",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_population.csv",
        mime="text/csv",
        key="population_download",
    )
