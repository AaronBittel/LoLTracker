from apps.backend.src import game_data_fetcher
from apps.backend.src import constants
from apps.backend.src import data_processor
from apps.backend.src import data_clean_up

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename="../logging/logging.txt", filemode="w")


def main():
    summoner_name = "정신력남자"
    server = "KR"
    queue = constants.Queue.RANKED
    number_of_games = 10
    till_season_patch = constants.Patch(12, 1)

    path = r"C:\Users\AaronWork\Projects\LoLTracker\apps\data\test_data.parquet"

    match_info_generator, puuid = game_data_fetcher.create_game_data_generator(
        summoner_name=summoner_name,
        server=server,
        queue=queue,
        number_of_games=number_of_games,
        till_season_patch=till_season_patch,
    )

    players_to_search = [
        name
        for name, player_puuid in constants.PLAYERS.items()
        if player_puuid != puuid
    ]

    player_data_list = []
    for i, game_data in enumerate(match_info_generator, start=1):
        player_data = {}

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
            data_processor.get_blue_team_kills_deaths(
                game_data["info"]["participants"], player_data["teamId"]
            )
        )

        logging.debug(f"Added {player_data}")
        player_data_list.append(player_data)
        print(f"{i} Games")

    df = pd.DataFrame(
        data=player_data_list,
        columns=(
            constants.META_DATA_COLUMNS
            + constants.INFO_DATA_COLUMNS
            + [
                "laneOpponent",
                "gameDuration_m_s",
                "totalAllyTeamKills",
                "totalAllyTeamDeaths",
            ]
            + players_to_search
            + constants.PARTICIPANT_DATA_COLUMNS
            # + constants.ROLES_PICK_COLUMNS
            + constants.ALLY_TEAM_PICKS
            + constants.ENEMY_TEAM_PICKS
            # + constants.ROLES_BAN_COLUMNS
            + constants.ALLY_TEAM_BANS
            + constants.ENEMY_TEAM_BANS
        ),
    )

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
    filt = df["gameDuration"] <= 5 * 60
    logging.info(f"{filt.sum()} games removed because of remakes.")
    df = df[~filt]

    data_clean_up.add_column_on_blue_side(df)

    df.to_parquet(path=path)


if __name__ == "__main__":
    main()
