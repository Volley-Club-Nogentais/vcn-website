#! /usr/bin/env python3

"""Download the FSGT calendars and generate the next weeks calendar."""

import json
import logging
import pathlib
import sys
import urllib.request
from datetime import datetime
from datetime import timedelta

WORKSPACE_PATH = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT_FOLDER = WORKSPACE_PATH / "data" / "calendars"
SEASON_ID = 5
FSGT = {
    "rhinos_feroces": 25,
    "pingouins_manchots": 100,
    "loups_phoques": 50,
    "pythons_colles": 74,
    "fatals_furets": 99,
    "team_glouglou": 77,
    "coconuts": 78,
}


DATE_LEN = len("00/00/0000")


def _extract_date(s: str) -> str | list[str]:
    if len(s) == DATE_LEN:
        return [datetime.strptime(s, "%d/%m/%Y").strftime("%Y-%m-%d")]

    dates = [datetime.strptime(x, "%d/%m/%Y").strftime("%Y-%m-%d") for x in s.split(" au ")]
    return dates


def parse_fsgt_team_calendar(calendar: dict):
    """Reformat the game object.

    :param: calendar Team calendar.
    """
    # { "local": ..., "visitor": ..., "date": ..., "gymnasium": {} }
    output = []
    for game in calendar:
        logging.debug(f"Parsing {game}")
        output.append(
            {
                "local": game["team_domicile"]["name"],
                "visitor": game["team_exterieur"]["name"],
                "date": _extract_date(game["date"]),
                "location": game["gymnase"],
            }
        )

    return output


def fsgt_store_calendar(team: str, team_id: int):
    uri = f"https://volley-fsgt94.fr/api/games/list/team/{team_id}/season/{SEASON_ID}"
    logging.debug(f"Trying '{uri}'")

    with urllib.request.urlopen(uri) as url:
        data = json.load(url)

    logging.debug(f"Parsing '{team}' schedule")
    output = parse_fsgt_team_calendar(data)
    with open(OUTPUT_FOLDER / f"{team}.json", "w") as fd:
        json.dump(output, fd, indent=4)
        logging.info(f"Wrote {len(output)} games in '{team}' JSON")


def fsgt_next_games_in_weeks(teams: list[str], number_weeks: int = 2):
    today = datetime.now()
    weeks_later = today + timedelta(weeks=number_weeks)

    _input = []
    for team in teams:
        with open(OUTPUT_FOLDER / f"{team}.json", "r") as fd:
            tmp = json.load(fd)
            _input = _input + tmp
            logging.debug(f"Append {len(tmp)} elements to input")

    # Filter objects by 'date' field
    _output = list(
        filter(
            lambda obj: today <= datetime.strptime(obj["date"][0], "%Y-%m-%d") <= weeks_later,
            _input,
        )
    )
    logging.debug(f"Found {len(_output)} games in the next {number_weeks} weeks")

    # Sort the objects by 'date'
    _output.sort(key=lambda obj: datetime.strptime(obj["date"][0], "%Y-%m-%d"))

    with open(OUTPUT_FOLDER / "fsgt_next_games.json", "w") as fd:
        json.dump(_output, fd, indent=4)


def main():
    for team, team_id in FSGT.items():
        fsgt_store_calendar(team, team_id)

    fsgt_next_games_in_weeks(FSGT.keys(), 2)


if __name__ == "__main__":
    loglevel = logging.INFO
    if len(sys.argv) != 1 and sys.argv[1] == "-d":
        loglevel = logging.DEBUG

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    )
    main()
