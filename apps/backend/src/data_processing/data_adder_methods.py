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
