import pytest
from apps.backend.src import extract_match_patch
from apps.backend.src import Patch


# Define a fixture to provide sample match info
@pytest.fixture
def sample_match_info():
    return {"info": {"gameVersion": "11.1.1"}}


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
    test_patch = Patch(10, 2)
    assert sample_patch == test_patch


def test_season_patch_is_ealier_1(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = Patch(10, 1)
    assert sample_patch > test_patch


def test_season_patch_is_ealier_2(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = Patch(9, 10)
    assert sample_patch > test_patch


def test_season_patch_is_later_1(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = Patch(10, 3)
    assert sample_patch < test_patch


def test_season_patch_is_later_2(sample_match_info: dict):
    sample_match_info["info"]["gameVersion"] = "10.2.3"
    sample_patch = extract_match_patch(sample_match_info)
    test_patch = Patch(11, 1)
    assert sample_patch < test_patch


# Run the tests
if __name__ == "__main__":
    pytest.main()
