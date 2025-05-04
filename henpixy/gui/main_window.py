from PySide6.QtWidgets import (QMainWindow, QMenuBar, QMenu, 
                              QFileDialog, QMessageBox, QLabel,
                              QWidget, QVBoxLayout)
from PySide6.QtGui import QAction, QPixmap, QImage
from PySide6.QtCore import Qt
from .about_dialog import AboutDialog
from PIL import Image
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Henpixy")
        self.setMinimumSize(800, 600)
        
        # Widget central e layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Label para exibir a imagem
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        
        # Criar a barra de menus
        self.create_menu_bar()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        # Ação Abrir
        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu("Ferramentas")
        
        # Menu Janela
        window_menu = menubar.addMenu("Janela")
        
        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")
        
        # Ação Sobre
        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def open_file(self):
        # Filtros para diferentes tipos de imagem
        image_filters = (
            "Imagens (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.tif *.webp *.ico *.psd *.xbm *.xpm);;"
            "PNG (*.png);;"
            "JPEG (*.jpg *.jpeg);;"
            "BMP (*.bmp);;"
            "GIF (*.gif);;"
            "TIFF (*.tiff *.tif);;"
            "WebP (*.webp);;"
            "ICO (*.ico);;"
            "PSD (*.psd);;"
            "XBM (*.xbm);;"
            "XPM (*.xpm);;"
            "Todos os arquivos (*.*)"
        )
        
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Imagem",
            "",
            image_filters
        )
        
        if file_name:
            try:
                # Abrir a imagem usando Pillow
                image = Image.open(file_name)
                
                # Tratar diferentes modos de imagem
                if image.mode in ('RGBA', 'LA'):
                    # Converter para RGB mantendo o canal alpha
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background
                elif image.mode not in ('RGB', 'L'):
                    # Converter para RGB se não for RGB ou escala de cinza
                    image = image.convert('RGB')
                
                # Converter para array numpy
                image_array = np.array(image)
                
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
                
                # Redimensionar a imagem para caber na janela mantendo a proporção
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                self.image_label.setPixmap(scaled_pixmap)
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Não foi possível abrir a imagem.\nErro: {str(e)}"
                )
    
    def resizeEvent(self, event):
        """Redimensiona a imagem quando a janela é redimensionada"""
        super().resizeEvent(event)
        if hasattr(self, 'image_label') and self.image_label.pixmap():
            scaled_pixmap = self.image_label.pixmap().scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec() 