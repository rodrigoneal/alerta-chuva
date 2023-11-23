# Esse modulo serve para salvar as informações da imagem do radar.

from datetime import datetime
from dataclasses import dataclass
import cv2
from pathlib import Path

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

        path = Path(f"imgs-radar/{self.data}.png")
        path.parent.mkdir(parents=True, exist_ok=True)
        img_file = str(path.absolute())
        try:
            cv2.imwrite(img_file, self.img)
            return img_file
        except Exception as e:
            return None