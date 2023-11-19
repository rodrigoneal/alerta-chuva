from typing import Sequence

from transbordou.domain.repositories.rain_repository import RainRepository


class RainRecord:
    def __init__(self, rain_register: Sequence, rain_repository: RainRepository):
        self.rain_repository = rain_repository
        self.rain_register = rain_register

    async def save(self):
        [await self.rain_repository.create(rain) for rain in self.rain_register]

    def __repr__(self) -> str:
        stations = " - ".join(
            str((i.station_id, i.station_name)) for i in self.rain_register
        )
        return f"RainRecord({stations})"
