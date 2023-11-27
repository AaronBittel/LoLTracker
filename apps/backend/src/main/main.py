from riotwatcher import LolWatcher

from apps.backend.src import game_data_fetcher
from apps.backend.src import game_data_extractor
from apps.helper import helper
from apps.backend.src import constants
from apps.backend.src import data_processor


def main(
    summoner_name: str,
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
        server=server,
        queue=queue,
        number_of_games=number_of_games,
        till_season_patch=till_season_patch,
    )

    df = game_data_extractor.create_dataframe(match_data_iterator)

    df = data_processor.process_dataframe(df)

    df.to_parquet("apps/data/test_data.parquet")


if __name__ == "__main__":
    input_values = {
        "summoner_name": "Don Noway",
        "server": "EUW1",
        "queue": constants.Queue.RANKED,
        "number_of_games": 5,
        "till_season_patch": constants.Patch(13, 1),
    }

    main(**input_values)
