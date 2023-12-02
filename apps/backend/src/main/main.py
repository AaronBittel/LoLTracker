import logging
import time
import os
import pandas as pd

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
    operation: constants.Operation,
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

    player_directory_name = (
        "test_data" if test_data else summoner_name.replace(" ", "_")
    )

    game_mode_directory_name = queue.name.capitalize()

    match operation:
        case constants.Operation.GET_DATA_FROM_API:
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
            df.to_parquet(f"apps/data/dataframes/{player_directory_name}.parquet")

        case constants.Operation.SAVE_RAW_DATA_TO_FILE:
            if os.path.exists(
                rf"apps/data/raw_data/{player_directory_name}/{game_mode_directory_name}"
            ):
                logging.debug(f"len match_list before: {len(match_list)}")
                match_list = helper.remove_already_stored_match_ids(
                    player_directory_name=player_directory_name,
                    game_mode_directory_name=game_mode_directory_name,
                    match_list=match_list,
                )

                if len(match_list) == 0:
                    return

                logging.debug(
                    f"Match list after removing already added ones: {match_list}"
                )

                logging.debug(f"len match_list after: {len(match_list)}")

            match_data_iterator = game_data_fetcher.create_match_data_iterator(
                lolwatcher=lolwatcher,
                match_list=match_list,
                region=region,
                till_season_patch=till_season_patch,
            )

            helper.save_raw_data(
                match_data_iterator=match_data_iterator,
                player_directory_name=player_directory_name,
                game_mode_directory_name=game_mode_directory_name,
            )
        case constants.Operation.GET_DATA_FROM_FILE:
            if os.path.exists(
                rf"apps/data/raw_data/{player_directory_name}/{game_mode_directory_name}"
            ):
                logging.debug(f"len match_list before: {len(match_list)}")
                match_list_in_file = helper.get_all_games_in_local(
                    player_directory_name=player_directory_name,
                    game_mode_directory_name=game_mode_directory_name,
                    match_list=match_list,
                )

                match_data_iterator = game_data_fetcher.local_game_data_fetcher(
                    filepath=rf"apps/data/raw_data/{player_directory_name}/{game_mode_directory_name}",
                    match_list=match_list_in_file,
                )

                file_df = game_data_extractor.create_dataframe(
                    game_data_iterator=match_data_iterator, puuid=puuid
                )
                file_df = data_processor.process_dataframe(file_df)

                if len(match_list) == len(match_list_in_file):
                    file_df.to_parquet(
                        f"apps/data/dataframes/{player_directory_name}.parquet"
                    )
                else:
                    match_list_to_add = helper.order_preserving_difference(
                        match_list, match_list_in_file
                    )

                    match_data_iterator = game_data_fetcher.create_match_data_iterator(
                        lolwatcher=lolwatcher,
                        match_list=match_list_to_add,
                        region=region,
                        till_season_patch=till_season_patch,
                    )

                    api_df = game_data_extractor.create_dataframe(
                        game_data_iterator=match_data_iterator, puuid=puuid
                    )
                    api_df = data_processor.process_dataframe(api_df)
                    pd.concat([file_df, api_df]).sort_values(
                        by="gameCreation", ascending=False
                    ).to_parquet(
                        f"apps/data/dataframes/{player_directory_name}.parquet"
                    )

            else:
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
                df.to_parquet(f"apps/data/dataframes/{player_directory_name}.parquet")


if __name__ == "__main__":
    input_values = {
        "summoner_name": "정신력남자",
        "tagline": "KR1",
        "server": "KR",
        "queue": constants.Queue.RANKED,
        "number_of_games": 340,
        "till_season_patch": constants.Patch(13, 19),
        "operation": constants.Operation.GET_DATA_FROM_FILE,
        "test_data": False,
    }

    start = time.time()

    main(**input_values)

    end = time.time()
    diff = end - start
    print(f"Execution Time: {int(diff // 60)} Minutes and {int(diff % 60)} Seconds.")
