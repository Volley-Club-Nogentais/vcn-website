#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Download the calendars from the Fédération Francaise de Volley-Ball."""

import argparse
import json
import logging
import pathlib
import re
from datetime import datetime
from datetime import timedelta

import niquests
from bs4 import BeautifulSoup

# Do not ask me why but the timestamp that is used in the URL is the saturday before the week that you want
# Example: if you want the games from the 13 oct 2025 to 19 oct 2025, the you should put the timestamp of Saturday
# October 11th 2025...
CLUB = "0943988"
URL = "https://www.ffvbbeach.org/ffvbapp/resu/planning_club.php"
USER_AGENT = "Mozilla/5.0 (MatchScraper/1.0)"

NOW = datetime.now()

WORKSPACE_PATH = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT_FOLDER = WORKSPACE_PATH / "data" / "calendars"

class NoHTMLData(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="FFVB games downloader")

    # Argument pour le niveau de verbosité
    parser.add_argument("-v", action="count", default=0, help="Increase verbosity level (can be put multiple times)")

    # Argument pour l'URL
    parser.add_argument(
        "--url", type=str, default="https://www.ffvbbeach.org/ffvbapp/resu/planning_club.php", help="URL to use"
    )

    return parser.parse_args()


def setup_logging(verbosity):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(verbosity, len(levels) - 1)]
    logging.basicConfig(level=level)


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ").strip())


def parse_one_week(url: str, timestamp: int):
    r = niquests.get(
        url=url,
        params={"aff_semaine": "SUI", "date_jour": str(timestamp), "cnclub": CLUB},
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    logging.info(f"Tried the URL: {r.url}")
    r.raise_for_status()

    if not r.text:
        raise NoHTMLData

    with open("file.html", "w") as fd:
        fd.write(r.text)

    soup = BeautifulSoup(r.text, "html.parser")

    # 1) 2e table de la page (index 1)
    lienblanc = soup.find_all("td", {"class": "lienblanc"})
    if not lienblanc:
        logging.error("Could not find cells with the class 'lienblanc'")
        return []

    logging.info(f"Found {len(lienblanc)} lienblanc ")

    next_games = []
    parents = [x.parent for x in lienblanc]
    for parent in parents:
        # Extract all cells
        tds = parent.find_all("td")

        if not tds:
            logging.error("No 'td' found for this parent")

        data = {
            "level": tds[0].text,
            "id": tds[1].text,
            "local": tds[4].text,
            "visitor": tds[6].text,
            "location": {"name": tds[8].text},
            "referee": tds[10].text if tds[10] and tds[10].text else None,
        }

        # Get the date
        for year in [NOW.year, NOW.year + 1]:
            if tds[3].text:
                date = f"{tds[2].text}/{year} {tds[3].text}"
                s = datetime.strptime(date, "%d/%m/%Y %H:%M")
            else:
                date = f"{tds[2].text}/{year}"
                s = datetime.strptime(date, "%d/%m/%Y")

            if s > NOW:
                data["date"] = str(s)
                break

        if data["referee"] and data["referee"].endswith(" / "):
            data["referee"] = data["referee"][:-3]

        next_games.append(data)

    return next_games



if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.v)

    next_games = []
    for i in range(0, 2):
        date = NOW - timedelta(days=3) + timedelta(weeks=i)
        week_games = parse_one_week(args.url, int(date.timestamp()))
        next_games = next_games + week_games

    with open(OUTPUT_FOLDER / "ffvb_next_games.json", "w") as fd:
        json.dump(next_games, fd, indent=4)
