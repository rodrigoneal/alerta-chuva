from datetime import date, datetime
from functools import lru_cache

from alerta_chuva.domain.entities.rain import RainRead
from alerta_chuva.domain.repositories.rain_repository import RainRepository
from alerta_chuva.services.crawler.crawler import Crawler


class Rain:
    chuva = (0.1, 10000.0)
    chuva_fraca = (0.1, 5.0)
    chuva_moderada = (5.1, 25.0)
    chuva_forte = (25.1, 50.0)
    chuva_muito_forte = (50.1, 1000.0)

    def __init__(self):
        self.crawler = Crawler()


    async def get_rain(self):
        return await self.crawler.get_rainfall_data()
        