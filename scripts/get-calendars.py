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
OUTPUT_FOLDER = WORKSPACE_PATH / "assets" / "calendars"
SEASON_ID = 4
FSGT = {
    "rhinos-feroces": 25,
    "pingouins-manchots": 100,
    "loups-phoques": 50,
    "pythons-colles": 74,
    "fatals-furets": 99,
}


def parse_fsgt_team_calendar(calendar: dict):
    """Reformat the match object.

    :param: calendar Team calendar.
    """
    # { "local": ..., "visitor": ..., "date": ..., "gymnasium": {} }
    output = []
    for match in calendar:
        logging.debug(f"Parsing {match}")
        output.append(
            {
                "local": match["team_domicile"]["name"],
                "visitor": match["team_exterieur"]["name"],
                "date": datetime.strptime(match["date"], "%d/%m/%Y").strftime("%Y-%m-%d"),
                "location": match["gymnase"],
            }
        )

    return output


def fsgt_store_calendar(team: str, team_id: int):
    with urllib.request.urlopen(f"https://volley-fsgt94.fr/api/games/list/team/{team_id}/season/{SEASON_ID}") as url:
        data = json.load(url)

    logging.debug(f"Parsing '{team}' schedule")
    output = parse_fsgt_team_calendar(data)
    with open(OUTPUT_FOLDER / f"{team}.json", "w") as fd:
        json.dump(output, fd, indent=4)
        logging.info(f"Wrote {len(output)} matchs in '{team}' JSON")


def fsgt_next_match_in_weeks(teams: list[str], number_weeks: int = 2):
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
            lambda obj: today <= datetime.strptime(obj["date"], "%Y-%m-%d") <= weeks_later,
            _input,
        )
    )
    logging.debug(f"Found {len(_output)} matches in the next {number_weeks} weeks")

    # Sort the objects by 'date'
    _output.sort(key=lambda obj: datetime.strptime(obj["date"], "%Y-%m-%d"))

    with open(OUTPUT_FOLDER / "fsgt-next-weeks.json", "w") as fd:
        json.dump(_output, fd, indent=4)


def main():
    for team, team_id in FSGT.items():
        fsgt_store_calendar(team, team_id)

    fsgt_next_match_in_weeks(FSGT.keys(), 2)


if __name__ == "__main__":
    loglevel = logging.INFO
    if len(sys.argv) != 1 and sys.argv[1] == "-d":
        loglevel = logging.DEBUG

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    )
    main()
