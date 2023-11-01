import httpx
import pytest
from pytest_httpx import HTTPXMock

from transbordou.domain.repositories.rain_repository import RainRepository
from transbordou.process.crawler import Crawler
from transbordou.utils.crawler import (download_rainfall_history_all_stations,
                                       download_rainfall_history_one_station)


def site_online():
    URL = "http://alertario.rio.rj.gov.br/download/dados-pluviometricos/"
    return httpx.get(URL).status_code == 200


@pytest.fixture(scope="session")
def html_response():
    with open("tests/data/IRAJA.html", "r") as f:
        return f.read()


@pytest.fixture
def crawler(chuva_repository):
    return Crawler(chuva_repository)


async def test_se_faz_o_crawler(httpx_mock: HTTPXMock, html_response, crawler: Crawler):
    httpx_mock.add_response(status_code=200, html=html_response)
    esperado = "IRAJA"
    await crawler.scrape()
    assert crawler.rains[0].estacao == esperado


@pytest.mark.slow
async def test_se_salva_no_banco_de_dados(crawler: Crawler, chuva_repository):
    await crawler.scrape()
    await crawler.save()
    assert await chuva_repository.read("IRAJA")


@pytest.mark.skipif(site_online, reason="Temporariamente desativado")
async def test_se_baixa_historico_de_uma_estacao_pluviometricos(
    crawler: Crawler, chuva_repository: RainRepository
):
    crawler = await crawler.download_rainfall_history(
        func=download_rainfall_history_one_station, estacao="IRAJA", year=2023
    )
    chuvas = await chuva_repository.read("IRAJA")
    assert len(chuvas) > 100


@pytest.mark.skipif(site_online, reason="Temporariamente desativado")
async def test_se_baixa_historico_pluviometricos_todas_estacoes(
    crawler: Crawler, chuva_repository: RainRepository
):
    crawler = await crawler.download_rainfall_history(
        func=download_rainfall_history_all_stations, year=1998
    )
    chuvas = await chuva_repository.read("IRAJA")
    assert len(chuvas) > 100
