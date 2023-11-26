import streamlit as st
import pandas as pd
import altair as alt
from typing import Callable


def container(title: str, description: str, create_chart: Callable = None, args=None):
    with st.container():
        st.header(title)
        st.write(description)

        if create_chart:
            chart = create_chart(*args)
            st.altair_chart(chart, use_container_width=True)


def read_data(account: str):
    return pd.read_parquet(r"apps\data\{}.parquet".format(account))


def create_horizontal_bar_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    sort_by="-x",
):
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(x=f"{x_column}:Q", y=alt.Y(f"{y_column}:N", sort=sort_by))
    )
    return chart
