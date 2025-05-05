"""
Diálogo para configuração do alargamento de contraste
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QDialogButtonBox, QGroupBox, QFormLayout, QComboBox
)


class ContrastStretchingDialog(QDialog):
    """
    Diálogo para configuração dos parâmetros do alargamento de contraste
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Alargamento de Contraste")
        self.resize(400, 300)
        
        self.main_layout = QVBoxLayout(self)
        
        # Preset de configurações
        self.preset_group = QGroupBox("Configurações Predefinidas")
        self.preset_layout = QVBoxLayout(self.preset_group)
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("Personalizado", "custom")
        self.preset_combo.addItem("Aumentar contraste (suave)", "soft")
        self.preset_combo.addItem("Aumentar contraste (médio)", "medium")
        self.preset_combo.addItem("Aumentar contraste (forte)", "strong")
        self.preset_combo.addItem("Criar imagem binária", "binary")
        self.preset_combo.addItem("Inverter tons", "invert")
        self.preset_combo.currentIndexChanged.connect(self.apply_preset)
        
        self.preset_layout.addWidget(self.preset_combo)
        self.main_layout.addWidget(self.preset_group)
        
        # Configurações dos pontos
        self.points_group = QGroupBox("Pontos de Controle")
        self.points_layout = QFormLayout(self.points_group)
        
        # Ponto 1 (r1, s1)
        self.r1_spin = QSpinBox()
        self.r1_spin.setRange(0, 255)
        self.r1_spin.setValue(50)
        self.r1_spin.valueChanged.connect(self.on_r1_changed)
        
        self.s1_spin = QSpinBox()
        self.s1_spin.setRange(0, 255)
        self.s1_spin.setValue(30)
        
        r1s1_layout = QHBoxLayout()
        r1s1_layout.addWidget(self.r1_spin)
        r1s1_layout.addWidget(self.s1_spin)
        
        self.points_layout.addRow("Ponto 1 (r1, s1):", r1s1_layout)
        
        # Ponto 2 (r2, s2)
        self.r2_spin = QSpinBox()
        self.r2_spin.setRange(0, 255)
        self.r2_spin.setValue(200)
        self.r2_spin.valueChanged.connect(self.on_r2_changed)
        
        self.s2_spin = QSpinBox()
        self.s2_spin.setRange(0, 255)
        self.s2_spin.setValue(220)
        
        r2s2_layout = QHBoxLayout()
        r2s2_layout.addWidget(self.r2_spin)
        r2s2_layout.addWidget(self.s2_spin)
        
        self.points_layout.addRow("Ponto 2 (r2, s2):", r2s2_layout)
        
        self.main_layout.addWidget(self.points_group)
        
        # Descrição da transformação
        self.description_label = QLabel(
            "O alargamento de contraste aplica uma transformação linear por partes "
            "definida pelos pontos (r1, s1) e (r2, s2), permitindo ajustar o contraste "
            "da imagem ou criar efeitos específicos."
        )
        self.description_label.setWordWrap(True)
        self.main_layout.addWidget(self.description_label)
        
        # Botões de confirmação
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)
    
    def apply_preset(self, index):
        """Aplica uma configuração predefinida aos parâmetros"""
        preset = self.preset_combo.currentData()
        
        if preset == "custom":
            # Mantém os valores atuais
            pass
        elif preset == "soft":
            # Aumento suave de contraste
            self.r1_spin.setValue(50)
            self.s1_spin.setValue(30)
            self.r2_spin.setValue(200)
            self.s2_spin.setValue(220)
        elif preset == "medium":
            # Aumento médio de contraste
            self.r1_spin.setValue(70)
            self.s1_spin.setValue(20)
            self.r2_spin.setValue(180)
            self.s2_spin.setValue(230)
        elif preset == "strong":
            # Aumento forte de contraste
            self.r1_spin.setValue(80)
            self.s1_spin.setValue(10)
            self.r2_spin.setValue(160)
            self.s2_spin.setValue(240)
        elif preset == "binary":
            # Imagem binária (limiarização)
            self.r1_spin.setValue(127)
            self.s1_spin.setValue(0)
            self.r2_spin.setValue(128)
            self.s2_spin.setValue(255)
        elif preset == "invert":
            # Inversão de tons
            self.r1_spin.setValue(0)
            self.s1_spin.setValue(255)
            self.r2_spin.setValue(255)
            self.s2_spin.setValue(0)
    
    def on_r1_changed(self, value):
        """Garante que r1 < r2"""
        if value >= self.r2_spin.value():
            self.r2_spin.setValue(value + 1)
    
    def on_r2_changed(self, value):
        """Garante que r1 < r2"""
        if value <= self.r1_spin.value():
            self.r1_spin.setValue(value - 1)
    
    def get_parameters(self):
        """Retorna os parâmetros configurados pelo usuário"""
        return {
            "r1": self.r1_spin.value(),
            "s1": self.s1_spin.value(),
            "r2": self.r2_spin.value(),
            "s2": self.s2_spin.value()
        } 