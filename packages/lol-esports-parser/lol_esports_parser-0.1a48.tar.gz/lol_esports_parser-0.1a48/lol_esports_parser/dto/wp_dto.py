from typing import Optional, List, Dict

from lol_dto.classes.game import LolGamePlayer, LolGame, LolGamePlayerWardEvent, LolEvent, LolGameTeam, Position


class LolWpGamePlayerWardEvent(LolGamePlayerWardEvent, total=False):
    deathTimestamp: Optional[float]
    killType: int  # TODO Properly handle that, does it mean anything?


class LolWpGamePlayerMonsterKillEvent(LolEvent):
    monsterType: Optional[str]  # "BLUE_BUFF", "RED_BUFF", None


class LolWpGamePlayerPosition(LolEvent):
    pass


class LolWpGamePlayer(LolGamePlayer, total=False):
    monstersKillsEvents: List[LolWpGamePlayerMonsterKillEvent]
    wardsEvents: List[LolWpGamePlayerWardEvent]
    position: List[LolWpGamePlayerPosition]  # Timestamp + position


class LolWpGameTeam(LolGameTeam):
    players: List[LolWpGamePlayer]


class LolWpGame(LolGame, total=False):
    teams: Dict[str, LolWpGameTeam]

    teamfights: list
