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


"""
IRAJA
VIDIGAL
URCA
ROCINHA
TIJUCA
SANTA TERESA
COPACABANA
GRAJAU
ILHA DO GOVERNADOR
PENHA
MADUREIRA
BANGU
PIEDADE
JACAREPAGUA/TANQUE
SAUDE
JARDIM BOTANICO
BARRA/BARRINHA
JACAREPAGUA/CIDADE DE DEUS
BARRA/RIOCENTRO
GUARATIBA
EST. GRAJAU/JACAREPAGUA
SANTA CRUZ
GRANDE MEIER
ANCHIETA
GROTA FUNDA
CAMPO GRANDE
SEPETIBA
ALTO DA BOA VISTA
AV. BRASIL/MENDANHA
RECREIO DOS BANDEIRANTES
LARANJEIRAS
SAO CRISTOVAO
TIJUCA/MUDA
IRAJA 
SEPETIBA 
CIDADE DE DEUS 
SANTA TERESA 
TANQUE 
URCA 
SAUDE 
GRANDE MEIER 
GROTA FUNDA 
ROCINHA 
PENHA 
GRAJAU 
BANGU 
RECREIO 
TIJUCA 
ILHA DO GOVERNADOR 
JARDIM BOTANICO 
MADUREIRA 
SANTA CRUZ 
VIDIGAL 
GUARATIBA 
ANCHIETA 
COPACABANA 
PIEDADE 
CAMPO GRANDE 
RIOCENTRO
"""
