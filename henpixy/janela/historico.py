"""
Módulo para gerenciamento do histórico de modificações de imagens
"""

import os
import json
import tempfile
import shutil
import time
from datetime import datetime
from PIL import Image
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem, 
                             QScrollArea, QWidget, QMessageBox)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QSize

class HistoryItem:
    """Representa um item no histórico de modificações"""
    
    def __init__(self, image, description, timestamp=None):
        """
        Inicializa um item do histórico
        
        Args:
            image (PIL.Image.Image): A imagem
            description (str): Descrição da modificação
            timestamp (float, optional): Timestamp da modificação. Se None, usa o tempo atual.
        """
        self.image = image.copy()  # Cópia da imagem
        self.description = description
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.temp_path = None  # Caminho temporário para a imagem salva
        
    def save_to_disk(self, history_dir):
        """
        Salva a imagem em disco
        
        Args:
            history_dir (str): Diretório para salvar a imagem
            
        Returns:
            str: Caminho para a imagem salva
        """
        # Cria o diretório se não existir
        os.makedirs(history_dir, exist_ok=True)
        
        # Gera nome de arquivo baseado no timestamp
        filename = f"history_{int(self.timestamp)}_{self.description.replace(' ', '_')}.png"
        filepath = os.path.join(history_dir, filename)
        
        # Salva a imagem
        self.image.save(filepath)
        self.temp_path = filepath
        
        return filepath
    
    def to_dict(self):
        """
        Converte o item para um dicionário
        
        Returns:
            dict: Representação do item como dicionário
        """
        return {
            "description": self.description,
            "timestamp": self.timestamp,
            "filepath": self.temp_path
        }
    
    @classmethod
    def from_dict(cls, data, history_dir):
        """
        Cria um item a partir de um dicionário
        
        Args:
            data (dict): Dicionário com os dados do item
            history_dir (str): Diretório dos arquivos de histórico
            
        Returns:
            HistoryItem: O item criado
        """
        filepath = data["filepath"]
        
        # Verifica se o arquivo existe
        if not os.path.exists(filepath):
            # Tenta reconstruir o caminho
            filename = os.path.basename(filepath)
            filepath = os.path.join(history_dir, filename)
            
            if not os.path.exists(filepath):
                return None
        
        # Carrega a imagem
        try:
            image = Image.open(filepath)
            item = cls(image, data["description"], data["timestamp"])
            item.temp_path = filepath
            return item
        except Exception as e:
            print(f"Erro ao carregar imagem do histórico: {e}")
            return None

class HistoryManager:
    """Gerencia o histórico de modificações de imagens"""
    
    def __init__(self, app_name="henpixy"):
        """
        Inicializa o gerenciador de histórico
        
        Args:
            app_name (str): Nome da aplicação para criar o diretório de histórico
        """
        # Diretório base para armazenar o histórico
        self.history_dir = os.path.join(tempfile.gettempdir(), app_name, "history")
        os.makedirs(self.history_dir, exist_ok=True)
        
        # Lista de itens do histórico
        self.history_items = []
        
        # Índice do item atual
        self.current_index = -1
        
        # Carrega o histórico do disco
        self.load_from_disk()
    
    def add_item(self, image, description):
        """
        Adiciona um item ao histórico
        
        Args:
            image (PIL.Image.Image): A imagem
            description (str): Descrição da modificação
            
        Returns:
            int: O índice do novo item
        """
        # Se estamos no meio do histórico, remove os itens posteriores
        if self.current_index < len(self.history_items) - 1:
            # Remove os arquivos temporários dos itens que serão excluídos
            for item in self.history_items[self.current_index + 1:]:
                if item.temp_path and os.path.exists(item.temp_path):
                    try:
                        os.remove(item.temp_path)
                    except Exception as e:
                        print(f"Erro ao remover arquivo: {e}")
            
            # Remove os itens do histórico
            self.history_items = self.history_items[:self.current_index + 1]
        
        # Cria o novo item
        item = HistoryItem(image, description)
        
        # Salva a imagem em disco
        item.save_to_disk(self.history_dir)
        
        # Adiciona o item ao histórico
        self.history_items.append(item)
        self.current_index = len(self.history_items) - 1
        
        # Salva o histórico no disco
        self.save_to_disk()
        
        return self.current_index
    
    def get_current_item(self):
        """
        Retorna o item atual do histórico
        
        Returns:
            HistoryItem: O item atual ou None se o histórico estiver vazio
        """
        if not self.history_items or self.current_index < 0:
            return None
        
        return self.history_items[self.current_index]
    
    def get_current_image(self):
        """
        Retorna a imagem atual do histórico
        
        Returns:
            PIL.Image.Image: A imagem atual ou None se o histórico estiver vazio
        """
        item = self.get_current_item()
        return item.image.copy() if item else None
    
    def go_to_item(self, index):
        """
        Vai para um item específico do histórico
        
        Args:
            index (int): O índice do item
            
        Returns:
            PIL.Image.Image: A imagem do item ou None se o índice for inválido
        """
        if index < 0 or index >= len(self.history_items):
            return None
        
        self.current_index = index
        self.save_to_disk()
        return self.get_current_image()
    
    def save_to_disk(self):
        """
        Salva o histórico no disco
        """
        try:
            # Cria o diretório se não existir
            os.makedirs(self.history_dir, exist_ok=True)
            
            # Salva o histórico como JSON
            history_data = {
                "current_index": self.current_index,
                "items": [item.to_dict() for item in self.history_items]
            }
            
            with open(os.path.join(self.history_dir, "history.json"), "w") as f:
                json.dump(history_data, f)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def load_from_disk(self):
        """
        Carrega o histórico do disco
        """
        try:
            # Verifica se o arquivo de histórico existe
            history_file = os.path.join(self.history_dir, "history.json")
            if not os.path.exists(history_file):
                return
            
            # Carrega o histórico
            with open(history_file, "r") as f:
                history_data = json.load(f)
            
            # Carrega os itens
            self.history_items = []
            for item_data in history_data["items"]:
                item = HistoryItem.from_dict(item_data, self.history_dir)
                if item:
                    self.history_items.append(item)
            
            # Carrega o índice atual
            self.current_index = history_data["current_index"]
            if self.current_index >= len(self.history_items):
                self.current_index = len(self.history_items) - 1
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            self.history_items = []
            self.current_index = -1
    
    def clear(self):
        """
        Limpa o histórico
        """
        # Remove os arquivos temporários
        for item in self.history_items:
            if item.temp_path and os.path.exists(item.temp_path):
                try:
                    os.remove(item.temp_path)
                except Exception as e:
                    print(f"Erro ao remover arquivo: {e}")
        
        # Limpa a lista de itens
        self.history_items = []
        self.current_index = -1
        
        # Salva o histórico no disco
        self.save_to_disk()

class HistoryDialog(QDialog):
    """Diálogo para exibir o histórico de modificações"""
    
    def __init__(self, history_manager, parent=None):
        """
        Inicializa o diálogo de histórico
        
        Args:
            history_manager (HistoryManager): O gerenciador de histórico
            parent (QWidget, optional): Widget pai
        """
        super().__init__(parent)
        self.history_manager = history_manager
        self.selected_index = history_manager.current_index
        self.thumbnail_size = QSize(100, 100)
        
        self.setWindowTitle("Histórico de Modificações")
        self.setMinimumSize(500, 400)
        
        self.init_ui()
        self.populate_list()
    
    def init_ui(self):
        """
        Inicializa a interface do diálogo
        """
        layout = QVBoxLayout(self)
        
        # Lista de histórico
        self.history_list = QListWidget()
        self.history_list.setIconSize(self.thumbnail_size)
        self.history_list.currentRowChanged.connect(self.on_item_selected)
        layout.addWidget(self.history_list)
        
        # Botões
        button_layout = QHBoxLayout()
        
        # Botão para restaurar
        self.restore_button = QPushButton("Restaurar")
        self.restore_button.clicked.connect(self.restore_item)
        button_layout.addWidget(self.restore_button)
        
        # Botão para fechar
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def populate_list(self):
        """
        Preenche a lista com os itens do histórico
        """
        self.history_list.clear()
        
        for i, item in enumerate(self.history_manager.history_items):
            # Cria o widget do item
            list_item = QListWidgetItem()
            
            # Cria a miniatura
            thumbnail = self.create_thumbnail(item.image)
            list_item.setIcon(thumbnail)
            
            # Formata o timestamp
            timestamp = datetime.fromtimestamp(item.timestamp).strftime("%d/%m/%Y %H:%M:%S")
            
            # Define o texto
            list_item.setText(f"{i+1}. {item.description} - {timestamp}")
            
            # Define dados personalziados
            list_item.setData(Qt.UserRole, i)
            
            # Adiciona o item à lista
            self.history_list.addItem(list_item)
        
        # Seleciona o item atual
        if self.history_manager.current_index >= 0:
            self.history_list.setCurrentRow(self.history_manager.current_index)
    
    def create_thumbnail(self, image):
        """
        Cria uma miniatura da imagem
        
        Args:
            image (PIL.Image.Image): A imagem
            
        Returns:
            QPixmap: A miniatura
        """
        # Redimensiona a imagem para caber na miniatura
        thumbnail_size = (self.thumbnail_size.width(), self.thumbnail_size.height())
        thumbnail_img = image.copy()
        thumbnail_img.thumbnail(thumbnail_size, Image.LANCZOS)
        
        # Converte para QPixmap
        if thumbnail_img.mode == "RGB":
            format = QImage.Format_RGB888
        elif thumbnail_img.mode == "RGBA":
            format = QImage.Format_RGBA8888
        else:
            thumbnail_img = thumbnail_img.convert("RGB")
            format = QImage.Format_RGB888
        
        img_data = thumbnail_img.tobytes("raw", thumbnail_img.mode)
        q_image = QImage(img_data, thumbnail_img.width, thumbnail_img.height, format)
        
        return QPixmap.fromImage(q_image)
    
    def on_item_selected(self, row):
        """
        Manipula a seleção de um item na lista
        
        Args:
            row (int): A linha selecionada
        """
        if row >= 0 and row < len(self.history_manager.history_items):
            self.selected_index = row
        else:
            self.selected_index = -1
    
    def restore_item(self):
        """
        Restaura o item selecionado
        """
        if self.selected_index < 0:
            return
        
        # Verifica se o item selecionado é diferente do atual
        if self.selected_index != self.history_manager.current_index:
            # Pede confirmação
            reply = QMessageBox.question(
                self,
                "Restaurar Imagem",
                "Isso removerá todas as modificações posteriores. Deseja continuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Restaura o item
                image = self.history_manager.go_to_item(self.selected_index)
                if image:
                    # Fecha o diálogo com sucesso
                    self.accept()
                else:
                    QMessageBox.critical(
                        self,
                        "Erro",
                        "Não foi possível restaurar a imagem."
                    )
        else:
            # Fecha o diálogo
            self.reject() 