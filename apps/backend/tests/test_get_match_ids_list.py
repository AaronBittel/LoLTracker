import pytest
from riotwatcher import LolWatcher
from apps.backend.src.data_collection import game_data_fetcher
from apps.backend.src.helper import constants
from apps.helper import helper


puuid = "Ojis3-jBDzeNHW325uynG8LlhWw5E1QqujrzHQy_w8GiFGvm1Cy4Dkk0H43hTVF7ifT3_ZwU7id-Zw"
server = "EUW1"


@pytest.fixture
def lolwatcher():
    # Set up any necessary objects or configurations for testing
    return LolWatcher(helper.get_api_key_from_file())


def test_get_match_list_returns_list(lolwatcher):
    result = game_data_fetcher.get_match_ids(
        lolwatcher, server, puuid, 5, constants.Queue.RANKED
    )
    assert isinstance(result, list)


def test_get_match_list_returns_correct_number_of_games(lolwatcher):
    result = game_data_fetcher.get_match_ids(
        lolwatcher, server, puuid, 3, constants.Queue.RANKED
    )
    assert len(result) == 3


def test_get_match_list_handles_large_number_of_games_1(lolwatcher):
    result = game_data_fetcher.get_match_ids(
        lolwatcher, server, puuid, 651, constants.Queue.RANKED
    )
    assert len(result) == 651


def test_get_match_list_handles_large_number_of_games_2(lolwatcher):
    result = game_data_fetcher.get_match_ids(
        lolwatcher, server, puuid, 295, constants.Queue.RANKED
    )
    assert len(result) == 295
