from enum import Enum
from collections import namedtuple


class Queue(Enum):
    RANKED = 420
    NORMAL = 400
    ARAM = 450


regions = {
    "EUROPE": "EUW1",
    "ASIA": "KR",
    "AMERICAS": "NA"
}


SeasonPatch = namedtuple("SeasonPatch", ["season", "patch"])
MAX_GAME_COUNT = 100
ALL_GAMES = None
