"""
Diálogo para configuração do filtro de suavização da média.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QSpinBox, QFormLayout,
    QComboBox
)
from PySide6.QtCore import Qt

class MeanFilterDialog(QDialog):
    """
    Diálogo para configuração do filtro de suavização da média.
    Permite ao usuário escolher o tamanho do kernel (vizinhança).
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Filtro de Suavização da Média")
        self.setMinimumWidth(300)
        
        # Valor inicial para o tamanho do kernel
        self.kernel_size = 3
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Adiciona um grupo para os parâmetros do filtro
        param_group = QGroupBox("Parâmetros do Filtro")
        param_layout = QFormLayout(param_group)
        
        # Combobox para seleção do tamanho do kernel
        self.kernel_combo = QComboBox()
        kernel_sizes = ["3x3", "5x5", "7x7", "9x9", "11x11"]
        self.kernel_combo.addItems(kernel_sizes)
        self.kernel_combo.setCurrentIndex(0)  # 3x3 por padrão
        param_layout.addRow("Tamanho do Kernel:", self.kernel_combo)
        
        # Adiciona o grupo de parâmetros ao layout principal
        layout.addWidget(param_group)
        
        # Adiciona informações sobre o filtro
        info_text = """
        <p><b>Filtro de Suavização da Média</b></p>
        <p>O filtro da média substitui cada pixel pela média dos valores dos pixels 
        em uma vizinhança definida pelo tamanho do kernel.</p>
        <p>Efeitos:</p>
        <ul>
            <li>Reduz ruído na imagem</li>
            <li>Causa borramento das bordas</li>
            <li>Suaviza falsos contornos</li>
            <li>Reduz detalhes pequenos</li>
        </ul>
        <p>Kernels maiores produzem maior suavização, mas causam mais borramento.</p>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
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
    
    def get_kernel_size(self):
        """
        Retorna o tamanho do kernel selecionado pelo usuário.
        
        Returns:
            int: Tamanho do kernel (3, 5, 7, 9 ou 11)
        """
        # Extrai o tamanho do kernel do texto selecionado (por exemplo, "3x3" -> 3)
        kernel_text = self.kernel_combo.currentText()
        return int(kernel_text.split('x')[0]) 