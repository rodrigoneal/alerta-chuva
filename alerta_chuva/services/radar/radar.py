from functools import cache
import os
from typing import Sequence

import cv2
import easyocr
import numpy as np
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from ipyleaflet import Circle, ImageOverlay, Map
from joblib import Parallel, delayed

from alerta_chuva.commom.aux import RadarImgInfo
from alerta_chuva.commom.types import RegionRadar, RegionType
from alerta_chuva.exceptions.radar_exceptions import NoRadarImagesFound, RegionNotExist
from alerta_chuva.parser.normalize_text import normalize_text
from alerta_chuva.parser.parser import img_bytes_to_ndarray
from alerta_chuva.services.crawler.crawler import Crawler


class Radar:
    """Classe para lidar com o dados e imagem do radar.

    Raises:
        RegionNotExist: Exceção caso nao consiga encontrar a regiao.
        NoRadarImagesFound: Exceção caso não consiga encontrar as imagens do radar.
    """

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
                for cor, grau in cores_e_graus.items():
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

    def check_radar(
        self,
        img_radar: str | bytes | np.ndarray,
        radar_area: RegionType | None = None,
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
        imagem = img_radar
        if isinstance(img_radar, str):
            imagem = cv2.imread(img_radar)
        elif isinstance(img_radar, bytes):
            imagem = img_bytes_to_ndarray(img_radar)
        if imagem is None:
            raise NoRadarImagesFound("No radar images found")
        area = radar_area if radar_area else "Rio"
        ponto_central, raio = self.region_of_interest(area)
        imagem = self.select_radar_area(imagem, ponto_central, raio)
        maior_grau = self.find_rain_intensity(imagem, self.cores_e_graus)
        return maior_grau

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

    def _extract_date_img_radar(self, img: np.ndarray | bytes) -> RadarImgInfo:
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
        """Cria um mapa da imagem do radar.
        A imagem do radar não vem um mapa para saber onde está a nuvem, por isso uno o mapa com a imagem do radar.
        Para ficar mais fácil de ver o mapa, eu salvo o mapa em um arquivo HTML. Pois a lib não tem como salvar diretatamente uma imagem.
        Pretendo em breve fazer um scrap com o selenium para salvar a imagem do mapa.

        Args:
            img_radar (str): Caminho da imagem do radar.

        Returns:
            str: Caminho do arquivo HTML.
        """
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

    def extract_date_img_radar(self, imgs: Sequence[bytes]) -> list[RadarImgInfo]:
        """
        Extrai a data e a hora da imagem do radar.
        Faz basicamente o que o metodo _extract_date_img_radar faz, só que paraliza o processo para extrair as datas e horas das imagens do radar.
        Pois normalmente são 20 imagens por requisição. O processo para extrair as datas e horas das imagens do radar é muito lento.
        Por isso paralelizo o processo.

        Obrigado ao GIL por dificultar tudo.

        Args:
            imgs (list[bytes]): Imagens do radar.

        Returns:
            list[RadarImgInfo]: Informações das imagens do radar.
        """
        num_processes = round(os.cpu_count() / 2)
        dates = Parallel(n_jobs=num_processes)(
            delayed(self._extract_date_img_radar)(img) for img in imgs
        )
        return dates

    def sort_img_by_date(self, dates: list[RadarImgInfo]) -> list[RadarImgInfo]:
        """Ordena as imagens do radar por data.
        O site do radar não mantem uma ordem para as imagens do radar. Por isso eu ordeno as imagens pelo valor da data.

        Args:
            dates (list[RadarImgInfo]): Informações das imagens do radar.

        Returns:
            list[RadarImgInfo]: Informações das imagens do radar.
        """
        return sorted(dates, key=lambda x: x.data, reverse=True)

    async def radar(self, region: RegionType = None) -> RadarImgInfo:
        """Baixa as 20 imagens do radar, extrai a data e a hora da imagem e ordena as imagens pelo valor da data e pega a intensidade da nuvem da imagem.
        É o motodo principal.

        Faz todo o processo para saber a intensidade da chuva.

        Args:
            region (RegionType, optional): Região que será analisada. Defaults to None.

        Raises:
            NoRadarImagesFound: Exceção caso não consiga encontrar as imagens do radar.

        Returns:
            RadarImgInfo: Informações da imagem do radar.
        """
        crawler = Crawler(None)
        imgs = await crawler.get_radar_img()
        imgs_radar = self.extract_date_img_radar(imgs)
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
