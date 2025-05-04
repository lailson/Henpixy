#!/usr/bin/env python
import os
import sys
import platform
import subprocess
import shutil

def create_icon_directory():
    """Cria diretório de ícones se não existir"""
    if not os.path.exists('resources'):
        os.makedirs('resources')

def create_default_icon():
    """Cria um ícone padrão se não existir"""
    if not os.path.exists('resources/icon.ico') and not os.path.exists('resources/icon.icns'):
        print("AVISO: Nenhum ícone encontrado. Executável não terá ícone personalizado.")
        print("Coloque um arquivo icon.ico (Windows) ou icon.icns (macOS) na pasta resources/")

def clean_build_directories():
    """Limpa diretórios de build anteriores"""
    dirs_to_remove = ['build', 'dist']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    if os.path.exists('Henpixy.spec'):
        os.remove('Henpixy.spec')

def build_executable():
    """Constrói o executável para a plataforma atual"""
    system = platform.system()
    
    # Comandos base
    base_command = [
        'pyinstaller',
        '--name=Henpixy',
        '--windowed',
        '--onefile',
    ]
    
    if system == 'Windows':
        if os.path.exists('resources/icon.ico'):
            base_command.append('--icon=resources/icon.ico')
    elif system == 'Darwin':  # macOS
        if os.path.exists('resources/icon.icns'):
            base_command.append('--icon=resources/icon.icns')
    
    # Adiciona o script principal
    base_command.append('henpixy/main.py')
    
    # Executa o comando
    subprocess.call(base_command)
    
    # Informa onde está o executável
    if system == 'Windows':
        print("\nExecutável criado: dist/Henpixy.exe")
    elif system == 'Darwin':
        print("\nExecutável criado: dist/Henpixy")
    else:
        print("\nExecutável criado: dist/Henpixy")

def main():
    """Função principal"""
    print("=== Construindo Henpixy ===")
    
    # Verifica ambiente virtual
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        print("AVISO: Você não parece estar em um ambiente virtual.")
        response = input("Continuar mesmo assim? (y/n): ")
        if response.lower() != 'y':
            print("Compilação cancelada.")
            return
    
    # Verifica se o PyInstaller está instalado
    try:
        subprocess.call(['pyinstaller', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("PyInstaller não está instalado. Instalando...")
        subprocess.call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    create_icon_directory()
    create_default_icon()
    clean_build_directories()
    build_executable()
    
    print("\nConstrução concluída!")

if __name__ == "__main__":
    main() 