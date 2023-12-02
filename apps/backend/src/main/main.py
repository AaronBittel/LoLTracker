import logging
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
    save_data_in_file: bool = False,
    test_data: bool = True,
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

    if not save_data_in_file:
        match_data_iterator = game_data_fetcher.create_match_data_iterator(
            lolwatcher=lolwatcher,
            match_list=match_list,
            region=region,
            till_season_patch=till_season_patch,
        )

        df = game_data_extractor.create_dataframe(
            game_data_iterator=match_data_iterator, puuid=puuid
        )
        df = data_processor.process_dataframe(df)
        df.to_parquet(f"apps/data/dataframes/{summoner_name}.parquet")

    else:
        summoner_name = "test_data" if test_data else summoner_name
        logging.debug(f"len match_list before: {len(match_list)}")
        match_list = helper.remove_already_stored_match_ids(summoner_name, match_list)
        logging.debug(f"len match_list after: {len(match_list)}")

        match_data_iterator = game_data_fetcher.create_match_data_iterator(
            lolwatcher=lolwatcher,
            match_list=match_list,
            region=region,
            till_season_patch=till_season_patch,
        )

        helper.save_raw_data(
            match_data_iterator=match_data_iterator,
            summoner_name=summoner_name,
            queue=queue,
        )


if __name__ == "__main__":
    input_values = {
        "summoner_name": "정신력남자",
        "tagline": "KR1",
        "server": "KR",
        "queue": constants.Queue.RANKED,
        "number_of_games": 3000,
        "till_season_patch": constants.Patch(1, 1),
        "save_data_in_file": True,
        "test_data": False,
    }

    start = time.time()

    main(**input_values)

    end = time.time()
    diff = end - start
    print(f"Execution Time: {int(diff // 60)} Minutes and {int(diff % 60)} Seconds.")
