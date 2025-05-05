"""
Módulo com funções para calcular o negativo de uma imagem
"""

import numpy as np
from PIL import Image

def negative(image):
    """
    Calcula o negativo de uma imagem
    
    A função implementa a transformação S = L - 1 - r, onde:
    - S é o valor resultante
    - L é o valor máximo possível para o pixel
    - r é o valor original do pixel
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
        
    Returns:
        PIL.Image.Image: Uma nova imagem com a transformação aplicada
    """
    # Cria uma cópia da imagem para não modificar a original
    result_image = image.copy()
    
    # Converte a imagem para array numpy para processamento mais eficiente
    image_array = np.array(result_image)
    
    # Determina as características da imagem
    if len(image_array.shape) == 2:
        # Imagem em escala de cinza
        height, width = image_array.shape
        depth = 1
        is_grayscale = True
    else:
        # Imagem colorida (RGB ou RGBA)
        height, width, depth = image_array.shape
        is_grayscale = False
    
    # Determina o valor máximo (L-1) baseado no tipo de dados
    dtype = image_array.dtype
    if dtype == np.uint8:
        max_value = 255  # 8 bits
    elif dtype == np.uint16:
        max_value = 65535  # 16 bits
    else:
        # Para outros tipos, converte para uint8 primeiro
        image_array = image_array.astype(np.uint8)
        max_value = 255
    
    # Cria lookup table (tabela de busca) para a transformação
    lut = np.arange(max_value + 1, dtype=dtype)
    lut = max_value - lut  # S = L-1 - r
    
    # Aplica a transformação
    if is_grayscale:
        # Imagem em escala de cinza
        transformed_array = lut[image_array]
    else:
        # Imagem colorida (RGB ou RGBA)
        if depth == 3:  # RGB
            # Aplica a transformação em cada canal de cor (R, G, B)
            transformed_array = np.zeros_like(image_array)
            for i in range(3):  # 3 canais: R, G, B
                transformed_array[:, :, i] = lut[image_array[:, :, i]]
        else:  # RGBA ou outros formatos com canal alpha
            # Aplica a transformação em cada canal de cor, preservando o canal alpha
            transformed_array = np.zeros_like(image_array)
            for i in range(3):  # primeiros 3 canais: R, G, B
                transformed_array[:, :, i] = lut[image_array[:, :, i]]
            if depth > 3:
                transformed_array[:, :, 3:] = image_array[:, :, 3:]  # Preserva o canal alpha e outros
    
    # Converte de volta para uma imagem PIL
    if is_grayscale:
        result_image = Image.fromarray(transformed_array)
    else:
        result_image = Image.fromarray(transformed_array, mode=image.mode)
    
    return result_image 