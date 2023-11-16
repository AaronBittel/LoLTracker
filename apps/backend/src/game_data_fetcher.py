import riotwatcher
from apps.backend.src import constants
from apps.helper import helper


def get_match_list(
        lolwatcher: riotwatcher.LolWatcher,
        region: str, puuid: str,
        number_of_games: int,
        queue: constants.Queue):

    match_list = []

    if number_of_games is None:
        number_of_games = 2000

    count = 100 if number_of_games > 100 else number_of_games

    for i in range((number_of_games // constants.MAX_GAME_COUNT) + 1):
        current_len = len(match_list)
        match_list.extend(lolwatcher.match.matchlist_by_puuid(
            region=region,
            puuid=puuid,
            start=i*constants.MAX_GAME_COUNT,
            count=count,
            queue=queue.value)
        )
        # Break when no games where added by latest match_list_by_puuid call
        if current_len == len(match_list):
            break

    return match_list


def main():
    server = "EUW1"
    summoner_name = "Don%20Noway"

    api_key = helper.get_api_key_from_file()
    watcher = riotwatcher.LolWatcher(api_key=api_key)
    puuid = watcher.summoner.by_name(region=server, summoner_name=summoner_name)["puuid"]

    match_list = get_match_list(
        lolwatcher=watcher,
        region="EUROPE",
        puuid=puuid,
        number_of_games=constants.ALL_GAMES,
        queue=constants.Queue.RANKED)

    print(puuid)
    print(len(match_list))


if __name__ == "__main__":
    main()
