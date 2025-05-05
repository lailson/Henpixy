"""
Diálogo para configuração e visualização do filtro Laplaciano.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QFormLayout,
    QComboBox, QRadioButton, QButtonGroup,
    QCheckBox, QTabWidget, QWidget, QSpinBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap

from henpixy.gui.image_viewer import ImageViewer
from PIL import Image, ImageQt

class LaplacianDialog(QDialog):
    """
    Diálogo para configuração e visualização do filtro Laplaciano.
    
    Este diálogo permite ao usuário configurar os parâmetros do filtro Laplaciano
    e visualizar os três resultados solicitados:
    a) Resultado do laplaciano sem ajuste
    b) Resultado do laplaciano com ajuste
    c) Imagem original aguçada com a imagem laplaciana
    """
    
    def __init__(self, image, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Filtro Laplaciano")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Armazena a imagem original
        self.original_image = image
        
        # Bandeiras para controlar as configurações
        self.include_diagonals = True  # Por padrão, usa o kernel com diagonais
        self.sharpening_factor = 0.5   # Fator para o aguçamento
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Área de configuração
        config_group = QGroupBox("Configuração do Filtro")
        config_layout = QVBoxLayout(config_group)
        
        # Seleção do tipo de kernel
        kernel_group = QGroupBox("Tipo de Kernel")
        kernel_layout = QVBoxLayout(kernel_group)
        
        self.kernel_button_group = QButtonGroup(self)
        
        # Kernel com diagonais (8-conectividade)
        self.diag_radio = QRadioButton("Kernel com Diagonais (8-conectividade)")
        self.diag_radio.setChecked(True)  # Selecionado por padrão
        self.kernel_button_group.addButton(self.diag_radio)
        kernel_layout.addWidget(self.diag_radio)
        
        # Kernel sem diagonais (4-conectividade)
        self.no_diag_radio = QRadioButton("Kernel sem Diagonais (4-conectividade)")
        self.kernel_button_group.addButton(self.no_diag_radio)
        kernel_layout.addWidget(self.no_diag_radio)
        
        # Adiciona descrições dos kernels
        diag_kernel_desc = QLabel("""
        Kernel com Diagonais:
        [ 1,  1, 1]
        [ 1, -8, 1]
        [ 1,  1, 1]
        """)
        diag_kernel_desc.setFont(self.font())
        kernel_layout.addWidget(diag_kernel_desc)
        
        no_diag_kernel_desc = QLabel("""
        Kernel sem Diagonais:
        [ 0,  1, 0]
        [ 1, -4, 1]
        [ 0,  1, 0]
        """)
        no_diag_kernel_desc.setFont(self.font())
        kernel_layout.addWidget(no_diag_kernel_desc)
        
        config_layout.addWidget(kernel_group)
        
        # Controle do fator de aguçamento
        sharp_form = QFormLayout()
        self.sharp_factor = QDoubleSpinBox()
        self.sharp_factor.setRange(0.1, 2.0)
        self.sharp_factor.setSingleStep(0.1)
        self.sharp_factor.setValue(0.5)
        self.sharp_factor.setDecimals(1)
        sharp_form.addRow("Fator de Aguçamento:", self.sharp_factor)
        
        config_layout.addLayout(sharp_form)
        
        # Adiciona o grupo de configuração ao layout principal
        main_layout.addWidget(config_group)
        
        # Área de visualização com abas para os três resultados
        self.tab_widget = QTabWidget()
        
        # Aba para o resultado do Laplaciano sem ajuste
        self.tab_no_adjust = QWidget()
        no_adjust_layout = QVBoxLayout(self.tab_no_adjust)
        self.no_adjust_viewer = ImageViewer()
        no_adjust_layout.addWidget(self.no_adjust_viewer)
        self.tab_widget.addTab(self.tab_no_adjust, "Laplaciano Sem Ajuste")
        
        # Aba para o resultado do Laplaciano com ajuste
        self.tab_adjusted = QWidget()
        adjusted_layout = QVBoxLayout(self.tab_adjusted)
        self.adjusted_viewer = ImageViewer()
        adjusted_layout.addWidget(self.adjusted_viewer)
        self.tab_widget.addTab(self.tab_adjusted, "Laplaciano Com Ajuste")
        
        # Aba para a imagem aguçada
        self.tab_sharpened = QWidget()
        sharpened_layout = QVBoxLayout(self.tab_sharpened)
        self.sharpened_viewer = ImageViewer()
        sharpened_layout.addWidget(self.sharpened_viewer)
        self.tab_widget.addTab(self.tab_sharpened, "Imagem Aguçada")
        
        # Adiciona informação sobre cada aba
        info_label = QLabel("""
        <h3>Visualizações do Filtro Laplaciano</h3>
        <p><b>Laplaciano Sem Ajuste:</b> Mostra o resultado direto do operador Laplaciano. 
        Valores negativos são truncados para 0, resultando em uma imagem principalmente escura 
        com bordas brancas.</p>
        
        <p><b>Laplaciano Com Ajuste:</b> Adiciona 128 ao resultado do Laplaciano para melhor 
        visualização. Bordas positivas aparecem como brancas, bordas negativas como pretas, 
        e regiões sem bordas como cinza médio.</p>
        
        <p><b>Imagem Aguçada:</b> Combina a imagem original com o resultado do Laplaciano 
        para aguçar detalhes e bordas. A fórmula utilizada é: Original - (Fator * Laplaciano).</p>
        """)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        main_layout.addWidget(info_label)
        
        # Adiciona o widget de abas ao layout principal
        main_layout.addWidget(self.tab_widget)
        
        # Botões de OK e Cancelar
        button_layout = QHBoxLayout()
        self.preview_button = QPushButton("Pré-visualizar")
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancelar")
        
        self.preview_button.clicked.connect(self.preview_filter)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)
        
        # Conecta sinais para atualização automática quando as configurações mudarem
        self.diag_radio.toggled.connect(self.update_include_diagonals)
        self.sharp_factor.valueChanged.connect(self.update_sharpening_factor)
        
        # Faz a pré-visualização inicial
        self.preview_filter()
    
    def update_include_diagonals(self, checked):
        """Atualiza a configuração de incluir diagonais."""
        self.include_diagonals = checked
    
    def update_sharpening_factor(self, value):
        """Atualiza o fator de aguçamento."""
        self.sharpening_factor = value
    
    def preview_filter(self):
        """
        Atualiza a pré-visualização dos três resultados do filtro Laplaciano.
        """
        from henpixy.tools.spatial_filtering import laplacian_filter
        
        # Obtém os parâmetros atuais
        include_diagonals = self.include_diagonals
        sharpening_factor = self.sharpening_factor
        
        # Aplica o filtro Laplaciano sem ajuste
        no_adjust_image = laplacian_filter(
            self.original_image, 
            include_diagonals=include_diagonals,
            apply_adjustment=False,
            sharpen_image=False
        )
        
        # Aplica o filtro Laplaciano com ajuste
        adjusted_image = laplacian_filter(
            self.original_image, 
            include_diagonals=include_diagonals,
            apply_adjustment=True,
            sharpen_image=False
        )
        
        # Aplica o aguçamento (imagem original + laplaciano)
        sharpened_image = laplacian_filter(
            self.original_image, 
            include_diagonals=include_diagonals,
            apply_adjustment=False,
            sharpen_image=True
        )
        
        # Atualiza os visualizadores de imagem
        self.no_adjust_viewer.set_image(no_adjust_image)
        self.adjusted_viewer.set_image(adjusted_image)
        self.sharpened_viewer.set_image(sharpened_image)
    
    def get_parameters(self):
        """
        Retorna os parâmetros configurados para o filtro Laplaciano.
        
        Returns:
            dict: Dicionário com os parâmetros do filtro
        """
        return {
            'include_diagonals': self.include_diagonals,
            'sharpening_factor': self.sharpening_factor
        } 