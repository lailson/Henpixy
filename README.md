# Henpixy

Um programa para processamento digital de imagens com interface gráfica em Python.

## Checklist de Desenvolvimento

A aplicação deve ter as seguintes funcionalidades:

- ✅ Interface gráfica 
- ✅ Carregar imagem 
- ✅ Salvar imagem 
- ✅ Intensidade zero: função para atribuir intensidade zero a todos os pixels da imagem 
- ✅ Retornar para a imagem original 
- ✅ Função negativo: implementação da transformação S = L - 1 - r
- ✅ Transformação de potência: possibilitando ao usuário definir o valor de gama e utilizar o valor de c = 1
- ✅ Alargamento de contraste: possibilitando ao usuário definir os valores de (r1, s1) e (r2, s2)
- ✅ Fatiamento por Planos de Bits: possibilitando ao usuário selecionar o plano de bits desejado para a visualização
- ✅ Equalização de histograma: o programa deve exibir a imagem equalizada, o histograma da imagem original e o histograma da imagem equalizada para fins de comparação
- ✅ Fatiamento por Intensidades para Pseudocores
- ✅ Filtros de suavização: Média
- ⬜ Filtros de estatísticas de ordem: Máx, Mín e Mediana
- ⬜ Filtro Laplaciano: utilizando a máscara com centro negativo e que inclui os termos diagonais, faça o que se peder: 
  - (a) apresente o resultado do laplaciano sem ajuste
  - (b) apresente o resultado do laplaciano com ajuste
  - (c) apresente a imagem original aguçada com a imagem laplaciana

## Funcionalidades

- Visualização de imagens em diversos formatos (PNG, JPEG, BMP, GIF, TIFF, WebP, etc.)
- Salvar imagens em diferentes formatos
- Interface simples e intuitiva com menus e atalhos
- Zoom para melhor visualização dos detalhes da imagem
- Visualização de informações detalhadas da imagem (tamanho, tipo, dimensões, espaço de cores)
- Visualização da intensidade de pixels selecionados
- Histórico de modificações com possibilidade de retornar a estados anteriores
- Análise e equalização de histogramas:
  - Visualização de histogramas em tempo real
  - Comparação entre imagem original e equalizada
  - Estatísticas detalhadas do histograma (mínimo, máximo, média, desvio padrão)
  - Visualização da função de distribuição acumulada (CDF)
  - Janela dedicada para análise de histograma

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

Para criar um pacote instalador DMG no macOS:

1. Instale o `create-dmg`:
```bash
brew install create-dmg
```

2. Execute o script de criação do DMG:
```bash
./create_macos_dmg.sh
```

3. O arquivo DMG será gerado em `dist/Henpixy-0.1.15.dmg`.

### Personalização do Ícone

- Para Windows: Adicione um arquivo `icon.ico` na pasta `resources/`
- Para macOS: Adicione um arquivo `icon.icns` na pasta `resources/`

Para personalizar a aparência do DMG no macOS:
- Adicione uma imagem de fundo em `resources/dmg_background.png` (800x400 pixels recomendado)

## Licença

[MIT](LICENSE)
