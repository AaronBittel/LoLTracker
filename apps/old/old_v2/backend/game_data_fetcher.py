import logging
import riotwatcher
from apps.backend.src.helper import constants
from apps.helper import helper
from typing import NamedTuple


logging.basicConfig(level=logging.INFO, filename="../../../backend/logging/logging.txt", filemode="w")


def get_match_list(
    lolwatcher: riotwatcher.LolWatcher,
    region: str,
    puuid: str,
    number_of_games: int,
    queue: constants.Queue,
):
    match_list = []

    if number_of_games is None:
        number_of_games = 2000

    count = 100 if number_of_games > 100 else number_of_games

    for i in range((number_of_games // constants.MAX_GAME_COUNT) + 1):
        current_len = len(match_list)
        match_list.extend(
            lolwatcher.match.matchlist_by_puuid(
                region=region,
                puuid=puuid,
                start=i * constants.MAX_GAME_COUNT,
                count=count,
                queue=queue.value if queue is not None else None,
            )
        )
        # Break when no games where added by latest match_list_by_puuid call
        if current_len == len(match_list):
            logging.info(
                f"Games ({len(match_list)}), Stopped because no more games available."
            )
            break

        number_of_games -= 100
        if number_of_games < 100:
            count = number_of_games
            logging.info(
                f"Games ({len(match_list)}), Stopped because number_of_games reached."
            )

    return match_list


def get_match_data(
    lolwatcher: riotwatcher.LolWatcher,
    match_list: list[str],
    region: str,
    till_season_patch: NamedTuple,
):
    try:
        for index, match_id in enumerate(match_list):
            match_info = lolwatcher.match.by_id(region=region, match_id=match_id)
            match_info_patch = extract_match_patch(match_info)

            if match_info_patch < till_season_patch:
                logging.debug(
                    f"Games ({index + 1}), Stopped because till_season_patch reached."
                )
                break

            time_line = lolwatcher.match.timeline_by_match(
                region=region, match_id=match_id
            )

            yield match_info, time_line

    except riotwatcher.ApiError as err:
        if err.response.status_code == 429:
            print("We should retry in {} seconds.".format(err.headers["Retry-After"]))
        else:
            print(err)
            raise


def create_game_data_generator(
    summoner_name: str,
    server: str,
    queue: constants.Queue,
    number_of_games: int,
    till_season_patch: NamedTuple,
):
    region = constants.regions[server]
    api_key = helper.get_api_key_from_file()
    lolwatcher = riotwatcher.LolWatcher(api_key=api_key)
    puuid = lolwatcher.summoner.by_name(region=server, summoner_name=summoner_name)[
        "puuid"
    ]

    match_list = get_match_list(
        lolwatcher=lolwatcher,
        region=region,
        puuid=puuid,
        number_of_games=number_of_games,
        queue=queue,
    )

    match_info_generator = get_match_data(
        lolwatcher=lolwatcher,
        match_list=match_list,
        region=region,
        till_season_patch=till_season_patch,
    )

    return match_info_generator, puuid


def extract_match_patch(match_info: dict) -> NamedTuple:
    season, patch = match_info["info"]["gameVersion"].split(".")[:2]
    return constants.Patch(season=int(season), patch=int(patch))


def main():
    pass


if __name__ == "__main__":
    main()
