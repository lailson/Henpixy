"""
Componente para visualização de imagens.
"""

from PySide6.QtWidgets import QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QSize
from PIL import Image, ImageQt
import numpy as np

class ImageViewer(QWidget):
    """
    Widget para visualização de imagens com suporte para ScrollArea.
    
    Este componente permite exibir imagens PIL com suporte para rolagem
    quando a imagem é maior que o espaço disponível.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Área de rolagem
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Label para a imagem
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setMinimumSize(1, 1)
        
        # Adiciona o label à área de rolagem
        self.scroll_area.setWidget(self.image_label)
        
        # Adiciona a área de rolagem ao layout
        layout.addWidget(self.scroll_area)
        
        # Armazena a imagem atual
        self.current_image = None
    
    def set_image(self, image):
        """
        Define a imagem a ser exibida.
        
        Args:
            image (PIL.Image.Image): Imagem a ser exibida
        """
        if image is None:
            return
        
        # Armazena a imagem
        self.current_image = image
        
        # Preparar a imagem para exibição
        display_image = image
        
        # Tratar diferentes modos de imagem
        if display_image.mode in ('RGBA', 'LA'):
            # Converter para RGB mantendo o canal alpha
            background = Image.new('RGB', display_image.size, (255, 255, 255))
            background.paste(display_image, mask=display_image.split()[-1])
            display_image = background
        elif display_image.mode not in ('RGB', 'L'):
            # Converter para RGB se não for RGB ou escala de cinza
            display_image = display_image.convert('RGB')
        
        # Converter para array numpy
        image_array = np.array(display_image)
        
        # Determinar o formato QImage baseado no modo da imagem
        if len(image_array.shape) == 2:  # Imagem em escala de cinza
            height, width = image_array.shape
            bytes_per_line = width
            q_image = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:  # Imagem RGB
            height, width, channel = image_array.shape
            bytes_per_line = 3 * width
            q_image = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Converter para QPixmap e exibir
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        
        # Ajustar o tamanho mínimo do label para o tamanho da imagem
        self.image_label.setMinimumSize(pixmap.size())
    
    def clear(self):
        """Remove a imagem atual."""
        self.current_image = None
        self.image_label.clear()
        self.image_label.setMinimumSize(1, 1)
    
    def resizeEvent(self, event):
        """Manipula o redimensionamento do widget."""
        super().resizeEvent(event)
        
        # Se não houver imagem, não precisa fazer nada
        if self.current_image is None:
            return
        
        # Calcula o tamanho disponível
        available_width = self.scroll_area.viewport().width()
        available_height = self.scroll_area.viewport().height()
        
        # Obtém o tamanho atual da imagem
        pixmap = self.image_label.pixmap()
        if pixmap:
            image_width = pixmap.width()
            image_height = pixmap.height()
            
            # Se a imagem for menor que o espaço disponível, centraliza
            if image_width < available_width and image_height < available_height:
                self.image_label.setAlignment(Qt.AlignCenter)
            else:
                self.image_label.setAlignment(Qt.AlignTop | Qt.AlignLeft) 