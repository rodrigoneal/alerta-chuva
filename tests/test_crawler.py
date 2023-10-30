from pytest_httpx import HTTPXMock
import pytest
from transbordou.process.crawler import Crawler


@pytest.fixture(scope="session")
def html_response():
    with open("tests/data/IRAJA.html", "r") as f:
        return f.read()


async def test_se_faz_o_crawler(httpx_mock: HTTPXMock, html_response):
    httpx_mock.add_response(status_code=200, html=html_response)
    esperado = "IRAJA"
    results = await Crawler().get_data()
    estacao = results[0]
    assert estacao[0].estacao == esperado
