from apps.backend.src import game_data_fetcher
from apps.backend.src import constants
from apps.backend.src import data_processor
from apps.backend.src import data_clean_up
from apps.backend.src import time_line_processor

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename="../logging/logging.txt", filemode="w")


def main():
    import time

    start = time.time()
    summoner_name = "Don%20Noway"
    server = "EUW1"
    queue = constants.Queue.RANKED
    number_of_games = 1
    till_season_patch = constants.Patch(12, 1)

    path = r"C:\Users\AaronWork\Projects\LoLTracker\apps\data\test_data.parquet"

    match_info_generator, puuid = game_data_fetcher.create_game_data_generator(
        summoner_name=summoner_name,
        server=server,
        queue=queue,
        number_of_games=number_of_games,
        till_season_patch=till_season_patch,
    )

    player_data_list = []

    for i, match_info in enumerate(match_info_generator, start=1):
        game_data, time_line = match_info
        player_data = {}

        generate_match_data(game_data, player_data, puuid)
        generate_match_time_line(time_line, player_data, puuid)

        logging.debug(f"Added {player_data}")
        player_data_list.append(player_data)
        print(f"{i} Games")

    df = pd.DataFrame(data=player_data_list, columns=list(player_data_list[0].keys()))

    data_clean_up.convert_unix_timestamp_ms_to_datetime(
        df=df, cols=["gameCreation", "gameEndTimestamp"]
    )
    data_clean_up.convert_game_version_to_patch(df=df, col="gameVersion")
    data_clean_up.convert_team_position_utility_to_support(df=df, cols=["teamPosition"])
    df["gameDuration_m_s"] = pd.to_datetime(df["gameDuration"], unit="s").dt.strftime(
        "%M:%S"
    )
    df.set_index("matchId", inplace=True)

    # drop all remake games
    filt = df["gameDuration"] <= constants.REMAKE_GAME_DURATION_THRESHOLD
    logging.info(f"{filt.sum()} games removed because of remakes.")
    df = df[~filt]

    data_clean_up.add_column_on_blue_side(df)

    df.to_parquet(path=path)
    end = time.time()
    seconds = end - start
    print(f"{int(seconds // 60)} minutes {int(seconds % 60)} seconds")


def generate_match_data(
    game_data: dict, player_data: dict[str, str | int | bool], puuid: str
):
    player_data.update(
        data_processor.get_data(
            game_data=game_data["metadata"], columns=constants.META_DATA_COLUMNS
        )
    )
    player_data.update(
        data_processor.get_data(
            game_data=game_data["info"], columns=constants.INFO_DATA_COLUMNS
        )
    )
    participant_index = game_data["metadata"]["participants"].index(puuid)
    player_data.update(
        data_processor.get_data(
            game_data=game_data["info"]["participants"][participant_index],
            columns=constants.PARTICIPANT_DATA_COLUMNS,
        )
    )
    # player_data.update(
    #    data_processor.get_champions_played(game_data["info"]["participants"])
    # )
    player_data.update(
        data_processor.get_champions_played_ally_team_first(
            participants_game_data=game_data["info"]["participants"],
            team_id=player_data["teamId"],
        )
    )
    player_data.update(
        data_processor.get_lane_opponent(
            game_data["info"]["participants"], participant_index
        )
    )
    # player_data.update(data_processor.get_champions_banned(game_data["info"]))
    player_data.update(
        (
            data_processor.get_champions_banned_ally_team_first(
                game_info_data=game_data["info"], team_id=player_data["teamId"]
            )
        )
    )
    player_data.update(
        data_processor.get_puuid_to_look_out_for(
            participants_list=game_data["metadata"]["participants"],
            puuids=constants.PLAYERS,
            player_puuid=puuid,
        )
    )
    player_data.update(
        data_processor.get_ally_team_kills_deaths(
            game_data["info"]["participants"], player_data["teamId"]
        )
    )


def generate_match_time_line(
    time_line: dict, player_data: dict[str, str | int | bool], puuid: str
):
    participant_index = (
        time_line["metadata"]["participants"].index(puuid) + 1
    )  # + 1 because index starts at 1
    # game_duration = int(time_line["info"]["frames"][-1]["timestamp"] / 60000) + 1
    game_duration = len(time_line["info"]["frames"])

    player_data.update(
        time_line_processor.get_total_gold_per_min(
            time_line=time_line,
            participant_index=participant_index,
            game_duration=game_duration,
        )
    )

    player_data.update(
        time_line_processor.get_cs_per_min(
            time_line=time_line,
            participant_index=participant_index,
            game_duration=game_duration,
        )
    )


if __name__ == "__main__":
    main()
