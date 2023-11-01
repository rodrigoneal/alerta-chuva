import numpy as np
from PIL import Image

from transbordou.utils.imagem import cortar_imagem


def test_se_corta_a_imagem_redonda_retirando_legenda():
    img = r"tests/data/img/radar.png"
    imagem_cortada = cortar_imagem(img)
    imagem = Image.open(img)
    imagem_array = np.array(imagem)
    assert not np.array_equal(imagem_array, imagem_cortada)


def test_se_verifica_se_corta_imagem_como_o_template():
    img = r"tests/data/img/radar.png"
    imagem_cortada = cortar_imagem(img)
    imagem = Image.open(r"tests/data/img/imagem_circular.png")
    imagem_array = np.array(imagem)
    assert np.array_equal(imagem_array, imagem_cortada)
