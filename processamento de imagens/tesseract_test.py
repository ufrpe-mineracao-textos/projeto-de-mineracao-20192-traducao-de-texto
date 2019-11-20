from PIL import Image # Importando o módulo Pillow para abrir a imagem no script

import pytesseract # Módulo para a utilização da tecnologia OCR

print( pytesseract.image_to_string( Image.open('image_processing/test_images/IAM/recorte2.png') ) ) # Extraindo o texto da imagem