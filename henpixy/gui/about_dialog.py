from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sobre o Henpixy")
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        # Informações do programa
        title = QLabel("Henpixy")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        version = QLabel("Versão: 1.0.0")
        description = QLabel("Um programa para processamento digital de imagens")
        website = QLabel("Website: https://github.com/seu-usuario/henpixy")
        
        # Adicionar widgets ao layout
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(description)
        layout.addWidget(website)
        
        # Botão OK
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)