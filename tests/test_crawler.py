import pytest
from pytest_httpx import HTTPXMock

from transbordou.process.crawler import Crawler


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


# async def test_se_salva_no_banco_de_dados(crawler: Crawler, chuva_repository):
#     await crawler.scrape()
#     await crawler.save_rain()
#     assert await chuva_repository.read("IRAJA")


async def test_se_baixa_historico__de_uma_estacao_pluviometricos(crawler: Crawler):
    crawler = await crawler.get_rainfall_history(estacao="IRAJA", year=2023)
    breakpoint()


async def test_se_baixa_historico_pluviometricos_todas_estacoes(crawler: Crawler):
    crawler = await crawler.get_rainfall_history_all_stations(1998)
    breakpoint()
