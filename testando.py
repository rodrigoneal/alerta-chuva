# import cv2

# # Carregar a imagem usando OpenCV
# imagem = cv2.imread('tests/data/img/img.png')

# # Exibir a imagem
# cv2.imshow('Imagem', imagem)
# cv2.waitKey(0)  # Aguardar até que uma tecla seja pressionada
# cv2.destroyAllWindows()  # Fechar todas as janelas ao pressionar uma tecla

import cv2
import easyocr

reader = easyocr.Reader(['en'])
# Carregue a imagem usando o OpenCV
imagem = cv2.imread('regiao_interesse.png')

regiao_interesse = imagem[0:30, 0:310]

text = reader.readtext(regiao_interesse, detail=0)
breakpoint()