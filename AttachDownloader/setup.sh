#!/bin/bash

# Script de configuración inicial para Gmail Downloader

echo "🚀 Configuración inicial de Gmail Attachment Downloader"
echo "========================================================"
echo ""

# Crear entorno virtual
echo "1️⃣ Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo ""
echo "2️⃣ Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Configuración inicial completada!"
echo ""
echo "📌 Próximos pasos:"
echo "1. Ve a https://console.cloud.google.com/"
echo "2. Crea un nuevo proyecto"
echo "3. Habilita Gmail API"
echo "4. Crea credenciales OAuth 2.0 (Aplicación de escritorio)"
echo "5. Descarga el archivo JSON y guárdalo como config/credentials.json"
echo ""
echo "📝 Después, ejecuta:"
echo "   source venv/bin/activate"
echo "   python src/main.py"
echo ""
