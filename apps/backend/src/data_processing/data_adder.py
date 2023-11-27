import pandas as pd
from apps.backend.src.data_processing import data_adder_methods


def data_add(df: pd.DataFrame) -> None:
    data_adder_methods.add_column_on_blue_side(df)
    data_adder_methods.drop_all_remake_games(df)
