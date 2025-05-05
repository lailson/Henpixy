"""
Módulo para transformação de imagens em escala de cinza para pseudocores
através de fatiamento por intensidades.
"""

import numpy as np
from PIL import Image

def intensity_slicing(image, slices=None, colors=None):
    """
    Realiza o fatiamento por intensidades de uma imagem em escala de cinza,
    atribuindo cores a cada faixa de intensidade.
    
    Args:
        image (PIL.Image.Image): Imagem de entrada em escala de cinza
        slices (list): Lista com os limites das fatias de intensidade
                     Ex: [64, 128, 192] divide a imagem em 4 faixas: 0-63, 64-127, 128-191, 192-255
        colors (list): Lista de tuplas RGB correspondentes a cada fatia
                     Ex: [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]
    
    Returns:
        PIL.Image.Image: Imagem colorida com pseudocores
    """
    # Converte para escala de cinza se necessário
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image.copy()
    
    # Converte para array numpy
    image_array = np.array(gray_image)
    
    # Se não foram fornecidas fatias, usa divisão em 8 níveis iguais (0-31, 32-63, ..., 224-255)
    if slices is None:
        slices = [32, 64, 96, 128, 160, 192, 224]
    
    # Se não foram fornecidas cores, usa um conjunto padrão de 8 cores
    if colors is None:
        colors = [
            (0, 0, 143),      # Azul escuro
            (0, 0, 255),      # Azul
            (0, 255, 255),    # Ciano
            (0, 255, 0),      # Verde
            (255, 255, 0),    # Amarelo
            (255, 128, 0),    # Laranja
            (255, 0, 0),      # Vermelho
            (128, 0, 0)       # Marrom
        ]
    
    # Verifica se o número de cores é compatível com o número de fatias
    if len(colors) != len(slices) + 1:
        raise ValueError(f"O número de cores ({len(colors)}) deve ser igual ao número de fatias + 1 ({len(slices) + 1})")
    
    # Cria uma imagem RGB vazia com o mesmo tamanho da imagem original
    height, width = image_array.shape
    pseudocolor_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Aplica o fatiamento por intensidades
    # Primeira fatia: intensidades de 0 até slices[0] - 1
    mask = (image_array < slices[0])
    pseudocolor_array[mask] = colors[0]
    
    # Fatias intermediárias
    for i in range(len(slices) - 1):
        mask = (image_array >= slices[i]) & (image_array < slices[i + 1])
        pseudocolor_array[mask] = colors[i + 1]
    
    # Última fatia: intensidades de slices[-1] até 255
    mask = (image_array >= slices[-1])
    pseudocolor_array[mask] = colors[-1]
    
    # Converte de volta para imagem PIL
    pseudocolor_image = Image.fromarray(pseudocolor_array, mode='RGB')
    
    return pseudocolor_image

def create_color_gradient(num_colors):
    """
    Cria um gradiente de cores para usar no fatiamento por intensidades.
    
    Args:
        num_colors (int): Número de cores desejadas
    
    Returns:
        list: Lista de tuplas RGB representando o gradiente de cores
    """
    colors = []
    
    # Percorre o espectro de cores usando HSV
    # H (matiz) vai de 0 a 1 (vermelho a vermelho, passando por todas as cores)
    # S (saturação) e V (valor) são fixos em 1 para cores vivas
    for i in range(num_colors):
        h = i / num_colors
        
        # Converter HSV para RGB manualmente (sem usar colorsys)
        if h < 1/6:  # Vermelho para amarelo
            r = 255
            g = int(255 * 6 * h)
            b = 0
        elif h < 2/6:  # Amarelo para verde
            r = int(255 * (2 - 6 * h))
            g = 255
            b = 0
        elif h < 3/6:  # Verde para ciano
            r = 0
            g = 255
            b = int(255 * (6 * h - 2))
        elif h < 4/6:  # Ciano para azul
            r = 0
            g = int(255 * (4 - 6 * h))
            b = 255
        elif h < 5/6:  # Azul para magenta
            r = int(255 * (6 * h - 4))
            g = 0
            b = 255
        else:  # Magenta para vermelho
            r = 255
            g = 0
            b = int(255 * (6 - 6 * h))
        
        colors.append((r, g, b))
    
    return colors

def create_predefined_maps():
    """
    Cria mapas de cores predefinidos para fatiamento por intensidades.
    
    Returns:
        dict: Dicionário com mapas de cores predefinidos
    """
    maps = {
        "Arco-íris": {
            "slices": [32, 64, 96, 128, 160, 192, 224],
            "colors": [
                (0, 0, 143),      # Azul escuro
                (0, 0, 255),      # Azul
                (0, 255, 255),    # Ciano
                (0, 255, 0),      # Verde
                (255, 255, 0),    # Amarelo
                (255, 128, 0),    # Laranja
                (255, 0, 0),      # Vermelho
                (128, 0, 0)       # Marrom
            ]
        },
        "Temperatura": {
            "slices": [64, 128, 192],
            "colors": [
                (0, 0, 255),      # Azul (frio)
                (0, 255, 255),    # Ciano
                (255, 255, 0),    # Amarelo
                (255, 0, 0)       # Vermelho (quente)
            ]
        },
        "Densidade": {
            "slices": [50, 100, 150, 200],
            "colors": [
                (0, 0, 0),        # Preto (baixa densidade)
                (128, 0, 128),    # Roxo
                (255, 0, 0),      # Vermelho
                (255, 255, 0),    # Amarelo
                (255, 255, 255)   # Branco (alta densidade)
            ]
        },
        "Topográfico": {
            "slices": [32, 64, 96, 128, 160, 192],
            "colors": [
                (0, 0, 128),      # Azul escuro (oceano profundo)
                (0, 128, 255),    # Azul claro (águas rasas)
                (0, 255, 0),      # Verde (vegetação plana)
                (128, 128, 0),    # Oliva (planaltos)
                (128, 64, 0),     # Marrom (montanhas)
                (192, 192, 192),  # Cinza (picos)
                (255, 255, 255)   # Branco (neve)
            ]
        },
        "Binário": {
            "slices": [128],
            "colors": [
                (0, 0, 0),        # Preto
                (255, 255, 255)   # Branco
            ]
        }
    }
    
    return maps

def apply_custom_transformation(image, red_function, green_function, blue_function):
    """
    Aplica transformações personalizadas a cada canal de cor da imagem.
    
    Args:
        image (PIL.Image.Image): Imagem de entrada em escala de cinza
        red_function (function): Função para transformar intensidades no canal vermelho
        green_function (function): Função para transformar intensidades no canal verde
        blue_function (function): Função para transformar intensidades no canal azul
    
    Returns:
        PIL.Image.Image: Imagem colorida resultante
    """
    # Converte para escala de cinza se necessário
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image.copy()
    
    # Converte para array numpy
    image_array = np.array(gray_image)
    
    # Cria uma imagem RGB vazia com o mesmo tamanho da imagem original
    height, width = image_array.shape
    color_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Aplica as funções de transformação para cada canal
    for i in range(height):
        for j in range(width):
            intensity = image_array[i, j]
            color_array[i, j, 0] = np.clip(red_function(intensity), 0, 255)    # Canal R
            color_array[i, j, 1] = np.clip(green_function(intensity), 0, 255)  # Canal G
            color_array[i, j, 2] = np.clip(blue_function(intensity), 0, 255)   # Canal B
    
    # Converte de volta para imagem PIL
    color_image = Image.fromarray(color_array, mode='RGB')
    
    return color_image

def create_custom_transformation_functions():
    """
    Cria funções de transformação personalizadas predefinidas para pseudocores.
    
    Returns:
        dict: Dicionário com conjuntos de funções de transformação para R, G e B
    """
    transformations = {
        "HotIron": {
            "red": lambda x: int(3 * x) if x < 85 else 255,
            "green": lambda x: 0 if x < 85 else int(3 * (x - 85)) if x < 170 else 255,
            "blue": lambda x: 0 if x < 170 else int(3 * (x - 170))
        },
        "Espectro": {
            "red": lambda x: 255 if x > 128 else 0,
            "green": lambda x: 255 if 64 <= x <= 192 else 0,
            "blue": lambda x: 255 if x < 128 else 0
        },
        "Senoidal": {
            "red": lambda x: 127.5 * (1 + np.sin((x / 255.0 * 2 - 1) * np.pi)),
            "green": lambda x: 127.5 * (1 + np.sin((x / 255.0 * 4 - 2) * np.pi)),
            "blue": lambda x: 127.5 * (1 + np.sin((x / 255.0 * 8 - 4) * np.pi))
        },
        "RGB Linear": {
            "red": lambda x: 255 - x,  # Negativo no vermelho
            "green": lambda x: x,      # Linear no verde
            "blue": lambda x: 127.5 * (1 + np.sin((x / 255.0 * 4) * np.pi))  # Senoidal no azul
        }
    }
    
    return transformations 