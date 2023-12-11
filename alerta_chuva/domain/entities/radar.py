import base64
import tempfile
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from ipyleaflet import Circle, ImageOverlay, Map  # type: ignore
from pydantic import BaseModel, ConfigDict

from alerta_chuva.utils.imagem import screenshot_map, transparency_mask


class RadarBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data: datetime | None
    img: np.ndarray | None
    grau: int | None

    def array_to_base64(self) -> str | None:
        """Converte uma imagem em array para base64.

        Args:
            img_array (np.ndarray): imagem em array.

        Returns:
            str: imagem em base64.
        """
        if self.img is None:
            return None
        img_array = self.img.tobytes()
        return base64.b64encode(img_array).decode("utf-8")

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


class RadarCreate(RadarBase):
    pass


class RadarUpdate(RadarBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data: datetime | None = None
    img: np.ndarray | None = None
    grau: int | None = None


class RadarRead(RadarBase):
    id: int
