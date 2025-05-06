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
    <string>0.1.24</string>
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
    --hide-extension "Henpixy.app"
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
create-dmg "${DMG_PARAMS[@]}" "dist/Henpixy-0.1.24.dmg" "build/dmg/"

# Verifica se o .dmg foi criado com sucesso
if [ -f "dist/Henpixy-0.1.24.dmg" ]; then
    echo "Sucesso! DMG criado em: dist/Henpixy-0.1.24.dmg"
else
    echo "Erro: Falha ao criar o arquivo DMG"
    exit 1
fi 