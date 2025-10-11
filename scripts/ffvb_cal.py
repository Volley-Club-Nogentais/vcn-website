#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.ffvbbeach.org/ffvbapp/resu/planning_club.php?cnclub=0943988&x=5&y=0"

# Regex simples
RE_CODE = re.compile(r"^[A-Z]{3,}\d{3}$")  # BRN004, ARFA006, ...
RE_DATE = re.compile(r"^\d{2}/\d{2}$")     # 12/10
RE_TIME = re.compile(r"^\d{1,2}:\d{2}$")   # 11:45

def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ").strip())

def main(url:str):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (MatchScraper/1.0)"}, timeout=20)
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"

    soup = BeautifulSoup(r.text, "html.parser")

    # 1) 2e table de la page (index 1)
    tables = soup.find_all("table")
    if len(tables) < 2:
        print(json.dumps([]))
        return
    second_table = tables[3]

    # 2) 5e ligne de cette table (index 4)
    trs = second_table.find_all("tr")

    if len(trs) < 5:
        print(json.dumps([]))
        return

    fifth_tr = trs[4]

    # 3) 1er td de cette ligne, qui contient le tableau à parcourir
    tds = fifth_tr.find_all("td")
    print(tds)
    if not tds:
        print(json.dumps([]))
        return
    container_td = tds[0]

    nested_table = container_td.find("table")
    if not nested_table:
        print(json.dumps([]))
        return

    # 4) Parcours du tableau imbriqué
    results = []
    for tr in nested_table.find_all("tr"):
        cells = [clean(td.get_text(" ", strip=True)) for td in tr.find_all("td")]
        if len(cells) < 4:
            continue

        # On s'attend à : CODE | DATE | HEURE | EQUIPE ...
        code, date, time = cells[0], cells[1], cells[2]
        equipe = cells[3]

        if not (RE_CODE.match(code) and RE_DATE.match(date) and RE_TIME.match(time)):
            continue

        results.append({
            "match": code,
            "date": date,
            "heure": time,
            "equipe": equipe
        })

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else URL
    main(url)
