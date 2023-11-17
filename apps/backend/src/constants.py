from enum import Enum
from collections import namedtuple


class Queue(Enum):
    RANKED = 420
    NORMAL = 400
    ARAM = 450


regions = {
    "BR1": "AMERICAS",
    "EUN1": "EUROPE",
    "EUW1": "EUROPE",
    "JP1": "ASIA",
    "KR": "ASIA",
    "LA1": "AMERICAS",
    "LA2": "AMERICAS",
    "NA1": "AMERICAS",
    "OC1": "SEA",
    "TR1": "EUROPE",
    "RU": "ASIA",
}


SeasonPatch = namedtuple("SeasonPatch", ["season", "patch"])
MAX_GAME_COUNT = 100
ALL_GAMES = None
