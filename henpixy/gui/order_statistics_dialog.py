"""
Diálogo para configuração dos filtros de estatísticas de ordem (máximo, mínimo e mediana).
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QFormLayout,
    QComboBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt

class OrderStatisticsDialog(QDialog):
    """
    Diálogo para configuração dos filtros de estatísticas de ordem.
    Permite ao usuário escolher o tipo de filtro (máximo, mínimo ou mediana)
    e o tamanho do kernel (vizinhança).
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Filtros de Estatísticas de Ordem")
        self.setMinimumWidth(400)
        
        # Valor inicial para o tipo de filtro e tamanho do kernel
        self.filter_type = "median"  # Mediana por padrão
        self.kernel_size = 3
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Adiciona um grupo para os parâmetros do filtro
        param_group = QGroupBox("Parâmetros do Filtro")
        param_layout = QVBoxLayout(param_group)
        
        # Seleção do tipo de filtro
        filter_group = QGroupBox("Tipo de Filtro")
        filter_layout = QVBoxLayout(filter_group)
        
        self.filter_button_group = QButtonGroup(self)
        
        # Botão para filtro de máximo
        self.max_radio = QRadioButton("Filtro de Máximo")
        self.filter_button_group.addButton(self.max_radio)
        filter_layout.addWidget(self.max_radio)
        
        # Botão para filtro de mínimo
        self.min_radio = QRadioButton("Filtro de Mínimo")
        self.filter_button_group.addButton(self.min_radio)
        filter_layout.addWidget(self.min_radio)
        
        # Botão para filtro de mediana
        self.median_radio = QRadioButton("Filtro de Mediana")
        self.median_radio.setChecked(True)  # Mediana selecionada por padrão
        self.filter_button_group.addButton(self.median_radio)
        filter_layout.addWidget(self.median_radio)
        
        param_layout.addWidget(filter_group)
        
        # Seleção do tamanho do kernel
        kernel_form = QFormLayout()
        
        # Combobox para seleção do tamanho do kernel
        self.kernel_combo = QComboBox()
        kernel_sizes = ["3x3", "5x5", "7x7", "9x9", "11x11"]
        self.kernel_combo.addItems(kernel_sizes)
        self.kernel_combo.setCurrentIndex(0)  # 3x3 por padrão
        kernel_form.addRow("Tamanho do Kernel:", self.kernel_combo)
        
        param_layout.addLayout(kernel_form)
        
        # Adiciona o grupo de parâmetros ao layout principal
        layout.addWidget(param_group)
        
        # Adiciona informações sobre os filtros
        info_text = """
        <h3>Filtros de Estatísticas de Ordem</h3>
        <p>Os filtros de estatísticas de ordem substituem cada pixel por um valor estatístico 
        calculado a partir dos pixels em uma vizinhança definida pelo tamanho do kernel.</p>
        
        <h4>Tipos de Filtros:</h4>
        
        <p><b>Filtro de Máximo</b>: Substitui cada pixel pelo valor máximo da vizinhança.</p>
        <ul>
            <li>Expande regiões claras e reduz regiões escuras</li>
            <li>Útil para destacar objetos claros em fundos escuros</li>
            <li>Equivalente à operação morfológica de dilatação</li>
        </ul>
        
        <p><b>Filtro de Mínimo</b>: Substitui cada pixel pelo valor mínimo da vizinhança.</p>
        <ul>
            <li>Expande regiões escuras e reduz regiões claras</li>
            <li>Útil para destacar objetos escuros em fundos claros</li>
            <li>Equivalente à operação morfológica de erosão</li>
        </ul>
        
        <p><b>Filtro de Mediana</b>: Substitui cada pixel pelo valor mediano da vizinhança.</p>
        <ul>
            <li>Excelente para remover ruído do tipo "sal e pimenta"</li>
            <li>Preserva melhor as bordas que o filtro da média</li>
            <li>Menos sensível a valores extremos na vizinhança</li>
        </ul>
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
    
    def get_filter_type(self):
        """
        Retorna o tipo de filtro selecionado pelo usuário.
        
        Returns:
            str: Tipo de filtro ('max', 'min' ou 'median')
        """
        if self.max_radio.isChecked():
            return "max"
        elif self.min_radio.isChecked():
            return "min"
        else:
            return "median" 