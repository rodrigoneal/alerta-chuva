from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np

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


@dataclass
class RadarImgInfo:
    data: datetime | None
    img: np.ndarray | None
    grau: int = 0

    def save_img(self) -> str | None:
        """Salva a imagem no disco

        Returns:
            str: caminho de onde a imagem foi salva
        """

        path = Path(f"radar/img/{self.data}.png")
        path.parent.mkdir(parents=True, exist_ok=True)
        img_file = str(path.absolute())
        try:
            cv2.imwrite(img_file, self.img)
            return img_file
        except Exception:
            return None
