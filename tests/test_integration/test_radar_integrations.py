import pytest
from alerta_chuva.services.radar.radar import Radar

@pytest.fixture
def radar():
    return Radar()

async def test_se_pega_dados_do_radar_e_mostra_presenca_de_chuva(radar: Radar):
    radar_info = await radar.radar()
    radar_info.save_img()
    assert radar_info.grau > 5