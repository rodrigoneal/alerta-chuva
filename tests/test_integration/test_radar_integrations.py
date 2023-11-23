import pytest
from alerta_chuva.services.radar.radar import Radar

@pytest.fixture
def radar():
    return Radar()

async def test_se_pega_dados_do_radar_e_mostra_presenca_de_chuva(radar: Radar):
    grau = await radar.radar()
    assert grau > 5