from datetime import datetime
from typing import Literal, TypedDict

import cv2
import easyocr
from joblib import Parallel, delayed
import numpy as np
from dateutil.parser import parse
from alerta_chuva.parser.normalize_text import normalize_text
from alerta_chuva.parser.parser import img_bytes_to_ndarray

from alerta_chuva.services.crawler.crawler import Crawler
from dateutil.parser._parser import ParserError


class RegionNotExist(Exception):
    pass


class ColorAndGrande(TypedDict):
    tuple[int, int, int]: int


class Radar:
    cores_e_graus = {
        (17, 167, 12): 1,  # Verde Claro (grau 1)
        (19, 122, 19): 2,  # Verde Médio (grau 2)
        (4, 85, 4): 3,  # Verde Escuro (grau 3)
        (195, 230, 0): 4,  # Amarelo (grau 4)
        (255, 112, 0): 5,  # Abóbora (grau 5)
        (227, 6, 5): 6,  # Vermelho (grau 6)
        (197, 0, 197): 7,  # Rosa (grau 7)
    }

    def __init__(
        self,
    ):
        self._last_img_radar = None

    def find_rain_intensity(
        self, img: np.ndarray, cores_e_graus: dict[tuple[int, int, int], int]
    ) -> int:
        """

        Args:
            img (np.ndarray): _description_
            cores_e_graus (dict[tuple[int, int, int], int]): _description_

        Returns:
            int: _description_
        """
        try:
            imagem = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception as exc:
            imagem = img
            pass

        maior_grau = 0
        for y in range(imagem.shape[0]):
            for x in range(imagem.shape[1]):
                cor_pixel_atual = imagem[y, x]

                # Verificar se a cor do pixel atual está na escala definida
                for cor, grau in cores_e_graus.items():
                    if np.array_equal(cor, cor_pixel_atual):
                        if grau > maior_grau:
                            maior_grau = grau  # Atualiza o maior grau encontrado

        return maior_grau

    def region_of_interest(
        self, region: Literal["Columbia", "Norte", "Sul", "Leste", "Oeste"]
    ) -> tuple[tuple[int, int], int]:
        match region:
            case "Columbia":
                return ((491, 346), 20)
            case "Norte":
                return ((480, 356), 50)
            case "Sul":
                return ((516, 407), 50)
            case "Oeste":
                return ((381, 370), 50)
            case _:
                raise RegionNotExist(f"Region: {region} does not exist")

    def check_radar(
        self,
        img_radar: str | bytes | np.ndarray,
        radar_area: Literal["Columbia", "Norte", "Sul", "Leste", "Oeste"] | None = None,
    ):
        img = img_radar
        if isinstance(img_radar, str):
            img = cv2.imread(img_radar)
        elif isinstance(img_radar, bytes):
            img = img_bytes_to_ndarray(img_radar)
        imagem = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if imagem is None:
            return 0  # Retorna 0 se a imagem não puder ser lida
        if radar_area:
            ponto_central, raio = self.region_of_interest(radar_area)
            imagem = self.select_radar_area(imagem, ponto_central, raio)
        # Encontrar o maior grau de grandeza na imagem
        maior_grau = self.find_rain_intensity(imagem, self.cores_e_graus)
        return maior_grau

    def select_radar_area(
        self, img: np.ndarray, central_point: tuple[int, int], radios: int
    ) -> np.ndarray:
        x1 = max(0, central_point[0] - radios)
        y1 = max(0, central_point[1] - radios)
        x2 = min(img.shape[1], central_point[0] + radios)
        y2 = min(img.shape[0], central_point[1] + radios)
        return img[y1:y2, x1:x2]

    def extract_date_img_radar(
        self, img: np.ndarray | bytes
    ) -> tuple[datetime, np.ndarray]:
        if isinstance(img, bytes):
            img = img_bytes_to_ndarray(img)
        reader = easyocr.Reader(["en"])
        text_area = img[0:30, 0:310]
        ocr_text = reader.readtext(text_area, detail=0)
        print(ocr_text)
        text = normalize_text(ocr_text)
        data = parse(text)

        return data, img

    async def last_img_radar(self) -> tuple[datetime, np.ndarray]:
        crawler = Crawler(None)
        imgs = await crawler.get_radar_img()
        last_date = datetime(year=1, month=1, day=1)
        last_img = None

        dates = Parallel(n_jobs=8)(
            delayed(self.extract_date_img_radar)(img.content)
            for img in imgs
            if img.status_code == 200
        )
        for date in dates:
            if date[0] > last_date:
                last_date = date[0]
                last_img = date

        self._last_img_radar = last_img
        return last_img
