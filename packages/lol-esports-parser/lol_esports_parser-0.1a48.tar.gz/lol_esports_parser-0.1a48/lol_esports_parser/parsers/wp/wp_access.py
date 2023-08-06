import requests
from retry import retry
from bs4 import BeautifulSoup
import mwclient

from lol_esports_parser import get_qq_series
from lol_esports_parser.config import endpoints, MAX_RETRIES, RETRY_DELAY
from lol_esports_parser.dto.series_dto import LolSeries, create_series
from lol_esports_parser.dto.wp_dto import LolWpGame
from lol_esports_parser.logger import lol_esports_parser_logger
from lol_esports_parser.parsers.wp.wp_parser import parse_wp_game


def get_chinese_series(qq_series_id: int, patch: str = None, add_names=True, discrete_mode=True) -> LolSeries:
    """Gets a wp series from its related qq series id, using leaguepedia for the join.

    Args:
        qq_series_id: the QQ ID of the series$
        patch: MM.mm patch, to add it to the object as it’s wrong by default in wp
        add_names: whether or not to add names to items, runes, and so on and so forth
        discrete_mode: whether or not to add fields that are specific to this data source
    """
    site = mwclient.Site("lol.gamepedia.com", path="/")
    result = site.api("cargoquery", tables="MatchSchedule", where=f'QQ="{qq_series_id}"', fields="Wanplus")

    wp_series = get_wp_series(
        result["cargoquery"][0]["title"]["Wanplus"], patch=patch, add_names=add_names, discrete_mode=discrete_mode
    )

    # We use QQ solely for picks and bans
    try:
        qq_series = get_qq_series(
            f"https://lpl.qq.com/es/stats.shtml?bmid={qq_series_id}", patch=patch, add_names=add_names
        )
        for idx, wp_game in enumerate(wp_series["games"]):
            qq_game = qq_series["games"][idx]

            for wp_team in wp_game["teams"].values():
                # Basing it on team side was buggy because QQ is often wrong
                qq_team = next(team for team in qq_game["teams"].values() if team["name"] == wp_team["name"])

                wp_team["bans"] = qq_team["bans"]
                wp_team["bansNames"] = qq_team.get("bansNames")

    except Exception as e:
        lol_esports_parser_logger.error(f"Could not properly parse QQ game {qq_series_id}, relying only on WP data.")
        lol_esports_parser_logger.error(e)

    return wp_series


def get_wp_series(series_url: str, patch: str = None, add_names=True, discrete_mode=True) -> LolSeries:
    """Gets a wp series from its url.

    Args:
        series_url: the URL to the wp match history
        patch: MM.mm patch, to add it to the object as it’s wrong by default in wp
        add_names: whether or not to add names to items, runes, and so on and so forth
        discrete_mode: whether or not to add fields that are specific to this data source
    """
    page = requests.get(series_url)

    soup = BeautifulSoup(page.content, "html.parser")

    games = []
    for link in soup.findAll("a", attrs={"data-matchid": True}):
        games.append(get_wp_game(int(link["data-matchid"]), patch, add_names, discrete_mode))

    return create_series(games)


def get_wp_game(
    wp_match_id: int, patch: str = None, add_names=True, discrete_mode=True, raise_missing_events=False
) -> LolWpGame:
    """Gets a wp game from its match ID.

    Args:
        wp_match_id: the wp match id
        patch: MM.mm patch, to add it to the object as it’s wrong by default in wp
        add_names: whether or not to add names to items, runes, and so on and so forth
        discrete_mode: whether or not to add fields that are specific to this data source
        raise_missing_events: whether or not to raise an Exception if events are missing

    Raises:
        HTTPError if the answer was a 4040
        GameMissingEventsException if the game does not have its "eventLine" field filled
    """

    raw_game = query_wp_game(wp_match_id)

    return parse_wp_game(
        raw_game,
        game_id=wp_match_id,
        patch=patch,
        add_names=add_names,
        discrete_mode=discrete_mode,
        raise_missing_events=raise_missing_events,
    )


@retry(tries=MAX_RETRIES, delay=RETRY_DELAY)
def query_wp_game(wp_match_id: int):
    url = endpoints["wp"]["match_detail"]
    headers = endpoints["wp"]["headers"]

    return requests.get(f"{url}{wp_match_id}", headers=headers).json()
