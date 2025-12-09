#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de instalación interactivo para AttachDownloader
Realiza los primeros pasos automáticamente
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n📌 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - ¡Completado!")
            return True
        else:
            print(f"❌ {description} - Error:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🚀 INSTALACIÓN DE GMAIL ATTACHMENT DOWNLOADER")
    print("=" * 60)

    # Obtener directorio actual
    current_dir = Path(__file__).parent

    # Paso 1: Crear entorno virtual
    print("\n1️⃣ Creando entorno virtual...")
    venv_dir = current_dir / "venv"

    if not venv_dir.exists():
        run_command("python3 -m venv venv", "Crear entorno virtual")
    else:
        print("ℹ️ Entorno virtual ya existe")

    # Paso 2: Instalar dependencias
    if sys.platform == "darwin":  # macOS
        pip_cmd = "./venv/bin/pip"
    else:
        pip_cmd = ".\\venv\\Scripts\\pip" if sys.platform == "win32" else "./venv/bin/pip"

    print("\n2️⃣ Instalando dependencias...")
    run_command(f"{pip_cmd} install --upgrade pip", "Actualizar pip")
    run_command(f"{pip_cmd} install -r requirements.txt", "Instalar dependencias")

    # Paso 3: Crear carpetas necesarias
    print("\n3️⃣ Creando estructura de carpetas...")
    (current_dir / "config").mkdir(exist_ok=True)
    (current_dir / "downloads").mkdir(exist_ok=True)
    print("✅ Carpetas creadas")

    # Paso 4: Información sobre credenciales
    print("\n4️⃣ Configuración de Google Cloud")
    print("=" * 60)
    print(
        """
⚠️  PASO IMPORTANTE - Sigue estas instrucciones:

1. Ve a: https://console.cloud.google.com/
2. Crea un nuevo proyecto
3. Busca y habilita: "Gmail API"
4. Ve a "Credenciales" en el menú lateral
5. Haz clic en "Crear credenciales"
   → "ID de cliente OAuth 2.0"
   → "Aplicación de escritorio"
6. Descarga el archivo JSON
7. Guarda el archivo como: config/credentials.json

⚠️  NO COMPARTAS ESTE ARCHIVO - Contiene datos sensibles
    """
    )

    # Paso 5: Verificar credenciales
    credentials_file = current_dir / "config" / "credentials.json"
    if credentials_file.exists():
        print("✅ Archivo credentials.json encontrado")
    else:
        print("❌ Archivo credentials.json NO encontrado")
        print("   Descárgalo desde Google Cloud Console")

    # Paso 6: Resumen
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE INSTALACIÓN")
    print("=" * 60)
    print("""
✅ Entorno virtual creado
✅ Dependencias instaladas
✅ Carpetas creadas

📝 PRÓXIMOS PASOS:

1. Descarga credentials.json desde Google Cloud
2. Guarda como: config/credentials.json
3. Ejecuta:
   - source venv/bin/activate  (macOS/Linux)
   - .\\venv\\Scripts\\activate (Windows)
   - python src/main.py

💡 Para más información:
   - Lee GUIA_RAPIDA.md para instrucciones rápidas
   - Lee README_GMAIL.md para documentación completa
   - Lee PROYECTO_RESUMEN.md para overview del proyecto
    """)

    print("=" * 60)
    print("🎉 ¡Instalación completada!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
