import pytest
from apps.backend.src.data_collection import game_data_fetcher
from apps.backend.src.helper import constants


# Define a fixture to provide sample match info
@pytest.fixture
def sample_match_info():
    return {"info": {"gameVersion": "11.1.1"}}


def test_extract_match_patch_valid_version(sample_match_info: dict):
    # Test case with a valid version
    result = game_data_fetcher.extract_match_patch(sample_match_info)
    assert result == (11, 1)


def test_extract_match_patch_different_version(sample_match_info: dict):
    # Test case with a different version
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    result = game_data_fetcher.extract_match_patch(sample_match_info)
    assert result == (10, 2)


def test_season_patch_is_equal(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = game_data_fetcher.extract_match_patch(sample_match_info)
    test_patch = constants.Patch(10, 2)
    assert sample_patch == test_patch


def test_season_patch_is_earlier_1(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = game_data_fetcher.extract_match_patch(sample_match_info)
    test_patch = constants.Patch(10, 1)
    assert sample_patch > test_patch


def test_season_patch_is_earlier_2(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = game_data_fetcher.extract_match_patch(sample_match_info)
    test_patch = constants.Patch(9, 10)
    assert sample_patch > test_patch


def test_season_patch_is_later_1(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = game_data_fetcher.extract_match_patch(sample_match_info)
    test_patch = constants.Patch(10, 3)
    assert sample_patch < test_patch


def test_season_patch_is_later_2(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = game_data_fetcher.extract_match_patch(sample_match_info)
    test_patch = constants.Patch(11, 1)
    assert sample_patch < test_patch


# Run the tests
if __name__ == "__main__":
    pytest.main()
