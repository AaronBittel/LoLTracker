import pandas as pd
from apps.backend.src.data_processing import data_cleaner
from apps.backend.src.data_processing import data_adder


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = data_cleaner.clean_dataframe(df)
    data_adder.data_add(df)
    df.sort_values(by="gameCreation", ascending=False, inplace=True)

    return df
