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

CLUB = "0943988"
CLUB_URL = "https://www.ffvbbeach.org/ffvbapp/resu/planning_club.php"
TEAM_URL =  "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php"
USER_AGENT = "Mozilla/5.0 (MatchScraper/1.0)"

NOW = datetime.now()

WORKSPACE_PATH = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT_FOLDER = WORKSPACE_PATH / "data" / "calendars"

SEASON = "2025/2026"
FFVB = {
    "departemental_masculins": {
        "poule": "ARM",
        "codent": "PTIDF94",
        "equipe": 20,
    },
    "departemental_feminines": {
        "poule": "ARF",
        "codent": "PTIDF94",
        "equipe": 11,
    },
    "regional_masculins": {
        "poule": "2MB",
        "codent": "LIIDF",
        "equipe": 9,
    },
    "regional_feminines": {
        "poule": "2FA",
        "codent": "LIIDF",
        "equipe": 4,
    },
}


class NoHTMLData(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="FFVB games downloader")

    # Argument pour le niveau de verbosité
    parser.add_argument("-v", action="count", default=0, help="Increase verbosity level (can be put multiple times)")

    return parser.parse_args()


def setup_logging(verbosity):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(verbosity, len(levels) - 1)]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    )


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ").strip())


def parse_one_week(timestamp: int):
    r = niquests.get(
        url=CLUB_URL,
        params={"date_jour": str(timestamp), "cnclub": CLUB},
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    logging.info(f"Tried the URL: {r.url}")
    r.raise_for_status()

    if not r.text:
        raise NoHTMLData

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
                data["date"] = [str(s)]
                break

        if data["referee"] and data["referee"].endswith(" / "):
            data["referee"] = data["referee"][:-3]

        next_games.append(data)
        logging.debug(f"Added: {data}")

    return next_games

def parse_all_team_calendars(teams):
    for team, data in teams.items():
        games = parse_team_calendar(team, data)

        with open(OUTPUT_FOLDER / f"{team}.json", "w") as fd:
            json.dump(games, fd, indent=4)


def parse_team_calendar(team:str, params: dict[str, str]):
    def extract_score(text):
        score = list()
        for x in text.split(", "):
            local, visitor = x.split(':')
            score.append((int(local), int(visitor)))
        return score

    l = list()
    params["saison"] = SEASON
    params["calend"] = "COMPLET"
    r = niquests.get(
        url=TEAM_URL,
        params=params,
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    logging.info(f"Tried the '{team}' URL: {r.url}")
    r.raise_for_status()

    if not r.text:
        raise NoHTMLData

    soup = BeautifulSoup(r.text, "html.parser")

    tables = soup.find_all('table')
    if len(tables) < 4:
        logging.error("Not enough tables in page")

    games = tables[3].find_all("tr", {"bgcolor": "#EEEEF8"})

    for game in games:
        tds = game.find_all("td")

        if "xxxxx" in game.text:
            continue

        # Game played
        if len(tds) == 12:
            data = {
                "level": params["poule"],
                "id": tds[0].text,
                "local": tds[3].text,
                "visitor": tds[5].text,
                "score": {
                    "local": int(tds[6].text),
                    "visitor": int(tds[7].text),
                    "sets": extract_score(tds[8].text)
                },
                "referee": tds[10].text if tds[10] and tds[10].text else None,
                "date": [str(datetime.strptime(f"{tds[1].text} {tds[2].text}", "%d/%m/%y %H:%M"))]
            }
        # Game to be played
        else:
            data = {
                "level": params["poule"],
                "id": tds[0].text,
                "local": tds[3].text,
                "visitor": tds[5].text,
                "location": {"name": tds[7].text},
                "referee": tds[10].text if tds[10] and tds[10].text else None,
                "date": [str(datetime.strptime(f"{tds[1].text} {tds[2].text}", "%d/%m/%y %H:%M"))]
            }

        logging.debug(f"Found game for '{team}': {data}")
        l.append(data)

    logging.info(f"Found {len(l)} games")
    return l


def last_friday(date):
    days_to_remove = (date.weekday() + 3) % 7 + 1  # 3 for friday
    last_friday = date - timedelta(days=days_to_remove)
    return last_friday


if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.v)

    next_games = []
    # Need the three next weeks
    for i in range(0, 3):
        date = NOW + timedelta(weeks=i)
        # Do not ask me why but the timestamp that is used in the URL is the saturday before the week that you want
        # Example: if you want the games from the 13 oct 2025 to 19 oct 2025, the you should put the timestamp of
        # Saturday
        # October 11th 2025...
        last_f = last_friday(date)
        week_games = parse_one_week(int(last_f.timestamp()))
        next_games = next_games + week_games

    # Filter objects by 'date' field and get the games in the next two weeeks
    _output = list(
        filter(
            lambda obj: NOW <= datetime.strptime(obj["date"][0][:10], "%Y-%m-%d") <= NOW + timedelta(weeks=2),
            next_games,
        )
    )
    logging.debug(f"Found {len(_output)} games in the next 2 weeks")

    with open(OUTPUT_FOLDER / "ffvb_next_games.json", "w") as fd:
        json.dump(_output, fd, indent=4)

    parse_all_team_calendars(FFVB)
