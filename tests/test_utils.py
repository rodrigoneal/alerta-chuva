import math
import pytest
from transbordou.locais import Local

from transbordou.utils.text import (
    extrair_nome_de_estacao,
    normalize_station_name,
    parser_float,
    pipeline_text,
    station_to_int,
)
import numpy as np


def estacao_nome():
    with open("tests/locais.txt") as file:
        params = []
        for line in enumerate(file.readlines(), start=1):
            params.append((line[1].strip(), line[0]))
    return params


@pytest.mark.parametrize("valor, esperado", estacao_nome())
def test_se_faz_a_normalização_da_estação(valor, esperado):
    text = normalize_station_name(valor)
    assert Local[text].value == esperado


@pytest.mark.parametrize("valor, esperado", estacao_nome())
def test_se_transforma_o_nome_da_estacao_em_int(valor, esperado):
    station = normalize_station_name(valor)
    assert station_to_int(station) == esperado


@pytest.mark.parametrize("valor, esperado", [(5.1, 5.1), ("ND", None), ("0.0", 0.0), (None, None)])
def test_se_converte_volume_de_chuva_para_float(valor, esperado):
    assert parser_float(valor) == esperado


@pytest.mark.parametrize("valor, esperado", estacao_nome())
def test_pipelipe_de_normalizar_estacao(valor, esperado):
    assert pipeline_text(valor) == esperado

@pytest.mark.parametrize("valor, esperado", [("Dados Pluviométrico da Estação Irajá", "IRAJA"), ("VIDIGAL", "VIDIGAL")])
def test_se_extrai_nome_da_estacao(valor, esperado):
    station = normalize_station_name(valor)
    assert extrair_nome_de_estacao(station) == esperado