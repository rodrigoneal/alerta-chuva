import re


from bs4 import BeautifulSoup
from dateutil import parser
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
