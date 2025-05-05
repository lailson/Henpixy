"""
Módulo para visualização de intensidade de pixels
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QGridLayout, QSpinBox,
                              QWidget, QScrollArea, QFormLayout)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QImage, QColor, QCursor
import numpy as np

class PixelIntensityDialog(QDialog):
    """Diálogo para exibir a intensidade dos pixels"""
    
    def __init__(self, parent=None):
        """
        Inicializa o diálogo de intensidade de pixels
        
        Args:
            parent (QWidget, optional): Widget pai
        """
        super().__init__(parent)
        self.setWindowTitle("Intensidade de Pixels")
        self.setMinimumSize(500, 400)
        
        # Configura para não ser modal
        self.setModal(False)
        
        # Imagem atual (será definida pelo método set_image)
        self.image = None
        self.image_array = None
        
        # Tamanho da matriz de visualização
        self.matrix_size = 5
        self.min_matrix_size = 1
        self.max_matrix_size = 15  # Valor inicial, será ajustado conforme o tamanho da imagem
        
        # Posição do pixel selecionado
        self.selected_x = -1
        self.selected_y = -1
        
        # Dimensões da imagem
        self.image_width = 0
        self.image_height = 0
        
        self.init_ui()
        self.show_instructions()
    
    def init_ui(self):
        """Inicializa a interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Área de instruções
        self.instruction_label = QLabel("Clique em um ponto da imagem para ver a intensidade dos pixels.")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction_label)
        
        # Área de entrada de coordenadas
        coord_layout = QHBoxLayout()
        
        # Formulário para entrada de coordenadas
        form_layout = QFormLayout()
        
        # Campo para coordenada X
        self.x_coord = QSpinBox()
        self.x_coord.setMinimum(0)
        self.x_coord.setMaximum(9999)  # Será ajustado com base no tamanho da imagem
        self.x_coord.setEnabled(False)
        form_layout.addRow("X:", self.x_coord)
        
        # Campo para coordenada Y
        self.y_coord = QSpinBox()
        self.y_coord.setMinimum(0)
        self.y_coord.setMaximum(9999)  # Será ajustado com base no tamanho da imagem
        self.y_coord.setEnabled(False)
        form_layout.addRow("Y:", self.y_coord)
        
        coord_layout.addLayout(form_layout)
        
        # Botão para aplicar coordenadas
        self.apply_coord_button = QPushButton("Aplicar")
        self.apply_coord_button.clicked.connect(self.apply_coordinates)
        self.apply_coord_button.setEnabled(False)
        coord_layout.addWidget(self.apply_coord_button)
        
        layout.addLayout(coord_layout)
        
        # Área de controle do tamanho da matriz
        control_layout = QHBoxLayout()
        
        # Botão para diminuir a matriz
        self.decrease_button = QPushButton("-")
        self.decrease_button.setFixedWidth(40)
        self.decrease_button.clicked.connect(self.decrease_matrix_size)
        self.decrease_button.setEnabled(False)
        control_layout.addWidget(self.decrease_button)
        
        # Label para exibir o tamanho atual da matriz
        self.size_label = QLabel(f"Tamanho: {self.matrix_size}x{self.matrix_size}")
        self.size_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(self.size_label)
        
        # Botão para aumentar a matriz
        self.increase_button = QPushButton("+")
        self.increase_button.setFixedWidth(40)
        self.increase_button.clicked.connect(self.increase_matrix_size)
        self.increase_button.setEnabled(False)
        control_layout.addWidget(self.increase_button)
        
        layout.addLayout(control_layout)
        
        # Área de rolagem para a matriz de intensidade
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Widget para conter a matriz
        self.matrix_widget = QWidget()
        self.matrix_layout = QGridLayout(self.matrix_widget)
        self.matrix_layout.setSpacing(2)
        
        scroll_area.setWidget(self.matrix_widget)
        layout.addWidget(scroll_area)
        
        # Botão para fechar
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
    
    def apply_coordinates(self):
        """Aplica as coordenadas digitadas pelo usuário"""
        x = self.x_coord.value()
        y = self.y_coord.value()
        
        # Verifica se as coordenadas são válidas
        if x >= 0 and x < self.image_width and y >= 0 and y < self.image_height:
            self.set_selected_pixel(x, y)
    
    def show_instructions(self):
        """Exibe as instruções para o usuário"""
        self.instruction_label.setText("Clique em um ponto da imagem ou digite as coordenadas para ver a intensidade dos pixels.")
        
        # Limpa a matriz
        self.clear_matrix()
        
        # Desabilita os botões de controle
        self.decrease_button.setEnabled(False)
        self.increase_button.setEnabled(False)
    
    def clear_matrix(self):
        """Limpa a matriz de intensidade"""
        # Remove todos os widgets do layout
        while self.matrix_layout.count():
            item = self.matrix_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def set_image(self, pil_image):
        """
        Define a imagem a ser analisada
        
        Args:
            pil_image (PIL.Image.Image): A imagem
        """
        self.image = pil_image
        
        # Converte a imagem para array numpy
        self.image_array = np.array(pil_image)
        
        # Armazena as dimensões da imagem
        height, width = self.image_array.shape[:2]
        self.image_height = height
        self.image_width = width
        
        # Ajusta o tamanho máximo da matriz com base no tamanho da imagem
        self.max_matrix_size = min(15, min(height, width))
        
        # Redefine a posição selecionada
        self.selected_x = -1
        self.selected_y = -1
        
        # Configura os campos de coordenadas
        self.x_coord.setMaximum(width - 1)
        self.y_coord.setMaximum(height - 1)
        self.x_coord.setEnabled(True)
        self.y_coord.setEnabled(True)
        self.apply_coord_button.setEnabled(True)
        
        # Exibe as instruções
        self.show_instructions()
    
    def set_selected_pixel(self, x, y):
        """
        Define o pixel selecionado
        
        Args:
            x (int): Coordenada x do pixel
            y (int): Coordenada y do pixel
        """
        if self.image_array is None:
            return
        
        # Verifica se as coordenadas são válidas
        if x < 0 or x >= self.image_width or y < 0 or y >= self.image_height:
            return
        
        self.selected_x = x
        self.selected_y = y
        
        # Atualiza os campos de coordenadas
        self.x_coord.setValue(x)
        self.y_coord.setValue(y)
        
        # Atualiza a instrução
        self.instruction_label.setText(f"Pixel selecionado: ({x}, {y})")
        
        # Habilita os botões de controle
        self.decrease_button.setEnabled(self.matrix_size > self.min_matrix_size)
        self.increase_button.setEnabled(self.matrix_size < self.max_matrix_size)
        
        # Atualiza a matriz
        self.update_matrix()
    
    def update_matrix(self):
        """Atualiza a matriz de intensidade"""
        if self.image_array is None or self.selected_x < 0 or self.selected_y < 0:
            return
        
        # Limpa a matriz
        self.clear_matrix()
        
        # Calcula as coordenadas inicial e final
        half_size = self.matrix_size // 2
        start_x = max(0, self.selected_x - half_size)
        start_y = max(0, self.selected_y - half_size)
        
        height, width = self.image_array.shape[:2]
        end_x = min(width, start_x + self.matrix_size)
        end_y = min(height, start_y + self.matrix_size)
        
        # Verifica se é necessário ajustar as coordenadas iniciais
        if end_x - start_x < self.matrix_size:
            start_x = max(0, end_x - self.matrix_size)
        if end_y - start_y < self.matrix_size:
            start_y = max(0, end_y - self.matrix_size)
        
        # Preenche a matriz
        for i, y in enumerate(range(start_y, end_y)):
            for j, x in enumerate(range(start_x, end_x)):
                # Cria um widget para exibir o valor do pixel
                pixel_widget = self.create_pixel_widget(x, y)
                
                # Destaca o pixel central
                if x == self.selected_x and y == self.selected_y:
                    pixel_widget.setStyleSheet("background-color: yellow; font-weight: bold;")
                
                # Adiciona o widget à matriz
                self.matrix_layout.addWidget(pixel_widget, i, j)
    
    def create_pixel_widget(self, x, y):
        """
        Cria um widget para exibir o valor do pixel
        
        Args:
            x (int): Coordenada x do pixel
            y (int): Coordenada y do pixel
            
        Returns:
            QLabel: Widget com o valor do pixel
        """
        # Obtém o valor do pixel
        pixel = self.image_array[y, x]
        
        # Cria um widget para exibir o valor
        widget = QLabel()
        widget.setAlignment(Qt.AlignCenter)
        widget.setFixedSize(80, 60)
        widget.setFrameShape(QLabel.Box)
        
        # Formata o texto com base no tipo de imagem
        if len(self.image_array.shape) == 2:  # Imagem em escala de cinza
            # Texto simples para intensidade em escala de cinza
            widget.setText(f"{pixel}")
        else:  # Imagem colorida (RGB ou RGBA)
            # Texto formatado para RGB
            if len(pixel) >= 3:
                r, g, b = pixel[:3]
                # Define a cor de fundo do widget
                widget.setStyleSheet(f"background-color: rgb({r}, {g}, {b}); color: {'white' if (r + g + b) / 3 < 128 else 'black'};")
                widget.setText(f"R: {r}\nG: {g}\nB: {b}")
        
        return widget
    
    def increase_matrix_size(self):
        """Aumenta o tamanho da matriz"""
        if self.matrix_size < self.max_matrix_size:
            self.matrix_size += 2  # Aumenta em 2 para manter o pixel central
            self.size_label.setText(f"Tamanho: {self.matrix_size}x{self.matrix_size}")
            
            # Atualiza o estado dos botões
            self.decrease_button.setEnabled(self.matrix_size > self.min_matrix_size)
            self.increase_button.setEnabled(self.matrix_size < self.max_matrix_size)
            
            # Atualiza a matriz
            self.update_matrix()
    
    def decrease_matrix_size(self):
        """Diminui o tamanho da matriz"""
        if self.matrix_size > self.min_matrix_size:
            self.matrix_size -= 2  # Diminui em 2 para manter o pixel central
            self.size_label.setText(f"Tamanho: {self.matrix_size}x{self.matrix_size}")
            
            # Atualiza o estado dos botões
            self.decrease_button.setEnabled(self.matrix_size > self.min_matrix_size)
            self.increase_button.setEnabled(self.matrix_size < self.max_matrix_size)
            
            # Atualiza a matriz
            self.update_matrix() 