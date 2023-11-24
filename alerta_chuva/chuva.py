from datetime import date, datetime
from functools import cache

from alerta_chuva.check import insentidade_chuva
from alerta_chuva.domain.entities.rain import RainRead
from alerta_chuva.domain.repositories.rain_repository import RainRepository


class Chuva:
    chuva_detectada = (0.1, 10000.0)
    chuva_fraca = (0.1, 5.0)
    chuva_moderada = (5.1, 25.0)
    chuva_forte = (25.1, 50.0)
    chuva_muito_forte = (50.1, 1000.0)

    def __init__(self, rain_repository: RainRepository):
        self._chuva: list[RainRead] = None
        self.rain_repository = rain_repository

    @cache
    async def get_rains(self, date: datetime | date, station_id: int) -> list[RainRead]:
        return await self.rain_repository.read_rain_by_date(date, station_id)

    @insentidade_chuva(intensidade=chuva_detectada)
    async def chuva_detectada(
        self, *, station: str | int, data: str = None, hora: str = None
    ) -> bool:
        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_fraca)
    async def choveu_fraca(
        self, *, station: str | int, data: str = None, hora: str = None
    ) -> bool:
        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_moderada)
    async def choveu_moderado(
        self, *, station: str | int, data: str = None, hora: str = None
    ) -> bool:
        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_forte)
    async def choveu_forte(
        self, *, station: str | int, data: str = None, hora: str = None
    ) -> bool:
        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_muito_forte)
    async def choveu_muito_forte(
        self, *, station: str | int, data: str = None, hora: str = None
    ) -> bool:
        ...  # pragma: no cover
