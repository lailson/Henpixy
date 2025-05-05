# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.1.22] - 2024-05-19

### Adicionado
- Implementação do filtro de suavização da média no menu Ferramentas
- Diálogo para configuração do tamanho do kernel do filtro (3x3, 5x5, 7x7, 9x9, 11x11)
- Nova implementação de filtragem espacial no módulo `spatial_filtering.py`
- Algoritmo eficiente de filtragem da média para imagens em escala de cinza e coloridas
- Preservação do canal alpha em imagens com transparência
- Informações sobre os efeitos e aplicações do filtro de suavização
- Integração com o sistema de histórico para facilitar comparações

## [0.1.21] - 2024-05-18

### Alterado
- Reorganização do menu Ferramentas, removendo o submenu Intensidade
- Todas as ferramentas de processamento de imagem agora estão diretamente no menu Ferramentas
- Simplificação da estrutura do menu para melhor usabilidade

## [0.1.20] - 2024-05-18

### Adicionado
- Implementação do fatiamento por intensidades para pseudocores no menu Ferramentas
- Interface com visualização lado a lado da imagem original e com pseudocores
- Mapas de cores predefinidos (Arco-íris, Temperatura, Densidade, Topográfico, Binário)
- Criação personalizada de intervalos de intensidade com seleção de cores
- Transformações RGB personalizadas (HotIron, Espectro, Senoidal, RGB Linear)
- Funcionalidades para distribuição uniforme de intervalos e geração automática de cores
- Informações teóricas sobre fatiamento por intensidades e suas aplicações
- Integração com o sistema de histórico do aplicativo

## [0.1.19] - 2024-05-17

### Adicionado
- Implementação da equalização de histograma no menu Ferramentas
- Nova janela de visualização de histograma no menu Janela
- Funcionalidade para calcular e exibir histogramas de imagens
- Comparação visual entre imagem original e equalizada
- Visualização paralela de histogramas original e equalizado
- Exibição da função de distribuição acumulada (CDF)
- Estatísticas detalhadas do histograma (dimensões, mínimo, máximo, média, desvio padrão, moda, mediana)
- Interface responsiva com suporte para redimensionamento e barras de rolagem
- Informações teóricas sobre histogramas e equalização

## [0.1.18] - 2024-05-16

### Alterado
- Aprimorado o "Fatiamento por Planos de Bits" para detectar automaticamente a profundidade de bits da imagem
- Adicionada exibição da intensidade máxima detectada na imagem
- Melhorada a interface com informações detalhadas sobre cada plano de bits
- Reorganizado o layout para melhor visualização das propriedades de cada plano
- Removida a funcionalidade de reconstrução para simplificar a interface

## [0.1.17] - 2024-05-16

### Adicionado
- Nova função "Fatiamento por Planos de Bits" no menu Ferramentas
- Implementação da decomposição de imagens em seus 8 planos de bits (0-7)
- Diálogo interativo para visualização de planos de bits individuais
- Funcionalidade para reconstrução de imagens a partir de planos selecionados
- Informações detalhadas sobre cada plano, incluindo seu peso e intervalo de intensidade
- Interface intuitiva com controles de seleção para cada plano
- Suporte para visualizar o impacto de cada plano de bits na qualidade da imagem
- Integração com o sistema de histórico para facilitar comparações

## [0.1.16] - 2024-05-15

### Adicionado
- Nova função "Alargamento de Contraste" no menu Ferramentas
- Implementação da transformação linear por partes definida por pontos (r1, s1) e (r2, s2)
- Diálogo interativo para configuração dos parâmetros de alargamento de contraste
- Configurações predefinidas para diferentes efeitos (contraste suave, médio, forte, binarização, inversão)
- Controles intuitivos para definir os pontos de controle
- Validação de parâmetros para garantir transformações válidas
- Descrição explicativa da função e seus efeitos no diálogo
- Preservação do canal alpha em imagens com transparência

## [0.1.15] - 2024-05-15

### Adicionado
- Nova função de transformação "Transformação Gama" no menu Ferramentas
- Implementação da transformação de potência (gama) com a fórmula S = c×r^γ
- Diálogo interativo para ajuste dos parâmetros gamma e c
- Suporte para processamento de diferentes profundidades de bits (8 e 16 bits)
- Informações detalhadas sobre o efeito de diferentes valores de gamma na imagem
- Preservação do canal alpha em imagens com transparência

## [0.1.14] - 2024-05-15

### Adicionado
- Nova função de transformação "Negativo" no menu Ferramentas
- Implementação da função de negativo usando lookup tables (S = L-1-r)
- Suporte para processamento de imagens em escala de cinza e coloridas (RGB/RGBA)
- Preservação do canal alpha em imagens com transparência

## [0.1.13] - 2024-05-15

### Alterado
- Modificado o comportamento do menu "Abrir modelo" para exibir um submenu em cascata
- Adicionado botão "Atualizar lista" no submenu de imagens de amostra
- Melhorada a experiência do usuário na seleção de imagens de amostra

## [0.1.12] - 2024-05-15

### Adicionado
- Diretório "samples" para armazenar imagens de amostra para testes
- Submenu "Abrir modelo" no menu Arquivo
- Seletor de imagens de amostra com exibição em menu contextual
- README explicativo para o diretório de amostras
- Configurações para ignorar imagens de amostra no controle de versão

## [0.1.11] - 2024-05-15

### Adicionado
- Novo menu "Exibir" com opções de zoom
- Função "Mais Zoom" para aumentar o tamanho da imagem (Ctrl++)
- Função "Menos Zoom" para diminuir o tamanho da imagem (Ctrl+-)
- Função "Zoom Original" para restaurar o tamanho original (Ctrl+0)
- Indicação do nível de zoom no título da janela
- Limites de zoom configuráveis (mínimo 10%, máximo 500%)

## [0.1.10] - 2024-05-15

### Adicionado
- Submenu "Informações" no menu Arquivo
- Diálogo detalhado com informações técnicas da imagem
- Exibição de estatísticas da imagem (nome, tipo, dimensões, tamanho em disco)
- Suporte para visualizar informações do espaço de cores e canais
- Exibição de metadados EXIF quando disponíveis
- Informações sobre DPI e resolução da imagem
- Interface organizada com rolagem para facilitar a visualização

## [0.1.9] - 2024-05-15

### Adicionado
- Campos para entrada manual de coordenadas (x,y) na janela de intensidade de pixels
- Botão "Aplicar" para visualizar a intensidade do pixel nas coordenadas digitadas
- Validação de coordenadas para garantir que estejam dentro dos limites da imagem
- Sincronização entre seleção de pixel por clique e coordenadas digitadas

## [0.1.8] - 2024-05-15

### Adicionado
- Nova funcionalidade "Intensidade" no menu Janela
- Visualização da matriz de intensidade de pixels
- Interface interativa para seleção de pixels na imagem
- Botões para aumentar e diminuir o tamanho da matriz de visualização
- Indicação visual do pixel selecionado na matriz
- Suporte para visualizar valores RGB em imagens coloridas
- Exibição colorida de pixels para facilitar a interpretação

## [0.1.7] - 2024-05-15

### Alterado
- Transformado o diálogo de histórico em janela auxiliar não-modal
- Agora é possível interagir com a janela principal enquanto o histórico está aberto
- A janela de histórico permanece aberta após restaurar uma imagem
- Melhorado o fluxo de trabalho para permitir múltiplas restaurações em sequência

## [0.1.6] - 2024-05-15

### Alterado
- Removida a mensagem de confirmação após aplicar o filtro de intensidade zero
- Corrigido bug na restauração de imagens a partir do histórico

## [0.1.5] - 2024-05-04

### Adicionado
- Submenu "Intensidade" no menu Ferramentas (posteriormente removido na v0.1.21)
- Função "Intensidade Zero" para alterar todos os pixels da imagem para zero
- Nova estrutura modular para ferramentas de processamento de imagem
- Separação entre GUI e lógica de processamento de imagem
- Função auxiliar para atualizar a exibição da imagem

## [0.1.4] - 2024-05-04

### Alterado
- Atualizado o diálogo "Sobre" com informações do desenvolvedor
- Adicionadas informações acadêmicas (UFPI) no diálogo "Sobre" 
- Adicionadas informações do professor orientador
- Atualizado link para o repositório do projeto
- Melhorado o layout do diálogo "Sobre" para melhor legibilidade

## [0.1.3] - 2024-05-04

### Adicionado
- Script de build para gerar executáveis (build.py)
- Suporte para gerar executáveis para Windows e macOS
- README com instruções de uso e build
- Arquivo de licença MIT
- Documentação para personalização do ícone do executável

## [0.1.2] - 2024-05-04

### Adicionado
- Submenu "Salvar" no menu Arquivo, com atalho Ctrl+S
- Submenu "Salvar Como" no menu Arquivo, com atalho Ctrl+Shift+S
- Funcionalidade para salvar imagens nos formatos PNG, JPEG, BMP, GIF, TIFF e WebP
- Detecção automática do formato do arquivo ao salvar
- Suporte para adicionar a extensão correta ao nome do arquivo
- Feedback visual após o salvamento (mensagem de sucesso ou erro)
- Título da janela agora mostra o nome do arquivo atual

## [0.1.1] - 2024-05-04

### Adicionado
- Submenu "Sair" no menu Arquivo
- Atalho de teclado "Ctrl+Q" para sair do programa
- Diálogo de confirmação ao fechar o programa
- Separador visual entre as opções "Abrir" e "Sair" no menu Arquivo

## [0.1.0] - 2024-05-04

### Adicionado
- Estrutura inicial do projeto
- Interface gráfica básica com PySide6
- Menu Arquivo com opção de abrir imagens
- Menu Ferramentas (preparado para implementações futuras)
- Menu Janela (preparado para implementações futuras)
- Menu Ajuda com opção "Sobre"
- Widget para exibição de imagens
- Carregamento de imagens usando Pillow
- Tratamento de erros para arquivos inválidos
- Redimensionamento automático de imagens
- Suporte para múltiplos formatos de imagem:
  - PNG
  - JPEG/JPG
  - BMP
  - GIF
  - TIFF/TIF
  - WebP
  - ICO
  - PSD
  - XBM
  - XPM
- Tratamento de imagens com canal alpha
- Suporte para imagens em escala de cinza
- Organização dos filtros de arquivo por tipo de imagem
- Arquivo .gitignore para Python e IDEs
- Configuração inicial do ambiente de desenvolvimento 