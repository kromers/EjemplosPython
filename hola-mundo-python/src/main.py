#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gmail Attachment Downloader
Script principal para descargar adjuntos de Gmail
"""

import sys
from pathlib import Path

# Añadir el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from gmail_downloader.auth import GmailAuthenticator
from gmail_downloader.downloader import GmailAttachmentDownloader


def main():
    """Función principal"""
    print("=" * 50)
    print("🚀 Gmail Attachment Downloader")
    print("=" * 50)

    try:
        # Paso 1: Autenticación
        print("\n📝 Autenticando con Gmail API...")
        authenticator = GmailAuthenticator()
        credentials = authenticator.authenticate()
        print("✅ Autenticación exitosa")

        # Paso 2: Descargar adjuntos
        print("\n📥 Iniciando descarga de adjuntos...")
        downloader = GmailAttachmentDownloader(
            credentials, download_folder="downloads"
        )
        stats = downloader.download_all_attachments()

        # Paso 3: Mostrar resultados
        print("\n" + "=" * 50)
        print("📊 Estadísticas de descarga:")
        print("=" * 50)
        print(f"Total de correos: {stats['total_emails']}")
        print(f"Correos con adjuntos: {stats['emails_with_attachments']}")
        print(f"Archivos descargados: {stats['files_downloaded']}")
        print("=" * 50)
        print("✅ ¡Descarga completada!")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📌 Pasos para configurar:")
        print("1. Visita: https://console.cloud.google.com/")
        print("2. Crea un nuevo proyecto")
        print("3. Habilita Gmail API")
        print("4. Crea credenciales OAuth 2.0 (Aplicación de escritorio)")
        print("5. Descarga el archivo JSON y guárdalo como config/credentials.json")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()