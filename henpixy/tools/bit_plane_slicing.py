"""
Módulo com funções para fatiamento por planos de bits
"""

import numpy as np
from PIL import Image
import math
import logging

def get_image_bit_depth(image):
    """
    Determina a profundidade de bits (quantidade de planos) e intensidade máxima da imagem
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
    
    Returns:
        tuple: (profundidade de bits, intensidade máxima)
    """
    try:
        # Converte para escala de cinza se necessário
        if image.mode != 'L':
            gray_image = image.convert('L')
        else:
            gray_image = image.copy()
        
        # Converte para array numpy
        image_array = np.array(gray_image)
        
        # Encontra o valor máximo de intensidade na imagem
        max_intensity = int(np.max(image_array))
        
        # Caso especial: imagem completamente preta ou com valores muito baixos
        if max_intensity <= 0:
            return 1, max_intensity
        
        # Tentativa segura de calcular a profundidade de bits
        try:
            # Calcula a profundidade de bits necessária para representar a intensidade máxima
            # log2(max_intensity + 1) arredondado para cima
            bit_depth = math.ceil(math.log2(float(max_intensity) + 1.0))
        except (ValueError, OverflowError, ZeroDivisionError, ArithmeticError) as e:
            # Se ocorrer qualquer erro matemático, usamos um método alternativo
            # Determinamos o número de bits necessários iterativamente
            bit_depth = 1
            while (1 << bit_depth) - 1 < max_intensity and bit_depth < 24:  # Limite em 24 bits por segurança
                bit_depth += 1
        
        # Garantir que sempre tenhamos pelo menos 1 bit de profundidade
        bit_depth = max(1, min(bit_depth, 24))  # Limitamos a 24 bits por segurança
        
        return bit_depth, max_intensity
    
    except Exception as e:
        # Caso ocorra qualquer erro, retornamos valores seguros
        logging.error(f"Erro ao calcular profundidade de bits: {str(e)}")
        return 8, 255  # Valores padrão seguros

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
    try:
        # Determina a profundidade de bits da imagem
        bit_depth, max_intensity = get_image_bit_depth(image)
        
        # Verifica se o plano está no intervalo válido
        if not 0 <= plane < bit_depth:
            print(f"Aviso: Plano {plane} fora do intervalo válido [0, {bit_depth-1}]")
            # Ajustamos para o intervalo válido
            plane = min(max(0, plane), bit_depth - 1)
        
        # Se a intensidade máxima é zero ou muito baixa, retornar uma imagem preta
        if max_intensity <= 1:
            print(f"Aviso: Imagem com intensidade máxima muito baixa ({max_intensity})")
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
        try:
            # Protege contra overflow em planos muito altos
            if plane >= 30:  # 2^30 já é enorme
                return Image.new('L', image.size, 0)  # Retorna imagem preta
                
            bit_mask = 1 << plane  # Equivalente a 2^plane
            bit_plane = (image_array & bit_mask) > 0
            
            # Converte para valores de 0 e 255 para visualização
            bit_plane = bit_plane.astype(np.uint8) * 255
            
            # Converte de volta para uma imagem PIL
            result_image = Image.fromarray(bit_plane, mode='L')
            
            return result_image
        
        except (OverflowError, ValueError, TypeError) as e:
            print(f"Erro ao extrair plano de bits: {str(e)}")
            # Em caso de erro, retorna uma imagem preta do mesmo tamanho
            return Image.new('L', image.size, 0)
    
    except Exception as e:
        print(f"Erro não esperado ao extrair plano de bits: {str(e)}")
        import traceback
        print(traceback.format_exc())
        # Em caso de erro, retorna uma imagem preta do mesmo tamanho
        return Image.new('L', image.size, 0)

def get_bit_plane_contribution(plane):
    """
    Retorna a contribuição (peso) de um plano de bits para a intensidade do pixel
    
    Args:
        plane (int): O plano de bits
    
    Returns:
        int: O valor máximo de contribuição deste plano (2^plane)
    """
    return 2 ** plane 