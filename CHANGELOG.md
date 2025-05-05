# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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
- Submenu "Intensidade" no menu Ferramentas
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