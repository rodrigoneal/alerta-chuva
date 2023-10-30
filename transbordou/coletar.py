import re


from bs4 import BeautifulSoup
from dateutil import parser
from unidecode import unidecode


from transbordou.acumulado import Acumulado


def parser_float(text: str):
    if text == "ND":
        return 0.0
    return float(text.strip().replace(",", "."))

def nome_estacão(texto: str):
    padrao = r"Estação\s+(.*)"
    estacao = re.search(padrao, texto)
    if estacao:
        return estacao.group(1).strip()
    else:
        return None


def coletar(str: str):
    soup = BeautifulSoup(str, "html.parser")
    rows = soup.find_all("tr")
    th_elements = soup.find_all('th')
    th_with_colspan = [th for th in th_elements if th.has_attr('colspan')]
    estacao = nome_estacão(th_with_colspan[0].text)
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
        quantidade_15_min = parser_float(columns[2].text)
        quantidade_1_h = parser_float(columns[3].text)
        quantidade_4_h = parser_float(columns[4].text.strip())
        quantidade_24_h = parser_float(columns[5].text.strip())
        quantidade_96_h = parser_float(columns[6].text.strip())
        quantidade_mes = parser_float(columns[7].text.strip())
        acumulado = Acumulado(
            parser.parse(data + " " + hora),
            estacao,
            quantidade_15_min,
            quantidade_1_h,
            quantidade_4_h,
            quantidade_24_h,
            quantidade_96_h,
            quantidade_mes,
        )
        acumulados.append(acumulado)
    return acumulados
