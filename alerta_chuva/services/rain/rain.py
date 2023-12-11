from datetime import date, datetime
from functools import lru_cache

from alerta_chuva.domain.entities.rain import RainRead
from alerta_chuva.domain.repositories.rain_repository import RainRepository


class Rain:
    chuva = (0.1, 10000.0)
    chuva_fraca = (0.1, 5.0)
    chuva_moderada = (5.1, 25.0)
    chuva_forte = (25.1, 50.0)
    chuva_muito_forte = (50.1, 1000.0)

    def __init__(self, rain_repository: RainRepository):
        self._chuva: list[RainRead] | None = None
        self.rain_repository = rain_repository

    @lru_cache(maxsize=10)
    async def get_rains(
        self, date: datetime | date, station_id: int
    ) -> RainRead | None:
        """
        Busca um acumulo de chuva no banco de dados a partir de uma data.

        Args:
            date (datetime | date): Data para buscar o acumulo de chuva.
            station_id (int): ID da estação para buscar o acumulo de chuva.

        Returns:
            RainRead: Acumulo de chuva.
        """
        model = await self.rain_repository.read_rain_by_date(date, station_id)
        if model:
            return RainRead.model_validate(model)
        return None
