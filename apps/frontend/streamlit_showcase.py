import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from apps.backend.src import constants

from apps.backend.src import main
import sys

sys.path.append(r"C:\Users\AaronWork\Projects\LoLTracker")


def read_data(account: str):
    return pd.read_parquet(
        r"C:\Users\AaronWork\Projects\LoLTracker\apps\data\{}.parquet".format(account)
    )


def cumulative_win_lose(df: pd.DataFrame):
    df["win_numeric"] = np.where(df["win"], 1, -1)
    df["gameCreation_day"] = df["gameCreation"].dt.floor("D")

    with st.container():
        st.header("Wins and Losses Over Time")
        st.write(
            "This bar chart represents the cumulative sum of wins (+1) and losses (-1) for each day."
        )
        # Group by day and sum the "win_numeric" column
        grouped_data = df.groupby("gameCreation_day")["win_numeric"].sum().reset_index()

        # Convert datetime to string representing only the date
        grouped_data["gameCreation_day"] = grouped_data["gameCreation_day"].dt.strftime(
            "%Y-%m-%d"
        )

        # Display the bar chart
        st.bar_chart(grouped_data.set_index("gameCreation_day"))


def create_horizontal_bar_chart(data, x_column, y_column, sort_by="-x"):
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(x=f"{x_column}:Q", y=alt.Y(f"{y_column}:N", sort=sort_by))
    )
    return chart


def show_champion_play_rate(df: pd.DataFrame, account_name: str):
    st.header(f"{account_name} - Champion Play rate")
    st.write("Champion ordered by plat rate")

    # Assuming df is your DataFrame
    champion_pick_rate = df["championName"].value_counts(normalize=True).reset_index()
    champion_pick_rate.columns = ["championName", "pick rate"]

    # Create a horizontal bar chart using the extracted method
    bar_chart = create_horizontal_bar_chart(
        champion_pick_rate, x_column="pick rate", y_column="championName"
    )

    # Display the chart in Streamlit
    st.altair_chart(bar_chart, use_container_width=True)


def show_champion_win_rate(df: pd.DataFrame, account_name: str):
    st.header(f"{account_name} - Champion Win rate")
    st.write("Champion ordered by win rate")

    # Calculate win rate for each champion
    win_rates = df.groupby("championName")["win"].mean().reset_index()
    win_rates.columns = ["championName", "winrate"]

    # Create a horizontal bar chart using the extracted method
    bar_chart = create_horizontal_bar_chart(
        win_rates, x_column="winrate", y_column="championName"
    )

    # Display the chart in Streamlit
    st.altair_chart(bar_chart, use_container_width=True)


# Function to display Page 1 content
def page(page_name: str, account_name: str):
    st.title(page_name)
    df = read_data(account_name)
    cumulative_win_lose(df)
    show_champion_play_rate(df, account_name)
    show_champion_win_rate(df, account_name)


def custom_page(page_name: str):
    st.title(page_name)
    summoner_name = st.text_input("Summoner name: ")
    server = st.selectbox("Server: ", options=["EUW1", "NA", "KR"])
    queue = st.selectbox(
        "Queue: ",
        options=[constants.Queue.RANKED, constants.Queue.NORMAL, constants.Queue.ARAM],
    )

    amount_of_games = st.slider("How many games?: ", min_value=10, max_value=45, step=1)
    st.button(
        label="Submit",
        on_click=fetch_data,
        args=[summoner_name, server, queue, amount_of_games],
    )


def fetch_data(
    summoner_name: str, server: str, queue: constants.Queue, amount_of_games: int
):
    st.write(
        f"Fetching data ... ({summoner_name}, {server}, {queue.value}, {amount_of_games})"
    )

    main.main(
        summoner_name=summoner_name,
        server=server,
        queue=queue,
        number_of_games=amount_of_games,
        till_season_patch=constants.Patch(12, 1),
        path=r"C:\Users\AaronWork\Projects\LoLTracker\apps\data\test_data.parquet",
    )

    df = read_data("test_data")
    st.write(df.head())


def main_v2():
    # Sidebar navigation
    selected_page = st.sidebar.selectbox(
        "Select Account", ["Noway Korea", "Don Noway", "noway2u", "custom search"]
    )

    # Display the selected page
    if selected_page == "Noway Korea":
        page(page_name="Noway Korea Trip", account_name="NowayKR")
    elif selected_page == "Don Noway":
        page(page_name="Don Noway", account_name="DonNowayEUW")
    elif selected_page == "noway2u":
        page(page_name="noway2u", account_name="noway2uEUW")
    elif selected_page == "custom search":
        custom_page(page_name="custom search")


if __name__ == "__main__":
    main_v2()
