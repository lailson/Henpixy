"""
Módulo com funções para aplicar transformação de potência (gama) em imagens
"""

import numpy as np
from PIL import Image

def power_transform(image, gamma, c=1.0):
    """
    Aplica a transformação de potência (gama) em uma imagem
    
    A função implementa a transformação S = c * r^γ, onde:
    - S é o valor resultante
    - c é uma constante multiplicativa (padrão = 1.0)
    - r é o valor original do pixel (normalizado entre 0 e 1)
    - γ (gamma) é o expoente que controla o contraste
    
    Características:
    - γ < 1: Expande valores escuros (mais detalhes em áreas escuras)
    - γ = 1: Transformação identidade (imagem não é alterada)
    - γ > 1: Expande valores claros (mais detalhes em áreas claras)
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
        gamma (float): O valor de gama (γ) para a transformação
        c (float, optional): Constante multiplicativa. Padrão é 1.0
        
    Returns:
        PIL.Image.Image: Uma nova imagem com a transformação aplicada
    """
    # Valida os parâmetros
    if gamma <= 0:
        raise ValueError("O valor de gama deve ser positivo")
    
    # Cria uma cópia da imagem para não modificar a original
    result_image = image.copy()
    
    # Converte a imagem para array numpy para processamento mais eficiente
    image_array = np.array(result_image, dtype=np.float32)
    
    # Determina as características da imagem
    if len(image_array.shape) == 2:
        # Imagem em escala de cinza
        is_grayscale = True
        depth = 1
    else:
        # Imagem colorida (RGB ou RGBA)
        is_grayscale = False
        depth = image_array.shape[2]
    
    # Determina o valor máximo baseado no tipo de dados da imagem original
    original_array = np.array(image)
    dtype = original_array.dtype
    if dtype == np.uint8:
        max_value = 255.0
    elif dtype == np.uint16:
        max_value = 65535.0
    else:
        max_value = 255.0  # Padrão para outros tipos
    
    # Normalizamos os valores para o intervalo [0, 1]
    image_array = image_array / max_value
    
    # Aplicamos a transformação de potência
    if is_grayscale:
        # Processamento para imagem em escala de cinza
        transformed_array = c * np.power(image_array, gamma)
    else:
        # Processamento para imagem colorida (RGB ou RGBA)
        transformed_array = image_array.copy()
        
        # Aplicamos a transformação em cada canal RGB
        for i in range(min(3, depth)):  # Primeiros 3 canais (RGB)
            channel = image_array[:, :, i]
            transformed_array[:, :, i] = c * np.power(channel, gamma)
        
        # Preservamos o canal alpha (se existir)
        if depth > 3:
            transformed_array[:, :, 3:] = image_array[:, :, 3:]
    
    # Voltamos para a escala original [0, max_value]
    transformed_array = transformed_array * max_value
    
    # Garantimos que os valores estejam no intervalo correto
    transformed_array = np.clip(transformed_array, 0, max_value)
    
    # Convertemos de volta para o tipo de dados original
    if dtype == np.uint8:
        transformed_array = transformed_array.astype(np.uint8)
    elif dtype == np.uint16:
        transformed_array = transformed_array.astype(np.uint16)
    else:
        transformed_array = transformed_array.astype(np.uint8)
    
    # Convertemos de volta para uma imagem PIL
    if is_grayscale:
        result_image = Image.fromarray(transformed_array)
    else:
        result_image = Image.fromarray(transformed_array, mode=image.mode)
    
    return result_image 