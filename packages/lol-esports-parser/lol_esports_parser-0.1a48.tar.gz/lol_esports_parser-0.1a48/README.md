[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Leaguepedia Esports Parser
A utility to transform LoL games data from both QQ and ACS into a single Data Transfer Object

This was developed in partnership between T1 and Leaguepedia staff.

# Usage
Test can be found in the `_tests` folder.
```python
import lol_esports_parser

# The package relies on match history URLs
# Both QQ and WP are support for Chinese games
# QQ
lpl_spring_finals = lol_esports_parser.get_qq_series("http://lol.qq.com/match/match_data.shtml?bmid=6131")
lpl_spring_finals["score"]  # {"JDG": 3, "TES": 2}

# WP
lpl_summer_series = lol_esports_parser.get_wp_series("https://www.wanplus.com/schedule/63496.html")
lpl_summer_series["score"]  # {"FPX": 2, "RNG": 1}

lck_spring_finals_g1 = lol_esports_parser.get_riot_game("https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1353193?gameHash=63e4e6e5d695f410")
lck_spring_finals_g1["winner"]  # "RED"
lck_spring_finals_g1["teams"]["RED"]["name"]  # "T1"
```

# Configuration
## Environment variables
Expected environment variables can be found in the `template.env` file in this repository:
```dotenv
# Queries retries settings
LOL_ESPORTS_PARSER_MAX_RETRIES=2
LOL_ESPORTS_PARSER_RETRY_DELAY=10

# A Riot username and password are required for pro match history
RIOT_USERNAME=xxx
RIOT_PASSWORD=xxx

# A Riot API key is required for amateur matches played on the live server
RIOT_API_KEY=xxx
```

To load a `.env` file in python, you can use [python-dotenv](https://pypi.org/project/python-dotenv/) which offers a
very simple syntax to load environment variables with `dotenv.load_env()`.

Alternatively, you can directly use `os.environ[key] = value` inside your python scripts, but they need to be set before
you load `lol_esports_parser`.

## Endpoints configuration and Docker mounting
Endpoints are stored in a file called `endpoints.json` located at `~/.config/lol_esports_parser`.

To access this local file inside of a docker container, you can use this mounting syntax (Windows example):

```powershell
--mount type=bind, \
        source=C:\Users\USERNAME\.config\lol_esports_parser, \
        target=/usr/.config/lol_esports_parser \
```
