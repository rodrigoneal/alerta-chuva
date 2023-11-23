from typing import Callable

from alerta_chuva.domain.entities.rain import RainRead
from alerta_chuva.domain.repositories.rain_repository import RainRepository
from alerta_chuva.enums.locais import Local
from alerta_chuva.parser.parser import str_to_datetime_or_date


class Chuva:
    chuva_detectada = (0.1, 10000.0)
    chuva_fraca = (0.1, 5.0)
    chuva_moderada = (5.1, 25.0)
    chuva_forte = (25.1, 50.0)
    chuva_muito_forte = (50.1, 1000.0)

    def __init__(self, rain_repository: RainRepository):
        self._chuva: list[RainRead] = None
        self.rain_repository = rain_repository

    @staticmethod
    def _rain_intensity(rain_intensity: str):
        def func(_: Callable[[str | int, str, str | None], bool]):
            async def inner(self, **kwargs):
                station = kwargs["station"].upper()
                if isinstance(station, str):
                    station = Local[station].value

                if await self.rain_repository.rain_intensity(
                    station,
                    str_to_datetime_or_date(kwargs.get("data"), kwargs.get("hora")),
                    getattr(self, rain_intensity),
                ):
                    return True
                return False

            return inner

        return func

    @_rain_intensity("chuva_detectada")
    async def choveu(self, *, station: str | int, data: str, hora: str = None) -> bool:
        ...  # pragma: no cover

    @_rain_intensity("chuva_fraca")
    async def choveu_fraca(
        self, *, station: str | int, data: str, hora: str = None
    ) -> bool:
        ...  # pragma: no cover

    @_rain_intensity("chuva_moderada")
    async def choveu_moderado(
        self, *, station: str | int, data: str, hora: str = None
    ) -> bool:
        ...  # pragma: no cover

    @_rain_intensity("chuva_forte")
    async def choveu_forte(
        self, *, station: str | int, data: str, hora: str = None
    ) -> bool:
        ...  # pragma: no cover

    @_rain_intensity("chuva_muito_forte")
    async def choveu_muito_forte(
        self, *, station: str | int, data: str, hora: str = None
    ) -> bool:
        ...  # pragma: no cover
