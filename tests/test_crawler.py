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
