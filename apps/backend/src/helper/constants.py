from enum import Enum
from collections import namedtuple
from enum import auto


# import requests

Patch = namedtuple("Patch", ["season", "patch"])
MatchData = namedtuple("MatchData", ["match_data", "time_line_data"])
MAX_GAME_COUNT = 100
ALL_GAMES = None
REMAKE_GAME_DURATION_THRESHOLD = 5 * 60
MINUTE_2 = 2
TIME_LINE_BLUE_SIDE_JUNGLER_INDEX = 2
TIME_LINE_RED_SIDE_JUNGLER_INDEX = 7

ACCOUNT_BY_GAME_NAME_TAGLINE = (
    "https://{}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}?api_key={}"
)


class Queue(Enum):
    RANKED = 420
    NORMAL = 400
    ARAM = 450


class Operation(Enum):
    GET_DATA_FROM_API = auto()
    SAVE_RAW_DATA_TO_FILE = auto()
    GET_DATA_FROM_FILE = auto()


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


META_DATA_COLUMNS = ["matchId"]

INFO_DATA_COLUMNS = ["gameCreation", "gameEndTimestamp", "gameDuration", "gameVersion"]

PARTICIPANT_DATA_COLUMNS = [
    "kills",
    "deaths",
    "assists",
    "championName",
    "firstBloodAssist",
    "firstBloodKill",
    "firstTowerAssist",
    "firstTowerKill",
    "gameEndedInEarlySurrender",
    "gameEndedInSurrender",
    "goldEarned",
    "magicDamageDealtToChampions",
    "physicalDamageDealtToChampions",
    "teamEarlySurrendered",
    "teamPosition",
    "totalDamageDealtToChampions",
    "totalTimeSpentDead",
    "wardsKilled",
    "wardsPlaced",
    "win",
    "teamId",
]

PARTICIPANT_CHALLENGES_DATA_COLUMNS = ["laneMinionsFirst10Minutes"]

ROLES_PICK_COLUMNS = [
    "bluePickTop",
    "bluePickJungle",
    "bluePickMiddle",
    "bluePickBottom",
    "bluePickSupport",
    "redPickTop",
    "redPickJungle",
    "redPickMiddle",
    "redPickBottom",
    "redPickSupport",
]

ALLY_TEAM_PICKS = [
    "allyTopPick",
    "allyJunglePick",
    "allyMiddlePick",
    "allyBottomPick",
    "allySupportPick",
]

ENEMY_TEAM_PICKS = [
    "enemyTopPick",
    "enemyJunglePick",
    "enemyMiddlePick",
    "enemyBottomPick",
    "enemySupportPick",
]

ROLES_BAN_COLUMNS = [
    "blueBanTop",
    "blueBanJungle",
    "blueBanMiddle",
    "blueBanBottom",
    "blueBanSupport",
    "redBanTop",
    "redBanJungle",
    "redBanMiddle",
    "redBanBottom",
    "redBanSupport",
]

ALLY_TEAM_BANS = [
    "allyTopBan",
    "allyJungleBan",
    "allyMiddleBan",
    "allyBottomBan",
    "allySupportBan",
]

ENEMY_TEAM_BANS = [
    "enemyTopBan",
    "enemyJungleBan",
    "enemyMiddleBan",
    "enemyBottomBan",
    "enemySupportBan",
]


"""
def create_champion_id_mapping():
    response = requests.get("https://ddragon.leagueoflegends.com/cdn/13.22.1/data/en_US/champion.json")
    champion_data = response.json()["data"]
    id_champion_dict = {}
    for champion_name, champion_data in champions_data.items():
        champion_key = int(champion_data["key"])
        id_champion_dict[champion_key] = champion_name
    return id_champion_dict


print(json.dumps(obj=create_champion_id_mapping(), indent=4))
for id, champion in create_champion_id_mapping().items():
    print(f'{id}: "{champion}",')
"""

PLAYERS = {
    "Maxi": "TqpAil-4OljSbW4-9VPxJGavdUWmRXQP33NqarYJEezLjiq31fKeF2wEh0Ni5voF4P-au0AUWIA3OA",
    "Moritz": "_QaZtwN1a6o1o6xud2JE1sNxbbKAesF-1nMRkc6sudsXQN5FoUjlZ8NzPE83ndcUrdIHShSBOFwpOw",
    "Niclas": "n6SWWXvRGAhZGM5ZsIRkVy3Oi8P8uvYMlDNWSsdRgqd1IVjq-lnCGDhivqyDD25uX6hOZP7-URNFTQ",
    "Aaron": "mZsAougfpi9QCkzfIK5DnhxGrC1EEt62X3RvaVvb9vW8TOBkmkBlLiGdiqkyt14mCFjQkAiLx2sNpg",
}

ID_CHAMPION_MAPPING = {
    266: "Aatrox",
    103: "Ahri",
    84: "Akali",
    166: "Akshan",
    12: "Alistar",
    32: "Amumu",
    34: "Anivia",
    1: "Annie",
    523: "Aphelios",
    22: "Ashe",
    136: "AurelionSol",
    268: "Azir",
    432: "Bard",
    200: "Belveth",
    53: "Blitzcrank",
    63: "Brand",
    201: "Braum",
    233: "Briar",
    51: "Caitlyn",
    164: "Camille",
    69: "Cassiopeia",
    31: "Chogath",
    42: "Corki",
    122: "Darius",
    131: "Diana",
    119: "Draven",
    36: "DrMundo",
    245: "Ekko",
    60: "Elise",
    28: "Evelynn",
    81: "Ezreal",
    9: "Fiddlesticks",
    114: "Fiora",
    105: "Fizz",
    3: "Galio",
    41: "Gangplank",
    86: "Garen",
    150: "Gnar",
    79: "Gragas",
    104: "Graves",
    887: "Gwen",
    120: "Hecarim",
    74: "Heimerdinger",
    420: "Illaoi",
    39: "Irelia",
    427: "Ivern",
    40: "Janna",
    59: "JarvanIV",
    24: "Jax",
    126: "Jayce",
    202: "Jhin",
    222: "Jinx",
    145: "Kaisa",
    429: "Kalista",
    43: "Karma",
    30: "Karthus",
    38: "Kassadin",
    55: "Katarina",
    10: "Kayle",
    141: "Kayn",
    85: "Kennen",
    121: "Khazix",
    203: "Kindred",
    240: "Kled",
    96: "KogMaw",
    897: "KSante",
    7: "Leblanc",
    64: "LeeSin",
    89: "Leona",
    876: "Lillia",
    127: "Lissandra",
    236: "Lucian",
    117: "Lulu",
    99: "Lux",
    54: "Malphite",
    90: "Malzahar",
    57: "Maokai",
    11: "MasterYi",
    902: "Milio",
    21: "MissFortune",
    62: "MonkeyKing",
    82: "Mordekaiser",
    25: "Morgana",
    950: "Naafiri",
    267: "Nami",
    75: "Nasus",
    111: "Nautilus",
    518: "Neeko",
    76: "Nidalee",
    895: "Nilah",
    56: "Nocturne",
    20: "Nunu",
    2: "Olaf",
    61: "Orianna",
    516: "Ornn",
    80: "Pantheon",
    78: "Poppy",
    555: "Pyke",
    246: "Qiyana",
    133: "Quinn",
    497: "Rakan",
    33: "Rammus",
    421: "RekSai",
    526: "Rell",
    888: "Renata",
    58: "Renekton",
    107: "Rengar",
    92: "Riven",
    68: "Rumble",
    13: "Ryze",
    360: "Samira",
    113: "Sejuani",
    235: "Senna",
    147: "Seraphine",
    875: "Sett",
    35: "Shaco",
    98: "Shen",
    102: "Shyvana",
    27: "Singed",
    14: "Sion",
    15: "Sivir",
    72: "Skarner",
    37: "Sona",
    16: "Soraka",
    50: "Swain",
    517: "Sylas",
    134: "Syndra",
    223: "TahmKench",
    163: "Taliyah",
    91: "Talon",
    44: "Taric",
    17: "Teemo",
    412: "Thresh",
    18: "Tristana",
    48: "Trundle",
    23: "Tryndamere",
    4: "TwistedFate",
    29: "Twitch",
    77: "Udyr",
    6: "Urgot",
    110: "Varus",
    67: "Vayne",
    45: "Veigar",
    161: "Velkoz",
    711: "Vex",
    254: "Vi",
    234: "Viego",
    112: "Viktor",
    8: "Vladimir",
    106: "Volibear",
    19: "Warwick",
    498: "Xayah",
    101: "Xerath",
    5: "XinZhao",
    157: "Yasuo",
    777: "Yone",
    83: "Yorick",
    350: "Yuumi",
    154: "Zac",
    238: "Zed",
    221: "Zeri",
    115: "Ziggs",
    26: "Zilean",
    142: "Zoe",
    143: "Zyra",
}
