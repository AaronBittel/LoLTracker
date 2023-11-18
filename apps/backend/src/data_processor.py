from apps.backend.src import constants


def get_data(game_data: dict, columns: list[str]):
    return {col: game_data[col] for col in columns}


def get_lane_opponent(participants_game_data: list[dict], participant_index: int):
    player_team_position = participants_game_data[participant_index]["teamPosition"]
    for index, participant in enumerate(participants_game_data):
        if index == participant_index:
            continue
        if player_team_position == participant["teamPosition"]:
            return {"laneOpponent": participant["championName"]}


def get_champions_played(participants_game_data: list[dict]):
    return {role: participant["championName"]
            for role, participant
            in zip(constants.ROLES_PICK_COLUMNS, participants_game_data)
    }


def get_champions_banned(game_info_data: dict):
    champion_bans = []
    for ban in game_info_data["teams"][0]["bans"] + game_info_data["teams"][1]["bans"]:
        champion_id = ban["championId"]
        champion_name = constants.ID_CHAMPION_MAPPING.get(champion_id, "NoBan")
        champion_bans.append(champion_name)

    return {role: champion_name for role, champion_name in zip(constants.ROLES_BAN_COLUMNS, champion_bans)}
