import pytest

from alerta_chuva.enums.locais import LocalRiver
from alerta_chuva.services.crawler.crawler import Crawler


async def test_se_pega_ultimos_acumulados_de_chuva(crawler: Crawler):
    acumulado = await crawler.get_rainfall_data()
    esperado = max([i.station_id for i in acumulado.rain_register])
    assert all(i.station_id for i in acumulado.rain_register)
    assert len(acumulado.rain_register) == esperado


async def test_se_pega_as_imagens_do_radar(crawler: Crawler):
    # O site pode ficar lento e não trazer as 20 imagens mas 1 pelo menos traz.
    imgs = await crawler.get_radar_img()
    assert len(tuple(imgs)) > 0


@pytest.mark.parametrize("index_img", [i for i in range(20)])
def test_se_cria_url_img_radar(crawler: Crawler, index_img: int):
    esperado = "radar00{}".format(index_img)
    if index_img >= 10:
        esperado = "radar0{}".format(index_img)
    url = crawler.create_url_img_radar(index_img)
    assert esperado in url


async def test_se_faz_crawler_do_river(crawler: Crawler):
    pavuna = LocalRiver.PAVUNA.value
    result = await crawler.get_river_data(pavuna)
    assert "Meriti" in result


async def test_se_extrai_dados_do_river(crawler: Crawler):
    pavuna = LocalRiver.PAVUNA.value
    result = await crawler.river_data(pavuna)
    assert tuple(result.keys()) == (
        "hora",
        "quantity_15_min",
        "quantity_1h",
        "quantity_14h",
        "quantity_24h",
        "quantity_96h",
        "quantity_30d",
        "rio",
    )
