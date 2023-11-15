import sys
sys.path.append(r"C:\Users\aaron\projects\lolTracker\apps\helper")

import riotwatcher
import constants
import helper


def get_match_list(lolwatcher: riotwatcher.LolWatcher, region: str, puuid: str, number_of_games: int, queue: constants.Queue):
    matchlist = []

    count = 100 if number_of_games > 100 else number_of_games

    for i in range((number_of_games // constants.MAX_GAME_COUNT) + 1):
        current_len = len(matchlist)
        matchlist.extend(lolwatcher.match.matchlist_by_puuid(region=region, puuid=puuid, start=i*constants.MAX_GAME_COUNT, count=count, queue=queue.value))
        # Break when no games where added by latest matchlist_by_puuid call
        if current_len == len(matchlist):
            break

    return matchlist


def main():
    server = "EUW1"
    summoner_name = "TRM%20BROSES"

    API_KEY = helper.get_api_key_from_file()
    lolwatcher = riotwatcher.LolWatcher(api_key=API_KEY)
    puuid = lolwatcher.summoner.by_name(region=server, summoner_name=summoner_name)["puuid"]

    print(puuid)

if __name__ == "__main__":
    main()
