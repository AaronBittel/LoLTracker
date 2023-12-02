from apps.backend.src.helper import constants


def get_total_gold_per_min(time_line: dict, participant_index: int, game_duration: int):
    lane_opponent_participant_index = (
        participant_index + 5 if participant_index <= 5 else participant_index - 5
    )

    total_gold_dict = {}
    gold_diff_dict = {}
    for i in range(game_duration):
        participant_frames = time_line["info"]["frames"][i]["participantFrames"]
        total_gold_dict[f"gold@{i}"] = participant_frames[str(participant_index)][
            "totalGold"
        ]
        gold_diff_dict[f"gold_diff@{i}"] = (
            total_gold_dict[f"gold@{i}"]
            - participant_frames[str(lane_opponent_participant_index)]["totalGold"]
        )

    total_gold_dict.update(gold_diff_dict)
    return total_gold_dict


def get_cs_per_min(time_line: dict, participant_index: int, game_duration: int):
    cs = {}
    for i in range(game_duration):
        participant = time_line["info"]["frames"][i]["participantFrames"][
            str(participant_index)
        ]
        cs[f"cs@{i}"] = (
            participant["jungleMinionsKilled"] + participant["minionsKilled"]
        )

    return cs


def get_early_death(time_line: dict, participant_index: int, till_minute: int):
    for frame in time_line["info"]["frames"][: (till_minute + 1)]:
        for event in frame["events"]:
            if (
                event["type"] == "CHAMPION_KILL"
                and event["victimId"] == participant_index
            ):
                return {f"deathBeforeMin{till_minute}": True}
    return {f"deathBeforeMin{till_minute}": False}


def get_total_team_gold_diff(
    time_line: dict, participant_index: int, at: list[int] = None
):
    game_duration = time_line["info"]["frames"][-1]["timestamp"] / 60000

    total_team_gold_diff_at_minutes = {}

    at = [5, 10, 15, 20] if at is None else at

    at = [minute for minute in at if minute <= game_duration]

    for minute in at:
        ally_team_total_gold = 0
        enemy_team_total_gold = 0

        frame = time_line["info"]["frames"][
            minute
        ]  # no + 1 needed because index starts at 0
        for i in range(1, 6):
            if participant_index <= 5:
                ally_team_total_gold += frame["participantFrames"][str(i)]["totalGold"]
                enemy_team_total_gold += frame["participantFrames"][str(i + 5)][
                    "totalGold"
                ]
            else:
                ally_team_total_gold += frame["participantFrames"][str(i + 5)][
                    "totalGold"
                ]
                enemy_team_total_gold += frame["participantFrames"][str(i)]["totalGold"]

        total_team_gold_diff_at_minutes[f"totalTeamGoldDiff@{minute}"] = (
            ally_team_total_gold - enemy_team_total_gold
        )

    return total_team_gold_diff_at_minutes


def get_seconds_of_first_successful_jungle_gank(time_line: dict):
    junglers_indexes = [
        constants.TIME_LINE_BLUE_SIDE_JUNGLER_INDEX,
        constants.TIME_LINE_RED_SIDE_JUNGLER_INDEX,
    ]
    for frame in time_line["info"]["frames"]:
        for event in frame["events"]:
            if (
                event["type"] == "CHAMPION_KILL"
                and "assistingParticipantIds" in event.keys()
            ) and (
                event["killerId"] in junglers_indexes
                or any(
                    jungler_index in event["assistingParticipantIds"]
                    for jungler_index in junglers_indexes
                )
            ):
                minutes_decimal = event["timestamp"] / 60000

                if minutes_decimal <= constants.MINUTE_2:
                    continue

                minutes = int(minutes_decimal)
                seconds = int((minutes_decimal - minutes) * 60)
                return {"firstSuccessfulJunglerGank_s": minutes * 60 + seconds}
    return {"remake": True}


def get_total_kills_at_minutes(time_line: dict, at: list[int] = None):
    game_duration = time_line["info"]["frames"][-1]["timestamp"] / 60000

    total_kills_at_minutes = {}

    at = [5, 10, 15, 20] if at is None else at
    at = [minute for minute in at if minute <= game_duration]

    total_kills = 0

    for minute, frame in enumerate(time_line["info"]["frames"]):
        for event in frame["events"]:
            if event["type"] == "CHAMPION_KILL":
                total_kills += 1
        if minute in at:
            total_kills_at_minutes[f"totalKillsAtMinute{minute}"] = total_kills

    return total_kills_at_minutes
