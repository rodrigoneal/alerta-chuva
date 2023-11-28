from alerta_chuva.domain.entities.river import RiverCreate
from alerta_chuva.domain.repositories.rain_repository import RainRepository
from alerta_chuva.enums.locais import LocalRiver
from alerta_chuva.services.crawler.crawler import Crawler


class River:
    def __init__(self, rain_repository: RainRepository | None = None):
        self.crawler = Crawler(rain_repository)

    def river_of_interest(self, river: str | LocalRiver) -> str:
        if isinstance(river, LocalRiver):
            return river.value
        elif isinstance(river, str):
            _river = river.upper()
            return LocalRiver[_river].value
        else:
            raise KeyError("River not found")

    async def get_river_data(self, river: LocalRiver | str) -> RiverCreate:
        river_location = self.river_of_interest(river)
        dados_rio = await self.crawler.river_data(river_location)
        return RiverCreate(**dados_rio)
