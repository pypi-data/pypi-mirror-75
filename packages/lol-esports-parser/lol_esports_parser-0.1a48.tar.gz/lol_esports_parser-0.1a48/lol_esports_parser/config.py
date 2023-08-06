import json
import os

# Configuration for endpoints retries
MAX_RETRIES = int(os.environ.get("LOL_ESPORTS_PARSER_MAX_RETRIES") or 2)
RETRY_DELAY = int(os.environ.get("LOL_ESPORTS_PARSER_RETRY_DELAY") or 10)  # Time to sleep on errors (in seconds)


class GhostLoadedConfiguration:
    def __init__(self):
        self._riot_username = None
        self._riot_password = None
        self._riot_api_key = None

    @property
    def riot_username(self):
        if not self._riot_username:
            self._riot_username = os.environ["RIOT_USERNAME"]
        return self._riot_username

    @property
    def riot_password(self):
        if not self._riot_password:
            self._riot_password = os.environ["RIOT_PASSWORD"]
        return self._riot_password

    @property
    def riot_api_key(self):
        if not self._riot_api_key:
            self._riot_api_key = os.environ.get("RIOT_API_KEY")
        return self._riot_api_key


config = GhostLoadedConfiguration()

# Local configuration files
config_folder = os.path.join(os.path.expanduser("~"), ".config", "lol_esports_parser")
endpoints_location = os.path.join(config_folder, "endpoints.json")

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
    raise FileNotFoundError(f"Please create {endpoints_location}.")

with open(endpoints_location) as file:
    endpoints = json.load(file)
