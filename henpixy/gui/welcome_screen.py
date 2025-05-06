"""
Tela de boas-vindas do Henpixy.
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QFileDialog, QListWidget,
    QScrollArea, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QDesktopServices
from PySide6.QtCore import Qt, QSize, QUrl, Signal

class WelcomeScreen(QWidget):
    """
    Tela de boas-vindas exibida ao iniciar o aplicativo.
    
    Exibe a logo, mensagem de boas-vindas e opções para abrir imagens
    ou acessar recursos do aplicativo.
    """
    
    # Sinais para comunicação com a janela principal
    open_image_requested = Signal(str)
    open_sample_requested = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurar a janela
        self.setObjectName("welcomeScreen")
        self.setStyleSheet("""
            #welcomeScreen {
                background-color: #f5f5f5;
            }
            .QPushButton {
                background-color: #2979ff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            .QPushButton:hover {
                background-color: #1565c0;
            }
            .QPushButton#secondaryButton {
                background-color: transparent;
                color: #2979ff;
                border: 1px solid #2979ff;
            }
            .QPushButton#secondaryButton:hover {
                background-color: rgba(41, 121, 255, 0.1);
            }
            .QPushButton#linkButton {
                background-color: transparent;
                color: #2979ff;
                border: none;
                text-decoration: underline;
                font-weight: normal;
                padding: 5px;
            }
            .QPushButton#linkButton:hover {
                color: #1565c0;
            }
            QLabel#titleLabel {
                color: #424242;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLabel#subtitleLabel {
                color: #616161;
                font-size: 16px;
                margin-bottom: 20px;
            }
            QFrame#card {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin: 10px;
            }
            QListWidget {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #2979ff;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Área superior com logo e título
        header_layout = QHBoxLayout()
        
        # Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                "resources", "henpixy.png")
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path)
        logo_pixmap = logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setFixedSize(150, 150)
        header_layout.addWidget(logo_label)
        
        # Título e subtítulo
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(20, 0, 0, 0)
        
        title_label = QLabel("Bem-vindo ao Henpixy")
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Seu aplicativo de processamento digital de imagens")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setWordWrap(True)
        title_layout.addWidget(subtitle_label)
        
        title_layout.addStretch()
        header_layout.addLayout(title_layout)
        header_layout.addStretch(1)
        
        main_layout.addLayout(header_layout)
        
        # Área de conteúdo principal (cartões)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Cartão para abrir imagem do computador
        open_card = QFrame()
        open_card.setObjectName("card")
        open_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        open_layout = QVBoxLayout(open_card)
        
        open_title = QLabel("Abrir Imagem")
        open_title.setObjectName("titleLabel")
        open_title.setAlignment(Qt.AlignCenter)
        open_layout.addWidget(open_title)
        
        open_desc = QLabel("Escolha uma imagem do seu computador para processar. Suportamos diversos formatos incluindo PNG, JPEG, BMP, GIF e TIFF.")
        open_desc.setWordWrap(True)
        open_desc.setAlignment(Qt.AlignCenter)
        open_layout.addWidget(open_desc)
        
        open_layout.addStretch()
        
        open_button = QPushButton("Escolher Imagem...")
        open_button.setIcon(QIcon.fromTheme("document-open"))
        open_button.clicked.connect(self.open_file_dialog)
        open_layout.addWidget(open_button, 0, Qt.AlignCenter)
        
        content_layout.addWidget(open_card)
        
        # Cartão para escolher imagem de amostra
        sample_card = QFrame()
        sample_card.setObjectName("card")
        sample_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        sample_layout = QVBoxLayout(sample_card)
        
        sample_title = QLabel("Imagens de Amostra")
        sample_title.setObjectName("titleLabel")
        sample_title.setAlignment(Qt.AlignCenter)
        sample_layout.addWidget(sample_title)
        
        sample_desc = QLabel("Utilize uma das nossas imagens de amostra para experimentar os recursos do Henpixy.")
        sample_desc.setWordWrap(True)
        sample_desc.setAlignment(Qt.AlignCenter)
        sample_layout.addWidget(sample_desc)
        
        # Lista de amostras
        self.sample_list = QListWidget()
        self.sample_list.setMaximumHeight(200)
        self.load_sample_list()
        self.sample_list.itemDoubleClicked.connect(self.open_sample)
        sample_layout.addWidget(self.sample_list)
        
        open_sample_button = QPushButton("Abrir Selecionada")
        open_sample_button.setObjectName("secondaryButton")
        open_sample_button.clicked.connect(lambda: self.open_sample(self.sample_list.currentItem()))
        sample_layout.addWidget(open_sample_button, 0, Qt.AlignCenter)
        
        content_layout.addWidget(sample_card)
        
        main_layout.addLayout(content_layout)
        
        # Área inferior com links
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 20, 0, 0)
        
        footer_layout.addStretch(1)
        
        doc_button = QPushButton("Documentação")
        doc_button.setObjectName("linkButton")
        doc_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/lailson/Henpixy")))
        footer_layout.addWidget(doc_button)
        
        site_button = QPushButton("Visite o Site")
        site_button.setObjectName("linkButton")
        site_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://henpixy.lailsonhenrique.com")))
        footer_layout.addWidget(site_button)
        
        footer_layout.addStretch(1)
        
        main_layout.addLayout(footer_layout)
    
    def load_sample_list(self):
        """Carrega a lista de imagens de amostra disponíveis."""
        samples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "samples")
        
        # Verifica se o diretório de amostras existe
        if not os.path.exists(samples_dir):
            self.sample_list.addItem("Diretório de amostras não encontrado")
            return
        
        # Lista os arquivos no diretório de amostras
        sample_files = [f for f in os.listdir(samples_dir) 
                      if os.path.isfile(os.path.join(samples_dir, f)) and
                      any(f.lower().endswith(ext) for ext in 
                          ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.webp'])]
        
        if not sample_files:
            self.sample_list.addItem("Nenhuma imagem disponível")
            return
        
        # Adiciona as imagens ao menu
        for sample_file in sorted(sample_files):
            self.sample_list.addItem(sample_file)
    
    def open_file_dialog(self):
        """Abre o diálogo para selecionar uma imagem do computador."""
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
            self.open_image_requested.emit(file_name)
    
    def open_sample(self, item):
        """Abre uma imagem de amostra selecionada."""
        if item is None:
            return
        
        sample_name = item.text()
        self.open_sample_requested.emit(sample_name) 