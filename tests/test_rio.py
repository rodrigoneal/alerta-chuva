import pytest
from pytest_httpx import HTTPXMock

from alerta_chuva.domain.entities.river import RiverCreate
from alerta_chuva.enums.locais import LocalRiver
from alerta_chuva.services.river.river import River


@pytest.fixture
def mock_request_river(httpx_mock: HTTPXMock):
    html = """
    <table class="Table" id="Table" style="width: 100%;">
    <tr>
        <td align="center" colspan="1" style="background-color: #EBECEE;">28/11/2023 13:30</td>
        <td align="center" colspan="1" style="background-color: #DDF4FF;">0.0</td>
        <td align="center" colspan="1" style="background-color: #DDF4FF;">0.0</td>
        <td align="center" colspan="1" style="background-color: #DDF4FF;">0.0</td>
        <td align="center" colspan="1" style="background-color: #DDF4FF;">0.4</td>
        <td align="center" colspan="1" style="background-color: #DDF4FF;">2.0</td>
        <td align="center" colspan="1" style="background-color: #DDF4FF;">34.0</td>
        <td align="center" colspan="1" style="background-color: #ABE3FF;">0.42</td>
    </tr></table>"""
    httpx_mock.add_response(
        status_code=200,
        content=html,
    )


@pytest.fixture
def river():
    return River()


def test_se_cria_um_instancia_rio():
    assert River()


async def test_se_pega_os_ultimos_dados_do_rio(
    river: River, mock_request_river: HTTPXMock
):
    esperado = RiverCreate(
        hora="28/11/2023 13:30",
        quantity_15_min=0.0,
        quantity_1h=0.0,
        quantity_14h=0.0,
        quantity_24h=0.4,
        quantity_96h=2.0,
        quantity_30d=34.0,
        rio=0.42,
    )

    data = await river.get_river_data(LocalRiver.PAVUNA)
    assert data == esperado
