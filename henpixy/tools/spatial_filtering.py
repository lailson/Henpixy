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

def laplacian_filter(image, include_diagonals=True, apply_adjustment=False, sharpen_image=False):
    """
    Aplica o filtro Laplaciano na imagem.
    
    O filtro Laplaciano é um operador de segunda ordem que detecta mudanças de intensidade
    (bordas e detalhes) em todas as direções.
    
    Args:
        image (PIL.Image.Image): Imagem de entrada
        include_diagonals (bool): Se True, usa a máscara 3x3 que inclui termos diagonais.
                                 Se False, usa a versão 4-vizinhos (sem diagonais).
        apply_adjustment (bool): Se True, ajusta a imagem Laplaciana para visualização
                               adicionando 128 a todos os pixels para centralizar em cinza médio.
        sharpen_image (bool): Se True, combina a imagem original com a Laplaciana para
                             aguçamento (resultado = original - constante * laplaciano).
    
    Returns:
        PIL.Image.Image: Imagem processada pelo filtro Laplaciano
    """
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
    
    # Define o kernel Laplaciano
    if include_diagonals:
        # Kernel Laplaciano 3x3 com diagonais (8-conectividade)
        # [ 1,  1, 1]
        # [ 1, -8, 1]
        # [ 1,  1, 1]
        kernel = np.array([[1, 1, 1],
                          [1, -8, 1],
                          [1, 1, 1]], dtype=np.float32)
    else:
        # Kernel Laplaciano 3x3 sem diagonais (4-conectividade)
        # [ 0,  1, 0]
        # [ 1, -4, 1]
        # [ 0,  1, 0]
        kernel = np.array([[0, 1, 0],
                          [1, -4, 1],
                          [0, 1, 0]], dtype=np.float32)
    
    # Calcula a borda (padding) necessária
    padding = 1  # Para kernel 3x3
    
    # Cria uma matriz para a imagem filtrada
    laplacian_array = np.zeros_like(img_array)
    
    # Aplica o filtro Laplaciano
    if channels == 1:
        # Para imagens em escala de cinza
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Extrai a vizinhança do pixel
                neighborhood = img_array[y - padding:y + padding + 1, 
                                      x - padding:x + padding + 1]
                
                # Aplica o kernel Laplaciano (convolução)
                laplacian_array[y, x] = np.sum(neighborhood * kernel)
    else:
        # Para imagens coloridas
        for y in range(padding, height - padding):
            for x in range(padding, width - padding):
                # Processa cada canal de cor separadamente
                for c in range(channels):
                    # Extrai a vizinhança do pixel para o canal atual
                    neighborhood = img_array[y - padding:y + padding + 1, 
                                          x - padding:x + padding + 1, c]
                    
                    # Aplica o kernel Laplaciano (convolução)
                    laplacian_array[y, x, c] = np.sum(neighborhood * kernel)
    
    # Decide qual resultado retornar com base nos parâmetros
    if sharpen_image:
        # Aguçamento da imagem: combinação da original com o Laplaciano
        # Usa subtração porque o Laplaciano detecta bordas com valores positivos
        # nas transições de claro para escuro
        sharpened_array = img_array - 0.5 * laplacian_array
        # Clip para garantir que os valores estejam no intervalo válido [0, 255]
        sharpened_array = np.clip(sharpened_array, 0, 255)
        result_array = sharpened_array
    elif apply_adjustment:
        # Ajusta o resultado do Laplaciano para visualização
        # Adiciona 128 para centralizar em torno de cinza médio
        adjusted_array = laplacian_array + 128
        # Clip para garantir que os valores estejam no intervalo válido [0, 255]
        adjusted_array = np.clip(adjusted_array, 0, 255)
        result_array = adjusted_array
    else:
        # Laplaciano sem ajuste (pode ter valores negativos que serão truncados)
        # Clip para garantir que os valores estejam no intervalo válido [0, 255]
        result_array = np.clip(laplacian_array, 0, 255)
    
    # Converte o array processado de volta para imagem PIL
    if channels == 1:
        # Escala de cinza
        result_image = Image.fromarray(result_array.astype(np.uint8), mode='L')
    else:
        # RGB
        result_image = Image.fromarray(result_array.astype(np.uint8), mode='RGB')
    
    # Reaplica o canal alpha se necessário
    if has_alpha:
        alpha_img = Image.fromarray(alpha_channel, mode='L')
        result_image.putalpha(alpha_img)
    
    return result_image 