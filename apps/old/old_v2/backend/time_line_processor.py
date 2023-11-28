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
