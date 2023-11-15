import sys
sys.path.append(r"C:\Users\aaron\projects\lolTracker\apps\backend\src")
sys.path.append(r"C:\Users\aaron\projects\lolTracker\apps\helper")

import pytest
from riotwatcher import LolWatcher
from game_data_fetcher import get_match_list
import helper.helper

puuid = "mZsAougfpi9QCkzfIK5DnhxGrC1EEt62X3RvaVvb9vW8TOBkmkBlLiGdiqkyt14mCFjQkAiLx2sNpg"
server = "EUW1"

@pytest.fixture
def lolwatcher():
    # Set up any necessary objects or configurations for testing
    return LolWatcher(helper.get_api_key_from_file())

def test_get_match_list_returns_list(lolwatcher):
    result = get_match_list(lolwatcher, server, puuid, 5, helper.constants.Queue.RANKED_SOLO)
    assert isinstance(result, list)

def test_get_match_list_returns_correct_number_of_games(lolwatcher):
    result = get_match_list(lolwatcher, server, puuid, 3, helper.constants.Queue.RANKED_SOLO)
    assert len(result) == 3

def test_get_match_list_handles_large_number_of_games(lolwatcher):
    result = get_match_list(lolwatcher, server, puuid, 1000, helper.constants.Queue.RANKED_SOLO)
    assert len(result) == 1000