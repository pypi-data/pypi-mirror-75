import logging
from retry import retry
from json import JSONDecodeError

import requests

from lol_esports_parser.config import endpoints, MAX_RETRIES, RETRY_DELAY, config
from lol_esports_parser.logger import lol_esports_parser_logger


class ACS:
    """Class handling connecting and retrieving games from ACS endpoints.
    """

    data = {
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": "eyJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJodHRwczpcL1wvYXV"
        "0aC5yaW90Z2FtZXMuY29tXC90b2tlbiIsInN1YiI6ImxvbCI"
        "sImlzcyI6ImxvbCIsImV4cCI6MTYwMTE1MTIxNCwiaWF0Ijo"
        "xNTM4MDc5MjE0LCJqdGkiOiIwYzY3OThmNi05YTgyLTQwY2I"
        "tOWViOC1lZTY5NjJhOGUyZDcifQ.dfPcFQr4VTZpv8yl1IDK"
        "WZz06yy049ANaLt-AKoQ53GpJrdITU3iEUcdfibAh1qFEpvV"
        "qWFaUAKbVIxQotT1QvYBgo_bohJkAPJnZa5v0-vHaXysyOHq"
        "B9dXrL6CKdn_QtoxjH2k58ZgxGeW6Xsd0kljjDiD4Z0CRR_F"
        "W8OVdFoUYh31SX0HidOs1BLBOp6GnJTWh--dcptgJ1ixUBjo"
        "XWC1cgEWYfV00-DNsTwer0UI4YN2TDmmSifAtWou3lMbqmiQ"
        "IsIHaRuDlcZbNEv_b6XuzUhi_lRzYCwE4IKSR-AwX_8mLNBL"
        "TVb8QzIJCPR-MGaPL8hKPdprgjxT0m96gw",
        "grant_type": "password",
        "username": config.riot_username,
        "password": config.riot_password,
        "scope": "openid offline_access lol ban profile email phone",
    }

    def __init__(self, retry_once=True):
        self.session = requests.Session()
        self.token = self.get_token()
        self.base_url = endpoints["acs"]["game"]
        self.retry_once = retry_once

    @retry(tries=MAX_RETRIES, delay=RETRY_DELAY)
    def get_token(self):
        try:
            token_request = self.session.post("https://auth.riotgames.com/token", data=self.data)
            return token_request.json()["id_token"]
        except JSONDecodeError as e:
            lol_esports_parser_logger.warning(f"Could not acquire ID token for user {config.riot_username}")
            raise e

    @retry(tries=MAX_RETRIES, delay=RETRY_DELAY)
    def _get_from_api(self, uri):
        request_url = f"{self.base_url}{uri}"
        lol_esports_parser_logger.debug("Making a call to: " + request_url)

        response = self.session.get(request_url, cookies={"id_token": self.token})

        if response.status_code != 200:
            lol_esports_parser_logger.error("Status code %d", response.status_code)
            lol_esports_parser_logger.error("Headers: %s", response.headers)
            lol_esports_parser_logger.error("Resp: %s", response.text)
            raise requests.HTTPError

        return response.json()

    def get_game(self, server, game_id, game_hash):
        return self._get_from_api(f"{server}/{game_id}?gameHash={game_hash}")

    def get_game_timeline(self, server, game_id, game_hash):
        return self._get_from_api(f"{server}/{game_id}/timeline?gameHash={game_hash}")
