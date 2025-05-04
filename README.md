# Henpixy

Um programa para processamento digital de imagens com interface gráfica em Python.

## Funcionalidades

- Visualização de imagens em diversos formatos (PNG, JPEG, BMP, GIF, TIFF, WebP, etc.)
- Salvar imagens em diferentes formatos
- Interface simples e intuitiva com menus e atalhos

## Requisitos para Desenvolvimento

- Python 3.12 ou superior
- PySide6 (Qt6)
- Pillow
- Numpy
- Scikit-image
- Matplotlib

## Instalação para Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/henpixy.git
cd henpixy
```

2. Crie e ative um ambiente virtual (usando conda):
```bash
conda create --prefix ./env python=3.12
conda activate ./env
```

3. Instale as dependências:
```bash
pip install -e .
```

4. Execute o programa:
```bash
python -m henpixy.main
```

## Gerando Executáveis

### Requisitos
- PyInstaller

### Instruções

Para gerar um executável para sua plataforma atual (Windows ou macOS), execute:

```bash
python build.py
```

O executável será gerado na pasta `dist/`.

### Executáveis por Plataforma

#### Windows
O executável gerado para Windows é o arquivo `Henpixy.exe` na pasta `dist/`.

#### macOS
O executável gerado para macOS é o arquivo `Henpixy` na pasta `dist/`.

### Personalização do Ícone

- Para Windows: Adicione um arquivo `icon.ico` na pasta `resources/`
- Para macOS: Adicione um arquivo `icon.icns` na pasta `resources/`

## Licença

[MIT](LICENSE)
