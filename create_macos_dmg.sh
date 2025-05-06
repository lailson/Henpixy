#!/bin/bash

# Script para criar um arquivo .dmg para o Henpixy no macOS
# Requer create-dmg instalado via Homebrew: brew install create-dmg

# Verifica se o create-dmg está instalado
if ! command -v create-dmg &> /dev/null; then
    echo "Erro: create-dmg não está instalado."
    echo "Instale com: brew install create-dmg"
    exit 1
fi

# Verifica se o executável existe
if [ ! -f "dist/Henpixy" ]; then
    echo "Erro: Executável dist/Henpixy não encontrado."
    echo "Primeiro, execute: python build.py"
    exit 1
fi

# Cria diretórios temporários
echo "Preparando diretórios..."
rm -rf build/dmg
mkdir -p build/dmg

# Cria a estrutura do .app
echo "Criando estrutura do aplicativo..."
mkdir -p "build/dmg/Henpixy.app/Contents/MacOS"
mkdir -p "build/dmg/Henpixy.app/Contents/Resources"

# Copia o executável para o .app
echo "Copiando executável..."
cp "dist/Henpixy" "build/dmg/Henpixy.app/Contents/MacOS/"

# Cria o arquivo Info.plist
cat > "build/dmg/Henpixy.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Henpixy</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.yourcompany.henpixy</string>
    <key>CFBundleName</key>
    <string>Henpixy</string>
    <key>CFBundleDisplayName</key>
    <string>Henpixy</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>0.1.25</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# Copia o ícone se existir
if [ -f "resources/icon.icns" ]; then
    echo "Copiando ícone..."
    cp "resources/icon.icns" "build/dmg/Henpixy.app/Contents/Resources/AppIcon.icns"
else
    echo "Aviso: Ícone não encontrado em resources/icon.icns"
    echo "O aplicativo não terá um ícone personalizado"
fi

# Torna o aplicativo executável
chmod +x "build/dmg/Henpixy.app/Contents/MacOS/Henpixy"

# Cria um README com instruções para usuários do macOS
cat > "build/dmg/README_INSTALACAO.txt" << EOF
INSTRUÇÕES DE INSTALAÇÃO DO HENPIXY PARA MACOS
==============================================

Se ao tentar abrir o Henpixy aparecer a mensagem "Henpixy.app está danificado e não pode ser aberto", siga um dos métodos abaixo:

MÉTODO 1 (Mais simples):
1. Clique com o botão direito do mouse (ou Control+clique) no aplicativo Henpixy.app
2. Selecione "Abrir" no menu de contexto
3. Na janela de aviso que aparecer, clique em "Abrir" novamente
4. O aplicativo será executado normalmente e nas próximas vezes poderá ser aberto com duplo clique

MÉTODO 2 (Via Terminal):
1. Abra o Terminal (em Aplicativos > Utilitários)
2. Digite o comando abaixo, substituindo o caminho pelo local onde você colocou o aplicativo:
   xattr -d com.apple.quarantine /Applications/Henpixy.app
3. Pressione Enter para executar o comando
4. Agora o aplicativo deve abrir normalmente

Para mais informações, visite: https://henpixy.lailsonhenrique.com
EOF

# Cria um atalho para a pasta Applications
echo "Criando atalho para Applications..."
ln -s /Applications "build/dmg/Applications"

# Define os parâmetros do DMG
DMG_PARAMS=(
    --volname "Henpixy Installer"
    --window-pos 200 120
    --window-size 800 400
    --icon-size 100
    --icon "Henpixy.app" 200 200
    --icon "Applications" 600 200
    --icon "README_INSTALACAO.txt" 400 320
    --hide-extension "Henpixy.app"
    --hide-extension "README_INSTALACAO.txt"
)

# Adiciona parâmetros opcionais se os arquivos existirem
if [ -f "resources/icon.icns" ]; then
    DMG_PARAMS+=(--volicon "resources/icon.icns")
fi

if [ -f "resources/dmg_background.png" ]; then
    echo "Usando imagem de fundo personalizada..."
    DMG_PARAMS+=(--background "resources/dmg_background.png")
fi

# Cria o .dmg
echo "Criando arquivo .dmg..."
create-dmg "${DMG_PARAMS[@]}" "dist/Henpixy-0.1.25.dmg" "build/dmg/"

# Verifica se o .dmg foi criado com sucesso
if [ -f "dist/Henpixy-0.1.25.dmg" ]; then
    echo "Sucesso! DMG criado em: dist/Henpixy-0.1.25.dmg"
else
    echo "Erro: Falha ao criar o arquivo DMG"
    exit 1
fi 