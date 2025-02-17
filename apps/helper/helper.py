import time
import datetime
import os
import json
from typing import Iterator

from apps.backend.src.helper import constants


UNIX_TIMESTAMP_START = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def get_api_key_from_file():
    file_name = r"..\api_key.txt"
    with open(file_name, "r") as f:
        return f.read()


def datetime_to_unix_seconds(date: datetime) -> int:
    return int(time.mktime(date.timetuple()))


def convert_unix_to_datetime(timestamp_ms: int):
    timestamp_sec = timestamp_ms / 1000.0
    return UNIX_TIMESTAMP_START + datetime.timedelta(seconds=timestamp_sec)


def convert_seconds_to_minutes_and_seconds(seconds: int) -> datetime.time:
    minutes = seconds // 60
    hours = minutes // 60
    remaining_seconds = seconds % 60

    return datetime.time(hour=hours, minute=minutes, second=remaining_seconds)


def print_progress_bar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    print_end="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)

    print(f"\r{prefix} |{bar}| ({iteration} Games) {percent}% {suffix}", end=print_end)

    # Print New Line on Complete
    if iteration == total:
        print()


def print_timestamp_in_minutes_and_seconds(time_stamp):
    time_stamp = time_stamp / 60000
    minutes = int(time_stamp)
    seconds = int((time_stamp - minutes) * 60)
    print(f"in game time: {minutes}:{seconds}")


def save_raw_data(
    match_data_iterator: Iterator,
    player_directory_name: str,
    game_mode_directory_name: str,
    filepath: str = r"apps/data/raw_data/",
):
    if not os.path.exists(
        rf"apps/data/raw_data/{player_directory_name}/{game_mode_directory_name}"
    ):
        os.makedirs(
            f"{filepath}{player_directory_name}/{game_mode_directory_name}/game_data"
        )
        os.makedirs(
            f"{filepath}{player_directory_name}/{game_mode_directory_name}/time_line_data"
        )

    for game_data, time_line_data in match_data_iterator:
        match_id = game_data["metadata"]["matchId"]

        if check_if_data_already_saved(
            player_name=player_directory_name,
            game_mode_directory_name=game_mode_directory_name,
            match_id=match_id,
        ):
            continue

        with open(
            file=f"{filepath}{player_directory_name}/{game_mode_directory_name}/game_data/{match_id}.json",
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(game_data, indent=4))

        with open(
            file=f"{filepath}{player_directory_name}/{game_mode_directory_name}/time_line_data/{match_id}.json",
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(time_line_data, indent=4))


def check_if_data_already_saved(
    player_name: str,
    game_mode_directory_name: str,
    match_id: str,
    filepath: str = r"apps/data/raw_data/",
):
    return (match_id + ".json") in os.listdir(
        f"{filepath}{player_name}/{game_mode_directory_name}/game_data"
    )


def remove_already_stored_match_ids(
    player_directory_name: str, game_mode_directory_name: str, match_list: list[str]
):
    all_match_ids = [
        match_id.replace(".json", "")
        for match_id in os.listdir(
            rf"apps/data/raw_data/{player_directory_name}/{game_mode_directory_name}/game_data"
        )
    ]

    return [match_id for match_id in match_list if match_id not in all_match_ids]


def get_all_games_in_local(
    player_directory_name: str, game_mode_directory_name: str, match_list: list[str]
):
    match_ids_in_file = [
        match_id.replace(".json", "")
        for match_id in os.listdir(
            rf"apps/data/raw_data/{player_directory_name}/{game_mode_directory_name}/game_data"
        )
    ]

    return [match_id for match_id in match_list if match_id in match_ids_in_file]


def order_preserving_difference(list1, list2):
    return [x for x in list1 if x not in list2]
