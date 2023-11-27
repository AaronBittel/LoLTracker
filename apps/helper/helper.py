import time
import datetime


UNIX_TIMESTAMP_START = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def get_api_key_from_file():
    file_name = r"..\..\..\..\..\api_key.txt"
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
