from datetime import datetime

import numpy as np
import pytest

from alerta_chuva.commom.aux import RadarImgInfo, RainRecord
from alerta_chuva.domain.entities.rain import RainCreate


@pytest.fixture
def rain_create():
    return RainCreate(
        station_id=1,
        station_name="Vidigal",
        region="RJ",
        data="2022-01-01 00:00:00",
        quantity_05_min=0.0,
        quantity_10_min=0.0,
        quantity_15_min=0.0,
        quantity_30_min=0.0,
        quantity_1_h=0.0,
        quantity_2_h=0.0,
        quantity_3_h=0.0,
        quantity_4_h=0.0,
        quantity_6_h=0.0,
        quantity_12_h=0.0,
        quantity_24_h=0.0,
        quantity_96_h=0.0,
        quantity_month=0.0,
        tx_15=0.0,
    )


async def test_se_salva_acumulo_de_chuva(chuva_repository, rain_create):
    esperado = 1
    rain_record = RainRecord([rain_create], chuva_repository)
    await rain_record.save()
    chuva = await chuva_repository.read(1, "station_id")
    assert chuva[0].id == esperado


def test_se_retorna_a_representacao_do_objecto(rain_create, chuva_repository):
    rain_record = RainRecord([rain_create], chuva_repository)
    assert repr(rain_record) == "RainRecord((1, 'Vidigal'))"


def test_se_salva_a_imagem_do_radar():
    from pathlib import Path

    imagem = np.zeros((100, 100, 3), dtype=np.uint8)
    radar_image = RadarImgInfo(datetime.now(), imagem)
    img = radar_image.save_img("radar")
    path = Path(img)
    assert path.exists()
    path.unlink()


@pytest.mark.xfail
def test_se_salva_mapa_do_radar():
    from pathlib import Path

    imagem = np.zeros((100, 100, 3), dtype=np.uint8)
    radar_image = RadarImgInfo(datetime.now(), imagem)
    img = radar_image.save_map("radar")
    path = Path(img)
    assert path.exists()
    path.unlink()
