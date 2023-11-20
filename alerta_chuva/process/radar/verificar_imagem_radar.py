import cv2
import numpy as np


class Radar:
    def verificar_imagem_radar(self, img: str) -> int:
        imagem = cv2.imread("laranja.png")

        # Converta a imagem para o espaço de cores HSV
        imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        # Defina os valores de pixel para os tons de cores específicos e seus graus de grandeza
        cores_e_graus = {
            (17, 167, 12): 1,  # Verde Claro (grau 1)
            (19, 122, 19): 2,  # Verde Médio (grau 2)
            (4, 85, 4): 3,  # Verde Escuro (grau 3)
            (195, 230, 0): 4,  # Amarelo (grau 4)
            (255, 112, 0): 5,  # Abóbora (grau 5)
            (227, 6, 5): 6,  # Vermelho (grau 6)
            (197, 0, 197): 7,  # Rosa (grau 7)
        }

        # Mapeie os tons de cores aos graus de grandeza
        grau_de_grandeza = 0

        for cor, grau in cores_e_graus.items():
            mascara_cor = cv2.inRange(imagem_hsv, np.array(cor), np.array(cor))
            contornos_cor, _ = cv2.findContours(
                mascara_cor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contorno in contornos_cor:
                (x, y, w, h) = cv2.boundingRect(contorno)
                cv2.rectangle(imagem, (x, y), (x + w, y + h), cor, 2)
                grau_de_grandeza = grau
        return grau_de_grandeza
