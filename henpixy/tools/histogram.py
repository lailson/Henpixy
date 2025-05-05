"""
Módulo para trabalho com histogramas e equalização
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def calculate_histogram(image, bins=256):
    """
    Calcula o histograma de uma imagem em escala de cinza
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
        bins (int): Número de bins do histograma (padrão: 256 para 8 bits)
    
    Returns:
        tuple: (histograma, histograma normalizado)
    """
    # Converte para escala de cinza se necessário
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image.copy()
    
    # Converte para array numpy
    image_array = np.array(gray_image)
    
    # Calcula o histograma
    histogram = np.zeros(bins, dtype=np.int32)
    
    # Altura e largura da imagem
    height, width = image_array.shape
    
    # Contador de pixels para cada intensidade
    for i in range(height):
        for j in range(width):
            intensity = image_array[i, j]
            histogram[intensity] += 1
    
    # Histograma normalizado (probabilidades)
    normalized_histogram = histogram / (height * width)
    
    return histogram, normalized_histogram

def calculate_cumulative_distribution(normalized_histogram):
    """
    Calcula a função de distribuição acumulada (CDF) de um histograma
    
    Args:
        normalized_histogram (numpy.ndarray): Histograma normalizado
    
    Returns:
        numpy.ndarray: Função de distribuição acumulada
    """
    return np.cumsum(normalized_histogram)

def equalize_histogram(image):
    """
    Realiza a equalização do histograma de uma imagem
    
    Args:
        image (PIL.Image.Image): A imagem de entrada
    
    Returns:
        tuple: (imagem equalizada, histograma original, histograma equalizado)
    """
    # Converte para escala de cinza se necessário
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image.copy()
    
    # Converte para array numpy
    image_array = np.array(gray_image)
    
    # Altura e largura da imagem
    height, width = image_array.shape
    
    # Calcula o histograma original e normalizado
    original_histogram, original_normalized = calculate_histogram(gray_image)
    
    # Calcula a CDF
    cdf = calculate_cumulative_distribution(original_normalized)
    
    # Número de níveis de intensidade
    L = 256  # Para imagens de 8 bits
    
    # Mapeamento de equalização (transformação)
    # sk = T(rk) = (L-1) * cdf(rk)
    equalization_map = np.round((L - 1) * cdf).astype(np.uint8)
    
    # Aplicar a transformação em cada pixel
    equalized_array = np.zeros_like(image_array)
    for i in range(height):
        for j in range(width):
            intensity = image_array[i, j]
            equalized_array[i, j] = equalization_map[intensity]
    
    # Criar a imagem equalizada
    equalized_image = Image.fromarray(equalized_array)
    
    # Calcular o histograma equalizado
    equalized_histogram, equalized_normalized = calculate_histogram(equalized_image)
    
    return equalized_image, original_histogram, equalized_histogram, original_normalized, equalized_normalized

def create_histogram_figure(hist, normalized_hist, title="Histograma", figsize=(6, 4), dpi=100):
    """
    Cria uma figura com o histograma para visualização
    
    Args:
        hist (numpy.ndarray): Histograma
        normalized_hist (numpy.ndarray): Histograma normalizado
        title (str): Título do gráfico
        figsize (tuple): Tamanho da figura (largura, altura) em polegadas
        dpi (int): Resolução da figura
    
    Returns:
        matplotlib.figure.Figure: Figura com o histograma
    """
    # Criar figura
    fig = Figure(figsize=figsize, dpi=dpi)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    
    # Configurar o gráfico
    x = np.arange(len(hist))
    width = 0.8  # Largura das barras
    
    # Plotar o histograma
    ax.bar(x, hist, width, alpha=0.7, color='blue')
    
    # Configurar eixos e título
    ax.set_xlabel('Intensidade')
    ax.set_ylabel('Frequência')
    ax.set_title(title)
    
    # Limitar o número de ticks no eixo x para evitar sobreposição
    max_ticks = 10
    if len(hist) > max_ticks:
        step = len(hist) // max_ticks
        ax.set_xticks(np.arange(0, len(hist), step))
    else:
        ax.set_xticks(np.arange(len(hist)))
    
    # Adicionar informações estatísticas
    if len(normalized_hist) > 0:
        non_zero_indices = np.where(hist > 0)[0]
        if len(non_zero_indices) > 0:
            min_intensity = np.min(non_zero_indices)
            max_intensity = np.max(non_zero_indices)
        else:
            min_intensity = 0
            max_intensity = 0
        
        mean_intensity = np.sum(x * normalized_hist)
        variance = np.sum(((x - mean_intensity) ** 2) * normalized_hist)
        std_dev = np.sqrt(variance)
        
        stats_text = (
            f"Min: {min_intensity}\n"
            f"Max: {max_intensity}\n"
            f"Média: {mean_intensity:.2f}\n"
            f"Desvio Padrão: {std_dev:.2f}"
        )
        
        # Adicionar texto com as estatísticas
        ax.text(0.95, 0.95, stats_text,
                horizontalalignment='right',
                verticalalignment='top',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.7))
    
    # Ajustar layout
    fig.tight_layout()
    
    return fig, canvas 