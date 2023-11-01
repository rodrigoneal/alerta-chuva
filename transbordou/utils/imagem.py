import numpy as np
from PIL import Image, ImageDraw


def cortar_imagem(img: str) -> np.array:
    # Abra a imagem original
    imagem = Image.open(img)

    # Crie uma máscara circular
    largura, altura = imagem.size
    mascara = Image.new("L", (largura, altura), 0)
    draw = ImageDraw.Draw(mascara)
    raio = min(largura, altura) // 2
    centro = (largura // 2, altura // 2)
    draw.ellipse(
        (centro[0] - raio, centro[1] - raio, centro[0] + raio, centro[1] + raio),
        fill=255,
    )

    # Aplique a máscara à imagem original
    imagem_circular = Image.new("RGBA", (largura, altura))
    imagem_circular.paste(imagem, (0, 0), mascara)
    imagem.close()
    return np.array(imagem_circular)
