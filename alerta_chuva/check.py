from typing import Callable, ParamSpec, TypeAlias
from alerta_chuva.enums.locais import LocalChuva
from alerta_chuva.parser.parser import str_to_datetime_or_date

P = ParamSpec("P")
T = ParamSpec("T")

Func: TypeAlias = Callable[P, T] # type: ignore


def local_str_to_int(local: str):
    if isinstance(local, int):
        return local
    _local = local.upper()
    return LocalChuva[_local].value


def check_intensity(chuva: float, intensity: tuple[float, float]) -> bool:
    return chuva >= intensity[0] and chuva < intensity[1]


def insentidade_chuva(intensidade: str):
    def func(f: Func) -> Func:
        async def inner(*args: P.args, **kwargs: P.kwargs) -> T: # type: ignore
            station = local_str_to_int(kwargs.get("station"))
            data_chuva = kwargs.get("data")
            hora_chuva = kwargs.get("hora")
            date = str_to_datetime_or_date(data_chuva, hora_chuva)
            self: "Chuva" = args[0]
            chuva = (await self.get_rains(date, station))
            if chuva:
                quantidade = chuva.quantity_24_h if not hora_chuva else chuva.quantity_15_min
                return check_intensity(chuva=quantidade, intensity=intensidade)
            return False

        return inner

    return func
