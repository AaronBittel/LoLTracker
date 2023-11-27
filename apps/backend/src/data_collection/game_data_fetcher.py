import logging

import riotwatcher
from riotwatcher import LolWatcher
from apps.backend.src.helper import constants
from apps.helper import helper
from typing import Iterator


logging.basicConfig(
    level=logging.DEBUG, filename="apps/backend/logging/logging.txt", filemode="w"
)


def get_match_ids(
    lolwatcher: LolWatcher,
    region: str,
    puuid: str,
    number_of_games: int,
    queue: constants.Queue,
):
    """
    Returns a list of match ids of the player with the puuid in the server. The list of match ids consists of specified
    number of games, if there are that many available

    Args:
        lolwatcher: riotwatcher API
        region: region of the player
        puuid: puuid of the player
        number_of_games: number of games to fetch
        queue: game mode

    Returns:
        list of match ids

    """
    match_ids = []

    if number_of_games is None:
        number_of_games = 2000

    count = 100 if number_of_games > 100 else number_of_games

    for i in range((number_of_games // constants.MAX_GAME_COUNT) + 1):
        current_len = len(match_ids)
        match_ids.extend(
            lolwatcher.match.matchlist_by_puuid(
                region=region,
                puuid=puuid,
                start=i * constants.MAX_GAME_COUNT,
                count=count,
                queue=queue.value if queue is not None else None,
            )
        )
        # Break when no games where added by latest match_list_by_puuid call
        if current_len == len(match_ids):
            logging.info(
                f"Games ({len(match_ids)}), Stopped because no more games available."
            )
            break

        number_of_games -= 100
        if number_of_games < 100:
            count = number_of_games
            logging.info(
                f"Games ({len(match_ids)}), Stopped because number_of_games ({number_of_games}) reached."
            )

    logging.info(f"Match ids Length: {len(match_ids)}")

    return match_ids


def get_match_data(
    lolwatcher: LolWatcher,
    match_id: str,
    region: str,
    till_season_patch: constants.Patch,
) -> dict | None:
    """
    Returns the match data of a given match id.

    Args:
        lolwatcher: riotwatcher API
        match_id: match id of game
        region: region of player
        till_season_patch: patch (stop criteria)

    Returns:
        Returns the match data of a given match id. If patch of match data is earlier then given patch
        (till_season_patch), returns None.

    """
    try:
        match_info = lolwatcher.match.by_id(region=region, match_id=match_id)
        match_info_patch = extract_match_patch(match_info)

        if match_info_patch < till_season_patch:
            logging.debug(f"Stopped because till_season_patch reached.")
            return None

        return match_info

    except riotwatcher.ApiError as err:
        if err.response.status_code == 429:
            logging.debug(
                "We should retry in {} seconds.".format(err.headers["Retry-After"])
            )
        else:
            logging.debug(err)
            raise


def get_time_line_data(
    lolwatcher: riotwatcher.LolWatcher,
    match_id: str,
    region: str,
) -> dict | None:
    """
    Returns the timeline data of a given match id.

    Args:
        lolwatcher: riotwatcher API
        match_id: match id of game
        region: region of player

    Returns:
        Returns the timeline data of a given match id.

    """
    try:
        return lolwatcher.match.timeline_by_match(region=region, match_id=match_id)

    except riotwatcher.ApiError as err:
        if err.response.status_code == 429:
            logging.debug(
                "We should retry in {} seconds.".format(err.headers["Retry-After"])
            )
        else:
            logging.debug(err)
            raise


def extract_match_patch(match_info: dict) -> constants.Patch:
    """
    Extracts patch of match info dict

    Args:
        match_info: match info dict

    Returns:
        Patch

    """
    season, patch = match_info["info"]["gameVersion"].split(".")[:2]
    return constants.Patch(season=int(season), patch=int(patch))


def get_puuid(lolwatcher: riotwatcher.LolWatcher, summoner_name: str, server: str):
    """
    Returns puuid of the account with summoner_name in server.

    Args:
        lolwatcher: riotwatcher API
        summoner_name: summoner name of player
        server: server of player

    Returns:
        puuid of player

    """
    return lolwatcher.summoner.by_name(region=server, summoner_name=summoner_name)[
        "puuid"
    ]


def map_server_to_region(server: str) -> str:
    """
    Maps the given server name to the region.

    Args:
        server: server of the player

    Returns:
        region that the server is on

    """
    return constants.regions[server]


def create_match_data_iterator(
    lolwatcher: riotwatcher.LolWatcher,
    summoner_name: str,
    server: str,
    queue: constants.Queue,
    number_of_games: int,
    till_season_patch: constants.Patch,
) -> Iterator:
    """
    Returns a generator that returns match data and timeline data.

    Args:
        lolwatcher: riotwatcher API
        summoner_name: summoner name of player
        server: server of player
        queue: game mode
        number_of_games: amount of games
        till_season_patch: patch (stop criteria)

    Returns:
        game data and timeline data as generator

    """
    estimated_execution_time_s = number_of_games // 2 + int(number_of_games * 2 / 100) * 100
    print(f"Estimated Time: {estimated_execution_time_s // 60} Minutes and {estimated_execution_time_s % 60} Seconds.")

    summoner_name = summoner_name.replace(" ", "%20")

    puuid = get_puuid(lolwatcher=lolwatcher, summoner_name=summoner_name, server=server)
    region = map_server_to_region(server=server)
    match_list = get_match_ids(
        lolwatcher=lolwatcher,
        region=region,
        puuid=puuid,
        number_of_games=number_of_games,
        queue=queue,
    )

    helper.print_progress_bar(iteration=12, total=234)

    for index, match_id in enumerate(match_list, start=1):
        helper.print_progress_bar(iteration=index, total=len(match_list))
        match_data = get_match_data(
            lolwatcher=lolwatcher,
            match_id=match_id,
            region=region,
            till_season_patch=till_season_patch,
        )
        if match_data is None:  # till_season_patch is reached
            logging.debug(f"Reached Patch {till_season_patch}, so data fetcher stopped")
            break
        time_line_data = get_time_line_data(
            lolwatcher=lolwatcher, match_id=match_id, region=region
        )

        yield constants.MatchData(match_data, time_line_data, puuid)
