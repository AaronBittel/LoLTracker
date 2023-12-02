import pandas as pd


def get_champion_game_time(df):
    filt = df["championName"].value_counts() >= 5
    filtered_df = df[df["championName"].isin(filt[filt].index)]

    return filtered_df.groupby("championName")["gameDuration"].mean() / 60
