from apps.backend.src.helper import constants


def get_data(game_data: dict, columns: list[str]):
    return {col: game_data[col] for col in columns}


def get_lane_opponent(participants_game_data: list[dict], participant_index: int):
    player_team_position = participants_game_data[participant_index]["teamPosition"]
    for index, participant in enumerate(participants_game_data):
        if index == participant_index:
            continue
        if player_team_position == participant["teamPosition"]:
            return {"laneOpponent": participant["championName"]}
    return {"laneOpponent": None}


def get_champions_played(participants_game_data: list[dict]):
    return {
        role: participant["championName"]
        for role, participant in zip(
            constants.ROLES_PICK_COLUMNS, participants_game_data
        )
    }


def get_champions_played_ally_team_first(
    participants_game_data: list[dict], team_id: int
):
    if team_id == 100:
        team_order = constants.ALLY_TEAM_PICKS + constants.ENEMY_TEAM_PICKS
    else:
        team_order = constants.ENEMY_TEAM_PICKS + constants.ALLY_TEAM_PICKS
    return {
        team_role: participant["championName"]
        for team_role, participant in zip(team_order, participants_game_data)
    }


def get_champions_banned(game_info_data: dict):
    champion_bans = []
    for ban in game_info_data["teams"][0]["bans"] + game_info_data["teams"][1]["bans"]:
        champion_id = ban["championId"]
        champion_name = constants.ID_CHAMPION_MAPPING.get(champion_id, "NoBan")
        champion_bans.append(champion_name)

    return {
        role: champion_name
        for role, champion_name in zip(constants.ROLES_BAN_COLUMNS, champion_bans)
    }


def get_champions_banned_ally_team_first(game_info_data: dict, team_id: int):
    champion_bans = []
    for ban in game_info_data["teams"][0]["bans"] + game_info_data["teams"][1]["bans"]:
        champion_id = ban["championId"]
        champion_name = constants.ID_CHAMPION_MAPPING.get(champion_id, "NoBan")
        champion_bans.append(champion_name)

    if team_id == 100:
        team_order = constants.ALLY_TEAM_BANS + constants.ENEMY_TEAM_BANS
    else:
        team_order = constants.ENEMY_TEAM_BANS + constants.ALLY_TEAM_BANS
    return {
        team_role: champion_name
        for team_role, champion_name in zip(team_order, champion_bans)
    }


def get_puuid_to_look_out_for(
    participants_list: list[str], puuids: dict[str, str], player_puuid: str
):
    return {
        name: (puuid in participants_list)
        for name, puuid in puuids.items()
        if player_puuid != puuid
    }


def get_ally_team_kills_deaths(participants_game_data: list[dict], team_id: int):
    if team_id == 100:
        start, end = 0, 5
    else:
        start, end = 5, 10
    return {
        "totalAllyTeamKills": sum(
            participants_game_data[i]["kills"] for i in range(start, end)
        ),
        "totalAllyTeamDeaths": sum(
            participants_game_data[i]["deaths"] for i in range(start, end)
        ),
    }


def get_participants_puuids(match_meta_data: dict, puuid: str):
    return {
        f"participant{i}": participant_puuid
        for i, participant_puuid in enumerate(match_meta_data["participants"], start=1)
        if participant_puuid != puuid
    }
