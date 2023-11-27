import logging
import pandas as pd

from typing import Iterator
from apps.backend.src.data_extraction import match_data_extractor
from apps.backend.src.data_extraction import time_line_data_extractor
from apps.backend.src.helper import constants


logging.basicConfig(
    level=logging.DEBUG, filename="../../logging/logging.txt", filemode="w"
)


def create_dataframe(game_data_iterator: Iterator) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                **extract_match_data(match_data=match_data, puuid=puuid),
                **extract_time_line_data(time_line_data=time_line_data, puuid=puuid),
                "puuid": puuid,
            }
            for match_data, time_line_data, puuid in game_data_iterator
        ]
    )


def extract_match_data(match_data: dict, puuid: str) -> dict[str, str | int | bool]:
    player_data = {}

    player_data.update(
        match_data_extractor.get_data(
            game_data=match_data["metadata"], columns=constants.META_DATA_COLUMNS
        )
    )
    player_data.update(
        match_data_extractor.get_data(
            game_data=match_data["info"], columns=constants.INFO_DATA_COLUMNS
        )
    )
    participant_index = match_data["metadata"]["participants"].index(puuid)
    player_data.update(
        match_data_extractor.get_data(
            game_data=match_data["info"]["participants"][participant_index],
            columns=constants.PARTICIPANT_DATA_COLUMNS,
        )
    )

    player_data.update(
        match_data_extractor.get_champions_played_ally_team_first(
            participants_game_data=match_data["info"]["participants"],
            team_id=player_data["teamId"],
        )
    )
    player_data.update(
        match_data_extractor.get_lane_opponent(
            match_data["info"]["participants"], participant_index
        )
    )

    player_data.update(
        (
            match_data_extractor.get_champions_banned_ally_team_first(
                game_info_data=match_data["info"], team_id=player_data["teamId"]
            )
        )
    )
    player_data.update(
        match_data_extractor.get_puuid_to_look_out_for(
            participants_list=match_data["metadata"]["participants"],
            puuids=constants.PLAYERS,
            player_puuid=puuid,
        )
    )
    player_data.update(
        match_data_extractor.get_ally_team_kills_deaths(
            match_data["info"]["participants"], player_data["teamId"]
        )
    )

    logging.debug("Successfully extracted match data")

    return player_data


def extract_time_line_data(time_line_data: dict, puuid: str) -> dict[str, str | int]:
    player_time_line_data = {}

    participant_index = (
        time_line_data["metadata"]["participants"].index(puuid) + 1
    )  # + 1 because index starts at 1
    game_duration = len(time_line_data["info"]["frames"])

    player_time_line_data.update(
        time_line_data_extractor.get_total_gold_per_min(
            time_line=time_line_data,
            participant_index=participant_index,
            game_duration=game_duration,
        )
    )

    player_time_line_data.update(
        time_line_data_extractor.get_cs_per_min(
            time_line=time_line_data,
            participant_index=participant_index,
            game_duration=game_duration,
        )
    )

    logging.debug("Successfully extracted time line data")

    return player_time_line_data
