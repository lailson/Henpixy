"""
Diálogo para exibição de histogramas e equalização
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QTabWidget,
    QScrollArea, QWidget, QSizePolicy, QGridLayout
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import numpy as np
from PIL import Image
import io
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from henpixy.tools.histogram import calculate_histogram, equalize_histogram, create_histogram_figure

class HistogramDialog(QDialog):
    """
    Diálogo para exibição de histogramas e equalização de imagens
    """
    
    def __init__(self, parent=None, image=None):
        super().__init__(parent)
        
        self.setWindowTitle("Histograma e Equalização")
        # Reduzir o tamanho inicial da janela
        self.resize(700, 550)
        
        # Permitir que a janela seja redimensionável
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Armazena a imagem original
        self.original_image = image
        
        # Variáveis para armazenar os resultados
        self.equalized_image = None
        self.original_hist = None
        self.equalized_hist = None
        self.orig_norm_hist = None
        self.eq_norm_hist = None
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        
        # Criar tabs para organizar a visualização
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Tab de comparação de imagens
        self.create_comparison_tab()
        
        # Tab de histogramas
        self.create_histograms_tab()
        
        # Tab de informações teóricas
        self.create_info_tab()
        
        # Botões para fechar e aplicar
        self.button_layout = QHBoxLayout()
        
        # Botão para aplicar a equalização à imagem principal
        self.apply_button = QPushButton("Aplicar")
        self.apply_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.apply_button)
        
        # Espaçador para alinhar os botões à direita
        self.button_layout.addStretch()
        
        # Botão para fechar o diálogo
        self.close_button = QPushButton("Fechar")
        self.close_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.close_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # Equaliza a imagem e atualiza a interface
        if self.original_image is not None:
            self.apply_equalization()
    
    def create_comparison_tab(self):
        """Cria a tab para comparação visual entre imagem original e equalizada"""
        # Criar um widget para o scroll area
        comparison_scroll = QScrollArea()
        comparison_scroll.setWidgetResizable(True)
        
        # Widget contido no scroll area
        comparison_content = QWidget()
        comparison_layout = QHBoxLayout(comparison_content)
        
        # Container para a imagem original
        original_group = QGroupBox("Imagem Original")
        original_layout = QVBoxLayout(original_group)
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        original_layout.addWidget(self.original_label)
        comparison_layout.addWidget(original_group)
        
        # Container para a imagem equalizada
        equalized_group = QGroupBox("Imagem Equalizada")
        equalized_layout = QVBoxLayout(equalized_group)
        self.equalized_label = QLabel()
        self.equalized_label.setAlignment(Qt.AlignCenter)
        self.equalized_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        equalized_layout.addWidget(self.equalized_label)
        comparison_layout.addWidget(equalized_group)
        
        # Definir o widget de conteúdo para o scroll area
        comparison_scroll.setWidget(comparison_content)
        
        self.tab_widget.addTab(comparison_scroll, "Comparação de Imagens")
    
    def create_histograms_tab(self):
        """Cria a tab para visualização dos histogramas"""
        # Criar um widget para o scroll area
        histograms_scroll = QScrollArea()
        histograms_scroll.setWidgetResizable(True)
        
        # Widget contido no scroll area
        histograms_content = QWidget()
        histograms_layout = QGridLayout(histograms_content)
        
        # Container para o histograma original
        original_hist_group = QGroupBox("Histograma Original")
        original_hist_layout = QVBoxLayout(original_hist_group)
        self.original_hist_label = QLabel()
        self.original_hist_label.setAlignment(Qt.AlignCenter)
        self.original_hist_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        original_hist_layout.addWidget(self.original_hist_label)
        histograms_layout.addWidget(original_hist_group, 0, 0)
        
        # Container para o histograma equalizado
        equalized_hist_group = QGroupBox("Histograma Equalizado")
        equalized_hist_layout = QVBoxLayout(equalized_hist_group)
        self.equalized_hist_label = QLabel()
        self.equalized_hist_label.setAlignment(Qt.AlignCenter)
        self.equalized_hist_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        equalized_hist_layout.addWidget(self.equalized_hist_label)
        histograms_layout.addWidget(equalized_hist_group, 0, 1)
        
        # Container para a Função de Distribuição Acumulada
        cdf_group = QGroupBox("Função de Distribuição Acumulada (CDF)")
        cdf_layout = QVBoxLayout(cdf_group)
        self.cdf_label = QLabel()
        self.cdf_label.setAlignment(Qt.AlignCenter)
        self.cdf_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cdf_layout.addWidget(self.cdf_label)
        histograms_layout.addWidget(cdf_group, 1, 0, 1, 2)
        
        # Definir o widget de conteúdo para o scroll area
        histograms_scroll.setWidget(histograms_content)
        
        self.tab_widget.addTab(histograms_scroll, "Histogramas")
    
    def create_info_tab(self):
        """Cria a tab com informações teóricas sobre histogramas e equalização"""
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        info_layout.addWidget(scroll_area)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Adicionar texto informativo
        info_text = """
        <h2>Histograma de Imagem</h2>
        <p>Um histograma é um gráfico em barras que fornece uma descrição global da imagem. 
        Cada barra do gráfico representa a frequência (número de pixels) com que determinado 
        nível de intensidade aparece na imagem.</p>
        
        <p>O histograma de uma imagem com intensidades no intervalo [0, L-1] pode ser expresso como:</p>
        <p style="text-align:center"><b>h(r<sub>k</sub>) = n<sub>k</sub></b></p>
        <p>onde:</p>
        <ul>
            <li>k = 0, 1, 2, ..., L-1</li>
            <li>r<sub>k</sub> é a k-ésima intensidade</li>
            <li>n<sub>k</sub> é o número de pixels com intensidade r<sub>k</sub></li>
        </ul>
        
        <h3>Histograma Normalizado</h3>
        <p>O histograma normalizado é uma estimativa de probabilidade, pois determina 
        a probabilidade de se encontrar um pixel com determinada intensidade:</p>
        <p style="text-align:center"><b>p<sub>r</sub>(r<sub>k</sub>) = h(r<sub>k</sub>) / (M×N) = n<sub>k</sub> / (M×N)</b></p>
        <p>onde:</p>
        <ul>
            <li>M é a altura da imagem</li>
            <li>N é a largura da imagem</li>
            <li>M×N é o total de pixels da imagem</li>
        </ul>
        <p>O somatório dos componentes do histograma normalizado é 1.</p>
        
        <h2>Equalização de Histograma</h2>
        <p>A equalização de histograma é uma técnica que visa produzir uma imagem com histograma 
        de forma mais uniforme, com os níveis de intensidade distribuídos com frequências similares.</p>
        
        <p>Benefícios da equalização:</p>
        <ul>
            <li>Aumenta o contraste global da imagem</li>
            <li>Evidencia detalhes antes não visíveis</li>
            <li>Útil para imagens com iluminação deficiente</li>
            <li>Normaliza imagens adquiridas sob diferentes condições de iluminação</li>
        </ul>
        
        <h3>Função de Transformação</h3>
        <p>A transformação utilizada na equalização é baseada na função de distribuição acumulada (CDF):</p>
        <p style="text-align:center"><b>s<sub>k</sub> = T(r<sub>k</sub>) = (L-1) × Σ p<sub>r</sub>(r<sub>j</sub>)</b></p>
        <p>onde:</p>
        <ul>
            <li>L é o número de níveis de intensidade</li>
            <li>Σ representa o somatório de j=0 até k</li>
            <li>r<sub>j</sub> são as intensidades de 0 até k</li>
        </ul>
        
        <p>Na prática, esta transformação mapeia os valores de intensidade da imagem original 
        para novos valores, buscando uma distribuição mais uniforme.</p>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        
        scroll_layout.addWidget(info_label)
        scroll_area.setWidget(scroll_content)
        
        self.tab_widget.addTab(info_tab, "Informações")
    
    def apply_equalization(self):
        """Aplica a equalização de histograma e atualiza a interface"""
        if self.original_image is None:
            return
        
        # Aplicar equalização
        (
            self.equalized_image, 
            self.original_hist, 
            self.equalized_hist,
            self.orig_norm_hist,
            self.eq_norm_hist
        ) = equalize_histogram(self.original_image)
        
        # Atualizar as imagens
        self.display_images()
        
        # Atualizar os histogramas
        self.display_histograms()
        
        # Atualizar a CDF
        self.display_cdf()
    
    def display_images(self):
        """Exibe as imagens original e equalizada"""
        if self.original_image is None or self.equalized_image is None:
            return
        
        # Converte a imagem original para QPixmap
        original_pixmap = self.pil_to_pixmap(self.original_image)
        if original_pixmap:
            # Redimensiona para caber no label
            scaled_original = original_pixmap.scaled(
                self.original_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.original_label.setPixmap(scaled_original)
        
        # Converte a imagem equalizada para QPixmap
        equalized_pixmap = self.pil_to_pixmap(self.equalized_image)
        if equalized_pixmap:
            # Redimensiona para caber no label
            scaled_equalized = equalized_pixmap.scaled(
                self.equalized_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.equalized_label.setPixmap(scaled_equalized)
    
    def display_histograms(self):
        """Exibe os histogramas original e equalizado"""
        if self.original_hist is None or self.equalized_hist is None:
            return
        
        # Criar figura do histograma original
        fig_orig, canvas_orig = create_histogram_figure(
            self.original_hist, 
            self.orig_norm_hist,
            "Histograma Original"
        )
        
        # Converter para QPixmap
        pixmap_orig = self.figure_to_pixmap(fig_orig)
        self.original_hist_label.setPixmap(pixmap_orig)
        
        # Criar figura do histograma equalizado
        fig_eq, canvas_eq = create_histogram_figure(
            self.equalized_hist, 
            self.eq_norm_hist,
            "Histograma Equalizado"
        )
        
        # Converter para QPixmap
        pixmap_eq = self.figure_to_pixmap(fig_eq)
        self.equalized_hist_label.setPixmap(pixmap_eq)
    
    def display_cdf(self):
        """Exibe as funções de distribuição acumulada"""
        if self.orig_norm_hist is None or self.eq_norm_hist is None:
            return
        
        # Calcular CDFs
        cdf_orig = np.cumsum(self.orig_norm_hist)
        cdf_eq = np.cumsum(self.eq_norm_hist)
        
        # Criar figura para as CDFs
        fig = Figure(figsize=(8, 4), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        # Plotar as CDFs
        x = np.arange(len(cdf_orig))
        ax.plot(x, cdf_orig, 'b-', label='Original')
        ax.plot(x, cdf_eq, 'r-', label='Equalizada')
        
        # Configurar eixos e título
        ax.set_xlabel('Intensidade')
        ax.set_ylabel('Probabilidade Acumulada')
        ax.set_title('Função de Distribuição Acumulada (CDF)')
        ax.legend()
        
        # Limitar o número de ticks no eixo x
        max_ticks = 10
        if len(cdf_orig) > max_ticks:
            step = len(cdf_orig) // max_ticks
            ax.set_xticks(np.arange(0, len(cdf_orig), step))
        
        fig.tight_layout()
        
        # Converter para QPixmap
        pixmap = self.figure_to_pixmap(fig)
        self.cdf_label.setPixmap(pixmap)
    
    def pil_to_pixmap(self, pil_image):
        """Converte uma imagem PIL para QPixmap"""
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        
        q_image = QImage(
            pil_image.tobytes(),
            pil_image.width,
            pil_image.height,
            pil_image.width * 3,
            QImage.Format_RGB888
        )
        return QPixmap.fromImage(q_image)
    
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
        """Redimensiona as imagens quando a janela é redimensionada"""
        super().resizeEvent(event)
        self.display_images()
        
    def set_image(self, image):
        """Define a imagem a ser processada"""
        self.original_image = image
        self.apply_equalization() 