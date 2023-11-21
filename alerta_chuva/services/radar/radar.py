from datetime import datetime
from typing import Literal

import cv2
import easyocr
import numpy as np
from dateutil.parser import parse


class RegionNotExist(Exception):
    pass


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

    def encontrar_maior_grau_de_grandeza(self, imagem, cores_e_graus):
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

    def regiao(
        self, regiao: Literal["Columbia", "Norte", "Sul", "Leste", "Oeste"]
    ) -> tuple[tuple[int, int], int]:
        regiao = regiao.upper()
        if regiao == "COLUMBIA":
            return ((491, 346), 20)
        elif regiao == "NORTE":
            return ((480, 356), 50)
        elif regiao == "SUL":
            return ((516, 407), 50)
        elif regiao == "LESTE":
            raise RegionNotExist(f"Região {regiao} Não existe no RJ")
        elif regiao == "OESTE":
            return ((381, 370), 50)
        else:
            raise RegionNotExist(f"Região {regiao} não existe")

    def verificar_radar(
        self,
        imagem_radar: str | bytes,
        regiao_buscada: Literal["Columbia", "Norte", "Sul", "Leste", "Oeste"]
        | None = None,
    ):
        if isinstance(imagem_radar, str):
            img = cv2.imread(imagem_radar)
        elif isinstance(imagem_radar, bytes):
            imagem_np = np.frombuffer(imagem_radar, np.uint8)
            img = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)
        imagem = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if imagem is None:
            return 0  # Retorna 0 se a imagem não puder ser lida
        if regiao_buscada:
            ponto_central, raio = self.regiao(regiao_buscada)
            imagem = self.recortar_imagem(imagem, ponto_central, raio)
        # Encontrar o maior grau de grandeza na imagem
        maior_grau = self.encontrar_maior_grau_de_grandeza(imagem, self.cores_e_graus)
        return maior_grau

    def recortar_imagem(
        self, imagem: np.ndarray, ponto_central: tuple[int, int], raio: int
    ) -> np.ndarray:
        x1 = max(0, ponto_central[0] - raio)
        y1 = max(0, ponto_central[1] - raio)
        x2 = min(imagem.shape[1], ponto_central[0] + raio)
        y2 = min(imagem.shape[0], ponto_central[1] + raio)
        return imagem[y1:y2, x1:x2]

    def get_img_date(self, imagem: np.array) -> datetime:
        reader = easyocr.Reader(["en"])
        text_area = imagem[0:30, 0:310]
        ocr_text = reader.readtext(text_area, detail=0)
        text = " ".join(ocr_text)
        return parse(text)
