"""
Módulo para implementação de filtros espaciais.
"""

import numpy as np
from PIL import Image

def mean_filter(image, kernel_size=3):
    """
    Aplica um filtro de suavização da média na imagem.
    
    O filtro da média substitui cada pixel pela média dos valores dos pixels
    em uma vizinhança definida pelo tamanho do kernel.
    
    Args:
        image (PIL.Image.Image): Imagem de entrada
        kernel_size (int): Tamanho do kernel (vizinhança) para o filtro.
                          Deve ser um número ímpar (3, 5, 7, etc.)
    
    Returns:
        PIL.Image.Image: Imagem suavizada
    """
    # Verifica se o tamanho do kernel é válido (deve ser ímpar)
    if kernel_size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser um número ímpar")
    
    # Obtém uma cópia da imagem de entrada para evitar modificar a original
    if image.mode == 'L':
        # Imagem em escala de cinza
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGB':
        # Imagem colorida RGB
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGBA':
        # Imagem colorida com canal alpha
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = True
        alpha_channel = np.array(image.getchannel('A'))
    else:
        # Converte outros modos para RGB
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    
    # Obtém as dimensões da imagem
    if len(img_array.shape) == 2:
        # Imagem em escala de cinza
        height, width = img_array.shape
        channels = 1
    else:
        # Imagem colorida (RGB)
        height, width, channels = img_array.shape
    
    # Calcula a borda (padding) necessária para processar os pixels da borda
    padding = kernel_size // 2
    
    # Cria uma nova matriz para armazenar a imagem filtrada
    filtered_array = np.zeros_like(img_array)
    
    # Aplica o filtro da média
    if channels == 1:
        # Para imagens em escala de cinza
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Extrai a vizinhança do pixel
                neighborhood = img_array[y - padding:y + padding + 1, x - padding:x + padding + 1]
                # Calcula a média da vizinhança
                filtered_array[y, x] = np.mean(neighborhood)
    else:
        # Para imagens coloridas
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Processa cada canal de cor separadamente
                for c in range(channels):
                    # Extrai a vizinhança do pixel para o canal atual
                    neighborhood = img_array[y - padding:y + padding + 1, 
                                           x - padding:x + padding + 1, c]
                    # Calcula a média da vizinhança
                    filtered_array[y, x, c] = np.mean(neighborhood)
    
    # Converte de volta para imagem PIL
    if channels == 1:
        # Escala de cinza
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='L')
    else:
        # RGB
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='RGB')
    
    # Reaplica o canal alpha se necessário
    if has_alpha:
        alpha_img = Image.fromarray(alpha_channel, mode='L')
        filtered_image.putalpha(alpha_img)
    
    return filtered_image

def max_filter(image, kernel_size=3):
    """
    Aplica um filtro de máximo na imagem.
    
    O filtro de máximo substitui cada pixel pelo valor máximo dos pixels
    em uma vizinhança definida pelo tamanho do kernel.
    
    Args:
        image (PIL.Image.Image): Imagem de entrada
        kernel_size (int): Tamanho do kernel (vizinhança) para o filtro.
                          Deve ser um número ímpar (3, 5, 7, etc.)
    
    Returns:
        PIL.Image.Image: Imagem filtrada
    """
    # Verifica se o tamanho do kernel é válido (deve ser ímpar)
    if kernel_size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser um número ímpar")
    
    # Obtém uma cópia da imagem de entrada para evitar modificar a original
    if image.mode == 'L':
        # Imagem em escala de cinza
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGB':
        # Imagem colorida RGB
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGBA':
        # Imagem colorida com canal alpha
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = True
        alpha_channel = np.array(image.getchannel('A'))
    else:
        # Converte outros modos para RGB
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    
    # Obtém as dimensões da imagem
    if len(img_array.shape) == 2:
        # Imagem em escala de cinza
        height, width = img_array.shape
        channels = 1
    else:
        # Imagem colorida (RGB)
        height, width, channels = img_array.shape
    
    # Calcula a borda (padding) necessária para processar os pixels da borda
    padding = kernel_size // 2
    
    # Cria uma nova matriz para armazenar a imagem filtrada
    filtered_array = np.zeros_like(img_array)
    
    # Aplica o filtro de máximo
    if channels == 1:
        # Para imagens em escala de cinza
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Extrai a vizinhança do pixel
                neighborhood = img_array[y - padding:y + padding + 1, x - padding:x + padding + 1]
                # Calcula o máximo da vizinhança
                filtered_array[y, x] = np.max(neighborhood)
    else:
        # Para imagens coloridas
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Processa cada canal de cor separadamente
                for c in range(channels):
                    # Extrai a vizinhança do pixel para o canal atual
                    neighborhood = img_array[y - padding:y + padding + 1, 
                                           x - padding:x + padding + 1, c]
                    # Calcula o máximo da vizinhança
                    filtered_array[y, x, c] = np.max(neighborhood)
    
    # Converte de volta para imagem PIL
    if channels == 1:
        # Escala de cinza
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='L')
    else:
        # RGB
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='RGB')
    
    # Reaplica o canal alpha se necessário
    if has_alpha:
        alpha_img = Image.fromarray(alpha_channel, mode='L')
        filtered_image.putalpha(alpha_img)
    
    return filtered_image

def min_filter(image, kernel_size=3):
    """
    Aplica um filtro de mínimo na imagem.
    
    O filtro de mínimo substitui cada pixel pelo valor mínimo dos pixels
    em uma vizinhança definida pelo tamanho do kernel.
    
    Args:
        image (PIL.Image.Image): Imagem de entrada
        kernel_size (int): Tamanho do kernel (vizinhança) para o filtro.
                          Deve ser um número ímpar (3, 5, 7, etc.)
    
    Returns:
        PIL.Image.Image: Imagem filtrada
    """
    # Verifica se o tamanho do kernel é válido (deve ser ímpar)
    if kernel_size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser um número ímpar")
    
    # Obtém uma cópia da imagem de entrada para evitar modificar a original
    if image.mode == 'L':
        # Imagem em escala de cinza
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGB':
        # Imagem colorida RGB
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGBA':
        # Imagem colorida com canal alpha
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = True
        alpha_channel = np.array(image.getchannel('A'))
    else:
        # Converte outros modos para RGB
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    
    # Obtém as dimensões da imagem
    if len(img_array.shape) == 2:
        # Imagem em escala de cinza
        height, width = img_array.shape
        channels = 1
    else:
        # Imagem colorida (RGB)
        height, width, channels = img_array.shape
    
    # Calcula a borda (padding) necessária para processar os pixels da borda
    padding = kernel_size // 2
    
    # Cria uma nova matriz para armazenar a imagem filtrada
    filtered_array = np.zeros_like(img_array)
    
    # Aplica o filtro de mínimo
    if channels == 1:
        # Para imagens em escala de cinza
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Extrai a vizinhança do pixel
                neighborhood = img_array[y - padding:y + padding + 1, x - padding:x + padding + 1]
                # Calcula o mínimo da vizinhança
                filtered_array[y, x] = np.min(neighborhood)
    else:
        # Para imagens coloridas
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Processa cada canal de cor separadamente
                for c in range(channels):
                    # Extrai a vizinhança do pixel para o canal atual
                    neighborhood = img_array[y - padding:y + padding + 1, 
                                           x - padding:x + padding + 1, c]
                    # Calcula o mínimo da vizinhança
                    filtered_array[y, x, c] = np.min(neighborhood)
    
    # Converte de volta para imagem PIL
    if channels == 1:
        # Escala de cinza
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='L')
    else:
        # RGB
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='RGB')
    
    # Reaplica o canal alpha se necessário
    if has_alpha:
        alpha_img = Image.fromarray(alpha_channel, mode='L')
        filtered_image.putalpha(alpha_img)
    
    return filtered_image

def median_filter(image, kernel_size=3):
    """
    Aplica um filtro de mediana na imagem.
    
    O filtro de mediana substitui cada pixel pelo valor mediano dos pixels
    em uma vizinhança definida pelo tamanho do kernel.
    Excelente para remover ruído do tipo "sal e pimenta" preservando bordas.
    
    Args:
        image (PIL.Image.Image): Imagem de entrada
        kernel_size (int): Tamanho do kernel (vizinhança) para o filtro.
                          Deve ser um número ímpar (3, 5, 7, etc.)
    
    Returns:
        PIL.Image.Image: Imagem filtrada
    """
    # Verifica se o tamanho do kernel é válido (deve ser ímpar)
    if kernel_size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser um número ímpar")
    
    # Obtém uma cópia da imagem de entrada para evitar modificar a original
    if image.mode == 'L':
        # Imagem em escala de cinza
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGB':
        # Imagem colorida RGB
        img_array = np.array(image.copy(), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    elif image.mode == 'RGBA':
        # Imagem colorida com canal alpha
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = True
        alpha_channel = np.array(image.getchannel('A'))
    else:
        # Converte outros modos para RGB
        img_array = np.array(image.convert('RGB'), dtype=np.float32)
        has_alpha = False
        alpha_channel = None
    
    # Obtém as dimensões da imagem
    if len(img_array.shape) == 2:
        # Imagem em escala de cinza
        height, width = img_array.shape
        channels = 1
    else:
        # Imagem colorida (RGB)
        height, width, channels = img_array.shape
    
    # Calcula a borda (padding) necessária para processar os pixels da borda
    padding = kernel_size // 2
    
    # Cria uma nova matriz para armazenar a imagem filtrada
    filtered_array = np.zeros_like(img_array)
    
    # Aplica o filtro de mediana
    if channels == 1:
        # Para imagens em escala de cinza
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Extrai a vizinhança do pixel
                neighborhood = img_array[y - padding:y + padding + 1, x - padding:x + padding + 1]
                # Calcula a mediana da vizinhança
                filtered_array[y, x] = np.median(neighborhood)
    else:
        # Para imagens coloridas
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Processa cada canal de cor separadamente
                for c in range(channels):
                    # Extrai a vizinhança do pixel para o canal atual
                    neighborhood = img_array[y - padding:y + padding + 1, 
                                           x - padding:x + padding + 1, c]
                    # Calcula a mediana da vizinhança
                    filtered_array[y, x, c] = np.median(neighborhood)
    
    # Converte de volta para imagem PIL
    if channels == 1:
        # Escala de cinza
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='L')
    else:
        # RGB
        filtered_image = Image.fromarray(filtered_array.astype(np.uint8), mode='RGB')
    
    # Reaplica o canal alpha se necessário
    if has_alpha:
        alpha_img = Image.fromarray(alpha_channel, mode='L')
        filtered_image.putalpha(alpha_img)
    
    return filtered_image 