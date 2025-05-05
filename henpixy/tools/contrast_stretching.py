"""
Módulo com funções para aplicar alargamento de contraste em imagens
"""

import numpy as np
from PIL import Image

def contrast_stretching(image, r1, s1, r2, s2):
    """
    Aplica o alargamento de contraste em uma imagem
    
    A função implementa uma transformação linear por partes definida por:
    - s = (s1/r1) * r                  para 0 <= r <= r1
    - s = ((s2-s1)/(r2-r1)) * (r-r1) + s1   para r1 < r <= r2
    - s = ((255-s2)/(255-r2)) * (r-r2) + s2  para r2 < r <= 255
    
    onde:
    - r é o valor original do pixel
    - s é o valor resultante
    - (r1, s1) e (r2, s2) são os pontos de controle da transformação
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
        r1 (int): Valor de referência 1 para entrada (0-255)
        s1 (int): Valor de referência 1 para saída (0-255)
        r2 (int): Valor de referência 2 para entrada (0-255)
        s2 (int): Valor de referência 2 para saída (0-255)
        
    Returns:
        PIL.Image.Image: Uma nova imagem com o alargamento de contraste aplicado
    """
    # Valida os parâmetros
    if not (0 <= r1 < r2 <= 255):
        raise ValueError("Deve ser 0 <= r1 < r2 <= 255")
    if not (0 <= s1 <= s2 <= 255):
        raise ValueError("Deve ser 0 <= s1 <= s2 <= 255")
    
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
    
    # Normaliza os valores r1, s1, r2, s2 para o intervalo da imagem
    if max_value != 255.0:
        r1_norm = r1 * (max_value / 255.0)
        s1_norm = s1 * (max_value / 255.0)
        r2_norm = r2 * (max_value / 255.0)
        s2_norm = s2 * (max_value / 255.0)
    else:
        r1_norm, s1_norm, r2_norm, s2_norm = r1, s1, r2, s2
    
    # Calcula os coeficientes para a transformação linear por partes
    if r1_norm == 0:
        # Evita divisão por zero
        a1 = 0
    else:
        a1 = s1_norm / r1_norm
    
    if r2_norm == r1_norm:
        # Evita divisão por zero
        a2 = 0
    else:
        a2 = (s2_norm - s1_norm) / (r2_norm - r1_norm)
    
    if max_value == r2_norm:
        # Evita divisão por zero
        a3 = 0
    else:
        a3 = (max_value - s2_norm) / (max_value - r2_norm)
    
    b2 = s1_norm - a2 * r1_norm
    b3 = s2_norm - a3 * r2_norm
    
    # Define a função de transformação
    def transform(pixel):
        if pixel <= r1_norm:
            return a1 * pixel
        elif pixel <= r2_norm:
            return a2 * pixel + b2
        else:
            return a3 * pixel + b3
    
    # Vetoriza a função de transformação para melhor desempenho
    transform_vec = np.vectorize(transform)
    
    # Aplica a transformação
    if is_grayscale:
        # Processamento para imagem em escala de cinza
        transformed_array = transform_vec(image_array)
    else:
        # Processamento para imagem colorida (RGB ou RGBA)
        transformed_array = image_array.copy()
        
        # Aplica a transformação em cada canal RGB
        for i in range(min(3, depth)):  # Primeiros 3 canais (RGB)
            channel = image_array[:, :, i]
            transformed_array[:, :, i] = transform_vec(channel)
        
        # Preserva o canal alpha (se existir)
        if depth > 3:
            transformed_array[:, :, 3:] = image_array[:, :, 3:]
    
    # Garante que os valores estejam no intervalo correto
    transformed_array = np.clip(transformed_array, 0, max_value)
    
    # Converte de volta para o tipo de dados original
    if dtype == np.uint8:
        transformed_array = transformed_array.astype(np.uint8)
    elif dtype == np.uint16:
        transformed_array = transformed_array.astype(np.uint16)
    else:
        transformed_array = transformed_array.astype(np.uint8)
    
    # Converte de volta para uma imagem PIL
    if is_grayscale:
        result_image = Image.fromarray(transformed_array)
    else:
        result_image = Image.fromarray(transformed_array, mode=image.mode)
    
    return result_image 