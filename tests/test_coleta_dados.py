import pytest

from transbordou.chuva import Chuva


@pytest.fixture
def chuva(chuva_repository):
    return Chuva(chuva_repository)


async def test_se_pega_chuva_pela_data(chuva: Chuva, load_database):
    assert await chuva.choveu(estacao="IRAJA", data="29/10/2023") is True


async def test_se_pega_chuva_pela_data_hora(chuva: Chuva, load_database):
    assert (
        await chuva.choveu(estacao="IRAJA", data="29/10/2023", hora="22:30:00") is True
    )


async def test_se_dados_informa_que_houve_chuva_fraca(chuva: Chuva, load_database):
    assert await chuva.choveu_fraca("29/10/2023") is True


async def test_se_dados_informa_que_houve_chuva_moderada(chuva: Chuva, load_database):
    assert await chuva.choveu_moderado("29/10/2023") is True


async def test_se_dados_informa_que_houve_chuva_forte(chuva: Chuva, load_database):
    assert await chuva.choveu_forte("29/10/2023") is False


async def test_se_dados_informa_que_houve_chuva_muito_forte(
    chuva: Chuva, load_database
):
    assert await chuva.choveu_muito_forte("29/10/2023") is False
