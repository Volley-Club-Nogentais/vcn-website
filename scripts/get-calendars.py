#! /usr/bin/env python3

import json
import logging
import pathlib
import sys
import urllib.request

WORKSPACE_PATH = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT_FOLDER = WORKSPACE_PATH / "assets" / "calendars"
print(OUTPUT_FOLDER)
SEASON_ID = 4
FSGT = {
    "rhinos-feroces": 25,
    "pingouins-manchots": 100,
    "loups-phoques": 50,
    "pythons-colles": 74,
    "fatals-furets": 99,
}


def parse_fsgt_team_calendar(calendar):
    output = {"headers": ["Équipes", "Date", "Gymnase", "Adresse"], "rows": []}
    for match in calendar:
        logging.debug(f"Parsing {match}")
        name = " VS ".join(
            (match["team_domicile"]["name"], match["team_exterieur"]["name"])
        )

        # Default value
        gymnase = {
            "name": "N/A",
            "adresse": "N/A",
            "ville": "N/A",
        }

        if match["gymnase"]:
            gymnase = match["gymnase"]

        address = f"{gymnase['adresse']}, {gymnase['ville']}"
        try:
            if not gymnase["voie"]:
                raise KeyError

            address = " ".join([str(gymnase["voie"]), address])
        except KeyError:
            logging.warning(
                f"No street number in the address for match '{match['id']}'"
            )
        output["rows"].append((name, match["date"], gymnase["name"], address))
    return output


def main():
    for team, team_id in FSGT.items():
        with urllib.request.urlopen(
            f"https://volley-fsgt94.fr/api/games/list/team/{team_id}/season/{SEASON_ID}"
        ) as url:
            data = json.load(url)

        logging.debug(f"Parsing '{team}' schedule")
        calendar = parse_fsgt_team_calendar(data)
        with open(OUTPUT_FOLDER / f"{team}.json", "w") as fd:
            json.dump(calendar, fd)
            logging.info(f"Wrote {len(calendar['rows'])} matchs in '{team}' JSON")


if __name__ == "__main__":
    loglevel = logging.INFO
    if len(sys.argv) != 1 and sys.argv[1] == "-d":
        loglevel = logging.DEBUG

    logging.basicConfig(
        level=loglevel, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
