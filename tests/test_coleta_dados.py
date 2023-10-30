import pytest
from transbordou.coletar import coletar


from transbordou.locais import Local
from transbordou.chuva import Chuva


@pytest.fixture(scope="session")
def html_response():
    with open("tests/data/IRAJA.html", "r") as f:
        return f.read()

@pytest.fixture(scope="session")
def chuva(html_response):
    chuva = Chuva()
    chuva._chuva = coletar(html_response)
    return chuva

def test_se_dados_informa_que_houve_chuva(chuva:Chuva):
    assert chuva.choveu(estacao="IRAJA", data="29/10/2023") is True


# def test_se_dados_informa_que_houve_chuva(chuva):
#     chuva = Chuva()
#     assert chuva.coletar("iraja").choveu("29/10/2023", "20:00:00") is True


# def test_se_dados_informa_que_houve_chuva_fraca(chuva):
#     chuva = Chuva()
#     assert chuva.coletar("iraja").choveu_fraca("29/10/2023") is True


# def test_se_dados_informa_que_houve_chuva_moderada(chuva):
#     chuva = Chuva()
#     assert chuva.coletar("iraja").choveu_moderado("29/10/2023") is True


# def test_se_dados_informa_que_houve_chuva_forte(chuva):
#     chuva = Chuva()
#     assert chuva.coletar("iraja").choveu_forte("29/10/2023") is False


# def test_se_pega_maior_acumulado_de_chuva(chuva):
#     chuva = Chuva()
#     chuva.coletar("iraja").maior_acumulado("29/10/2023").quantidade_15_min == 14.4
