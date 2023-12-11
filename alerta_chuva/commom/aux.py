from typing import Sequence

from alerta_chuva.domain.repositories.rain_repository import RainRepository


class RainRecord:
    """Objeto auxiliar para conseguir salvar os acumulos de chuva no banco de dados."""

    def __init__(self, rain_register: Sequence, rain_repository: RainRepository):
        self.rain_repository = rain_repository
        self.rain_register = rain_register

    async def save(self):
        """Salva os acumulos de chuva no banco de dados."""
        [await self.rain_repository.create(rain) for rain in self.rain_register]

    def __repr__(self) -> str:
        stations = " - ".join(
            str((i.station_id, i.station_name)) for i in self.rain_register
        )
        return f"RainRecord({stations})"


# Esse modulo serve para salvar as informações da imagem do radar.


# TODO Mudar a Classe RadarImgInfo para uma classe normal com a opção de salvar a imagem no banco de dados.
