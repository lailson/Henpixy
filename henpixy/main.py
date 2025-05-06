import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from henpixy.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Forçar tema claro, ignorando configurações do sistema
    app.setStyle("Fusion")
    
    # No macOS, desabilitar o modo escuro
    if sys.platform == "darwin":
        # Impedir que o aplicativo use o modo escuro do macOS
        os.environ["QT_MAC_WANTS_LAYER"] = "1"
        # Desativar a adaptação de cores para o modo escuro
        os.environ["QT_QPA_PLATFORM"] = "cocoa:darkmode=0"
    
    # Aplicar paleta clara
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(0, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(41, 121, 255))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 