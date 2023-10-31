import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from unidecode import unidecode

from transbordou.domain.entities.rain import RainCreate


def coletar(str: str):
    soup = BeautifulSoup(str, "html.parser")
    rows = soup.find_all("tr")
    th_elements = soup.find_all("th")
    th_with_colspan = [th for th in th_elements if th.has_attr("colspan")]
    estacao = th_with_colspan[0].text
    estacao = unidecode(estacao.upper())
    acumulados = []
    for row in rows:
        # Encontre todas as colunas (td) na linha
        columns = row.find_all("td")
        if not columns:
            continue
        # Acesse as informações que você deseja com base na posição das colunas
        data = columns[0].text.strip()
        hora = columns[1].text.strip()
        quantidade_15_min = columns[2].text
        quantidade_1_h = columns[3].text
        quantidade_4_h = columns[4].text.strip()
        quantidade_24_h = columns[5].text.strip()
        quantidade_96_h = columns[6].text.strip()
        quantidade_mes = columns[7].text.strip()
        acumulado = RainCreate(
            data=data + " " + hora,
            estacao=estacao,
            quantidade_15_min=quantidade_15_min,
            quantidade_1_h=quantidade_1_h,
            quantidade_4_h=quantidade_4_h,
            quantidade_24_h=quantidade_24_h,
            quantidade_96_h=quantidade_96_h,
            quantidade_mes=quantidade_mes,
        )
        acumulados.append(acumulado)
    return acumulados


def unzip_all_file(file_name, delete_after_extract: bool = True):
    for file in Path(file_name).glob("*.zip"):
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(file_name)
        if delete_after_extract:
            file.unlink()


def parser_txt_to_DataFrame(file: str, station_name: str):
    columns = [
        "data",
        "estacao",
        "quantidade_15_min",
        "quantidade_1_h",
        "quantidade_4_h",
        "quantidade_24_h",
        "quantidade_96_h",
        "quantidade_mes",
    ]

    df = pd.read_csv(file, sep=r"\s+", encoding="latin-1", skiprows=4)
    if df.empty:
        return
    df.dropna(how="all", axis=1, inplace=True)
    df.rename(columns=dict(zip(df.columns, columns)), inplace=True)
    df["data"] = df["data"] + " " + df["estacao"]
    df["estacao"] = station_name
    df["quantidade_mes"] = np.nan
    df["quantidade_15_min"] = pd.to_numeric(df["quantidade_15_min"], errors="coerce")
    return df


def extract_name_from_txt(text: str):
    pattern = r"^([^0-9]+)"
    match = re.search(pattern, text)
    return match.group(1).strip().replace("_", " ").upper()
