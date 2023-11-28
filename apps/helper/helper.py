import time
import datetime


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
