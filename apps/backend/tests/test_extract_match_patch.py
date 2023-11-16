from collections import namedtuple
import pytest
from apps.backend.src.game_data_fetcher import extract_match_patch
from apps.backend.src.constants import SeasonPatch


# Define a fixture to provide sample match info
@pytest.fixture
def sample_match_info():
    return {
        "info": {
            "gameVersion": "11.1.1"
        }
    }


def test_extract_match_patch_valid_version(sample_match_info: dict):
    # Test case with a valid version
    result = extract_match_patch(sample_match_info)
    assert result == (11, 1)


def test_extract_match_patch_different_version(sample_match_info: dict):
    # Test case with a different version
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    result = extract_match_patch(sample_match_info)
    assert result == (10, 2)


def test_season_patch_is_eqaul(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = SeasonPatch(10, 2)
    assert sample_patch == test_patch


def test_season_patch_is_ealier_1(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = SeasonPatch(10, 1)
    assert sample_patch > test_patch


def test_season_patch_is_ealier_2(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = SeasonPatch(9, 10)
    assert sample_patch > test_patch


def test_season_patch_is_later_1(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = SeasonPatch(10, 3)
    assert sample_patch < test_patch


def test_season_patch_is_later_2(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = SeasonPatch(11, 1)
    assert sample_patch < test_patch


# Run the tests
if __name__ == "__main__":
    pytest.main()
