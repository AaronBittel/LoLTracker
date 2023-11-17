import time
import datetime


def get_api_key_from_file():
    file_name = r"C:\Users\AaronWork\Projects\api_key.txt"
    with open(file_name, "r") as f:
        return f.read()


def datetime_to_unix_seconds(date: datetime) -> int:
    return int(time.mktime(date.timetuple()))


def convert_seconds_to_minutes_and_seconds(seconds: int) -> tuple[int, int]:
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return int(round(minutes, 0)), int(round(remaining_seconds, 0))
