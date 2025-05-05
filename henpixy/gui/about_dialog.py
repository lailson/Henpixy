from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sobre o Henpixy")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        main_layout = QVBoxLayout(self)
        
        # Área de rolagem para comportar bastante texto
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(15)
        
        # Informações do programa
        title = QLabel("Henpixy")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        
        version = QLabel("Versão: 0.1.13")
        version.setAlignment(Qt.AlignCenter)
        
        description = QLabel("Software para processamento digital de imagens")
        description.setAlignment(Qt.AlignCenter)
        
        developer = QLabel("Desenvolvido por Lailson Henrique Oliveira dos Santos")
        developer.setAlignment(Qt.AlignCenter)
        developer.setWordWrap(True)
        
        academic_info = QLabel("Este software é produto da disciplina de Análise e Processamento de Imagens na UFPI - Universidade Federal do Piauí")
        academic_info.setAlignment(Qt.AlignCenter)
        academic_info.setWordWrap(True)
        
        professor_info = QLabel("Professor: Dr. Laurindo de Sousa Britto Neto")
        professor_info.setAlignment(Qt.AlignCenter)
        
        professor_email = QLabel("Email: laurindoneto@ufpi.edu.br")
        professor_email.setAlignment(Qt.AlignCenter)
        
        website = QLabel("Site do projeto: github.com/lailson/Henpixy")
        website.setAlignment(Qt.AlignCenter)
        
        # Adicionar widgets ao layout com espaçamento
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(description)
        layout.addWidget(QLabel("")) # Espaçador
        layout.addWidget(developer)
        layout.addWidget(QLabel("")) # Espaçador
        layout.addWidget(academic_info)
        layout.addWidget(professor_info)
        layout.addWidget(professor_email)
        layout.addWidget(QLabel("")) # Espaçador
        layout.addWidget(website)
        layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Botão OK
        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(100)
        ok_button.clicked.connect(self.accept)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.setAlignment(Qt.AlignCenter)
        
        main_layout.addLayout(button_layout)