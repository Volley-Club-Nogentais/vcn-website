#! /usr/bin/env python3
# coding: utf-8

import json
import pathlib

WORKSPACE_PATH = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT_FOLDER = WORKSPACE_PATH / "data" / "calendars"

if __name__ == "__main__":
    next_games = []

    for i in ["ffvb", "fsgt"]:
        with open(OUTPUT_FOLDER / f"{i}_next_games.json") as fd:
            data = json.load(fd)
            next_games = next_games + data

    next_games = sorted(next_games, key=lambda d: d['date'][0])
    with open(OUTPUT_FOLDER / "next_games.json", "w") as fd:
        json.dump(next_games, fd, indent=4)
