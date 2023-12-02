import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from apps.backend.src.data_analyzing import data_analyizer

sys.path.append(os.getcwd())

st.title("Home")

df = pd.read_parquet(
    r"C:\Users\AaronWork\Projects\LoLTracker\apps\data\dataframes\정신력남자.parquet"
)

filt = df["championName"].value_counts() >= 5
filtered_df = df[df["championName"].isin(filt[filt].index)]

data = (filtered_df.groupby("championName")["gameDuration"].mean() / 60).sort_values()

average_game_time = df["gameDuration"].mean() / 60

st.write(average_game_time)

# Create a bar chart using Plotly Express
fig = px.bar(
    y=data.index,
    x=data.values,
    orientation="h",
    labels={"x": "Champion", "y": "Average Game Duration (minutes)"},
    title="Average Game Duration per Champion",
)

fig.add_shape(
    go.layout.Shape(
        type="line",
        x0=average_game_time,
        x1=average_game_time,
        y0=0,
        y1=13,
        line=dict(color="red", width=3),
    )
)

# Show the Plotly chart using st.plotly_chart
st.plotly_chart(fig)
