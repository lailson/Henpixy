"""
Janela para exibição de histograma da imagem atual
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QScrollArea, QWidget, QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import io
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from henpixy.tools.histogram import calculate_histogram, create_histogram_figure

class HistogramWindow(QDialog):
    """
    Janela para exibição do histograma da imagem atual
    """
    
    def __init__(self, parent=None, image=None):
        super().__init__(parent)
        
        self.setWindowTitle("Histograma")
        self.resize(600, 450)
        
        # Permitir que a janela seja redimensionável
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Armazena a imagem original
        self.original_image = image
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        
        # Área de rolagem para o histograma
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)
        
        # Widget de conteúdo para a área de rolagem
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Container para o histograma
        self.hist_group = QGroupBox("Histograma da Imagem")
        self.hist_layout = QVBoxLayout(self.hist_group)
        
        # Label para exibir o histograma
        self.hist_label = QLabel()
        self.hist_label.setAlignment(Qt.AlignCenter)
        self.hist_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.hist_layout.addWidget(self.hist_label)
        
        # Adicionar o grupo ao layout de conteúdo
        self.content_layout.addWidget(self.hist_group)
        
        # Informações sobre o histograma
        self.info_group = QGroupBox("Informações")
        self.info_layout = QVBoxLayout(self.info_group)
        
        # Label para exibir informações estatísticas
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_layout.addWidget(self.info_label)
        
        # Adicionar o grupo de informações ao layout de conteúdo
        self.content_layout.addWidget(self.info_group)
        
        # Definir o widget de conteúdo para a área de rolagem
        self.scroll_area.setWidget(self.content_widget)
        
        # Botão para fechar o diálogo
        self.button_layout = QHBoxLayout()
        self.close_button = QPushButton("Fechar")
        self.close_button.clicked.connect(self.close)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.close_button)
        self.main_layout.addLayout(self.button_layout)
        
        # Calcular e exibir o histograma
        if self.original_image is not None:
            self.calculate_and_display_histogram()
    
    def calculate_and_display_histogram(self):
        """Calcula e exibe o histograma da imagem"""
        if self.original_image is None:
            return
        
        # Calcular o histograma
        histogram, normalized_hist = calculate_histogram(self.original_image)
        
        # Criar figura do histograma
        fig, canvas = create_histogram_figure(
            histogram, 
            normalized_hist,
            "Histograma da Imagem"
        )
        
        # Converter para QPixmap
        pixmap = self.figure_to_pixmap(fig)
        self.hist_label.setPixmap(pixmap)
        
        # Calcular estatísticas
        self.update_statistics(histogram, normalized_hist)
    
    def update_statistics(self, histogram, normalized_hist):
        """Atualiza as estatísticas do histograma"""
        import numpy as np
        
        # Número total de pixels
        total_pixels = np.sum(histogram)
        
        # Encontrar valor mínimo e máximo não zero
        non_zero_indices = np.where(histogram > 0)[0]
        if len(non_zero_indices) > 0:
            min_intensity = np.min(non_zero_indices)
            max_intensity = np.max(non_zero_indices)
        else:
            min_intensity = 0
            max_intensity = 0
        
        # Calcular média e desvio padrão
        x = np.arange(len(histogram))
        mean_intensity = np.sum(x * normalized_hist)
        variance = np.sum(((x - mean_intensity) ** 2) * normalized_hist)
        std_dev = np.sqrt(variance)
        
        # Calcular moda (valor mais frequente)
        mode_intensity = np.argmax(histogram)
        
        # Calcular mediana
        cumulative = np.cumsum(normalized_hist)
        median_idx = np.searchsorted(cumulative, 0.5)
        
        # Atualizar o texto de informações
        info_text = f"""
        <b>Estatísticas do Histograma:</b><br>
        <table>
            <tr><td>Dimensões da imagem:</td><td>{self.original_image.width} × {self.original_image.height} pixels</td></tr>
            <tr><td>Total de pixels:</td><td>{total_pixels}</td></tr>
            <tr><td>Intensidade mínima:</td><td>{min_intensity}</td></tr>
            <tr><td>Intensidade máxima:</td><td>{max_intensity}</td></tr>
            <tr><td>Média de intensidade:</td><td>{mean_intensity:.2f}</td></tr>
            <tr><td>Desvio padrão:</td><td>{std_dev:.2f}</td></tr>
            <tr><td>Moda (valor mais frequente):</td><td>{mode_intensity}</td></tr>
            <tr><td>Mediana:</td><td>{median_idx}</td></tr>
        </table>
        <br>
        <b>Interpretação:</b><br>
        <p>O histograma mostra a distribuição de valores de intensidade na imagem.
        Uma distribuição ampla indica contraste, enquanto uma distribuição 
        concentrada indica baixo contraste. Picos em regiões específicas
        indicam predominância desses valores de intensidade na imagem.</p>
        """
        
        self.info_label.setText(info_text)
        self.info_label.setTextFormat(Qt.RichText)
    
    def figure_to_pixmap(self, figure):
        """Converte uma figura matplotlib para QPixmap"""
        # Salvar a figura em um buffer de memória
        buf = io.BytesIO()
        figure.savefig(buf, format='png', dpi=figure.dpi)
        buf.seek(0)
        
        # Criar um QPixmap a partir dos dados
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        
        return pixmap
    
    def resizeEvent(self, event):
        """Redimensiona o histograma quando a janela é redimensionada"""
        super().resizeEvent(event)
        if hasattr(self, 'hist_label') and self.hist_label.pixmap():
            self.calculate_and_display_histogram()
    
    def set_image(self, image):
        """Define a imagem a ser analisada"""
        self.original_image = image
        self.calculate_and_display_histogram() 