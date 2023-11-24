# Esse modulo serve para salvar as informações da imagem do radar.

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


@dataclass
class RadarImgInfo:
    data: datetime
    img: np.ndarray
    grau: int = 0

    def save_img(self) -> str:
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
