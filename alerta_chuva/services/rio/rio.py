from alerta_chuva.domain.repositories.rain_repository import RainRepository
from alerta_chuva.enums.locais import LocalRiver
from alerta_chuva.services.crawler.crawler import Crawler


class Rio:
    def __init__(self, rain_repository: RainRepository | None = None):
        self.crawler = Crawler(rain_repository)

    def river_of_interest(self, river: str | LocalRiver) -> str:
        if isinstance(river, str):
            _river = river.upper()
            return LocalRiver[_river].value
        else:
            return river.value

    async def get_river_data(self, river: str) -> str:
        river_location = self.river_of_interest(river)
        return await self.get_river_data(river_location)
