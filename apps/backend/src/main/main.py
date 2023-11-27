import pandas as pd

from riotwatcher import LolWatcher

from apps.backend.src.data_collection import game_data_fetcher
from apps.backend.src.data_extraction import game_data_extractor
from apps.helper import helper
from apps.backend.src.helper import constants
from apps.backend.src.data_processing import data_processor


def main():
    api_key = helper.get_api_key_from_file()
    lolwatcher = LolWatcher(api_key=api_key)

    input_values = {
        "summoner_name": "TRM%20BROSES",
        "server": "EUW1",
        "queue": constants.Queue.RANKED,
        "number_of_games": 1,
        "till_season_patch": constants.Patch(13, 19),
    }

    match_data_iterator = game_data_fetcher.create_match_data_iterator(
        lolwatcher=lolwatcher, **input_values
    )

    df = game_data_extractor.create_dataframe(match_data_iterator)

    df = data_processor.process_dataframe(df)

    df.to_parquet("test_data.parquet")


if __name__ == "__main__":
    main()
