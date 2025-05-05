"""
Diálogo para aplicação de pseudocores usando fatiamento por intensidades
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QTabWidget,
    QScrollArea, QWidget, QSizePolicy, QGridLayout,
    QComboBox, QSpinBox, QSlider, QFrame, QColorDialog,
    QListWidget, QListWidgetItem
)
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtCore import Qt, Signal

import numpy as np
from PIL import Image
import io

from henpixy.tools.pseudocolor import (
    intensity_slicing, create_predefined_maps, 
    create_color_gradient, apply_custom_transformation,
    create_custom_transformation_functions
)

class ColorButton(QPushButton):
    """Botão personalizado para seleção de cores"""
    
    def __init__(self, color=None, parent=None):
        super().__init__(parent)
        self.setMinimumSize(30, 30)
        self.setMaximumSize(30, 30)
        self.color = QColor(255, 0, 0) if color is None else QColor(*color)
        self.setStyleSheet(f"background-color: {self.color.name()}")
        self.clicked.connect(self.choose_color)
    
    def choose_color(self):
        """Abre um diálogo para escolher uma cor"""
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.setStyleSheet(f"background-color: {self.color.name()}")
    
    def get_color(self):
        """Retorna a cor atual como uma tupla RGB"""
        return (self.color.red(), self.color.green(), self.color.blue())

class ColorSlider(QWidget):
    """Widget para definir um intervalo de intensidade e sua cor associada"""
    
    def __init__(self, index, min_val, max_val, color=(255, 0, 0), parent=None):
        super().__init__(parent)
        self.index = index
        self.layout = QHBoxLayout(self)
        
        # Label para o índice do intervalo
        self.label = QLabel(f"Intervalo {index + 1}:")
        self.layout.addWidget(self.label)
        
        # Spinner para o valor mínimo
        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 255)
        self.min_spin.setValue(min_val)
        self.layout.addWidget(self.min_spin)
        
        # Slider para o intervalo
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(min_val)
        self.layout.addWidget(self.slider)
        
        # Spinner para o valor máximo
        self.max_spin = QSpinBox()
        self.max_spin.setRange(0, 255)
        self.max_spin.setValue(max_val)
        self.layout.addWidget(self.max_spin)
        
        # Botão para seleção de cor
        self.color_button = ColorButton(color)
        self.layout.addWidget(self.color_button)
        
        # Conectando signals e slots
        self.min_spin.valueChanged.connect(self.update_slider_min)
        self.max_spin.valueChanged.connect(self.update_slider_max)
    
    def update_slider_min(self, value):
        """Atualiza o valor mínimo do slider"""
        self.slider.setMinimum(value)
    
    def update_slider_max(self, value):
        """Atualiza o valor máximo do slider"""
        self.slider.setMaximum(value)
    
    def get_range(self):
        """Retorna o intervalo de intensidade"""
        return self.min_spin.value(), self.max_spin.value()
    
    def get_color(self):
        """Retorna a cor associada ao intervalo"""
        return self.color_button.get_color()

class PseudocolorDialog(QDialog):
    """
    Diálogo para aplicação de pseudocores usando fatiamento por intensidades
    """
    
    # Sinal emitido quando uma transformação é selecionada
    transformation_selected = Signal(object)
    
    def __init__(self, parent=None, image=None):
        super().__init__(parent)
        
        self.setWindowTitle("Fatiamento por Intensidades para Pseudocores")
        self.resize(850, 600)
        
        # Permitir que a janela seja redimensionável
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Armazena a imagem original
        self.original_image = image
        self.result_image = None
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        
        # Criar tabs para organizar a visualização
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Tab de comparação visual
        self.create_comparison_tab()
        
        # Tab de mapas predefinidos
        self.create_predefined_tab()
        
        # Tab de intervalos customizados
        self.create_custom_tab()
        
        # Tab de transformações RGB
        self.create_rgb_tab()
        
        # Tab de informações teóricas
        self.create_info_tab()
        
        # Botões para fechar e aplicar
        self.button_layout = QHBoxLayout()
        
        self.apply_button = QPushButton("Aplicar")
        self.apply_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.apply_button)
        
        # Espaçador para alinhar os botões à direita
        self.button_layout.addStretch()
        
        self.close_button = QPushButton("Fechar")
        self.close_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.close_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # Carregar mapas predefinidos
        self.load_predefined_maps()
        
        # Inicializar a visualização com a imagem original
        if self.original_image is not None:
            self.update_displays()
    
    def create_comparison_tab(self):
        """Cria a tab para comparação visual entre imagem original e com pseudocores"""
        comparison_scroll = QScrollArea()
        comparison_scroll.setWidgetResizable(True)
        
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
        
        # Container para a imagem com pseudocores
        pseudo_group = QGroupBox("Imagem com Pseudocores")
        pseudo_layout = QVBoxLayout(pseudo_group)
        self.pseudo_label = QLabel()
        self.pseudo_label.setAlignment(Qt.AlignCenter)
        self.pseudo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pseudo_layout.addWidget(self.pseudo_label)
        comparison_layout.addWidget(pseudo_group)
        
        comparison_scroll.setWidget(comparison_content)
        self.tab_widget.addTab(comparison_scroll, "Comparação")
    
    def create_predefined_tab(self):
        """Cria a tab para seleção de mapas de cores predefinidos"""
        predefined_tab = QWidget()
        predefined_layout = QVBoxLayout(predefined_tab)
        
        # Selector de mapa predefinido
        map_group = QGroupBox("Mapas de Cores Predefinidos")
        map_layout = QVBoxLayout(map_group)
        
        self.map_combo = QComboBox()
        map_layout.addWidget(self.map_combo)
        
        # Descrição do mapa selecionado
        self.map_description = QLabel()
        self.map_description.setWordWrap(True)
        map_layout.addWidget(self.map_description)
        
        # Visualização do mapa de cores
        self.map_preview = QFrame()
        self.map_preview.setMinimumHeight(50)
        self.map_preview.setFrameShape(QFrame.Box)
        map_layout.addWidget(self.map_preview)
        
        # Botão para aplicar mapa
        apply_map_button = QPushButton("Aplicar Mapa")
        apply_map_button.clicked.connect(self.apply_predefined_map)
        map_layout.addWidget(apply_map_button)
        
        predefined_layout.addWidget(map_group)
        predefined_layout.addStretch()
        
        self.tab_widget.addTab(predefined_tab, "Mapas Predefinidos")
    
    def create_custom_tab(self):
        """Cria a tab para customização manual de intervalos e cores"""
        custom_tab = QScrollArea()
        custom_tab.setWidgetResizable(True)
        
        custom_content = QWidget()
        custom_layout = QVBoxLayout(custom_content)
        
        # Container para os controles de intervalos
        intervals_group = QGroupBox("Intervalos Personalizados")
        intervals_layout = QVBoxLayout(intervals_group)
        
        # Controles para adicionar/remover intervalos
        controls_layout = QHBoxLayout()
        
        # Spinner para o número de intervalos
        intervals_layout.addWidget(QLabel("Número de intervalos:"))
        self.interval_count = QSpinBox()
        self.interval_count.setRange(1, 10)
        self.interval_count.setValue(3)
        self.interval_count.valueChanged.connect(self.update_interval_widgets)
        intervals_layout.addWidget(self.interval_count)
        
        # Botão para distribuir uniformemente
        distribute_button = QPushButton("Distribuir Uniformemente")
        distribute_button.clicked.connect(self.distribute_intervals)
        intervals_layout.addWidget(distribute_button)
        
        # Botão para gerar cores automaticamente
        auto_colors_button = QPushButton("Gerar Cores")
        auto_colors_button.clicked.connect(self.generate_auto_colors)
        intervals_layout.addWidget(auto_colors_button)
        
        intervals_layout.addLayout(controls_layout)
        
        # Container para os sliders de intervalo
        self.intervals_container = QWidget()
        self.intervals_layout = QVBoxLayout(self.intervals_container)
        intervals_layout.addWidget(self.intervals_container)
        
        # Botão para aplicar intervalos customizados
        apply_custom_button = QPushButton("Aplicar Intervalos")
        apply_custom_button.clicked.connect(self.apply_custom_intervals)
        intervals_layout.addWidget(apply_custom_button)
        
        custom_layout.addWidget(intervals_group)
        custom_tab.setWidget(custom_content)
        
        self.tab_widget.addTab(custom_tab, "Intervalos Personalizados")
        
        # Inicializar os widgets de intervalo
        self.interval_widgets = []
        self.update_interval_widgets(self.interval_count.value())
    
    def create_rgb_tab(self):
        """Cria a tab para transformações RGB personalizadas"""
        rgb_tab = QScrollArea()
        rgb_tab.setWidgetResizable(True)
        
        rgb_content = QWidget()
        rgb_layout = QVBoxLayout(rgb_content)
        
        # Container para transformações predefinidas
        transform_group = QGroupBox("Transformações RGB Predefinidas")
        transform_layout = QVBoxLayout(transform_group)
        
        # Combobox para seleção de transformação
        self.transform_combo = QComboBox()
        transform_layout.addWidget(self.transform_combo)
        
        # Descrição da transformação
        self.transform_description = QLabel()
        self.transform_description.setWordWrap(True)
        transform_layout.addWidget(self.transform_description)
        
        # Botão para aplicar transformação
        apply_transform_button = QPushButton("Aplicar Transformação")
        apply_transform_button.clicked.connect(self.apply_rgb_transformation)
        transform_layout.addWidget(apply_transform_button)
        
        rgb_layout.addWidget(transform_group)
        
        # Aqui poderíamos adicionar mais controles para personalização
        # de funções RGB, mas isso seria uma expansão futura
        
        rgb_layout.addStretch()
        rgb_tab.setWidget(rgb_content)
        
        self.tab_widget.addTab(rgb_tab, "Transformações RGB")
        
        # Carregar transformações predefinidas
        self.load_transformations()
    
    def create_info_tab(self):
        """Cria a tab com informações teóricas sobre fatiamento por intensidades"""
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        info_layout.addWidget(scroll_area)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Adicionar texto informativo
        info_text = """
        <h2>Fatiamento por Intensidades para Pseudocores</h2>
        
        <p>O fatiamento por intensidades é uma técnica de processamento digital de imagens que 
        consiste em atribuir cores a valores ou faixas de intensidade de cinza com base em 
        determinados critérios.</p>
        
        <p>O termo <i>pseudo</i> diferencia o processo de atribuir cores a imagens monocromáticas, 
        distinguindo-as das imagens adquiridas com sensores de cores reais (como câmeras digitais).</p>
        
        <h3>Motivação</h3>
        <p>O olho humano consegue distinguir apenas algumas dezenas de níveis de cinza, enquanto 
        pode diferenciar milhares de cores diferentes. O uso de pseudocores melhora significativamente 
        a interpretação e visualização de características que seriam difíceis de perceber em 
        imagens em escala de cinza.</p>
        
        <h3>Princípio do Fatiamento por Intensidades</h3>
        <p>A ideia fundamental é dividir o intervalo de intensidades de cinza (tipicamente 0-255 para 
        imagens de 8 bits) em faixas menores, e atribuir uma cor específica a cada faixa.</p>
        
        <p>Matematicamente, podemos ver o fatiamento como a criação de planos paralelos que intersectam 
        a função de intensidade da imagem (vista como uma superfície 3D), atribuindo cores diferentes 
        às regiões acima e abaixo de cada plano.</p>
        
        <h3>Aplicações</h3>
        <ul>
            <li><b>Imagens Médicas:</b> Realce de estruturas específicas em radiografias, tomografias, etc.</li>
            <li><b>Sensoriamento Remoto:</b> Visualização de dados de satélite, mapas de temperatura, etc.</li>
            <li><b>Imagens Técnicas:</b> Análise de defeitos em soldas, rachaduras em estruturas.</li>
            <li><b>Imagens Científicas:</b> Visualização de densidade em microscopia, padrões de difração, etc.</li>
        </ul>
        
        <h3>Abordagens para Pseudocolorização</h3>
        
        <h4>1. Fatiamento por Intensidades</h4>
        <p>Divide o intervalo de intensidades em faixas e atribui uma cor específica a cada faixa.</p>
        
        <h4>2. Transformações RGB Independentes</h4>
        <p>Aplica três funções de transformação diferentes (uma para cada canal R, G e B) 
        à imagem original em escala de cinza. Esta abordagem produz uma imagem colorida onde 
        o conteúdo de cor é modulado pela natureza de cada função de transformação.</p>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        
        scroll_layout.addWidget(info_label)
        scroll_area.setWidget(scroll_content)
        
        self.tab_widget.addTab(info_tab, "Informações")
    
    def load_predefined_maps(self):
        """Carrega os mapas de cores predefinidos no combobox"""
        self.predefined_maps = create_predefined_maps()
        self.map_combo.clear()
        
        for map_name in self.predefined_maps.keys():
            self.map_combo.addItem(map_name)
        
        self.map_combo.currentIndexChanged.connect(self.update_map_preview)
        
        # Atualiza o preview com o mapa inicial
        if self.map_combo.count() > 0:
            self.update_map_preview(0)
    
    def update_map_preview(self, index):
        """Atualiza a visualização do mapa de cores selecionado"""
        if index < 0 or self.map_combo.count() == 0:
            return
        
        map_name = self.map_combo.currentText()
        map_info = self.predefined_maps.get(map_name)
        
        if map_info:
            # Atualiza a descrição
            slices = map_info["slices"]
            colors = map_info["colors"]
            
            description = f"Mapa '{map_name}': Divide a imagem em {len(slices) + 1} faixas.\n"
            description += f"Fatias em: {', '.join(str(s) for s in slices)}"
            
            self.map_description.setText(description)
            
            # Cria um gradiente para visualizar o mapa
            gradient_style = "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            
            # Adiciona os pontos de cor
            stops = []
            
            # Primeira cor (no início)
            stops.append(f"stop:0 rgb{str(colors[0])}")
            
            # Cores intermediárias
            for i, slice_val in enumerate(slices):
                # Posição normalizada no gradiente
                pos = slice_val / 255.0
                # Adiciona a cor anterior até o ponto de corte
                stops.append(f"stop:{pos} rgb{str(colors[i])}")
                # Adiciona a próxima cor logo após o ponto de corte
                stops.append(f"stop:{pos + 0.001} rgb{str(colors[i + 1])}")
            
            # Última cor (no final)
            stops.append(f"stop:1 rgb{str(colors[-1])}")
            
            gradient_style += ", ".join(stops) + ");"
            
            # Aplica o estilo ao quadro de visualização
            self.map_preview.setStyleSheet(gradient_style)
    
    def update_interval_widgets(self, count):
        """Atualiza os widgets de intervalo baseado no número selecionado"""
        # Limpa o layout atual
        for widget in self.interval_widgets:
            widget.setParent(None)
        
        self.interval_widgets = []
        
        # Cria novos widgets de intervalo
        for i in range(count):
            # Define os valores min/max baseado na distribuição uniforme
            min_val = int(i * (256 / count))
            max_val = int((i + 1) * (256 / count)) - 1 if i < count - 1 else 255
            
            # Cria o widget de intervalo
            interval_widget = ColorSlider(i, min_val, max_val)
            self.intervals_layout.addWidget(interval_widget)
            self.interval_widgets.append(interval_widget)
    
    def distribute_intervals(self):
        """Distribui os intervalos uniformemente"""
        count = len(self.interval_widgets)
        if count == 0:
            return
        
        # Calcula a largura de cada intervalo
        interval_width = 256 // count
        
        # Atualiza os valores de cada widget
        for i, widget in enumerate(self.interval_widgets):
            min_val = i * interval_width
            max_val = (i + 1) * interval_width - 1 if i < count - 1 else 255
            
            widget.min_spin.setValue(min_val)
            widget.max_spin.setValue(max_val)
    
    def generate_auto_colors(self):
        """Gera cores automaticamente para os intervalos"""
        count = len(self.interval_widgets)
        if count == 0:
            return
        
        # Gera um gradiente de cores
        colors = create_color_gradient(count)
        
        # Aplica as cores aos widgets
        for i, widget in enumerate(self.interval_widgets):
            widget.color_button.color = QColor(*colors[i])
            widget.color_button.setStyleSheet(f"background-color: {widget.color_button.color.name()}")
    
    def load_transformations(self):
        """Carrega as transformações RGB predefinidas"""
        self.transformations = create_custom_transformation_functions()
        self.transform_combo.clear()
        
        for transform_name in self.transformations.keys():
            self.transform_combo.addItem(transform_name)
        
        self.transform_combo.currentIndexChanged.connect(self.update_transform_description)
        
        # Atualiza a descrição da transformação inicial
        if self.transform_combo.count() > 0:
            self.update_transform_description(0)
    
    def update_transform_description(self, index):
        """Atualiza a descrição da transformação selecionada"""
        if index < 0 or self.transform_combo.count() == 0:
            return
        
        transform_name = self.transform_combo.currentText()
        
        descriptions = {
            "HotIron": "Transformação que começa com preto, passa por vermelho, laranja e termina em amarelo.\nÚtil para visualização de temperatura ou intensidade.",
            "Espectro": "Transformação que atribui cores primárias a diferentes faixas de intensidade.\nCria um efeito de alto contraste entre regiões.",
            "Senoidal": "Transformação que utiliza funções senoidais para criar um padrão cíclico de cores.\nProduz transições suaves entre cores complementares.",
            "RGB Linear": "Combinação de transformações lineares e não-lineares nos diferentes canais.\nCria um efeito visual com bom contraste e variação de cores."
        }
        
        description = descriptions.get(transform_name, "Sem descrição disponível.")
        self.transform_description.setText(description)
    
    def apply_predefined_map(self):
        """Aplica o mapa de cores predefinido selecionado"""
        if self.original_image is None:
            return
        
        map_name = self.map_combo.currentText()
        map_info = self.predefined_maps.get(map_name)
        
        if map_info:
            slices = map_info["slices"]
            colors = map_info["colors"]
            
            # Aplica o fatiamento por intensidades
            self.result_image = intensity_slicing(self.original_image, slices, colors)
            
            # Atualiza a exibição
            self.update_displays()
    
    def apply_custom_intervals(self):
        """Aplica o fatiamento por intensidades com os intervalos personalizados"""
        if self.original_image is None or len(self.interval_widgets) == 0:
            return
        
        # Extrai os limites dos intervalos
        slices = []
        colors = []
        
        # Ordena os widgets por valor mínimo
        sorted_widgets = sorted(self.interval_widgets, key=lambda w: w.min_spin.value())
        
        # Primeira cor (para valores menores que o primeiro limite)
        colors.append(sorted_widgets[0].get_color())
        
        # Extrai os limites e cores
        for widget in sorted_widgets:
            min_val, max_val = widget.get_range()
            slices.append(min_val)
            colors.append(widget.get_color())
        
        # Remove valores duplicados ou inválidos
        slices = sorted(list(set(slices)))
        if len(slices) == 0:
            return
        
        # Ajusta o número de cores se necessário
        while len(colors) < len(slices) + 1:
            colors.append((255, 255, 255))  # Adiciona branco para fatias indefinidas
        
        # Trunca cores extras
        colors = colors[:len(slices) + 1]
        
        # Aplica o fatiamento por intensidades
        self.result_image = intensity_slicing(self.original_image, slices, colors)
        
        # Atualiza a exibição
        self.update_displays()
    
    def apply_rgb_transformation(self):
        """Aplica a transformação RGB selecionada"""
        if self.original_image is None:
            return
        
        transform_name = self.transform_combo.currentText()
        transform_info = self.transformations.get(transform_name)
        
        if transform_info:
            red_func = transform_info["red"]
            green_func = transform_info["green"]
            blue_func = transform_info["blue"]
            
            # Aplica a transformação RGB
            self.result_image = apply_custom_transformation(
                self.original_image, red_func, green_func, blue_func
            )
            
            # Atualiza a exibição
            self.update_displays()
    
    def update_displays(self):
        """Atualiza a exibição das imagens"""
        if self.original_image is None:
            return
        
        # Exibe a imagem original
        original_pixmap = self.pil_to_pixmap(self.original_image)
        if original_pixmap:
            # Redimensiona para caber no label
            scaled_original = original_pixmap.scaled(
                self.original_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.original_label.setPixmap(scaled_original)
        
        # Exibe a imagem com pseudocores (se disponível)
        if self.result_image is not None:
            pseudo_pixmap = self.pil_to_pixmap(self.result_image)
            if pseudo_pixmap:
                # Redimensiona para caber no label
                scaled_pseudo = pseudo_pixmap.scaled(
                    self.pseudo_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.pseudo_label.setPixmap(scaled_pseudo)
    
    def pil_to_pixmap(self, pil_image):
        """Converte uma imagem PIL para QPixmap"""
        if pil_image.mode == "L":
            # Imagem em escala de cinza
            q_image = QImage(
                pil_image.tobytes(), 
                pil_image.width, 
                pil_image.height, 
                pil_image.width, 
                QImage.Format_Grayscale8
            )
        elif pil_image.mode == "RGB":
            # Imagem RGB
            q_image = QImage(
                pil_image.tobytes(), 
                pil_image.width, 
                pil_image.height, 
                pil_image.width * 3, 
                QImage.Format_RGB888
            )
        else:
            # Converte para RGB para outros modos
            pil_image = pil_image.convert("RGB")
            q_image = QImage(
                pil_image.tobytes(), 
                pil_image.width, 
                pil_image.height, 
                pil_image.width * 3, 
                QImage.Format_RGB888
            )
        
        return QPixmap.fromImage(q_image)
    
    def resizeEvent(self, event):
        """Redimensiona as imagens quando a janela é redimensionada"""
        super().resizeEvent(event)
        self.update_displays()
    
    def set_image(self, image):
        """Define a imagem a ser processada"""
        self.original_image = image
        self.result_image = None
        self.update_displays() 