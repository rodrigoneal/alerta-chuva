import pytest
from pytest_httpx import HTTPXMock

from alerta_chuva.services.radar.radar import Radar


@pytest.fixture
def radar():
    return Radar()


@pytest.fixture
def radar_img(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=200,
        content=open("tests/data/img/radar.png", "rb").read(),
    )


async def test_se_pega_dados_do_radar_e_mostra_presenca_de_chuva(
    radar: Radar, radar_img
):
    radar_info = await radar.get_rain_intensity()
    _radar = sorted(radar_info, key=lambda x: x.grau, reverse=True)[0]
    assert _radar.grau >= 5


async def test_se_pega_dados_do_radar_e_mostra_presenca_de_chuva_no_columbia(
    radar: Radar, radar_img
):
    radar_info = await radar.get_rain_intensity("Columbia")
    _radar = sorted(radar_info, key=lambda x: x.grau, reverse=True)[0]
    assert _radar.grau == 0
