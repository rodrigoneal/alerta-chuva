import pytest

from transbordou.chuva import Chuva
from transbordou.coletar import coletar


@pytest.fixture
def html_response():
    with open("tests/data/IRAJA.html", "r") as f:
        return f.read()


@pytest.fixture
async def load_database(html_response, chuva_repository):
    dados = coletar(html_response)
    [await chuva_repository.create(dado) for dado in dados]


@pytest.fixture
def chuva(chuva_repository):
    return Chuva(chuva_repository)


async def test_se_pega_chuva_pela_data(chuva: Chuva, load_database):
    assert await chuva.choveu(estacao="IRAJA", data="29/10/2023") is True


async def test_se_pega_chuva_pela_data_hora(chuva: Chuva, load_database):
    assert (
        await chuva.choveu(estacao="IRAJA", data="29/10/2023", hora="22:30:00") is True
    )


async def test_se_dados_informa_que_houve_chuva_fraca(chuva: Chuva):
    assert await chuva.choveu_fraca("29/10/2023") is True


async def test_se_dados_informa_que_houve_chuva_moderada(chuva: Chuva):
    assert await chuva.choveu_moderado("29/10/2023") is True


async def test_se_dados_informa_que_houve_chuva_forte(chuva: Chuva):
    assert await chuva.choveu_forte("29/10/2023") is False


async def test_se_dados_informa_que_houve_chuva_muito_forte(chuva: Chuva):
    assert await chuva.choveu_muito_forte("29/10/2023") is False


