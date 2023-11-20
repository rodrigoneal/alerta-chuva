from datetime import datetime

import pytest

from alerta_chuva.domain.entities.rain import RainCreate, RainUpdate


@pytest.fixture
def acumulado():
    data = "30/01/2022 10:00"
    return RainCreate(
        station_id=11,
        station_name="Estacao de teste",
        region="teste",
        data=data,
        quantity_05_min="10",
        quantity_10_min="10",
        quantity_15_min="10",
        quantity_30_min="10",
        quantity_1_h="10",
        quantity_2_h="10",
        quantity_3_h="10",
        quantity_4_h="10",
        quantity_6_h="10",
        quantity_12_h="10",
        quantity_24_h="10",
        quantity_96_h="10",
        quantity_month="10",
        tx_15="10",
    )


@pytest.fixture
def acumulado_update():
    return RainUpdate(station_id=55)


async def test_se_cria_chuva(acumulado, chuva_repository):
    chuva = await chuva_repository.create(acumulado)
    assert chuva.id == 1


async def test_se_consulta_chuva_pela_id_da_estacao(chuva_repository, load_database):
    chuva = await chuva_repository.read(1, "station_id")
    assert chuva[0].station_id == 1


async def test_se_consulta_chuva_pela_data(chuva_repository, load_database):
    data = datetime.strptime("20/11/2023 13:50:00", "%d/%m/%Y %H:%M:%S")
    chuva = await chuva_repository.read(data, "data")
    assert chuva[0].data == data


async def test_se_consulta_chuva_pelo_nome_da_estacao(chuva_repository, load_database):
    esperado = "Vidigal"
    chuva = await chuva_repository.read("Vidigal", "station_name")
    assert chuva[0].station_name == esperado


async def test_se_consulta_chuva_pela_regiao(chuva_repository, load_database):
    esperado = "Vidigal"
    chuva = await chuva_repository.read("Zona Sul", "region")
    assert chuva[0].station_name == esperado


async def test_se_atualiza_chuva(acumulado_update, chuva_repository, load_database):
    chuva = await chuva_repository.update(acumulado_update, 1)
    assert chuva.station_id == 55


async def test_se_deleta_chuva(chuva_repository, load_database):
    chuva = await chuva_repository.delete(1)
    assert chuva.id == 1
