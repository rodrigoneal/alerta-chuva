from datetime import date, datetime

from dateutil import parser
from sqlalchemy.ext.asyncio import AsyncEngine

from transbordou.domain.entities.rain import RainRead
from transbordou.domain.repositories.rain_repository import RainRepository
from transbordou.locais import Local


class Chuva:
    chuva_fraca = (0.1, 5.0)
    chuva_moderada = (5.1, 25.0)
    chuva_forte = (25.1, 50.0)
    chuva_muito_forte = (50.1, 1000.0)

    def __init__(self, rain_repository: RainRepository):
        self._chuva: list[RainRead] = None
        self.rain_repository = rain_repository

    def _to_datetime_or_date(self, data: str, hora: str = None) -> datetime | date:
        if hora:
            date = parser.parse(data + " " + hora, dayfirst=True)
        else:
            date = parser.parse(data, dayfirst=True).date()
        return date

    async def choveu(self, estacao: str | int, data: str, hora: str = None) -> bool:
        if isinstance(estacao, int):
            _estacao = Local(int).name
        elif isinstance(estacao, str):
            _estacao = estacao.upper()
        date = self._to_datetime_or_date(data, hora)
        result = await self.rain_repository.is_raining(_estacao, date)
        if result:
            return True
        return False

    async def choveu_fraca(self, data: str, hora: str = None) -> bool:
        return await self._rain_intensity(data, self.chuva_fraca, hora)

    async def choveu_forte(self, data: str, hora: str = None) -> bool:
        return await self._rain_intensity(data, self.chuva_forte, hora)

    async def choveu_muito_forte(self, data: str, hora: str = None) -> bool:
        return await self._rain_intensity(data, self.chuva_muito_forte, hora)

    async def choveu_moderado(self, data: str, hora: str = None) -> bool:
        return await self._rain_intensity(data, self.chuva_moderada, hora)

    async def _rain_intensity(
        self, data: str, intensity: tuple[float], hora: str = None
    ) -> bool:
        if await self.rain_repository.rain_intensity(
            "IRAJA", self._to_datetime_or_date(data, hora), intensity
        ):
            return True
        return False

    def maior_acumulado(self, data: str) -> RainRead:
        date = parser.parse(data).date()
        chuvas = [chuva for chuva in self._chuva if chuva.data.date() == date]
        return max(chuvas, key=lambda chuva: chuva.quantidade_1_h)
