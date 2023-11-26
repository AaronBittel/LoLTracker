import streamlit as st
import sys
import os

# sys.path.append(os.getcwd())
from apps.frontend import streamlit_tools


st.title("Noway Korea Trip Analytics")
st.write("This is a page for Noway's Korea Trip Analytics.")


df = streamlit_tools.read_data("NowayKR")
champion_pick_rate = df["championName"].value_counts().reset_index()
champion_pick_rate.columns = ["championName", "pick rate"]


streamlit_tools.container(
    title="Order Champions played by pick rate",
    description="",
    create_chart=streamlit_tools.create_horizontal_bar_chart,
    args=[champion_pick_rate, "pick rate", "championName"],
)


win_rates = df.groupby("championName")["win"].mean().reset_index()
win_rates.columns = ["championName", "win rate"]


streamlit_tools.container(
    title="Order Champions played by win rate",
    description="",
    create_chart=streamlit_tools.create_horizontal_bar_chart,
    args=[win_rates, "win rate", "championName"],
)

import time

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()
