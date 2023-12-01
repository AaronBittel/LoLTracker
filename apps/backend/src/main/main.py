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


def save_raw_data(
    match_data_iterator: Iterator,
    player_name: str,
    filepath: str = r"apps/data/raw_data/",
):
    os.makedirs(f"{filepath}{player_name}/game_data")
    os.makedirs(f"{filepath}{player_name}/time_line_data")
    for game_data, time_line_data, _ in match_data_iterator:
        with open(
            file=filepath
            + player_name
            + "/game_data/"
            + game_data["metadata"]["matchId"]
            + ".json",
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(game_data, indent=4))

        with open(
            file=filepath
            + player_name
            + "/time_line_data/"
            + game_data["metadata"]["matchId"]
            + ".json",
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(time_line_data, indent=4))


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

    match_data_iterator = game_data_fetcher.create_match_data_iterator(
        lolwatcher=lolwatcher,
        summoner_name=summoner_name,
        tagline=tagline,
        server=server,
        queue=queue,
        number_of_games=number_of_games,
        till_season_patch=till_season_patch,
    )

    if not debug:
        df = game_data_extractor.create_dataframe(match_data_iterator)
        df = data_processor.process_dataframe(df)
        df.to_parquet(f"apps/data/dataframes/{player_name}.parquet")
    else:
        save_raw_data(match_data_iterator=match_data_iterator, player_name=player_name)


if __name__ == "__main__":
    input_values = {
        "summoner_name": "정신력남자",
        "tagline": "KR1",
        "server": "KR",
        "queue": constants.Queue.RANKED,
        "number_of_games": 45,
        "till_season_patch": constants.Patch(13, 1),
        "debug": True,
        "player_name": "NowayKR",
    }

    start = time.time()

    main(**input_values)

    end = time.time()
    diff = end - start
    print(f"Execution Time: {int(diff // 60)} Minutes and {int(diff % 60)} Seconds.")
