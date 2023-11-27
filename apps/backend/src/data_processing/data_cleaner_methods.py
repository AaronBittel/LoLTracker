import pandas as pd
from apps.helper import helper


def convert_unix_timestamp_ms_to_datetime(df: pd.DataFrame, cols: list[str]):
    for col in cols:
        df[col] = pd.to_datetime(df[col], unit="ms").dt.floor("s")


def convert_game_version_to_patch(df: pd.DataFrame, col):
    df[col] = df[col].apply(lambda x: ".".join(x.split(".")[:2]))


def convert_team_position_utility_to_support(df: pd.DataFrame, cols: list[str]):
    for col in cols:
        df.loc[df[col] == "UTILITY", col] = "SUPPORT"


def convert_seconds_to_datetime_time(df: pd.DataFrame, cols: list[str]):
    for col in cols:
        df[col] = df[col].apply(helper.convert_seconds_to_minutes_and_seconds)
