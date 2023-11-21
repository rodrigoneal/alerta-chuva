import re

from unidecode import unidecode

from alerta_chuva.enums.locais import Local


def normalize_station_name(text: str) -> str:
    upper_text = text.upper().strip().replace(" ", "_")
    upper_text = unidecode(upper_text)
    if upper_text in Local.__members__:
        return upper_text
    if "/" in upper_text:
        return upper_text.split("/")[1].strip()
    return upper_text


def station_to_int(text: str) -> int:
    try:
        return Local[text].value
    except KeyError:
        if text == "RECREIO":
            return Local.RECREIO_DOS_BANDEIRANTES.value


def parser_float(text: str) -> float:
    if isinstance(text, float):
        return text
    if text == "ND" or not text:
        return None
    return float(text.strip().replace(",", "."))


def extrair_nome_de_estacao(text: str):
    padrao = r"ESTACAO_(.*)"
    estacao = re.search(padrao, text)
    if estacao:
        estacao = estacao.group(1).strip()
        return estacao.strip()
    else:
        return text


def pipeline_text(text: str):
    station = normalize_station_name(text)
    station = extrair_nome_de_estacao(station)
    return station_to_int(station)
