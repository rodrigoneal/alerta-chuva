import base64
import httpx
import pytest
from pytest_httpx import HTTPXMock


from transbordou.domain.repositories.rain_repository import RainRepository
from transbordou.process.crawler import Crawler


def site_online():
    URL = "http://alertario.rio.rj.gov.br/download/dados-pluviometricos/"
    return httpx.get(URL).status_code != 200


@pytest.fixture(scope="session")
def html_response():
    with open("tests/data/IRAJA.html", "r") as f:
        return f.read()


@pytest.fixture
def crawler(chuva_repository):
    return Crawler(chuva_repository)


async def test_se_pega_ultimos_acumulados_de_chuva(crawler: Crawler):
    acumulado = await crawler.get_rainfall_data()
    esperado = max([i.station_id for i in acumulado.rain_register])
    assert all(i.station_id for i in acumulado.rain_register)
    assert len(acumulado.rain_register) == esperado


async def test_se_pega_as_imagens_do_radar(crawler: Crawler):
    imgs = await crawler.get_radar_img()
    assert len(imgs) == 20
