"""
Diálogo para visualização e manipulação de planos de bits
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QRadioButton, QPushButton,
    QButtonGroup, QScrollArea, QWidget, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal

class BitPlaneDialog(QDialog):
    """
    Diálogo para fatiamento por planos de bits
    
    Permite ao usuário visualizar um plano de bits específico
    """
    
    # Sinal emitido quando um plano de bits é selecionado para visualização
    bit_plane_selected = Signal(int)
    
    def __init__(self, parent=None, bit_depth=8, max_intensity=255):
        super().__init__(parent)
        
        self.setWindowTitle("Fatiamento por Planos de Bits")
        self.resize(550, 400)
        
        # Armazena a profundidade de bits e intensidade máxima
        self.bit_depth = bit_depth
        self.max_intensity = max_intensity
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        
        # Informações sobre a imagem e planos de bits
        self.info_layout = QVBoxLayout()
        
        self.intensity_label = QLabel(
            f"<b>Intensidade máxima detectada:</b> {self.max_intensity}"
        )
        self.info_layout.addWidget(self.intensity_label)
        
        self.bit_depth_label = QLabel(
            f"<b>Profundidade de bits (quantidade de planos):</b> {self.bit_depth}"
        )
        self.info_layout.addWidget(self.bit_depth_label)
        
        self.info_label = QLabel(
            f"Uma imagem com {self.bit_depth} bits ({self.max_intensity+1} níveis de intensidade) "
            f"pode ser decomposta em {self.bit_depth} planos de bits. Cada plano representa "
            "o estado (0 ou 1) de um bit específico em cada pixel da imagem."
        )
        self.info_label.setWordWrap(True)
        self.info_layout.addWidget(self.info_label)
        
        self.main_layout.addLayout(self.info_layout)
        
        # Criar área de rolagem para os planos de bits
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        
        # Grupo para seleção de plano de bits
        self.planes_group = QGroupBox("Planos de Bits")
        self.planes_layout = QGridLayout(self.planes_group)
        
        # Criar botões de rádio para cada plano de bits para visualização
        self.plane_radios = []
        self.bit_plane_group = QButtonGroup(self)
        
        # Adicionar cabeçalho ao layout
        self.planes_layout.addWidget(QLabel("<b>Plano de Bits</b>"), 0, 0)
        self.planes_layout.addWidget(QLabel("<b>Peso (Contribuição)</b>"), 0, 1)
        self.planes_layout.addWidget(QLabel("<b>Intervalo de Intensidade</b>"), 0, 2)
        
        # Adicionar botões de rádio para cada plano de bits
        for i in range(self.bit_depth):
            # Calcular o peso/contribuição do plano (2^i)
            weight = 2 ** i
            intensity_range = f"[{0 if i == 0 else 2**(i-1)}, {2**i - 1}]"
            
            # Rótulo do plano (plano 0, plano 1, ...)
            plane_label = QLabel(f"Plano {i}")
            
            # Rótulo do peso (1, 2, 4, 8, ...)
            weight_label = QLabel(f"{weight}")
            
            # Rótulo do intervalo de intensidade
            range_label = QLabel(intensity_range)
            
            # Radio button para seleção
            radio = QRadioButton("")
            self.plane_radios.append(radio)
            self.bit_plane_group.addButton(radio, i)
            
            # Adiciona ao layout
            row = i + 1  # +1 por causa do cabeçalho
            self.planes_layout.addWidget(radio, row, 0)
            self.planes_layout.addWidget(weight_label, row, 1)
            self.planes_layout.addWidget(range_label, row, 2)
        
        # Seleciona o plano mais significativo por padrão
        if self.bit_depth > 0:
            self.plane_radios[self.bit_depth - 1].setChecked(True)
        
        self.scroll_layout.addWidget(self.planes_group)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)
        
        # Botões de ação
        self.button_layout = QHBoxLayout()
        
        # Botão para visualizar o plano selecionado
        self.view_button = QPushButton("Visualizar")
        self.view_button.clicked.connect(self.on_view_clicked)
        self.button_layout.addWidget(self.view_button)
        
        # Botão para fechar o diálogo
        self.close_button = QPushButton("Fechar")
        self.close_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.close_button)
        
        self.main_layout.addLayout(self.button_layout)
    
    def on_view_clicked(self):
        """Ação quando o botão de visualizar é clicado"""
        # Obtém o plano selecionado
        selected_plane = self.bit_plane_group.checkedId()
        
        if selected_plane >= 0:
            # Emite o sinal com o plano selecionado
            self.bit_plane_selected.emit(selected_plane)
        else:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecione um plano de bits para visualizar."
            )
    
    def get_selected_plane(self):
        """Retorna o plano de bits selecionado para visualização"""
        return self.bit_plane_group.checkedId()
    
    def update_image_info(self, bit_depth, max_intensity):
        """Atualiza as informações da imagem e recria os controles de planos de bits"""
        self.bit_depth = bit_depth
        self.max_intensity = max_intensity
        
        # Atualiza os rótulos de informação
        self.intensity_label.setText(f"<b>Intensidade máxima detectada:</b> {self.max_intensity}")
        self.bit_depth_label.setText(f"<b>Profundidade de bits (quantidade de planos):</b> {self.bit_depth}")
        self.info_label.setText(
            f"Uma imagem com {self.bit_depth} bits ({self.max_intensity+1} níveis de intensidade) "
            f"pode ser decomposta em {self.bit_depth} planos de bits. Cada plano representa "
            "o estado (0 ou 1) de um bit específico em cada pixel da imagem."
        )
        
        # Limpa os controles existentes
        for radio in self.plane_radios:
            self.bit_plane_group.removeButton(radio)
        
        # Limpa o layout de planos
        while self.planes_layout.count():
            item = self.planes_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Reinicializa a lista de rádios
        self.plane_radios = []
        
        # Adicionar cabeçalho ao layout
        self.planes_layout.addWidget(QLabel("<b>Plano de Bits</b>"), 0, 0)
        self.planes_layout.addWidget(QLabel("<b>Peso (Contribuição)</b>"), 0, 1)
        self.planes_layout.addWidget(QLabel("<b>Intervalo de Intensidade</b>"), 0, 2)
        
        # Recria os controles para cada plano
        for i in range(self.bit_depth):
            # Calcular o peso/contribuição do plano (2^i)
            weight = 2 ** i
            intensity_range = f"[{0 if i == 0 else 2**(i-1)}, {2**i - 1}]"
            
            # Rótulo do plano
            plane_label = QLabel(f"Plano {i}")
            
            # Rótulo do peso
            weight_label = QLabel(f"{weight}")
            
            # Rótulo do intervalo de intensidade
            range_label = QLabel(intensity_range)
            
            # Radio button para seleção
            radio = QRadioButton("")
            self.plane_radios.append(radio)
            self.bit_plane_group.addButton(radio, i)
            
            # Adiciona ao layout
            row = i + 1  # +1 por causa do cabeçalho
            self.planes_layout.addWidget(radio, row, 0)
            self.planes_layout.addWidget(weight_label, row, 1)
            self.planes_layout.addWidget(range_label, row, 2)
        
        # Seleciona o plano mais significativo por padrão
        if self.bit_depth > 0:
            self.plane_radios[self.bit_depth - 1].setChecked(True) 