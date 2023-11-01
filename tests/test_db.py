import pytest

from transbordou.domain.entities.rain import RainCreate, RainUpdate


@pytest.fixture
def acumulado():
    data = "30/01/2022 10:00"
    return RainCreate(
        data=data,
        estacao="IRAJA",
        quantidade_15_min="0",
        quantidade_1_h="0",
        quantidade_4_h="0",
        quantidade_24_h="0",
        quantidade_96_h="0",
        quantidade_mes="0",
    )


@pytest.fixture
def acumulado_update():
    return RainUpdate(estacao="PAVUNA")


async def test_se_cria_chuva(acumulado, chuva_repository):
    chuva = await chuva_repository.create(acumulado)
    assert chuva.id == 1


async def test_se_consulta_chuva(chuva_repository, load_database):
    chuva = await chuva_repository.read("IRAJA")
    assert chuva[0].estacao == "IRAJA"


async def test_se_atualiza_chuva(acumulado_update, chuva_repository, load_database):
    chuva = await chuva_repository.update(acumulado_update, 1)
    assert chuva.estacao == "PAVUNA"


async def test_se_deleta_chuva(session, chuva_repository, load_database):
    chuva = await chuva_repository.delete(1)
    assert chuva.id == 1
