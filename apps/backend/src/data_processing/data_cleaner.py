import logging

import pandas as pd
from apps.backend.src import data_cleaner_methods

logging.basicConfig(
    level=logging.DEBUG, filename="../../logging/logging.txt", filemode="w"
)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    data_cleaner_methods.convert_unix_timestamp_ms_to_datetime(
        df=df, cols=["gameCreation", "gameEndTimestamp"]
    )
    data_cleaner_methods.convert_game_version_to_patch(df=df, col="gameVersion")
    data_cleaner_methods.convert_team_position_utility_to_support(
        df=df, cols=["teamPosition"]
    )
    df["gameDuration_m_s"] = pd.to_datetime(df["gameDuration"], unit="s").dt.strftime(
        "%M:%S"
    )
    df.set_index("matchId", inplace=True)
    return df
