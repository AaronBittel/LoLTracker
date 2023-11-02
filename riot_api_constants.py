from enum import Enum


GET_SUMMONER_BY_NAME = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
GET_MATCH_IDS_BY_PUUID_1 = "https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?"
GET_MATCH_IDS_BY_PUUID_2 = "start={}&count={}&api_key={}"
GET_MATCH_DATA_BY_MATCH_ID = "https://{}.api.riotgames.com/lol/match/v5/matches/{}?api_key={}"


class RiotQueue(Enum):
    RANKED = 420
    ARAM = 450
    NORMAL = 400
