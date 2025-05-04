from PySide6.QtWidgets import (QMainWindow, QMenuBar, QMenu, 
                              QFileDialog, QMessageBox, QLabel,
                              QWidget, QVBoxLayout)
from PySide6.QtGui import QAction, QPixmap, QImage
from PySide6.QtCore import Qt
from .about_dialog import AboutDialog
from PIL import Image
import numpy as np
import os

# Importar nossas ferramentas
from henpixy.tools.intensity import zero_intensity

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
        
        # Armazenar o caminho da imagem atual
        self.current_image_path = None
        self.current_image = None
        
        # Criar a barra de menus
        self.create_menu_bar()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        # Ação Abrir
        open_action = QAction("Abrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Ação Salvar
        save_action = QAction("Salvar", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Ação Salvar Como
        save_as_action = QAction("Salvar Como", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        # Separador
        file_menu.addSeparator()
        
        # Ação Sair
        exit_action = QAction("Sair", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu("Ferramentas")
        
        # Submenu Intensidade
        intensity_menu = QMenu("Intensidade", self)
        
        # Ação Intensidade Zero
        zero_intensity_action = QAction("Intensidade Zero", self)
        zero_intensity_action.triggered.connect(self.apply_zero_intensity)
        intensity_menu.addAction(zero_intensity_action)
        
        # Adicionar submenu ao menu Ferramentas
        tools_menu.addMenu(intensity_menu)
        
        # Menu Janela
        window_menu = menubar.addMenu("Janela")
        
        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")
        
        # Ação Sobre
        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def closeEvent(self, event):
        """Evento chamado quando a janela é fechada"""
        reply = QMessageBox.question(
            self,
            "Sair",
            "Deseja realmente sair?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def apply_zero_intensity(self):
        """Aplica a ferramenta de intensidade zero na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Aplica a ferramenta de intensidade zero
            processed_image = zero_intensity(self.current_image)
            
            # Atualiza a imagem atual
            self.current_image = processed_image
            
            # Exibe a imagem processada
            self.update_display_image()
            
            QMessageBox.information(
                self,
                "Sucesso",
                "A intensidade da imagem foi alterada para zero."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível processar a imagem.\nErro: {str(e)}"
            )
    
    def update_display_image(self):
        """Atualiza a exibição da imagem atual"""
        if self.current_image is None:
            return
        
        # Preparar a imagem para exibição
        display_image = self.current_image
        
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
        
        # Redimensionar a imagem para caber na janela mantendo a proporção
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled_pixmap)
    
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
                
                # Guardar a imagem original e o caminho
                self.current_image = image
                self.current_image_path = file_name
                
                # Atualizar o título da janela
                self.setWindowTitle(f"Henpixy - {os.path.basename(file_name)}")
                
                # Exibir a imagem
                self.update_display_image()
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Não foi possível abrir a imagem.\nErro: {str(e)}"
                )
    
    def save_file(self):
        """Salva a imagem atual no mesmo local onde foi aberta"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para salvar."
            )
            return
        
        # Se já temos um caminho, salvar diretamente
        if self.current_image_path:
            try:
                self.current_image.save(self.current_image_path)
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Imagem salva em:\n{self.current_image_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Não foi possível salvar a imagem.\nErro: {str(e)}"
                )
        else:
            # Se não temos um caminho, usar "Salvar Como"
            self.save_file_as()
    
    def save_file_as(self):
        """Salva a imagem atual em um novo local"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para salvar."
            )
            return
        
        # Filtros para diferentes tipos de imagem
        save_filters = (
            "PNG (*.png);;"
            "JPEG (*.jpg);;"
            "BMP (*.bmp);;"
            "GIF (*.gif);;"
            "TIFF (*.tiff);;"
            "WebP (*.webp)"
        )
        
        # Determinar filtro padrão baseado na extensão do arquivo atual
        default_filter = "PNG (*.png)"
        if self.current_image_path:
            ext = os.path.splitext(self.current_image_path)[1].lower()
            if ext == ".jpg" or ext == ".jpeg":
                default_filter = "JPEG (*.jpg)"
            elif ext == ".bmp":
                default_filter = "BMP (*.bmp)"
            elif ext == ".gif":
                default_filter = "GIF (*.gif)"
            elif ext == ".tiff" or ext == ".tif":
                default_filter = "TIFF (*.tiff)"
            elif ext == ".webp":
                default_filter = "WebP (*.webp)"
        
        # Abrir diálogo para salvar
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Salvar Imagem",
            "",
            save_filters,
            default_filter
        )
        
        if file_path:
            try:
                # Adicionar extensão se não houver
                if not os.path.splitext(file_path)[1]:
                    if selected_filter == "PNG (*.png)":
                        file_path += ".png"
                    elif selected_filter == "JPEG (*.jpg)":
                        file_path += ".jpg"
                    elif selected_filter == "BMP (*.bmp)":
                        file_path += ".bmp"
                    elif selected_filter == "GIF (*.gif)":
                        file_path += ".gif"
                    elif selected_filter == "TIFF (*.tiff)":
                        file_path += ".tiff"
                    elif selected_filter == "WebP (*.webp)":
                        file_path += ".webp"
                
                # Salvar a imagem
                self.current_image.save(file_path)
                
                # Atualizar o caminho atual
                self.current_image_path = file_path
                
                # Atualizar o título da janela
                self.setWindowTitle(f"Henpixy - {os.path.basename(file_path)}")
                
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Imagem salva em:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Não foi possível salvar a imagem.\nErro: {str(e)}"
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