from datetime import datetime
from pydantic import BaseModel, PositiveInt, NonNegativeInt

from typing import List


class MetaData(BaseModel):
    dataVersion: str
    matchId: str
    # participants: List[str]


class InfoData(BaseModel):
    game_creation: datetime
    game_end_timestamp: datetime
    game_duration: PositiveInt
    game_version: str


class MatchData(BaseModel):
    metadata: MetaData
    info: InfoData


class PlayerGameData(BaseModel):
    kills: NonNegativeInt
    deaths: NonNegativeInt
    assists: NonNegativeInt
    championName: str
    firstBloodAssist: bool
    firstBloodKill: bool
    firstTowerAssist: bool
    firstTowerKill: bool
    gameEndedInEarlySurrender: bool
    gameEndedInSurrender: bool
    goldEarned: NonNegativeInt
    magicDamageDealtToChampions: NonNegativeInt
    physicalDamageDealtToChampions: NonNegativeInt
    teamEarlySurrendered: bool
    teamPosition: str
    totalDamageDealtToChampions: NonNegativeInt
    totalTimeSpentDead: NonNegativeInt
    wardsKilled: NonNegativeInt
    wardsPlaced: NonNegativeInt
    win: bool
    teamId: int
    laneMinionsFirst10Minutes: NonNegativeInt
