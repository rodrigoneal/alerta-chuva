import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np
from ipyleaflet import Circle, ImageOverlay, Map  # type: ignore

from alerta_chuva.domain.repositories.rain_repository import RainRepository
from alerta_chuva.utils.imagem import screenshot_map, transparency_mask


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

    def save_img(self, filename: str) -> str | None:
        """Salva a imagem do radar no caminho passado.

        Args:
            folder (str): pasta onde a imagem deve ser salva.

        Returns:
            str | None: caminho da imagem salva.
        """
        path = Path(filename).with_suffix(".png")
        file = str(path.absolute())
        if self.img is None:
            return None
        img = transparency_mask(self.img)

        try:
            cv2.imwrite(file, img)
            return file
        except Exception:
            return None

    def save_map(self, filename: str) -> str | None:
        """Cria um mapa da imagem do radar.
        A imagem do radar não vem um mapa para saber onde está a nuvem, por isso uno o mapa com a imagem do radar.
        Para ficar mais fácil de ver o mapa, eu salvo o mapa em um arquivo HTML. Pois a lib não tem como salvar diretatamente uma imagem.
        Pretendo em breve fazer um scrap com o selenium para salvar a imagem do mapa.

        Args:
            img_radar (str): Caminho da imagem do radar.

        Returns:
            str: Caminho do arquivo HTML.
        """
        img_radar = self.save_img(filename)
        if img_radar is None:
            return None
        img_radar = Path(img_radar)  # type: ignore
        absolute_img_radar = str(img_radar.absolute())  # type: ignore
        mymap = Map(center=(-22.9499, -43.4199), zoom=8)
        circle = Circle(
            location=(-22.960849, -43.2646667), radius=138900, color="blue", fill=False
        )
        mymap.add_layer(circle)
        image_overlay = ImageOverlay(
            url=absolute_img_radar,
            bounds=((-24.431567, -45.336972), (-21.478793, -41.159092)),
        )
        mymap.add_layer(image_overlay)

        mymap
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            mymap.save(f.name)
            html_uri = Path(f.name).absolute().as_uri()
            screen = screenshot_map(html_uri, absolute_img_radar)
        return screen
