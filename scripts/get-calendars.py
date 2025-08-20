#! /usr/bin/env python3

import json
import urllib.request

FSGT = {"rhinos-feroces": "https://volley-fsgt94.fr/api/games/list/team/25/season/4"}


def parse_fsgt_team_calendar(calendar):
    output = {"headers": ["Équipes", "Date", "Lieu"], "rows": []}
    for match in calendar:
        name = " VS ".join(
            (match["team_domicile"]["name"], match["team_exterieur"]["name"])
        )
        gymnase = match["gymnase"]
        address = f"{gymnase['adresse']}, {gymnase['ville']}"
        if gymnase["voie"]:
            address = " ".join([str(gymnase["voie"]), address])
        output["rows"].append((name, match["date"], address))
    return output


def main():
    for team, uri in FSGT.items():
        with urllib.request.urlopen(uri) as url:
            data = json.load(url)

        calendar = parse_fsgt_team_calendar(data)
        with open(f"static/calendars/{team}.json", "w") as fd:
            json.dump(calendar, fd)


if __name__ == "__main__":
    main()
