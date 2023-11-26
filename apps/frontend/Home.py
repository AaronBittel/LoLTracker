import sys
import os

sys.path.append(os.getcwd())

import streamlit as st
from apps.frontend import streamlit_tools


st.title("Home")


df = streamlit_tools.read_data("NowayKR")


with st.container():
    st.header("Pick rate")
    st.text("pick rate description")

    value = st.radio(
        label="Options", options=["absolute values", "proportion"], index=1
    )

    in_proportion = True if value == "proportion" else False
    champion_pick_rate = (
        df["championName"].value_counts(normalize=in_proportion).reset_index()
    )
    champion_pick_rate.columns = ["championName", "pick rate"]

    chart = streamlit_tools.create_horizontal_bar_chart(
        data=champion_pick_rate, x_column="pick rate", y_column="championName"
    )

    st.altair_chart(chart, use_container_width=True)
