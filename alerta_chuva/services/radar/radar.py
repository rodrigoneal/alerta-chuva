import os
from typing import Any, Callable, ClassVar, Iterable, Literal, Sequence, TypeVar

import cv2
import easyocr  # type: ignore
import numpy as np
from dateutil.parser import parse  # type: ignore
from dateutil.parser._parser import ParserError  # type: ignore
from joblib import Parallel, delayed  # type: ignore

from alerta_chuva.commom.aux import RadarImgInfo
from alerta_chuva.commom.types import ColorAndGrade, RegionRadar, RegionType
from alerta_chuva.exceptions.radar_exceptions import NoRadarImagesFound, RegionNotExist
from alerta_chuva.parser.normalize_text import normalize_text
from alerta_chuva.parser.parser import img_bytes_to_ndarray, parser_to_ndarray
from alerta_chuva.services.crawler.crawler import Crawler

num_cpus = os.cpu_count()

T = TypeVar("T")
P = TypeVar("P")


class Radar:
    """Classe para lidar com o dados e imagem do radar.

    Raises:
        RegionNotExist: Exceção caso nao consiga encontrar a regiao.
        NoRadarImagesFound: Exceção caso não consiga encontrar as imagens do radar.

    args:
        num_processors (int): Quantidade de processadores que serão usados. default: round(os.cpu_count() / 2), Metade de cores do processador.
        cores_e_graus (dict[tuple[int, int, int], int]): Dicionário com as cores e graus. default: {(17, 167, 12): 1, (19, 122, 19): 2, (4, 85, 4): 3, (195, 230, 0): 4, (255, 112, 0): 5, (227, 6, 5): 6, (197, 0, 197): 7}.
    """

    num_processors: ClassVar[int] = round(num_cpus / 2) if num_cpus else 1
    cores_e_graus: ClassVar[ColorAndGrade] = {
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

    def find_rain_intensity(self, img: np.ndarray) -> int:
        """Analise a imagem do radar e busca por nuvens com a intesidade da chuva.
        Retorna a grau de intensidade da chuva.
        Quanto maior a intensidade da chuva, maior o grau.
        Vai de 0 a 7.
        Onde 0 é sem chuva e 7 é chuva intensa.


        Args:
            img (np.ndarray): Imagem do radar
            cores_e_graus (dict[tuple[int, int, int], int]): Cores e seus graus

        Returns:
            int: Grau de intensidade da chuva
        """

        try:
            imagem = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception:
            imagem = img
            pass

        maior_grau = 0
        for y in range(imagem.shape[0]):
            for x in range(imagem.shape[1]):
                cor_pixel_atual = imagem[y, x]

                # Verificar se a cor do pixel atual está na escala definida
                for cor, grau in self.cores_e_graus.items():
                    if np.array_equal(cor, cor_pixel_atual):
                        if grau > maior_grau:
                            maior_grau = grau  # Atualiza o maior grau encontrado

        return maior_grau

    def region_of_interest(
        self,
        region: RegionType,
    ) -> RegionRadar:
        """Retorna o ponto central e raio da regiao do radar.
        Para fazer busca em uma região do Rio de Janeiro.

        Args:
            region (RegionType): Região que será buscado a intensidade da chuva.

        Raises:
            RegionNotExist: Exceção caso não consiga encontrar a região.

        Returns:
            RegionRadar: Ponto central e raio da regiao do radar
        """

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

    def select_radar_area(
        self, img: np.ndarray, central_point: tuple[int, int], radios: int
    ) -> np.ndarray:
        """Limita da imagem que será analisada do radar.

        Args:
            img (np.ndarray): Imagem do radar.
            central_point (tuple[int, int]): Ponto central do radar da area selecionada.
            radios (int): Raio da area selecionada.

        Returns:
            np.ndarray: Area da imagem que será analisada.
        """

        x1 = max(0, central_point[0] - radios)
        y1 = max(0, central_point[1] - radios)
        x2 = min(img.shape[1], central_point[0] + radios)
        y2 = min(img.shape[0], central_point[1] + radios)
        return img[y1:y2, x1:x2]

    def extract_date_img_radar(self, img: np.ndarray | bytes) -> RadarImgInfo:
        """O site onde eu pego a imagem do radar não vem a data e a hora que a imagem foi capturada.
        Mas na propria imagem do radar, tem a data e a hora que foi capturada.
        Usando o OCR, eu consigo extrair a data e a hora da imagem.
        Retorna um objeto com a data e a hora da imagem e a imagem.

        Args:
            img (np.ndarray | bytes): Imagem do radar.

        Returns:
            RadarImgInfo: Informações da imagem do radar.
        """

        if isinstance(img, bytes):
            img = img_bytes_to_ndarray(img)
        reader = easyocr.Reader(["en"])
        text_area = img[0:30, 0:310]
        ocr_text = reader.readtext(text_area, detail=0)
        text = normalize_text(ocr_text)
        print(text)
        try:
            data = parse(text)
        except ParserError:
            return RadarImgInfo(None, None)
        return RadarImgInfo(data, img)

    def check_radar(
        self,
        img_radar: str | bytes | np.ndarray,
        radar_area: RegionType | Literal["Rio"] = "Rio",
    ):
        """Faz analise na imagem do radar e mostra a intensidade da chuva.
        Se nenhuma imagem for encontrada, levanta uma exceção NoRadarImagesFound.
        Se nenhuma area for passada será considerada a area do Rio.

        Args:
            img_radar (str | bytes | np.ndarray): Imagem do radar que será analisada.
            radar_area (RegionType | None, optional): Região que será analisada. Defaults to None.

        Returns:
            _type_: _description_
        """
        img_array = parser_to_ndarray(img_radar)
        if img_array is None:
            raise NoRadarImagesFound("No radar images found")
        if not isinstance(img_array, np.ndarray):
            raise NoRadarImagesFound(f"img is type {type(img_array)} not a numpy array")
        radar_info = self.extract_date_img_radar(img_array)
        ponto_central, raio = self.region_of_interest(radar_area)
        img_area = self.select_radar_area(img_array, ponto_central, raio)
        maior_grau = self.find_rain_intensity(img_area)
        radar_info.grau = maior_grau
        return radar_info

    def parallel_extract(
        self, func: Callable[[P, Any], T], args: Iterable[Sequence[P]], **kwargs: Any
    ) -> list[T]:
        """Paraleliza o processo para extrair dados do radar.

        Args:
            func (Callable[[P], T]): Função que vai ser paralelizada.
            imgs (Iterable[P]): Argumentos da função que vai ser paralelizada.

        Returns:
            list[T]: Resultado da função paralelizada.
        """
        return Parallel(n_jobs=self.num_processors)(
            delayed(func)(arg, **kwargs) for arg in args
        )

    async def get_rain_intensity(
        self, radar_area: RegionType | None = None
    ) -> list[RadarImgInfo]:
        """Retorna a intensidade da chuva na imagem do radar.

        Args:
            img_radar (str | bytes | np.ndarray): Imagem do radar que será analisada.
            radar_area (RegionType | None, optional): Região que será analisada. Defaults to None.

        Returns:
            int: Intensidade da chuva.
        """
        crawler = Crawler()
        imgs = await crawler.get_radar_img()
        return self.parallel_extract(self.check_radar, imgs, radar_area=radar_area)  # type: ignore
