import time

from riotwatcher import LolWatcher

from apps.backend.src.data_collection import game_data_fetcher
from apps.backend.src.data_extraction import game_data_extractor
from apps.helper import helper
from apps.backend.src.helper import constants
from apps.backend.src.data_processing import data_processor


def main(
    summoner_name: str,
    tagline: str,
    server: str,
    queue: constants.Queue,
    number_of_games: int,
    till_season_patch: constants.Patch,
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

    df = game_data_extractor.create_dataframe(match_data_iterator)

    df = data_processor.process_dataframe(df)

    df.to_parquet("apps/data/agurin.parquet")


if __name__ == "__main__":
    input_values = {
        "summoner_name": "Wufo",  # "정신력남자",
        "tagline": "xdd",
        "server": "EUW1",
        "queue": constants.Queue.RANKED,
        "number_of_games": 100,
        "till_season_patch": constants.Patch(13, 1),
    }

    start = time.time()

    main(**input_values)

    end = time.time()
    diff = end - start
    print(f"Execution Time: {int(diff // 60)} Minutes and {int(diff % 60)} Seconds.")
