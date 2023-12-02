import time
import json
import os

from riotwatcher import LolWatcher

from apps.backend.src.data_collection import game_data_fetcher
from apps.backend.src.data_extraction import game_data_extractor
from apps.helper import helper
from apps.backend.src.helper import constants
from apps.backend.src.data_processing import data_processor

from typing import Iterator


def main(
    summoner_name: str,
    tagline: str,
    server: str,
    queue: constants.Queue,
    number_of_games: int,
    till_season_patch: constants.Patch,
    player_name: str,
    debug: bool = False,
):
    api_key = helper.get_api_key_from_file()
    lolwatcher = LolWatcher(api_key=api_key)

    region = game_data_fetcher.map_server_to_region(server=server)

    puuid = game_data_fetcher.get_puuid(
        api_key=api_key, summoner_name=summoner_name, tagline=tagline, region=region
    )

    match_list = game_data_fetcher.get_match_ids(
        lolwatcher=lolwatcher,
        puuid=puuid,
        region=region,
        number_of_games=number_of_games,
        queue=queue,
    )

    match_data_iterator = game_data_fetcher.create_match_data_iterator(
        lolwatcher=lolwatcher,
        match_list=match_list,
        region=region,
        till_season_patch=till_season_patch,
    )

    if not debug:
        df = game_data_extractor.create_dataframe(
            game_data_iterator=match_data_iterator, puuid=puuid
        )
        df = data_processor.process_dataframe(df)
        df.to_parquet(f"apps/data/dataframes/{player_name}.parquet")
    else:
        helper.save_raw_data(
            match_data_iterator=match_data_iterator, player_name=player_name
        )


if __name__ == "__main__":
    input_values = {
        "summoner_name": "noway2u",  # "정신력남자",
        "tagline": "EUW1",
        "server": "EUW1",
        "queue": constants.Queue.RANKED,
        "number_of_games": 45,
        "till_season_patch": constants.Patch(12, 1),
        "debug": False,
        "player_name": "test_data",
    }

    start = time.time()

    main(**input_values)

    end = time.time()
    diff = end - start
    print(f"Execution Time: {int(diff // 60)} Minutes and {int(diff % 60)} Seconds.")
