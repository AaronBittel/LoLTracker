from apps.backend.src.game_data_fetcher import create_game_data_generator, extract_match_patch
from apps.backend.src.constants import  SeasonPatch


def main():

    summoner_name = "TRM%20BROSES"
    server = "EUW1"
    number_of_games = 10
    till_season_patch = SeasonPatch(13, 1)

    match_info_generator, puuid = create_game_data_generator(
        summoner_name=summoner_name,
        server=server,
        number_of_games=number_of_games,
        till_season_patch=till_season_patch
    )

    for i, match_data in enumerate(match_info_generator):
        participant_index = match_data["metadata"]["participants"].index(puuid)
        print(
            i + 1,
            extract_match_patch(match_data),
            match_data["info"]["participants"][participant_index]["championName"],
            match_data["info"]["gameDuration"] // 60
        )


if __name__ == "__main__":
    main()