from datetime import datetime

import cv2
import numpy as np
import pytest

from alerta_chuva.enums.locais import LocalRadar
from alerta_chuva.services.radar.radar import Radar


@pytest.fixture
def radar():
    return Radar()


def test_se_encontra_as_cores_e_graus(radar: Radar):
    assert radar.cores_e_graus == {
        (17, 167, 12): 1,
        (19, 122, 19): 2,
        (4, 85, 4): 3,
        (195, 230, 0): 4,
        (255, 112, 0): 5,
        (227, 6, 5): 6,
        (197, 0, 197): 7,
    }


@pytest.fixture
def imagem_radar():
    return cv2.imread("tests/data/img/radar.png")


@pytest.mark.parametrize(
    "imagem, grau",
    [
        (np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), 0),
        (np.array([[[17, 167, 12]]]), 1),
        (np.array([[[19, 122, 19]]]), 2),
        (np.array([[[4, 85, 4]]]), 3),
        (np.array([[[195, 230, 0]]]), 4),
        (np.array([[[255, 112, 0]]]), 5),
        (np.array([[[227, 6, 5]]]), 6),
        (np.array([[[197, 0, 197]]]), 7),
    ],
)
def test_se_encontra_grandeza(radar: Radar, imagem, grau):
    assert radar.find_rain_intensity(imagem) == grau


async def test_se_abre_imagem_em_bytes(radar: Radar):
    with open("tests/data/img/img.png", "rb") as f:
        imagem = f.read()
    grandeza = radar.check_radar(imagem, LocalRadar.COLUMBIA)
    assert grandeza.grau == 3
    assert grandeza.grau == 3


@pytest.mark.parametrize(
    "imagem, grau",
    [
        (("tests/data/img/radar.png"), 0),
        (("tests/data/img/img.png"), 3),
    ],
)
def test_se_encontra_grandeza_no_columbia(radar: Radar, imagem, grau):
    grandeza = radar.check_radar(imagem, LocalRadar.COLUMBIA)
    assert grandeza.grau == grau


def test_se_pega_a_data_da_imagem_do_radar(radar: Radar):
    esperado = datetime(2023, 11, 20, 14, 54, 57)
    imagem = cv2.imread("tests/data/img/img.png")
    date = radar.extract_date_img_radar(imagem)
    assert date.data == esperado


# async def test_se_pega_a_ultima_imagem_do_radar(radar: Radar):
#     last = await radar.last_img_radar()
#     assert isinstance(last[0], datetime)
#     assert isinstance(last[1], np.ndarray)


def test_se_encontra_chuva_na_ilha(radar: Radar, imagem_radar: np.ndarray):
    grandeza = radar.check_radar(imagem_radar, LocalRadar.ILHA_DO_GOVERNADOR)
    assert grandeza.grau == 3


def test_se_encontra_chuva_no_campo_grande(radar: Radar, imagem_radar: np.ndarray):
    grandeza = radar.check_radar(imagem_radar, LocalRadar.CAMPO_GRANDE)
    assert grandeza.grau == 0


def test_se_encontra_chuva_no_columbia(radar: Radar, imagem_radar: np.ndarray):
    grandeza = radar.check_radar(imagem_radar, LocalRadar.COLUMBIA)
    assert grandeza.grau == 0


async def test_se_pega_a_intensidade_de_todas_as_imagens_do_radar(radar: Radar):
    intensidades = await radar.get_rain_intensity(LocalRadar.RIO)
    assert len(intensidades) > 0


@pytest.mark.parametrize(
    "regiao, esperado",
    [
        (
            "COLUMBIA",
            ((491, 346), 20),
        ),
        (
            "CAMPO_GRANDE",
            ((429, 366), 30),
        ),
        (
            "ILHA_DO_GOVERNADOR",
            ((527, 341), 50),
        ),
        (
            "NORTE",
            ((480, 356), 50),
        ),
        (
            "SUL",
            ((516, 407), 50),
        ),
        (
            "OESTE",
            ((381, 370), 50),
        ),
        (
            "LESTE",
            ((490, 366), 320),
        ),
        (
            "RIO",
            ((490, 366), 320),
        ),
    ],
)
def test_se_retorna_a_regiao_do_radar(radar: Radar, regiao, esperado):
    attr = getattr(LocalRadar, regiao)
    assert radar.region_of_interest(attr) == esperado


@pytest.mark.parametrize(
    "regiao, esperado",
    [
        (
            "COLUMBIA",
            ((491, 346), 20),
        ),
        (
            "CAMPO GRANDE",
            ((429, 366), 30),
        ),
        (
            "ILHA DO GOVERNADOR",
            ((527, 341), 50),
        ),
        (
            "NORTE",
            ((480, 356), 50),
        ),
        (
            "SUL",
            ((516, 407), 50),
        ),
        (
            "OESTE",
            ((381, 370), 50),
        ),
        (
            "LESTE",
            ((490, 366), 320),
        ),
        (
            "RIO",
            ((490, 366), 320),
        ),
    ],
)
def test_se_retorna_regiao_por_string(radar: Radar, regiao, esperado):
    assert radar.region_of_interest(regiao) == esperado
