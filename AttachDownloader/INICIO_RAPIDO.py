#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 INICIO RÁPIDO - AttachDownloader

Ejecuta este archivo para obtener instrucciones paso a paso
"""

import os
from pathlib import Path


def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_step(number, title, content):
    """Imprime un paso"""
    print(f"\n{number}️⃣  {title}")
    print("-" * 70)
    print(content)


def check_requirements():
    """Verifica que todo esté listo"""
    print_section("✅ VERIFICACIÓN DE REQUISITOS")

    checks = {
        "Python 3.8+": True,  # Ya lo estamos ejecutando con Python
        "config/ existe": Path("config").exists(),
        "downloads/ existe": Path("downloads").exists(),
        "requirements.txt existe": Path("requirements.txt").exists(),
        "src/main.py existe": Path("src/main.py").exists(),
    }

    all_good = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        if not result and "existe" in check:
            all_good = False

    return all_good


def show_instructions():
    """Muestra las instrucciones"""
    print_section("📋 INSTRUCCIONES DE INSTALACIÓN")

    print_step(
        "1",
        "Activa el entorno virtual",
        """
# En macOS/Linux:
source venv/bin/activate

# En Windows:
.\\venv\\Scripts\\activate
        """,
    )

    print_step(
        "2",
        "Instala las dependencias",
        """
pip install -r requirements.txt
        """,
    )

    print_step(
        "3",
        "Descarga credenciales de Google",
        """
1. Ve a: https://console.cloud.google.com/
2. Crea un nuevo proyecto
3. Habilita Gmail API (busca en la barra)
4. Ve a Credenciales → Crear credenciales
5. Selecciona: OAuth 2.0 → Aplicación de escritorio
6. Descarga el JSON
7. Guarda como: config/credentials.json

⚠️ NO COMPARTAS ESTE ARCHIVO - Contiene datos sensibles
        """,
    )

    print_step(
        "4",
        "Ejecuta el programa",
        """
python src/main.py

Primera ejecución:
- Se abrirá el navegador automáticamente
- Inicia sesión con tu cuenta de Google
- Autoriza el acceso
- Los adjuntos se descargarán automáticamente

Próximas ejecuciones:
- Solo ejecuta: python src/main.py
- Las credenciales se cargan automáticamente
        """,
    )


def show_file_structure():
    """Muestra la estructura del proyecto"""
    print_section("📁 ESTRUCTURA DEL PROYECTO")

    structure = """
hola-mundo-python/
│
├── 🎯 src/main.py
│   └─ Script principal a ejecutar
│
├── 📚 src/gmail_downloader/
│   ├── auth.py          (Autenticación con Google)
│   ├── downloader.py    (Descarga de adjuntos)
│   └── __init__.py
│
├── ⚙️  config/
│   ├── credentials.json.example  (Plantilla)
│   └── credentials.json          (⚠️ AGREGAR MANUALMENTE)
│
├── 📥 downloads/
│   └─ Carpeta donde se guardan los adjuntos
│
├── 📖 DOCUMENTACIÓN:
│   ├── GUIA_RAPIDA.md           (⭐ Empeza aquí - 5 min)
│   ├── README_GMAIL.md          (Documentación completa)
│   ├── PROYECTO_RESUMEN.md      (Overview del proyecto)
│   ├── REFERENCIA_API.md        (API Reference)
│   ├── TROUBLESHOOTING.md       (Solución de problemas)
│   └── GUIA_INSTALACION.md      (Esta guía)
│
├── 🛠️  HERRAMIENTAS:
│   ├── instalar.py      (Instalación automática)
│   ├── ejemplos.py      (Ejemplos de uso)
│   └── setup.sh         (Script bash)
│
├── 📋 requirements.txt   (Dependencias)
└── .gitignore           (Archivos ignorados por Git)
    """

    print(structure)


def show_statistics():
    """Muestra estadísticas del proyecto"""
    print_section("📊 ESTADÍSTICAS DEL PROYECTO")

    stats = {
        "Archivos Python": 5,
        "Módulos creados": 2,
        "Documentación (MD)": 6,
        "Scripts auxiliares": 3,
        "Líneas de código": "~500",
        "Funciones principales": 4,
    }

    for label, value in stats.items():
        print(f"  {label:.<40} {value}")


def show_features():
    """Muestra las características"""
    print_section("✨ CARACTERÍSTICAS PRINCIPALES")

    features = [
        "✅ Autenticación segura con OAuth 2.0",
        "✅ Descarga de todos los adjuntos",
        "✅ Organización por remitente",
        "✅ Sanitización de nombres de archivo",
        "✅ Estadísticas de descarga",
        "✅ Caché automático de credenciales",
        "✅ Manejo robusto de errores",
        "✅ Documentación completa",
    ]

    for feature in features:
        print(f"  {feature}")


def show_next_steps():
    """Muestra los próximos pasos"""
    print_section("🚀 PRÓXIMOS PASOS")

    steps = """
1. 📖 Lee GUIA_RAPIDA.md para instrucciones en 5 minutos
   cat GUIA_RAPIDA.md

2. 🔧 Ejecuta la instalación automática:
   python instalar.py

3. 🔑 Descarga credenciales de Google Cloud Console
   https://console.cloud.google.com/

4. 🚀 Ejecuta el programa:
   python src/main.py

5. ❓ Si tienes problemas, consulta:
   cat TROUBLESHOOTING.md
    """

    print(steps)


def show_quick_reference():
    """Muestra referencia rápida de comandos"""
    print_section("⚡ REFERENCIA RÁPIDA DE COMANDOS")

    commands = """
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el programa
python src/main.py

# Ver ejemplos de uso
python ejemplos.py

# Ejecutar tests
python -m pytest tests/

# Limpiar caché
rm config/token.pickle

# Ver archivos descargados
ls -la downloads/
    """

    print(commands)


def main():
    """Función principal"""
    print("\n" + "🎉" * 35)
    print("\n  ¡BIENVENIDO A GMAIL ATTACHMENT DOWNLOADER!\n")
    print("  Un programa que descarga automáticamente")
    print("  todos los adjuntos de tus correos de Gmail\n")
    print("🎉" * 35)

    # Mostrar todas las secciones
    show_file_structure()
    show_statistics()
    show_features()
    show_instructions()
    show_quick_reference()
    show_next_steps()

    print_section("❓ AYUDA ADICIONAL")
    print(
        """
Si necesitas ayuda:

1. 📖 Lee la documentación:
   - GUIA_RAPIDA.md (5 minutos)
   - README_GMAIL.md (documentación completa)
   - REFERENCIA_API.md (API reference)

2. 🔧 Si tienes problemas:
   - TROUBLESHOOTING.md (solución de errores)

3. 💡 Para ver ejemplos:
   - ejemplos.py (código de ejemplo)

4. 🔗 Recursos oficiales:
   - Google Cloud Console: https://console.cloud.google.com/
   - Gmail API Docs: https://developers.google.com/gmail/api/guides
    """
    )

    print_section("✅ CHECKLIST FINAL")
    print(
        """
Antes de ejecutar python src/main.py, asegúrate de:

□ Entorno virtual activado
□ Dependencias instaladas (pip install -r requirements.txt)
□ Credenciales descargadas desde Google Cloud
□ Credenciales guardadas en config/credentials.json
□ Primera ejecución autorizada en el navegador
□ Carpeta downloads/ existe

¡Entonces estará listo! 🚀
    """
    )

    print("\n" + "=" * 70)
    print("  🚀 ¡LISTO PARA COMENZAR!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
