# Modulo com os enums para o site da prefeitura do Rio.

from enum import Enum


class LocalChuva(Enum):
    """Locais que o o site da prefeitura do rio tem captação da chuva.
    Eu fiz a conversão do nome do local para o valor do enum.
    Para ajudar a compreender e pegar os locais usados no site da prefeitura do
    Rio.

    Args:
        Enum (_type_): _description_
    """

    VIDIGAL = 1
    URCA = 2
    ROCINHA = 3
    TIJUCA = 4
    SANTA_TERESA = 5
    COPACABANA = 6
    GRAJAU = 7
    ILHA_DO_GOVERNADOR = 8
    PENHA = 9
    MADUREIRA = 10
    IRAJA = 11
    BANGU = 12
    PIEDADE = 13
    TANQUE = 14
    SAUDE = 15
    JARDIM_BOTANICO = 16
    BARRINHA = 17
    CIDADE_DE_DEUS = 18
    RIOCENTRO = 19
    GUARATIBA = 20
    JACAREPAGUA = 21
    SANTA_CRUZ = 22
    GRANDE_MEIER = 23
    ANCHIETA = 24
    GROTA_FUNDA = 25
    CAMPO_GRANDE = 26
    SEPETIBA = 27
    ALTO_DA_BOA_VISTA = 28
    MENDANHA = 29
    RECREIO_DOS_BANDEIRANTES = 30
    LARANJEIRAS = 31
    SAO_CRISTOVAO = 32
    MUDA = 33


class LocalRadar(Enum):
    """Locais que consegui identificar no radar.
    Pode usar esses lugares para verificar se há alguma chuva captada pelo radar.
    Enumerei para quando alguém precisar saber quais locaia já foram identificadas
    no radar.
    """

    RIO = ((490, 366), 320)
    COLUMBIA = ((491, 346), 20)
    CAMPO_GRANDE = ((429, 366), 30)
    ILHA_DO_GOVERNADOR = ((527, 341), 50)
    NORTE = ((480, 356), 50)
    SUL = ((516, 407), 50)
    LESTE = ((490, 366), 320)
    OESTE = ((381, 370), 50)

    def __repr__(self) -> str:
        return self.name


class LocalRiver(str, Enum):
    """Locais onde há dados do nivel dos rios, Eu resolvi limitar por locais proximos a capital,
    pois se eu fosse pegar todos os locais iria demorar muito.

    """

    PAVUNA = "224329420"
    MARACANA = "22544313020"
    CACHOEIRA = "BE70E16620"
    GUANDU = "22484337020"
    BOTA = "22484337020"
    CACHIMBO = "224329320"
    CAPIVARI = "224327820"
    SARACURUNA = "224327420"

    def __repr__(self) -> str:
        return self.name
