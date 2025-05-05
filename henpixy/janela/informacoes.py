"""
Módulo para exibição de informações detalhadas sobre imagens
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QGridLayout, QScrollArea, QWidget)
from PySide6.QtCore import Qt
import os
from PIL import Image
import datetime

class ImageInfoDialog(QDialog):
    """Diálogo para exibir informações detalhadas sobre a imagem"""
    
    def __init__(self, parent=None):
        """
        Inicializa o diálogo de informações da imagem
        
        Args:
            parent (QWidget, optional): Widget pai
        """
        super().__init__(parent)
        self.setWindowTitle("Informações da Imagem")
        self.setMinimumSize(500, 400)
        
        # Configura para não ser modal
        self.setModal(False)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Área de rolagem para as informações
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Widget para conter as informações
        info_widget = QWidget()
        self.info_layout = QGridLayout(info_widget)
        self.info_layout.setColumnStretch(1, 1)  # A segunda coluna pode esticar
        self.info_layout.setVerticalSpacing(10)
        
        scroll_area.setWidget(info_widget)
        layout.addWidget(scroll_area)
        
        # Botão para fechar
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close)
        close_button.setFixedWidth(100)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        
        # Inicializa com mensagem de nenhuma imagem
        self.set_no_image()
    
    def set_no_image(self):
        """Exibe mensagem quando não há imagem carregada"""
        self.clear_info()
        
        label = QLabel("Nenhuma imagem carregada.")
        label.setAlignment(Qt.AlignCenter)
        self.info_layout.addWidget(label, 0, 0, 1, 2)
    
    def clear_info(self):
        """Limpa todas as informações do layout"""
        while self.info_layout.count():
            item = self.info_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def set_image_info(self, image_path, pil_image):
        """
        Define as informações da imagem
        
        Args:
            image_path (str): Caminho do arquivo de imagem
            pil_image (PIL.Image.Image): A imagem
        """
        if not pil_image:
            self.set_no_image()
            return
        
        self.clear_info()
        
        # Lista de informações para exibir
        info_list = []
        
        # Informações básicas do arquivo
        if image_path:
            file_info = os.stat(image_path)
            filename = os.path.basename(image_path)
            file_ext = os.path.splitext(filename)[1].lower()
            
            info_list.append(("Nome do arquivo:", filename))
            info_list.append(("Caminho:", image_path))
            info_list.append(("Tipo:", file_ext[1:].upper() if file_ext else "Desconhecido"))
            
            # Tamanho do arquivo
            size_bytes = file_info.st_size
            if size_bytes < 1024:
                size_str = f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.2f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
            
            info_list.append(("Tamanho do arquivo:", size_str))
            
            # Data de modificação
            mod_time = datetime.datetime.fromtimestamp(file_info.st_mtime)
            info_list.append(("Data de modificação:", mod_time.strftime("%d/%m/%Y %H:%M:%S")))
            
        # Informações da imagem
        info_list.append(("Dimensões:", f"{pil_image.width} x {pil_image.height} pixels"))
        info_list.append(("Total de pixels:", f"{pil_image.width * pil_image.height}"))
        info_list.append(("Modo de cor:", pil_image.mode))
        
        # Informações específicas do modo de cor
        if pil_image.mode == 'RGB':
            info_list.append(("Espaço de cores:", "RGB (Vermelho, Verde, Azul)"))
            info_list.append(("Canais:", "3 (R, G, B)"))
            info_list.append(("Profundidade de bits:", "24 bits (8 bits por canal)"))
        elif pil_image.mode == 'RGBA':
            info_list.append(("Espaço de cores:", "RGBA (Vermelho, Verde, Azul, Alpha)"))
            info_list.append(("Canais:", "4 (R, G, B, A)"))
            info_list.append(("Profundidade de bits:", "32 bits (8 bits por canal)"))
            info_list.append(("Canal alpha:", "Sim"))
        elif pil_image.mode == 'L':
            info_list.append(("Espaço de cores:", "Escala de cinza"))
            info_list.append(("Canais:", "1"))
            info_list.append(("Profundidade de bits:", "8 bits"))
        elif pil_image.mode == 'CMYK':
            info_list.append(("Espaço de cores:", "CMYK (Ciano, Magenta, Amarelo, Preto)"))
            info_list.append(("Canais:", "4 (C, M, Y, K)"))
            info_list.append(("Profundidade de bits:", "32 bits (8 bits por canal)"))
        elif pil_image.mode == 'P':
            info_list.append(("Espaço de cores:", "Paleta de cores"))
            info_list.append(("Canais:", "1 (índice da paleta)"))
            
        # Informação sobre canal alpha
        if 'A' in pil_image.mode:
            info_list.append(("Canal alpha:", "Sim"))
        else:
            info_list.append(("Canal alpha:", "Não"))
        
        # Tenta obter DPI (resolução)
        if hasattr(pil_image, 'info') and 'dpi' in pil_image.info:
            dpi = pil_image.info['dpi']
            info_list.append(("Resolução:", f"{dpi[0]} x {dpi[1]} DPI"))
        
        # Tenta obter informações EXIF
        exif = pil_image.getexif() if hasattr(pil_image, 'getexif') else None
        if exif and len(exif) > 0:
            info_list.append(("Dados EXIF:", "Disponíveis"))
            
            # Informações da câmera
            if 272 in exif and exif[272]:  # Modelo da câmera
                info_list.append(("Câmera:", exif[272]))
            if 271 in exif and exif[271]:  # Fabricante da câmera
                info_list.append(("Fabricante:", exif[271]))
            
            # Data da foto
            if 306 in exif and exif[306]:  # Data e hora
                info_list.append(("Data da foto:", exif[306]))
            
            # Configurações da foto
            if 33437 in exif and exif[33437]:  # Abertura
                info_list.append(("Abertura:", f"f/{float(exif[33437])}"))
            if 33434 in exif and exif[33434]:  # Tempo de exposição
                info_list.append(("Tempo de exposição:", f"{exif[33434][0]}/{exif[33434][1]} s"))
            if 34855 in exif and exif[34855]:  # ISO
                info_list.append(("ISO:", exif[34855]))
        
        # Exibe as informações no layout
        for row, (label_text, value_text) in enumerate(info_list):
            # Label para o nome da propriedade
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold;")
            self.info_layout.addWidget(label, row, 0)
            
            # Label para o valor da propriedade
            value = QLabel(str(value_text))
            value.setWordWrap(True)
            self.info_layout.addWidget(value, row, 1) 