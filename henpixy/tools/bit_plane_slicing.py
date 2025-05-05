"""
Módulo com funções para fatiamento por planos de bits
"""

import numpy as np
from PIL import Image
import math

def get_image_bit_depth(image):
    """
    Determina a profundidade de bits (quantidade de planos) e intensidade máxima da imagem
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
    
    Returns:
        tuple: (profundidade de bits, intensidade máxima)
    """
    # Converte para escala de cinza se necessário
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image.copy()
    
    # Converte para array numpy
    image_array = np.array(gray_image)
    
    # Encontra o valor máximo de intensidade na imagem
    max_intensity = np.max(image_array)
    
    # Trata o caso especial de uma imagem completamente preta (intensidade zero)
    if max_intensity == 0:
        return 1, 0  # Retorna pelo menos 1 bit de profundidade
    
    # Calcula a profundidade de bits necessária para representar a intensidade máxima
    # log2(max_intensity + 1) arredondado para cima
    bit_depth = math.ceil(math.log2(max_intensity + 1))
    
    # Garantir que sempre tenhamos pelo menos 1 bit de profundidade
    bit_depth = max(1, bit_depth)
    
    return bit_depth, max_intensity

def extract_bit_plane(image, plane):
    """
    Extrai um plano de bits específico de uma imagem
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
        plane (int): O plano de bits a ser extraído (0 a bit_depth-1), onde:
                    0 é o bit menos significativo (LSB)
                    bit_depth-1 é o bit mais significativo (MSB)
    
    Returns:
        PIL.Image.Image: Uma imagem binária representando o plano de bits escolhido
    """
    # Determina a profundidade de bits da imagem
    bit_depth, max_intensity = get_image_bit_depth(image)
    
    # Verifica se o plano está no intervalo válido
    if not 0 <= plane < bit_depth:
        raise ValueError(f"O plano de bits deve estar entre 0 e {bit_depth-1}")
    
    # Se a intensidade máxima é zero, retornar uma imagem preta
    if max_intensity == 0:
        # Retorna uma cópia da imagem (que já é preta)
        return image.copy() if image.mode == 'L' else image.convert('L')
    
    # Converte para escala de cinza se necessário
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image.copy()
    
    # Converte para array numpy
    image_array = np.array(gray_image)
    
    # Extrai o plano de bits específico
    # Usamos a operação AND bit a bit com a máscara (2^plane)
    # e normalizamos para 0 ou 255
    bit_mask = 1 << plane  # Equivalente a 2^plane
    bit_plane = (image_array & bit_mask) > 0
    
    # Converte para valores de 0 e 255 para visualização
    bit_plane = bit_plane.astype(np.uint8) * 255
    
    # Converte de volta para uma imagem PIL
    result_image = Image.fromarray(bit_plane, mode='L')
    
    return result_image

def get_bit_plane_contribution(plane):
    """
    Retorna a contribuição (peso) de um plano de bits para a intensidade do pixel
    
    Args:
        plane (int): O plano de bits
    
    Returns:
        int: O valor máximo de contribuição deste plano (2^plane)
    """
    return 2 ** plane 