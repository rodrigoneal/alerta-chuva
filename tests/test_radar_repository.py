from datetime import datetime

import numpy as np
import pytest

from alerta_chuva.domain.entities.radar import RadarCreate, RadarUpdate
from alerta_chuva.domain.repositories.radar_repository import RadarRepository


@pytest.fixture
def radar_repository(session):
    return RadarRepository(session)


@pytest.fixture
async def populate_db(radar_repository):
    radar = RadarCreate(
        data=datetime.now(), img=np.zeros((10, 10, 3), np.uint8), grau=2
    )
    radar = await radar_repository.create(radar)
    return radar


async def test_se_salva_um_radar_no_banco_de_dados(radar_repository):
    radar = RadarCreate(
        data=datetime.now(), img=np.zeros((10, 10, 3), np.uint8), grau=2
    )
    radar = await radar_repository.create(radar)
    assert radar.id == 1


async def test_se_pega_um_valor_do_banco_de_dados(radar_repository, populate_db):
    radar = await radar_repository.read()
    assert radar[0].grau == 2


async def test_se_atualiza_um_radar_no_banco_de_dados(radar_repository, populate_db):
    radar = RadarUpdate(grau=3)
    result = await radar_repository.update(schema=radar, _id=1)
    assert result.grau == 3
    assert result.img


async def test_se_deleta_um_radar_no_banco_de_dados(radar_repository, populate_db):
    result = await radar_repository.delete(_id=1)
    assert result.id == 1


async def test_se_pega_um_valor_pela_data(radar_repository, populate_db):
    agora = datetime.now()
    radar = await radar_repository.read_by_date(date=agora)
    assert radar[0].grau == 2
