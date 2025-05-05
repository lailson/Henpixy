"""
Módulo com funções para fatiamento por planos de bits
"""

import numpy as np
from PIL import Image

def extract_bit_plane(image, plane):
    """
    Extrai um plano de bits específico de uma imagem
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
        plane (int): O plano de bits a ser extraído (0-7), onde:
                    0 é o bit menos significativo (LSB)
                    7 é o bit mais significativo (MSB)
    
    Returns:
        PIL.Image.Image: Uma imagem binária representando o plano de bits escolhido
    """
    # Verifica se o plano está no intervalo válido
    if not 0 <= plane <= 7:
        raise ValueError("O plano de bits deve estar entre 0 e 7")
    
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

def reconstruct_from_bit_planes(image, planes):
    """
    Reconstrói uma imagem a partir de planos de bits selecionados
    
    Args:
        image (PIL.Image.Image): A imagem original
        planes (list): Lista de planos de bits a serem incluídos na reconstrução (0-7)
    
    Returns:
        PIL.Image.Image: A imagem reconstruída usando apenas os planos especificados
    """
    # Valida os planos
    for plane in planes:
        if not 0 <= plane <= 7:
            raise ValueError("Os planos de bits devem estar entre 0 e 7")
    
    # Converte para escala de cinza se necessário
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image.copy()
    
    # Converte para array numpy
    image_array = np.array(gray_image)
    
    # Inicializa o array para a imagem reconstruída
    reconstructed = np.zeros_like(image_array)
    
    # Adiciona cada plano de bits
    for plane in planes:
        bit_mask = 1 << plane  # Equivalente a 2^plane
        bit_plane = (image_array & bit_mask) > 0
        reconstructed += bit_plane * (2 ** plane)
    
    # Limita os valores ao intervalo [0, 255]
    reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)
    
    # Converte de volta para uma imagem PIL
    result_image = Image.fromarray(reconstructed, mode='L')
    
    return result_image

def get_bit_plane_contribution(plane):
    """
    Retorna a contribuição (peso) de um plano de bits para a intensidade do pixel
    
    Args:
        plane (int): O plano de bits (0-7)
    
    Returns:
        int: O valor máximo de contribuição deste plano (2^plane)
    """
    return 2 ** plane 