import requests
import datetime
import json
import helper
import riot_api_constants
import time


API_KEY = helper.get_api_key_from_file()


def get_puuid_by_summoner_name(server: str, summoner_name: str, api_key: str = API_KEY) -> str:
    summoner_info_response = requests.get(riot_api_constants.GET_SUMMONER_BY_NAME.format(server, summoner_name, api_key))
    
    if summoner_info_response.status_code != 200:
        return summoner_info_response
    
    return summoner_info_response.json()["puuid"]


def get_match_ids_by_puuid(region: str, puuid: str, api_key: str = API_KEY, startTime: int = None, endTime: int = None, queue: int = None, start: int = 0, count: int = 20):
    request_string = riot_api_constants.GET_MATCH_IDS_BY_PUUID_1.format(region, puuid)
    for param_name, param_value in {"startTime": startTime, "endTime": endTime, "queue": queue}.items():
        if param_value is None:
            continue
        request_string += f'{param_name}={param_value}&'

    request_string += riot_api_constants.GET_MATCH_IDS_BY_PUUID_2.format(start, count, api_key)
    
    match_ids_response = requests.get(request_string)

    if match_ids_response.status_code != 200:
        return match_ids_response.status_code
    
    return match_ids_response.json()


def get_match_data_by_match_id(region: str, match_id: str, api_key: str = API_KEY):
    match_data_response = requests.get(riot_api_constants.GET_MATCH_DATA_BY_MATCH_ID.format(region, match_id, api_key))

    if match_data_response.status_code != 200:
        return match_data_response.status_code

    return match_data_response.json()


def get_participant_index(puuid: str, match_data: dict) -> int:
    participants = match_data["metadata"]["participants"]
    return participants.index(puuid)


def get_player_data_by_participant_index(match_data: dict, participant_index: int) -> dict:
    return match_data["info"]["participants"][participant_index]


def get_lane_opponent(match_data: dict, player_team_position: str, player_puuid: str):
    for player_data in match_data["info"]["participants"]:

        if player_data["teamPosition"] == player_team_position and (player_data["puuid"] != player_puuid):
            return player_data


def main():
    time_wait = 80
    while time_wait >= 0:
        time.sleep(1)
        print(f"Starting in {time_wait}")
        time_wait -= 1

    server = "euw1"
    region = "europe"
    summoner_name = "정신력남자"
    # summoner_name = "짭짤한 왕자"
    summoner_name = "TRM%20BROSES"
    # summoner_name = "Don%20Noway"
    # summoner_name = "Curling%20Captain"
    # summoner_name = "die%20for%20it"
    # summoner_name = "Henrabar%20Mids"
    count = 53

    puuid = get_puuid_by_summoner_name(server, summoner_name)

    match_ids = get_match_ids_by_puuid(
        region=region,
        puuid=puuid,
        # startTime=helper.datetime_to_unix_seconds(datetime.datetime(2023, 10, 20)),
        # endTime=helper.datetime_to_unix_seconds(datetime.datetime(2023, 10, 30)),
        queue=riot_api_constants.RiotQueue.RANKED.value,
        start=0,
        count=count
    )

    # blue_side_count, blue_side_win, red_side_count, red_side_win = 0, 0, 0, 0
    # lane_opponent_count = {}
    # ally_champions_count = {}
    # enemy_champions_count = {}
    # game_ended_in_surrender_count = 0
    # game_won_with_inhibitors_down_count = 0
    # lose_game_without_inhibitors_down_count = 0
    # game_won_with_inhibitors_kill_count = 0
    # win_game_without_inhibitors_kill_count = 0

    game_time_in_wins_sum = 0.0
    wins_count = 0
    game_time_in_lose_sum = 0.0
    lose_count = 0

    for i, match_id in enumerate(match_ids):
        match_data = get_match_data_by_match_id(region=region, match_id=match_id)
        
        participant_index = get_participant_index(match_data=match_data, puuid=puuid)

        player_data = get_player_data_by_participant_index(match_data=match_data, participant_index=participant_index)

        if player_data["win"]:
            wins_count += 1
            game_time_in_wins_sum += match_data["info"]["gameDuration"]
        else:
            lose_count += 1
            game_time_in_lose_sum += match_data["info"]["gameDuration"]

        print(f'{int(round((i + 1) / count * 100, 0))} % Done.')

    average_win_time_m_s = helper.convert_seconds_to_minutes_and_seconds(game_time_in_wins_sum / wins_count)
    average_lose_time_m_s = helper.convert_seconds_to_minutes_and_seconds(game_time_in_lose_sum / lose_count)
    print(f"Average game time in wins: {average_win_time_m_s[0]} Minutes, {average_win_time_m_s[1]} Seconds")
    print(f"Average game time in lose: {average_lose_time_m_s[0]} Minutes, {average_lose_time_m_s[1]} Seconds")

        # if player_data["inhibitorsLost"] > 0 and player_data["win"] == True:
        #     game_won_with_inhibitors_down_count += 1

        # if player_data["inhibitorKills"] > 0 and player_data["win"] == True:
        #     game_won_with_inhibitors_kill_count += 1

        # if player_data["inhibitorsLost"] == 0 and player_data["win"] == False:
        #     lose_game_without_inhibitors_down_count += 1

        # if player_data["inhibitorKills"] == 0 and player_data["win"] == True:
        #     win_game_without_inhibitors_kill_count += 1

        # if player_data["gameEndedInSurrender"]:
        #     game_ended_in_surrender_count += 1

    # print(f"Lost inhibitors and won the game: {game_won_with_inhibitors_down_count}. Out of {len(match_ids)}. That makes {round(game_won_with_inhibitors_down_count / len(match_ids) * 100, 1)} %")
    # print(f"Killed inhibitors and won the game: {game_won_with_inhibitors_kill_count}. Out of {len(match_ids)}. That makes {round(game_won_with_inhibitors_kill_count / len(match_ids) * 100, 1)} %")
    # print(f"Lost games before inhibitors fell: {lose_game_without_inhibitors_down_count}. Out of {len(match_ids)}. That makes {round(lose_game_without_inhibitors_down_count / len(match_ids) * 100, 1)} %")
    # print(f"Win games without killing inhibitors: {win_game_without_inhibitors_kill_count}. Out of {len(match_ids)}. That makes {round(win_game_without_inhibitors_kill_count / len(match_ids) * 100, 1)} %")

    # print(f"{game_ended_in_surrender_count} Games Ended in Surrender out of {len(match_ids)}. That makes {round(game_ended_in_surrender_count / len(match_ids) * 100, 0)} %")
        # for category, value in player_data.items():
        #     if category == "challenges":
        #         continue
        #     print(category, value, sep="\t")
        
        # print(len(player_data))

        # player_team_position = player_data["teamPosition"]

    #     player_team_id = player_data["teamId"]

    #     all_participants = match_data["info"]["participants"]

    #     for participant in all_participants:
    #         if participant["puuid"] == puuid:
    #             continue
    #         if player_team_id == participant["teamId"]:
    #             if participant["championName"] in ally_champions_count:
    #                 ally_champions_count[participant["championName"]] += 1
    #             else:
    #                 ally_champions_count[participant["championName"]] = 1
    #         else:
    #             if participant["championName"] in enemy_champions_count:
    #                 enemy_champions_count[participant["championName"]] += 1
    #             else:
    #                 enemy_champions_count[participant["championName"]] = 1

    # print(f"Ally Team Champion Count: {ally_champions_count}")
    # print()
    # print(f"Enemy Team Champion Count: {enemy_champions_count}")
        # if player_team_position != "MIDDLE":
        #     continue

        # lane_opponent = get_lane_opponent(match_data, player_team_position, puuid)

        # lane_opponent_champion = lane_opponent["championName"]

        # if lane_opponent_champion in lane_opponent_count:
        #     lane_opponent_count[lane_opponent_champion] += 1
        # else:
        #     lane_opponent_count[lane_opponent_champion] = 1
    
    # print(lane_opponent_count)

    #     print(f'MatchUp: <{player_team_position}> {player_data["championName"]} vs {lane_opponent["championName"]}')
    #     if player_data["teamId"] == 100:
    #         blue_side_count += 1

    #         if player_data["win"] == 1:
    #             blue_side_win += 1

    #     else:
    #         red_side_count += 1

    #         if player_data["win"] == 1:
    #             red_side_win += 1


    # print(f'blue side: {blue_side_count} ({round(blue_side_count / count * 100, 0)} %), red side: {red_side_count} ({round(red_side_count / count * 100, 0)} %)')
    # print(f'blue side wr: {round(blue_side_win / blue_side_count * 100, 0)} %, red side wr: {round(red_side_win / red_side_count * 100, 0)} %')

if __name__ == '__main__':
    main()