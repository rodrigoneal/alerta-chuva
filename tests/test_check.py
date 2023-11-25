from alerta_chuva.check import local_str_to_int


def test_se_retorna_id_local():
    assert local_str_to_int("Vidigal") == 1


def test_se_retorna_id_local_int():
    assert local_str_to_int(1) == 1
