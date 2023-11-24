from typing import Callable, ParamSpec, TypeAlias

from alerta_chuva.enums.locais import LocalChuva
from alerta_chuva.parser.parser import str_to_datetime_or_date

P = ParamSpec("P")
T = ParamSpec("T")

Func: TypeAlias = Callable[P, T]  # type: ignore


def local_str_to_int(station: str) -> int:
    """
    Converte o nome do local para o id da estação.

    Args:
        station (str): Estação. Ex: 'Vidigal'

    Returns:
        int: Id da estação.
    """
    if isinstance(station, int):
        return station
    _local = station.upper()
    return LocalChuva[_local].value


def check_intensity(chuva: float, intensity: tuple[float, float]) -> bool:
    """
    Verifica se a chuva esta dentro da faixa.
    Para saber se houve chuva forte, fraca e etc.
    Você passa a faixa de chuva e a chuva que foi registrada.
    Exemplo:
        chuva >= 0.8 and chuva < 1.0


    Args:
        chuva (float): Quantidade de chuva acumulada que será verificado.
        intensity (tuple[float, float]): Faixa de chuva que será verificada.

    Returns:
        bool: Retorna True se houve chuva dentro da faixa.
    """
    return chuva >= intensity[0] and chuva < intensity[1]


def insentidade_chuva(intensidade: str):
    """
    Decorator para verificar a intensidade da chuva.
    Pega a intensidade do argumento e chama a função check_intensity

    Exemplo:
        @insentidade_chuva('forte')
        async def check_chuva(self, **kwargs):
            return True

    Args:
        intensidade (str): _description_
    """

    def func(f: Func) -> Func:
        async def inner(*args: P.args, **kwargs: P.kwargs) -> T:  # type: ignore
            station = local_str_to_int(kwargs.get("station"))
            data_chuva = kwargs.get("data")
            hora_chuva = kwargs.get("hora")
            date = str_to_datetime_or_date(data_chuva, hora_chuva)
            self = args[0]
            chuva = await self.get_rains(date, station)
            if chuva:
                quantidade = (
                    chuva.quantity_24_h if not hora_chuva else chuva.quantity_15_min
                )
                return check_intensity(chuva=quantidade, intensity=intensidade)
            return False

        return inner

    return func
