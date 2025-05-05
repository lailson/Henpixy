"""
Diálogo para visualização e manipulação de planos de bits
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QDialogButtonBox, QGroupBox, QRadioButton, QPushButton,
    QButtonGroup, QScrollArea, QWidget, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal

class BitPlaneDialog(QDialog):
    """
    Diálogo para fatiamento e reconstrução por planos de bits
    
    Permite ao usuário:
    - Visualizar um plano de bits específico
    - Reconstruir a imagem selecionando quais planos incluir
    """
    
    # Sinal emitido quando um plano de bits é selecionado para visualização
    bit_plane_selected = Signal(int)
    
    # Sinal emitido quando planos de bits são selecionados para reconstrução
    reconstruction_selected = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Fatiamento por Planos de Bits")
        self.resize(550, 400)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        
        # Informações sobre planos de bits
        self.info_label = QLabel(
            "Uma imagem com 8 bits (256 níveis de intensidade) pode ser decomposta "
            "em 8 planos de bits. Cada plano representa o estado (0 ou 1) de um bit "
            "específico em cada pixel da imagem."
        )
        self.info_label.setWordWrap(True)
        self.main_layout.addWidget(self.info_label)
        
        # Seção para escolher o modo de visualização
        self.mode_group = QButtonGroup(self)
        self.mode_layout = QHBoxLayout()
        
        # Opção para visualizar plano único
        self.view_plane_radio = QRadioButton("Visualizar plano de bits")
        self.view_plane_radio.setChecked(True)
        self.mode_group.addButton(self.view_plane_radio)
        self.mode_layout.addWidget(self.view_plane_radio)
        
        # Opção para reconstruir a partir de planos selecionados
        self.reconstruct_radio = QRadioButton("Reconstruir imagem a partir de planos selecionados")
        self.mode_group.addButton(self.reconstruct_radio)
        self.mode_layout.addWidget(self.reconstruct_radio)
        
        self.main_layout.addLayout(self.mode_layout)
        
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
        
        # Adicionar botões de radio e de checagem para cada plano de bits
        for i in range(8):
            # Calcular o peso/contribuição do plano (2^i)
            weight = 2 ** i
            intensity_range = f"[{0 if i == 0 else 2**(i-1)}, {2**i - 1}]"
            
            # Radio button para visualização de plano único
            radio = QRadioButton(f"Plano {i}: Peso {weight}, Intensidade {intensity_range}")
            self.plane_radios.append(radio)
            self.bit_plane_group.addButton(radio, i)
            
            # Checkbox para reconstrução
            checkbox = QCheckBox()
            checkbox.setChecked(True)  # Por padrão, todos os planos estão selecionados
            
            # Adiciona ao layout
            self.planes_layout.addWidget(radio, i, 0)
            self.planes_layout.addWidget(checkbox, i, 1)
        
        # Adiciona a descrição de colunas
        self.planes_layout.addWidget(QLabel("Plano de Bits"), 0, 0)
        self.planes_layout.addWidget(QLabel("Incluir na Reconstrução"), 0, 1)
        
        # Seleciona o plano mais significativo por padrão
        self.plane_radios[7].setChecked(True)
        
        self.scroll_layout.addWidget(self.planes_group)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)
        
        # Botões de ação
        self.button_layout = QHBoxLayout()
        
        # Botão para visualizar o plano selecionado
        self.view_button = QPushButton("Visualizar")
        self.view_button.clicked.connect(self.on_view_clicked)
        self.button_layout.addWidget(self.view_button)
        
        # Botão para reconstruir a partir dos planos selecionados
        self.reconstruct_button = QPushButton("Reconstruir")
        self.reconstruct_button.clicked.connect(self.on_reconstruct_clicked)
        self.button_layout.addWidget(self.reconstruct_button)
        
        # Botão para fechar o diálogo
        self.close_button = QPushButton("Fechar")
        self.close_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.close_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # Conecta os botões de rádio do modo para atualizar a UI
        self.view_plane_radio.toggled.connect(self.update_ui)
        self.reconstruct_radio.toggled.connect(self.update_ui)
        
        # Inicializa a UI
        self.update_ui()
    
    def update_ui(self):
        """Atualiza a interface baseada no modo selecionado"""
        view_mode = self.view_plane_radio.isChecked()
        
        # Atualiza os botões
        self.view_button.setEnabled(view_mode)
        self.reconstruct_button.setEnabled(not view_mode)
        
        # Atualiza o texto dos botões
        if view_mode:
            self.view_button.setText("Visualizar")
            self.reconstruct_button.setText("Reconstruir")
        else:
            self.view_button.setText("Visualizar")
            self.reconstruct_button.setText("Reconstruir")
    
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
    
    def on_reconstruct_clicked(self):
        """Ação quando o botão de reconstruir é clicado"""
        # Obtém os planos selecionados para reconstrução
        selected_planes = []
        
        for i, radio in enumerate(self.plane_radios):
            # Para cada plano, verifica se o checkbox está marcado
            checkbox = self.planes_layout.itemAtPosition(i+1, 1).widget()
            if checkbox.isChecked():
                selected_planes.append(i)
        
        if selected_planes:
            # Emite o sinal com os planos selecionados
            self.reconstruction_selected.emit(selected_planes)
        else:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecione pelo menos um plano de bits para reconstrução."
            )
    
    def get_selected_plane(self):
        """Retorna o plano de bits selecionado para visualização"""
        return self.bit_plane_group.checkedId()
    
    def get_selected_planes_for_reconstruction(self):
        """Retorna a lista de planos selecionados para reconstrução"""
        selected_planes = []
        
        for i, radio in enumerate(self.plane_radios):
            # Para cada plano, verifica se o checkbox está marcado
            checkbox = self.planes_layout.itemAtPosition(i+1, 1).widget()
            if checkbox.isChecked():
                selected_planes.append(i)
        
        return selected_planes 