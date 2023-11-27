import pandas as pd
from apps.backend.src.data_processing import data_cleaner
from apps.backend.src.data_processing import data_adder


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = data_cleaner.clean_dataframe(df)
    data_adder.data_add(df)

    return df
