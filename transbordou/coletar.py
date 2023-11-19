import re
import zipfile
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from transbordou.domain.entities.rain import RainCreate


def coletar(str: str):
    acumulados = []
    soup = BeautifulSoup(str, "html.parser")
    rows = soup.find_all(
        lambda tag: tag.name == "tr" and tag.get("id", "").startswith("linha")
    )
    for row in rows:
        # Encontre todas as colunas (td) na linha
        columns = row.find_all("td")
        if not columns or len(columns) < 17:
            continue
        # Acesse as informações que você deseja com base na posição das colunas
        _temp = dict(
            station_id=columns[0].text.strip(),
            station_name=columns[1].text.strip(),
            region=columns[2].text.strip(),
            data=columns[3].text.strip(),
            quantity_05_min=columns[4].text.strip(),
            quantity_10_min=columns[5].text.strip(),
            quantity_15_min=columns[6].text.strip(),
            quantity_30_min=columns[7].text.strip(),
            quantity_1_h=columns[8].text.strip(),
            quantity_2_h=columns[9].text.strip(),
            quantity_3_h=columns[10].text.strip(),
            quantity_4_h=columns[11].text.strip(),
            quantity_6_h=columns[12].text.strip(),
            quantity_12_h=columns[13].text.strip(),
            quantity_24_h=columns[14].text.strip(),
            quantity_96_h=columns[15].text.strip(),
            quantity_month=columns[16].text.strip(),
            tx_15=columns[17].text.strip(),
        )

        acumulado = RainCreate(**_temp)
        acumulados.append(acumulado)
    return acumulados
