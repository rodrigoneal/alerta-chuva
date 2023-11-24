import os
from datetime import datetime
from typing import Literal, TypeAlias, TypedDict

import cv2
import easyocr
import numpy as np
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from ipyleaflet import Circle, ImageOverlay, Map
from joblib import Parallel, delayed
from alerta_chuva.commom.entities import RadarImgInfo
from alerta_chuva.exceptions.radar_exceptions import NoRadarImagesFound

from alerta_chuva.parser.normalize_text import normalize_text
from alerta_chuva.parser.parser import img_bytes_to_ndarray
from alerta_chuva.services.crawler.crawler import Crawler

RegionType: TypeAlias = Literal[
    "Columbia", "Campo Grande", "Ilha do Governador", "Norte", "Sul", "Leste", "Oeste"
]


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
        self,
        region: RegionType,
    ) -> tuple[tuple[int, int], int]:
        match region:
            case "Columbia":
                return ((491, 346), 20)
            case "Campo Grande":
                return ((429, 366), 30)
            case "Ilha do Governador":
                return ((527, 341), 50)
            case "Norte":
                return ((480, 356), 50)
            case "Sul":
                return ((516, 407), 50)
            case "Oeste":
                return ((381, 370), 50)
            case "Leste":
                raise RegionNotExist(f"Region: {region} does not exist")
            case "Rio":
                return ((490, 366), 320)
            case _:
                return ((490, 366), 320)

    def check_radar(
        self,
        img_radar: str | bytes | np.ndarray,
        radar_area: RegionType | None = None,
    ):
        imagem = img_radar
        if isinstance(img_radar, str):
            imagem = cv2.imread(img_radar)
        elif isinstance(img_radar, bytes):
            imagem = img_bytes_to_ndarray(img_radar)
        if imagem is None:
            return 0  # Retorna 0 se a imagem não puder ser lida
        area = radar_area if radar_area else "Rio"
        ponto_central, raio = self.region_of_interest(area)
        imagem = self.select_radar_area(imagem, ponto_central, raio)
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

    def _extract_date_img_radar(self, img: np.ndarray | bytes) -> RadarImgInfo:
        if isinstance(img, bytes):
            img = img_bytes_to_ndarray(img)
        reader = easyocr.Reader(["en"], gpu=False)
        text_area = img[0:30, 0:310]
        ocr_text = reader.readtext(text_area, detail=0)
        text = normalize_text(ocr_text)
        print(text)
        try:
            data = parse(text)
        except ParserError:
            return RadarImgInfo(None, None)
        return RadarImgInfo(data, img)

    def radar_map(self, img_radar: str) -> str:
        mymap = Map(center=(-22.9499, -43.4199), zoom=8)
        circle = Circle(
            location=(-22.960849, -43.2646667), radius=138900, color="blue", fill=False
        )
        mymap.add_layer(circle)
        image_overlay = ImageOverlay(
            url=img_radar, bounds=((-24.431567, -45.336972), (-21.478793, -41.159092))
        )
        mymap.add_layer(image_overlay)

        mymap
        mymap.save("mapa.html")
        return "mapa.html"

    async def extract_date_img_radar(self, imgs: list[bytes]) -> list[RadarImgInfo]:
        num_processes = round(os.cpu_count() * 0.7)
        dates = Parallel(n_jobs=num_processes)(
            delayed(self._extract_date_img_radar)(img) for img in imgs
        )
        return dates

    def sort_img_by_date(self, dates: list[RadarImgInfo]) -> list[RadarImgInfo]:
        return sorted(dates, key=lambda x: x.data, reverse=True)

    async def radar(self, region: RegionType = None) -> RadarImgInfo:
        crawler = Crawler(None)
        imgs = await crawler.get_radar_img()
        imgs_radar = await self.extract_date_img_radar(imgs)
        imgs_sorted = self.sort_img_by_date(imgs_radar)
        try:
            img = imgs_sorted[0]
        except IndexError:
            raise NoRadarImagesFound(
                "No image found. The radar website may be offline. Please wait a few minutes and try again."
            )
        grau = self.check_radar(img.img, region)
        img.grau = grau
        return img
