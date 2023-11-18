from apps.backend.src import game_data_fetcher
from apps.backend.src import constants
from apps.backend.src import data_processor
from apps.backend.src import data_clean_up
from apps.helper import helper

import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG, filename="logging.txt", filemode="w")


def main():
    summoner_name = "Don%20Noway"  # 정신력남자
    server = "EUW1"
    queue = constants.Queue.RANKED
    number_of_games = 10
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

    data_clean_up.convert_unix_timestamp_ms_to_datetime(df=df, cols=["gameCreation", "gameEndTimestamp"])
    data_clean_up.convert_game_version_to_patch(df=df, col="gameVersion")
    data_clean_up.convert_team_position_utility_to_support(df=df, cols=["teamPosition"])
    df["gameDuration_m_s"] = df["gameDuration"].apply(helper.convert_seconds_to_minutes_and_seconds)
    df.set_index("matchId", inplace=True)

    df.to_parquet(path=r"C:\Users\AaronWork\Projects\LoLTracker\apps\data\NowayEUW.parquet")


if __name__ == "__main__":
    main()
