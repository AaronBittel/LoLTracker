from apps.backend.src import game_data_fetcher
from apps.backend.src import constants
from apps.backend.src import data_processor

import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG, filename="logging.txt", filemode="w")


def main():
    summoner_name = "정신력남자"
    server = "KR"
    queue = constants.Queue.RANKED
    number_of_games = 85
    till_season_patch = constants.Patch(13, 1)

    match_info_generator, puuid = game_data_fetcher.create_game_data_generator(
        summoner_name=summoner_name,
        server=server,
        queue=queue,
        number_of_games=number_of_games,
        till_season_patch=till_season_patch
    )

    player_data_list = []
    for i, game_data in enumerate(match_info_generator):
        player_data = {}
        player_data.update(
            data_processor.get_data(game_data=game_data["metadata"], columns=constants.META_DATA_COLUMNS))
        player_data.update(data_processor.get_data(game_data=game_data["info"], columns=constants.INFO_DATA_COLUMNS))

        participant_index = game_data["metadata"]["participants"].index(puuid)

        player_data.update(data_processor.get_data(
            game_data=game_data["info"]["participants"][participant_index],
            columns=constants.PARTICIPANT_DATA_COLUMNS)
        )

        player_data.update(data_processor.get_champions_played(game_data["info"]["participants"]))

        player_data.update(data_processor.get_lane_opponent(game_data["info"]["participants"], participant_index))

        player_data.update(data_processor.get_champions_banned(game_data["info"]))

        logging.debug(f"Added {player_data}")
        player_data_list.append(player_data)
        print(f"{i + 1} Games")

    df = pd.DataFrame(
        data=player_data_list,
        columns=(
                constants.META_DATA_COLUMNS +
                constants.INFO_DATA_COLUMNS +
                ["laneOpponent"] +
                constants.PARTICIPANT_DATA_COLUMNS +
                constants.ROLES_PICK_COLUMNS +
                constants.ROLES_BAN_COLUMNS
        )
    )

    df.to_parquet(path=r"C:\Users\AaronWork\Projects\LoLTracker\apps\data\test_data.parquet")


if __name__ == "__main__":
    main()
