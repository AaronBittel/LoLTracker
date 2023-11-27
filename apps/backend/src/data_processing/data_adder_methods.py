import logging
import pandas as pd
from apps.backend.src.helper import constants


logging.basicConfig(
    level=logging.DEBUG, filename="../../logging/logging.txt", filemode="w"
)


def add_column_on_blue_side(df: pd.DataFrame):
    df["onBlueSide"] = df["teamId"] == 100


def drop_all_remake_games(df: pd.DataFrame):
    # drop all remake games
    filt = df["gameDuration"] <= constants.REMAKE_GAME_DURATION_THRESHOLD
    logging.info(f"{filt.sum()} games removed because of remakes.")
    df = df[~filt]


def add_column_session(df: pd.DataFrame) -> pd.DataFrame:
    df["timeBetweenGames"] = df["gameCreation"].shift(1) - df["gameEndTimestamp"]

    df["session"] = 0

    # Set session_number based on conditions
    current_session = 0
    for match_id in df.index:
        if df["timeBetweenGames"].loc[match_id] > pd.Timedelta(hours=1):
            current_session += 1
        df.at[match_id, "session"] = current_session

    return df


def add_column_queue_time(df: pd.DataFrame) -> pd.DataFrame:
    pass
