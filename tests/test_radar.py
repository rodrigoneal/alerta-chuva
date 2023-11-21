from datetime import datetime

import cv2
import numpy as np
import pytest

from alerta_chuva.services.radar.radar import Radar



@pytest.fixture
def radar():
    return Radar()

def test_se_encontrar_maior_grau_de_grandeza_no_radar(radar: Radar):
    imagem = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert radar.encontrar_maior_grau_de_grandeza(imagem, radar.cores_e_graus) == 0


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
    assert radar.encontrar_maior_grau_de_grandeza(imagem, radar.cores_e_graus) == grau


async def test_se_abre_imagem_em_bytes(radar: Radar):
    with open("tests/data/img/img.png", "rb") as f:
        imagem = f.read()
    grandeza = radar.verificar_radar(imagem, "Columbia")
    assert grandeza == 3


@pytest.mark.parametrize(
    "imagem, grau",
    [
        (("tests/data/img/radar.png"), 0),
        (("tests/data/img/img.png"), 3),
    ],
)
def test_se_encontra_grandeza_no_columbia(radar: Radar, imagem, grau):
    grandeza = radar.verificar_radar(imagem, "Columbia")
    assert grandeza == grau


def test_se_pega_a_data_da_imagem_do_radar(radar: Radar):
    esperado = datetime(2023, 11, 20, 14, 54, 57)
    imagem = cv2.imread("tests/data/img/img.png")
    date = radar.get_img_date(imagem)
    assert date == esperado
