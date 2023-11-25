from datetime import datetime

from alerta_chuva.domain.model import ChuvaModel


def test_se_model_cria_uma_representacao_do_objeto():
    chuva = ChuvaModel(id=1, data=datetime(2022, 1, 1, 0, 0), station_id=1)
    assert (
        "ChuvaModel(data: datetime.datetime(2022, 1, 1, 0, 0), id: 1, quantity_05_min: None, quantity_10_min: None,"
        in repr(chuva)
    )
