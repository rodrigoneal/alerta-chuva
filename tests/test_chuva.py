import pytest

from alerta_chuva.domain.entities.rain import RainCreate
from alerta_chuva.services.crawler.crawler import Crawler
from alerta_chuva.services.rain.rain import Rain


@pytest.fixture
async def rain_create(html_response, crawler: Crawler):
    return crawler.extract_info_rain(html_response)[0]


@pytest.mark.parametrize(
    "rain,expected",
    [
        (Rain.chuva, True),
        ((0.0, 0.0), False),
        (Rain.chuva_fraca, True),
        (Rain.chuva_moderada, False),
        (Rain.chuva_forte, False),
        (Rain.chuva_muito_forte, False),
    ],
)
def test_se_detecta_chuva(rain_create: RainCreate, rain, expected):
    result = rain_create == rain
    assert result == expected
