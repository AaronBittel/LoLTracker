import pandas as pd
from apps.old.old_v2.backend import game_data_fetcher, time_line_processor, match_data_processor
from apps.backend.src.helper import constants
from apps.helper import helper
from riotwatcher import LolWatcher

from typing import Generator


def create_dataframe(match_data_generator: Generator) -> pd.DataFrame:
    all_match_data_list = []
    for match_data, time_line_data in match_data_generator:
        match_data_dict = match_data_processor.get_info(match_data)
        time_line_dict = time_line_processor.get_info(time_line)
        match_data_dict.update(time_line_dict)
        all_match_data_list.append(match_data_dict)
    return pd.DataFrame(all_match_data_list, columns=all_match_data_list[0].keys())


if __name__ == "__main__":
    input_values = {
        "summoner_name": "TRM%20BROSES",
        "server": "EUW1",
        "queue": constants.Queue.RANKED,
        "number_of_games": 1,
        "till_season_patch": constants.Patch(13, 1),
    }

    api_key = helper.get_api_key_from_file()
    watcher = LolWatcher(api_key=api_key)

    match_data_generator = game_data_fetcher.create_match_data_generator(
        lolwatcher=watcher, **input_values
    )

    df = create_dataframe(match_data_generator)
