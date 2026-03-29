#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Download the calendars from the Fédération Francaise de Volley-Ball."""

import argparse
import csv
import json
import logging
import pathlib
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Callable
from urllib import parse
from urllib import request

CLUB = "0943988"
EXPORT_URL = "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier_export_club.php"
USER_AGENT = "Mozilla/5.0 (MatchScraper/1.0)"

NOW = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

WORKSPACE_PATH = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT_FOLDER = WORKSPACE_PATH / "data" / "calendars"

SEASON = "2025/2026"
FFVB = {
    "departemental_masculins": ["ARM"],
    "departemental_feminines": ["ARF"],
    "regional_masculins": ["2MB"],
    "regional_feminines": ["2FA"],
    "compet_lib": ["LOMA", "LMAA"],
}


class NoHTMLData(Exception):
    """Exception raised if there is no text in the niquests response."""

    pass


def parse_args():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="FFVB games downloader")

    # Argument pour le niveau de verbosité
    parser.add_argument("-v", action="count", default=0, help="Increase verbosity level (can be put multiple times)")

    return parser.parse_args()


def setup_logging(verbosity):
    """Setup logging verbosity."""
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(verbosity, len(levels) - 1)]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    )


def remove_unnecesary_fields(row: dict[str, Any]) -> dict[str, Any]:
    for k in ["EQA_no", "EQB_no"]:
        row.pop(k)

    return row


def remove_empty_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Remove empty fields"""
    return {k: v for k, v in row.items() if v}


def rework_timestamp(row: dict[str, Any]) -> dict[str, Any]:
    """Create timestamp field and remove 'Date' and 'Heure'."""
    row["date"] = [row["Date"]]

    for k in ("Date", "Heure"):
        del row[k]

    return row


def rework_score(row: dict[str, Any]) -> dict[str, Any]:
    if "sets" not in row:
        return row

    if "score" not in row:
        return row

    local, visitor = row["sets"].strip().split("/")

    row["score"] = {
        "local": local,
        "visitor": visitor,
        "sets": [list(map(int, x.split("-"))) for x in row["score"].split(",")],
    }

    del row["sets"]
    del row["total"]

    return row


def rework_referees(row: dict[str, Any]) -> dict[str, Any]:
    row["referee"] = [row[i].title() for i in ["referee1", "referee2"] if row.get(i)]

    for i in ["referee1", "referee2"]:
        if i in row:
            row.pop(i)

    return row


def rework_place(row: dict[str, Any]) -> dict[str, Any]:
    if "Salle" not in row:
        return row

    row["location"] = {"name": row["Salle"]}
    del row["Salle"]

    return row


def transform_row(row):
    """Execute a list of rules that will transform the CSV row."""
    rules: list[Callable[[dict[str, Any]], dict[str, Any]]] = [
        remove_unnecesary_fields,
        remove_empty_fields,
        rework_timestamp,
        rework_score,
        rework_referees,
        rework_place,
    ]

    for rule in rules:
        row = rule(row)

    return row


def get_all_games() -> list[str]:
    """Retrieve all games in season."""
    post_data = parse.urlencode(
        {
            "cnclub": CLUB,
            "cal_saison": SEASON,
            "type": "RES",
            "typ_edition": "E",
        }
    ).encode("utf-8")

    req = request.Request(EXPORT_URL, post_data, {"User-Agent": USER_AGENT})
    logging.info(f"Tried the URL: {req.get_full_url()}")

    with request.urlopen(req) as resp:
        data = resp.read().decode("latin-1")

    logging.debug(data)

    return data.splitlines()


def rename_fields(header: str) -> str:
    fields = {
        "Entité": "league",
        "Jo": "matchday",
        "Match": "id",
        "EQA_nom": "local",
        "EQB_nom": "visitor",
        "Set": "sets",
        "Score": "score",
        "Total": "total",
        "Arb1": "referee1",
        "Arb2": "referee2",
    }

    for k, v in fields.items():
        header = header.replace(k, v, 1)

    return header


if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.v)

    l = get_all_games()
    l[0] = rename_fields(header=l[0])

    final = []
    for game in csv.DictReader(l, delimiter=";"):
        game = transform_row(game)
        logging.debug(game)
        final.append(game)

    # Sort the array by date (older first)
    final.sort(key=lambda x: datetime.strptime(x["date"][0], "%Y-%m-%d"))

    # Write all the games in simple JSON file
    with open(OUTPUT_FOLDER / "ffvb_all_games.json", "w") as fd:
        fd.write(json.dumps(final, indent=2))

    # Filter games by team
    for team, poule in FFVB.items():
        _output = list(
            filter(
                lambda obj: any(obj["id"].startswith(prefix) for prefix in poule),
                final,
            )
        )

        logging.info(f"Found {len(_output)} games for '{team}'")
        with open(OUTPUT_FOLDER / f"{team}.json", "w") as fd:
            fd.write(json.dumps(_output, indent=2))

    # Filter games: store only the games in the next 2 weeks
    _output = list(
        filter(
            lambda obj: NOW <= datetime.strptime(obj["date"][0], "%Y-%m-%d") <= NOW + timedelta(weeks=2),
            final,
        )
    )

    logging.info(f"Found {len(_output)} games in the next 2 weeks")
    with open(OUTPUT_FOLDER / "ffvb_next_games.json", "w") as fd:
        fd.write(json.dumps(_output, indent=2))
