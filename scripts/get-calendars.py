#! /usr/bin/env python3

import json
import logging
import pathlib
import sys
import urllib.request

from datetime import datetime

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


def parse_fsgt_team_calendar(calendar):
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


def main():
    for team, team_id in FSGT.items():
        with urllib.request.urlopen(
            f"https://volley-fsgt94.fr/api/games/list/team/{team_id}/season/{SEASON_ID}"
        ) as url:
            data = json.load(url)

        logging.debug(f"Parsing '{team}' schedule")
        output = parse_fsgt_team_calendar(data)
        with open(OUTPUT_FOLDER / f"{team}.json", "w") as fd:
            json.dump(output, fd, indent=4)
            logging.info(f"Wrote {len(output)} matchs in '{team}' JSON")


if __name__ == "__main__":
    loglevel = logging.INFO
    if len(sys.argv) != 1 and sys.argv[1] == "-d":
        loglevel = logging.DEBUG

    logging.basicConfig(
        level=loglevel, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
