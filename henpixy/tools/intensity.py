"""
Ferramentas de manipulação de intensidade de imagem
"""

import numpy as np
from PIL import Image

def zero_intensity(image):
    """
    Altera a intensidade de todos os pixels da imagem para zero.
    
    Args:
        image (PIL.Image.Image): A imagem para ser processada
        
    Returns:
        PIL.Image.Image: A imagem resultante com intensidade zero
    """
    # Criamos uma cópia da imagem para não modificar a original
    result = image.copy()
    
    # Convertemos para o formato adequado para trabalhar
    # Preservamos o modo da imagem original
    original_mode = result.mode
    
    # Transformamos em array numpy
    img_array = np.array(result)
    
    # Se for imagem em escala de cinza
    if len(img_array.shape) == 2:
        # Criar um array de zeros com o mesmo tamanho
        zeros = np.zeros_like(img_array)
        new_img = Image.fromarray(zeros, mode='L')
    
    # Se for RGB
    elif original_mode == 'RGB':
        # Criar um array de zeros com o mesmo tamanho e 3 canais
        zeros = np.zeros_like(img_array)
        new_img = Image.fromarray(zeros, mode='RGB')
    
    # Se for RGBA (com canal alpha)
    elif original_mode == 'RGBA':
        # Precisamos preservar o canal alpha
        zeros = np.zeros_like(img_array)
        # Mantém apenas o canal alpha original
        if img_array.shape[2] == 4:  # Confirmando que temos 4 canais
            zeros[:, :, 3] = img_array[:, :, 3]  # Preserva o canal alpha
        new_img = Image.fromarray(zeros, mode='RGBA')
    
    # Outros modos (como L, LA, etc.)
    else:
        # Convertemos para RGB primeiro
        rgb_image = result.convert('RGB')
        # Aplicamos a função de intensidade zero
        img_array = np.array(rgb_image)
        zeros = np.zeros_like(img_array)
        # Convertemos de volta para o modo original
        new_img = Image.fromarray(zeros, mode='RGB').convert(original_mode)
    
    return new_img 