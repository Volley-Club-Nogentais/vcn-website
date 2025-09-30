#! /usr/bin/env python3

import niquests
from bs4 import BeautifulSoup

URL = "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2025%2F2026"
MATCHES = {
    "departemental-masculins": f"{URL}&codent=PTIDF94&poule=ARM&calend=COMPLET&equipe=20&x=9&y=10",
    "departemental-feminines": f"{URL}&codent=PTIDF94&poule=ARF&calend=COMPLET&equipe=11&x=9&y=7",
    "regional-masculins": f"{URL}&codent=PTIDF94&poule=PAM&calend=COMPLET&equipe=4&x=6&y=12",
    "regional-feminines": f"{URL}&codent=PTIDF94&poule=PAF&calend=COMPLET&equipe=2&x=12&y=8",
}

for name, url in MATCHES.items():
    result = niquests.get(url)

    with open(f"{name}.html", "w") as fd:
        fd.write(result.text)
