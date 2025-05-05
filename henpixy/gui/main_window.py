from PySide6.QtWidgets import (QMainWindow, QMenuBar, QMenu, 
                              QFileDialog, QMessageBox, QLabel,
                              QWidget, QVBoxLayout, QDialog,
                              QInputDialog, QDoubleSpinBox, QHBoxLayout,
                              QPushButton, QFormLayout)
from PySide6.QtGui import QAction, QPixmap, QImage, QCursor
from PySide6.QtCore import Qt, QPoint, QRect
from .about_dialog import AboutDialog
from .contrast_stretching_dialog import ContrastStretchingDialog
from .bit_plane_dialog import BitPlaneDialog
from .histogram_dialog import HistogramDialog
from .histogram_window import HistogramWindow
from .pseudocolor_dialog import PseudocolorDialog
from .mean_filter_dialog import MeanFilterDialog
from .order_statistics_dialog import OrderStatisticsDialog
from PIL import Image
import numpy as np
import os

# Importar nossas ferramentas
from henpixy.tools.intensity import zero_intensity
from henpixy.tools.negative import negative
from henpixy.tools.power import power_transform
from henpixy.tools.contrast_stretching import contrast_stretching
from henpixy.tools.bit_plane_slicing import extract_bit_plane, get_image_bit_depth
from henpixy.tools.spatial_filtering import mean_filter, min_filter, max_filter, median_filter

# Importar o gerenciador de histórico
from henpixy.janela.historico import HistoryManager, HistoryDialog

# Importar o diálogo de intensidade de pixels
from henpixy.janela.intensidade import PixelIntensityDialog

# Importar o diálogo de informações da imagem
from henpixy.janela.informacoes import ImageInfoDialog

class GammaDialog(QDialog):
    """Diálogo para ajuste dos parâmetros da transformação gama"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Transformação Gama")
        self.setMinimumWidth(300)
        
        # Valores iniciais
        self.gamma_value = 1.0
        self.c_value = 1.0
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Form layout para os campos
        form_layout = QFormLayout()
        
        # Campo para o valor de gamma
        self.gamma_spin = QDoubleSpinBox()
        self.gamma_spin.setRange(0.1, 10.0)
        self.gamma_spin.setSingleStep(0.1)
        self.gamma_spin.setValue(self.gamma_value)
        self.gamma_spin.setDecimals(2)
        form_layout.addRow("Valor de Gama (γ):", self.gamma_spin)
        
        # Campo para o valor de c (constante)
        self.c_spin = QDoubleSpinBox()
        self.c_spin.setRange(0.1, 5.0)
        self.c_spin.setSingleStep(0.1)
        self.c_spin.setValue(self.c_value)
        self.c_spin.setDecimals(2)
        form_layout.addRow("Constante (c):", self.c_spin)
        
        # Adicionando form layout ao layout principal
        layout.addLayout(form_layout)
        
        # Informações sobre a transformação
        info_text = """
        <p><b>Transformação Gama: S = c × r^γ</b></p>
        <p>- S é o valor resultante</p>
        <p>- c é uma constante multiplicativa</p>
        <p>- r é o valor original do pixel (normalizado entre 0 e 1)</p>
        <p>- γ (gama) é o expoente que controla o contraste</p>
        <p>Características:</p>
        <p>- γ < 1: Expande valores escuros (mais detalhes em áreas escuras)</p>
        <p>- γ = 1: Transformação identidade (imagem não é alterada)</p>
        <p>- γ > 1: Expande valores claros (mais detalhes em áreas claras)</p>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Botões de OK e Cancelar
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancelar")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def get_values(self):
        """Retorna os valores dos parâmetros"""
        self.gamma_value = self.gamma_spin.value()
        self.c_value = self.c_spin.value()
        return self.gamma_value, self.c_value

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
        
        # Inicializa o gerenciador de histórico
        self.history_manager = HistoryManager()
        
        # Referência para o diálogo de histórico
        self.history_dialog = None
        
        # Referência para o diálogo de intensidade
        self.intensity_dialog = None
        
        # Referência para o diálogo de informações
        self.info_dialog = None
        
        # Referência para a janela de histograma
        self.histogram_window = None
        
        # Menu de amostras (inicializado no create_menu_bar)
        self.sample_menu = None
        
        # Modo de seleção de pixel
        self.pixel_selection_mode = False
        
        # Fator de zoom
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        
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
        
        # Submenu Abrir Modelo
        self.sample_menu = QMenu("Abrir modelo", self)
        self.update_sample_menu()  # Preenche o submenu com as imagens disponíveis
        file_menu.addMenu(self.sample_menu)
        
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
        
        # Ação Informações
        info_action = QAction("Informações", self)
        info_action.setShortcut("Ctrl+I")
        info_action.triggered.connect(self.show_image_info)
        file_menu.addAction(info_action)
        
        # Separador
        file_menu.addSeparator()
        
        # Ação Sair
        exit_action = QAction("Sair", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Exibir
        view_menu = menubar.addMenu("Exibir")
        
        # Ação Mais Zoom
        zoom_in_action = QAction("Mais Zoom", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        # Ação Menos Zoom
        zoom_out_action = QAction("Menos Zoom", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        # Ação Reset Zoom
        reset_zoom_action = QAction("Zoom Original", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu("Ferramentas")
        
        # Ação Intensidade Zero
        zero_intensity_action = QAction("Intensidade Zero", self)
        zero_intensity_action.triggered.connect(self.apply_zero_intensity)
        tools_menu.addAction(zero_intensity_action)
        
        # Ação Negativo
        negative_action = QAction("Negativo", self)
        negative_action.triggered.connect(self.apply_negative)
        tools_menu.addAction(negative_action)
        
        # Ação Transformação Gama
        gamma_action = QAction("Transformação Gama", self)
        gamma_action.triggered.connect(self.apply_gamma)
        tools_menu.addAction(gamma_action)
        
        # Ação Alargamento de Contraste
        contrast_stretching_action = QAction("Alargamento de Contraste", self)
        contrast_stretching_action.triggered.connect(self.apply_contrast_stretching)
        tools_menu.addAction(contrast_stretching_action)
        
        # Ação Fatiamento por Planos de Bits
        bit_plane_action = QAction("Fatiamento por Planos de Bits", self)
        bit_plane_action.triggered.connect(self.apply_bit_plane_slicing)
        tools_menu.addAction(bit_plane_action)
        
        # Ação Equalização de Histograma
        histogram_action = QAction("Equalização de Histograma", self)
        histogram_action.triggered.connect(self.apply_histogram_equalization)
        tools_menu.addAction(histogram_action)
        
        # Ação Fatiamento por Intensidades para Pseudocores
        pseudocolor_action = QAction("Fatiamento por Intensidades para Pseudocores", self)
        pseudocolor_action.triggered.connect(self.apply_pseudocolor)
        tools_menu.addAction(pseudocolor_action)
        
        # Adiciona um separador para os filtros
        tools_menu.addSeparator()
        
        # Ação Filtro da Média
        mean_filter_action = QAction("Filtro da Média", self)
        mean_filter_action.triggered.connect(self.apply_mean_filter)
        tools_menu.addAction(mean_filter_action)
        
        # Ação Filtros de Estatísticas de Ordem
        order_statistics_action = QAction("Filtros de Estatísticas de Ordem", self)
        order_statistics_action.triggered.connect(self.apply_order_statistics_filter)
        tools_menu.addAction(order_statistics_action)
        
        # Menu Janela
        window_menu = menubar.addMenu("Janela")
        
        # Ação Histórico
        history_action = QAction("Histórico", self)
        history_action.setShortcut("Ctrl+H")
        history_action.triggered.connect(self.show_history)
        window_menu.addAction(history_action)
        
        # Ação Intensidade
        pixel_intensity_action = QAction("Intensidade", self)
        pixel_intensity_action.setShortcut("Ctrl+P")  # Alterado para Ctrl+P para evitar conflito com Informações
        pixel_intensity_action.triggered.connect(self.show_pixel_intensity)
        window_menu.addAction(pixel_intensity_action)
        
        # Ação Histograma
        histogram_action = QAction("Histograma", self)
        histogram_action.triggered.connect(self.show_histogram)
        window_menu.addAction(histogram_action)
        
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
    
    def show_history(self):
        """Exibe o diálogo de histórico"""
        if not self.history_manager.history_items:
            QMessageBox.information(
                self,
                "Histórico",
                "Não há histórico disponível."
            )
            return
        
        # Verifica se o diálogo já está aberto
        if self.history_dialog is not None and self.history_dialog.isVisible():
            # Traz o diálogo para frente
            self.history_dialog.raise_()
            self.history_dialog.activateWindow()
            return
        
        # Cria um novo diálogo de histórico
        self.history_dialog = HistoryDialog(self.history_manager, self)
        
        # Conecta o sinal de aceitação para processar a restauração da imagem
        self.history_dialog.accepted.connect(self.on_history_accepted)
        
        # Mostra o diálogo de forma não-modal
        self.history_dialog.show()
    
    def on_history_accepted(self):
        """Chamado quando o diálogo de histórico é aceito"""
        # O usuário restaurou uma imagem do histórico
        self.current_image = self.history_manager.get_current_image()
        self.update_display_image()
    
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
            
            # Adiciona ao histórico
            self.history_manager.add_item(processed_image, "Intensidade Zero")
            
            # Atualiza a imagem atual
            self.current_image = processed_image
            
            # Exibe a imagem processada
            self.update_display_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível processar a imagem.\nErro: {str(e)}"
            )
    
    def apply_negative(self):
        """Aplica a função de negativo na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Aplica a função de negativo
            processed_image = negative(self.current_image)
            
            # Adiciona ao histórico
            self.history_manager.add_item(processed_image, "Negativo")
            
            # Atualiza a imagem atual
            self.current_image = processed_image
            
            # Exibe a imagem processada
            self.update_display_image()
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
        
        # Aplicar zoom
        if self.zoom_factor != 1.0:
            # Calcula o novo tamanho baseado no zoom
            new_width = int(pixmap.width() * self.zoom_factor)
            new_height = int(pixmap.height() * self.zoom_factor)
            
            # Redimensiona o pixmap
            scaled_pixmap = pixmap.scaled(
                new_width,
                new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            # Redimensionar a imagem para caber na janela mantendo a proporção
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        
        self.image_label.setPixmap(scaled_pixmap)
    
    def zoom_in(self):
        """Aumenta o zoom da imagem"""
        if self.current_image is None:
            return
        
        # Aumenta o fator de zoom em 10%
        self.zoom_factor = min(self.zoom_factor * 1.1, self.max_zoom)
        self.update_display_image()
        
        # Atualiza o título da janela para mostrar o fator de zoom
        self.update_window_title()
    
    def zoom_out(self):
        """Diminui o zoom da imagem"""
        if self.current_image is None:
            return
        
        # Diminui o fator de zoom em 10%
        self.zoom_factor = max(self.zoom_factor / 1.1, self.min_zoom)
        self.update_display_image()
        
        # Atualiza o título da janela para mostrar o fator de zoom
        self.update_window_title()
    
    def reset_zoom(self):
        """Redefine o zoom para o tamanho original"""
        if self.current_image is None:
            return
        
        # Redefine o fator de zoom
        self.zoom_factor = 1.0
        self.update_display_image()
        
        # Atualiza o título da janela para mostrar o fator de zoom
        self.update_window_title()
    
    def update_window_title(self):
        """Atualiza o título da janela"""
        if self.current_image_path:
            filename = os.path.basename(self.current_image_path)
            zoom_percent = int(self.zoom_factor * 100)
            self.setWindowTitle(f"Henpixy - {filename} ({zoom_percent}%)")
        else:
            self.setWindowTitle("Henpixy")
    
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
                
                # Adicionar ao histórico
                self.history_manager.clear()  # Limpa o histórico anterior
                self.history_manager.add_item(image, f"Original: {os.path.basename(file_name)}")
                
                # Redefine o zoom ao abrir uma nova imagem
                self.zoom_factor = 1.0
                
                # Atualizar o título da janela
                self.update_window_title()
                
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
        if hasattr(self, 'image_label') and self.image_label.pixmap() and self.zoom_factor == 1.0:
            # Só redimensiona automaticamente se o zoom estiver em 100%
            scaled_pixmap = self.image_label.pixmap().scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()
    
    def show_pixel_intensity(self):
        """Exibe o diálogo de intensidade de pixels"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para analisar."
            )
            return
        
        # Verifica se o diálogo já está aberto
        if self.intensity_dialog is not None and self.intensity_dialog.isVisible():
            # Traz o diálogo para frente
            self.intensity_dialog.raise_()
            self.intensity_dialog.activateWindow()
            return
        
        # Cria um novo diálogo de intensidade
        self.intensity_dialog = PixelIntensityDialog(self)
        self.intensity_dialog.set_image(self.current_image)
        
        # Exibe o diálogo
        self.intensity_dialog.show()
        
        # Ativa o modo de seleção de pixel
        self.pixel_selection_mode = True
        QMessageBox.information(
            self,
            "Selecionar Pixel",
            "Clique em um ponto da imagem para ver a intensidade dos pixels."
        )
        
        # Muda o cursor para indicar o modo de seleção
        self.setCursor(Qt.CrossCursor)
        
        # Conectar o evento de clique na imagem
        self.image_label.mousePressEvent = self.on_image_click
    
    def on_image_click(self, event):
        """Manipula o clique na imagem para selecionar um pixel"""
        if not self.pixel_selection_mode or self.intensity_dialog is None:
            # Chamada ao método padrão se não estiver no modo de seleção
            QLabel.mousePressEvent(self.image_label, event)
            return
        
        # Obtém as coordenadas do clique relativas à imagem
        pos = event.pos()
        pixmap = self.image_label.pixmap()
        
        if pixmap:
            # Calcula as coordenadas reais na imagem
            image_rect = self.get_image_display_rect()
            
            if image_rect.contains(pos):
                # Converte as coordenadas do clique para coordenadas na imagem original
                img_x = int((pos.x() - image_rect.left()) * self.current_image.width / image_rect.width())
                img_y = int((pos.y() - image_rect.top()) * self.current_image.height / image_rect.height())
                
                # Define o pixel selecionado no diálogo de intensidade
                self.intensity_dialog.set_selected_pixel(img_x, img_y)
                
                # Desativa o modo de seleção
                self.pixel_selection_mode = False
                
                # Restaura o cursor
                self.setCursor(Qt.ArrowCursor)
    
    def get_image_display_rect(self):
        """
        Retorna o retângulo onde a imagem está sendo exibida
        
        Returns:
            QRect: Retângulo da imagem
        """
        pixmap = self.image_label.pixmap()
        if not pixmap:
            return None
        
        # Obtém o tamanho da label
        label_size = self.image_label.size()
        
        # Calcula o tamanho da imagem escalada
        scaled_size = pixmap.size()
        scaled_size.scale(label_size, Qt.KeepAspectRatio)
        
        # Calcula a posição da imagem dentro da label
        pos_x = (label_size.width() - scaled_size.width()) / 2
        pos_y = (label_size.height() - scaled_size.height()) / 2
        
        # Retorna o retângulo
        return QRect(int(pos_x), int(pos_y), scaled_size.width(), scaled_size.height())
    
    def show_image_info(self):
        """Exibe o diálogo de informações da imagem"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para exibir informações."
            )
            return
        
        # Verifica se o diálogo já está aberto
        if self.info_dialog is not None and self.info_dialog.isVisible():
            # Traz o diálogo para frente
            self.info_dialog.raise_()
            self.info_dialog.activateWindow()
            return
        
        # Cria um novo diálogo de informações
        self.info_dialog = ImageInfoDialog(self)
        
        # Define as informações da imagem
        self.info_dialog.set_image_info(self.current_image_path, self.current_image)
        
        # Exibe o diálogo
        self.info_dialog.show()
    
    def update_sample_menu(self):
        """Atualiza o submenu de amostras com as imagens disponíveis"""
        # Limpa o menu atual
        self.sample_menu.clear()
        
        # Caminho para o diretório de amostras
        samples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "samples")
        
        # Verifica se o diretório de amostras existe
        if not os.path.exists(samples_dir):
            action = QAction("Diretório de amostras não encontrado", self)
            action.setEnabled(False)
            self.sample_menu.addAction(action)
            return
        
        # Lista os arquivos no diretório de amostras
        sample_files = [f for f in os.listdir(samples_dir) 
                      if os.path.isfile(os.path.join(samples_dir, f)) and
                      any(f.lower().endswith(ext) for ext in 
                          ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.webp'])]
        
        if not sample_files:
            action = QAction("Nenhuma imagem disponível", self)
            action.setEnabled(False)
            self.sample_menu.addAction(action)
            
            # Adiciona uma ação para atualizar o menu
            self.sample_menu.addSeparator()
            refresh_action = QAction("Atualizar lista", self)
            refresh_action.triggered.connect(self.update_sample_menu)
            self.sample_menu.addAction(refresh_action)
            return
        
        # Adiciona as imagens ao menu
        for sample_file in sorted(sample_files):
            action = QAction(sample_file, self)
            action.triggered.connect(lambda checked, file=sample_file: self.load_sample(file))
            self.sample_menu.addAction(action)
        
        # Adiciona uma ação para atualizar o menu
        self.sample_menu.addSeparator()
        refresh_action = QAction("Atualizar lista", self)
        refresh_action.triggered.connect(self.update_sample_menu)
        self.sample_menu.addAction(refresh_action)
    
    def open_sample(self):
        """Abre uma imagem de amostra do diretório de amostras - OBSOLETO"""
        # Este método foi substituído pelo submenu cascata
        # e está mantido apenas para compatibilidade
        self.update_sample_menu()
    
    def load_sample(self, sample_file):
        """
        Carrega uma imagem de amostra específica
        
        Args:
            sample_file (str): Nome do arquivo de amostra
        """
        # Caminho completo para a imagem de amostra
        samples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "samples")
        file_path = os.path.join(samples_dir, sample_file)
        
        if not os.path.exists(file_path):
            QMessageBox.warning(
                self,
                "Aviso",
                f"O arquivo '{sample_file}' não foi encontrado."
            )
            return
        
        try:
            # Abrir a imagem usando Pillow
            image = Image.open(file_path)
            
            # Guardar a imagem original e o caminho
            self.current_image = image
            self.current_image_path = file_path
            
            # Adicionar ao histórico
            self.history_manager.clear()  # Limpa o histórico anterior
            self.history_manager.add_item(image, f"Original: {sample_file}")
            
            # Redefine o zoom ao abrir uma nova imagem
            self.zoom_factor = 1.0
            
            # Atualizar o título da janela
            self.update_window_title()
            
            # Exibir a imagem
            self.update_display_image()
            
            # Informar ao usuário
            statusBar = self.statusBar()
            if statusBar:
                statusBar.showMessage(f"Imagem de amostra carregada: {sample_file}", 3000)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível abrir a imagem.\nErro: {str(e)}"
            )

    def apply_gamma(self):
        """Aplica a transformação gama na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Abre o diálogo de ajuste dos parâmetros da transformação gama
            dialog = GammaDialog(self)
            result = dialog.exec()
            
            # Verifica se o usuário cancelou a operação
            if result != QDialog.Accepted:
                return
            
            # Obtém os valores dos parâmetros
            gamma_value, c_value = dialog.get_values()
            
            # Aplica a transformação gama
            processed_image = power_transform(self.current_image, gamma_value, c_value)
            
            # Adiciona ao histórico
            self.history_manager.add_item(processed_image, f"Transformação Gama (γ={gamma_value}, c={c_value})")
            
            # Atualiza a imagem atual
            self.current_image = processed_image
            
            # Exibe a imagem processada
            self.update_display_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível processar a imagem.\nErro: {str(e)}"
            )
    
    def apply_contrast_stretching(self):
        """Aplica o alargamento de contraste na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Abre o diálogo de ajuste dos parâmetros do alargamento de contraste
            dialog = ContrastStretchingDialog(self)
            result = dialog.exec()
            
            # Verifica se o usuário cancelou a operação
            if result != QDialog.Accepted:
                return
            
            # Obtém os valores dos parâmetros
            params = dialog.get_parameters()
            r1, s1, r2, s2 = params["r1"], params["s1"], params["r2"], params["s2"]
            
            # Aplica o alargamento de contraste
            processed_image = contrast_stretching(self.current_image, r1, s1, r2, s2)
            
            # Adiciona ao histórico
            self.history_manager.add_item(
                processed_image, 
                f"Alargamento de Contraste (r1={r1}, s1={s1}, r2={r2}, s2={s2})"
            )
            
            # Atualiza a imagem atual
            self.current_image = processed_image
            
            # Exibe a imagem processada
            self.update_display_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível processar a imagem.\nErro: {str(e)}"
            )
    
    def apply_bit_plane_slicing(self):
        """Aplica o fatiamento por planos de bits na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Obtém uma cópia da imagem atual para processamento
            image_to_process = self.current_image.copy()
            
            # Tenta determinar a profundidade de bits e intensidade máxima da imagem
            try:
                bit_depth, max_intensity = get_image_bit_depth(image_to_process)
            except Exception as e:
                # Se falhar, usa valores padrão seguros
                import traceback
                print(f"Erro ao calcular profundidade de bits: {str(e)}")
                print(traceback.format_exc())
                bit_depth, max_intensity = 8, 255
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"Não foi possível determinar a profundidade de bits da imagem.\n"
                    f"Usando valores padrão (8 bits, 255 níveis de intensidade).\n"
                    f"Detalhes do erro: {str(e)}"
                )
            
            # Cria uma instância do diálogo com as informações da imagem
            dialog = BitPlaneDialog(self, bit_depth, max_intensity)
            
            # Conecta o sinal ao slot correspondente
            dialog.bit_plane_selected.connect(self.on_bit_plane_selected)
            
            # Exibe o diálogo (não modal para permitir visualização enquanto aberto)
            dialog.show()
            
        except ValueError as e:
            # Erro específico ao calcular valores inválidos
            QMessageBox.critical(
                self,
                "Erro de Validação",
                f"Não foi possível processar a imagem:\n{str(e)}"
            )
        except Exception as e:
            # Mensagem de erro mais detalhada
            import traceback
            error_details = traceback.format_exc()
            print(f"Erro no fatiamento por planos de bits: {str(e)}")
            print(error_details)
            
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível abrir o diálogo de fatiamento por planos de bits.\n"
                f"Erro: {str(e)}"
            )
    
    def on_bit_plane_selected(self, plane):
        """
        Processa a seleção de um plano de bits para visualização
        
        Args:
            plane (int): O plano de bits a ser visualizado
        """
        try:
            # Extrai o plano de bits selecionado
            bit_plane_image = extract_bit_plane(self.current_image, plane)
            
            # Adiciona ao histórico
            self.history_manager.add_item(
                bit_plane_image,
                f"Plano de Bits {plane} (peso {2**plane})"
            )
            
            # Atualiza a imagem atual
            self.current_image = bit_plane_image
            
            # Exibe a imagem processada
            self.update_display_image()
            
        except ValueError as e:
            # Erro específico de validação
            QMessageBox.warning(
                self,
                "Aviso",
                f"Não foi possível extrair o plano de bits:\n{str(e)}"
            )
        except Exception as e:
            # Erro genérico com mais detalhes
            import traceback
            error_details = traceback.format_exc()
            
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível extrair o plano de bits.\n"
                f"Erro: {str(e)}\n\n"
                f"Detalhes técnicos (para desenvolvimento):\n{error_details}"
            )

    def apply_histogram_equalization(self):
        """Aplica equalização de histograma na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Cria o diálogo de equalização
            dialog = HistogramDialog(self, self.current_image)
            
            # Se o usuário aceitar, aplica a equalização
            if dialog.exec() == QDialog.Accepted:
                # Obtém a imagem equalizada
                equalized_image = dialog.equalized_image
                
                if equalized_image:
                    # Adiciona ao histórico
                    self.history_manager.add_item(equalized_image, "Equalização de Histograma")
                    
                    # Atualiza a imagem atual
                    self.current_image = equalized_image
                    
                    # Exibe a imagem processada
                    self.update_display_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível equalizar o histograma.\nErro: {str(e)}"
            )
    
    def apply_pseudocolor(self):
        """Aplica fatiamento por intensidades para pseudocores na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Cria o diálogo de pseudocores
            dialog = PseudocolorDialog(self, self.current_image)
            
            # Se o usuário aceitar, aplica a transformação
            if dialog.exec() == QDialog.Accepted:
                # Obtém a imagem com pseudocores
                pseudocolor_image = dialog.result_image
                
                if pseudocolor_image:
                    # Adiciona ao histórico
                    self.history_manager.add_item(pseudocolor_image, "Fatiamento por Intensidades para Pseudocores")
                    
                    # Atualiza a imagem atual
                    self.current_image = pseudocolor_image
                    
                    # Exibe a imagem processada
                    self.update_display_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível aplicar o fatiamento por intensidades.\nErro: {str(e)}"
            )
    
    def apply_mean_filter(self):
        """Aplica o filtro de suavização da média na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Cria o diálogo para configuração do filtro
            dialog = MeanFilterDialog(self)
            
            # Se o usuário aceitar, aplica o filtro
            if dialog.exec() == QDialog.Accepted:
                # Obtém o tamanho do kernel selecionado
                kernel_size = dialog.get_kernel_size()
                
                # Aplica o filtro da média
                filtered_image = mean_filter(self.current_image, kernel_size)
                
                # Adiciona ao histórico
                self.history_manager.add_item(filtered_image, f"Filtro da Média {kernel_size}x{kernel_size}")
                
                # Atualiza a imagem atual
                self.current_image = filtered_image
                
                # Exibe a imagem processada
                self.update_display_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível aplicar o filtro da média.\nErro: {str(e)}"
            )
    
    def apply_order_statistics_filter(self):
        """Aplica filtros de estatísticas de ordem (máximo, mínimo, mediana) na imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para processar."
            )
            return
        
        try:
            # Cria o diálogo para configuração dos filtros
            dialog = OrderStatisticsDialog(self)
            
            # Se o usuário aceitar, aplica o filtro selecionado
            if dialog.exec() == QDialog.Accepted:
                # Obtém o tamanho do kernel e tipo de filtro selecionados
                kernel_size = dialog.get_kernel_size()
                filter_type = dialog.get_filter_type()
                
                # Aplica o filtro selecionado
                if filter_type == "max":
                    filtered_image = max_filter(self.current_image, kernel_size)
                    filter_name = "Máximo"
                elif filter_type == "min":
                    filtered_image = min_filter(self.current_image, kernel_size)
                    filter_name = "Mínimo"
                else:  # mediana
                    filtered_image = median_filter(self.current_image, kernel_size)
                    filter_name = "Mediana"
                
                # Adiciona ao histórico
                self.history_manager.add_item(filtered_image, f"Filtro de {filter_name} {kernel_size}x{kernel_size}")
                
                # Atualiza a imagem atual
                self.current_image = filtered_image
                
                # Exibe a imagem processada
                self.update_display_image()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível aplicar o filtro de estatística de ordem.\nErro: {str(e)}"
            )
    
    def show_histogram(self):
        """Exibe a janela de histograma da imagem atual"""
        if self.current_image is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Não há imagem para analisar."
            )
            return
        
        # Verifica se a janela já está aberta
        if self.histogram_window is not None and self.histogram_window.isVisible():
            # Traz a janela para frente
            self.histogram_window.raise_()
            self.histogram_window.activateWindow()
            return
        
        # Cria uma nova janela de histograma
        self.histogram_window = HistogramWindow(self, self.current_image)
        
        # Exibe a janela
        self.histogram_window.show() 