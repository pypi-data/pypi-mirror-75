import json
import urllib.parse
from typing import Optional

from retry import retry
import requests

from lol_esports_parser.config import endpoints, MAX_RETRIES, RETRY_DELAY
from lol_esports_parser.logger import lol_esports_parser_logger


@retry(tries=MAX_RETRIES, delay=RETRY_DELAY)
def request_retry(url):
    response = requests.get(url)
    return response.json()["msg"]


def get_qq_games_list(qq_match_url) -> list:
    """Gets a games list from a QQ series match history URL.

    Relies on having bmid=xxx in the URL.
    """
    parsed_url = urllib.parse.urlparse(qq_match_url)
    qq_match_id = urllib.parse.parse_qs(parsed_url.query)["bmid"][0]

    games_list_query_url = f"{endpoints['qq']['match_list']}{qq_match_id}"

    lol_esports_parser_logger.debug(f"Querying {games_list_query_url}")

    return request_retry(games_list_query_url)


def get_all_qq_game_info(qq_game_id: int) -> Optional[tuple]:
    """Queries all QQ endpoints sequentially to gather all available information.

    Params:
        qq_game_id: the field called sMatchId in the searchSMatchList endpoint

    Returns:
        game_info, team_info, runes_info, server_id, battle_id
        team_info and and runes will be empty if the endpoints are empty.
    """

    game_info = get_basic_qq_game_info(qq_game_id)

    qq_server_id = int(game_info["sMatchInfo"]["AreaId"])
    qq_battle_id = int(game_info["sMatchInfo"]["BattleId"])

    try:
        team_info = get_team_info(qq_server_id, qq_battle_id)

        qq_world_id = team_info["world_"]
        qq_room_id = team_info["room_id_"]

        try:
            runes_info = get_runes_info(qq_world_id, qq_room_id)
        except RunesMissingWarning:
            lol_esports_parser_logger.warning(
                f"Runes information endpoint not returning any information for "
                f"world ID {qq_world_id} and room id {qq_room_id}"
            )
            runes_info = None

    except TeamInfoMissingWarning:
        lol_esports_parser_logger.warning(
            f"Team information endpoint not returning any information for "
            f"server ID {qq_server_id} and battle id {qq_battle_id}"
        )
        team_info = runes_info = None

    return game_info, team_info, runes_info, qq_server_id, qq_battle_id


class GameInfoMissingError(Exception):
    pass


def get_basic_qq_game_info(qq_game_id: int) -> dict:
    """Gets the basic info about the game, including sides and end of game stats for players.
    """

    game_query_url = f"{endpoints['qq']['match_info']}{qq_game_id}"

    lol_esports_parser_logger.debug(f"Querying {game_query_url}")

    try:
        return request_retry(game_query_url)
    except Exception:
        raise GameInfoMissingError


class TeamInfoMissingWarning(Exception):
    pass


def get_team_info(qq_server_id, qq_battle_id) -> dict:
    """Gets team-specific information, but also world_id and room_id for runes queries.
    """
    team_info_url = (
        endpoints["qq"]["battle_info"].replace("BATTLE_ID", str(qq_battle_id)).replace("WORLD_ID", str(qq_server_id))
    )

    lol_esports_parser_logger.debug(f"Querying {team_info_url}")

    try:
        return json.loads(request_retry(team_info_url))["battle_list_"][0]
    except Exception:
        raise TeamInfoMissingWarning


class RunesMissingWarning(Exception):
    pass


def get_runes_info(qq_world_id, qq_room_id) -> dict:
    """Gets runes lists per players.
    """
    runes_info_url = endpoints["qq"]["runes"].replace("WORLD_ID", str(qq_world_id)).replace("ROOM_ID", str(qq_room_id))

    lol_esports_parser_logger.debug(f"Querying {runes_info_url}")

    try:
        return json.loads(request_retry(runes_info_url))["hero_list_"]
    except Exception:
        raise RunesMissingWarning
