#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejemplo alternativo de uso del Gmail Downloader
Demuestra diferentes formas de usar la librería
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from gmail_downloader.auth import GmailAuthenticator
from gmail_downloader.downloader import GmailAttachmentDownloader


def ejemplo_basico():
    """Ejemplo básico: descargar todos los adjuntos"""
    print("📌 Ejemplo 1: Descarga básica")
    print("-" * 40)

    try:
        authenticator = GmailAuthenticator()
        credentials = authenticator.authenticate()

        downloader = GmailAttachmentDownloader(credentials)
        stats = downloader.download_all_attachments()

        print(f"✅ Descargados {stats['files_downloaded']} archivos")

    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_carpeta_personalizada():
    """Ejemplo 2: Descargar a una carpeta personalizada"""
    print("\n📌 Ejemplo 2: Carpeta personalizada")
    print("-" * 40)

    try:
        authenticator = GmailAuthenticator()
        credentials = authenticator.authenticate()

        # Descargar a una carpeta específica
        downloader = GmailAttachmentDownloader(
            credentials, download_folder="adjuntos_personalizados"
        )
        stats = downloader.download_all_attachments()

        print(f"✅ Archivos guardados en: adjuntos_personalizados/")
        print(f"   Total: {stats['files_downloaded']} archivos")

    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_con_estadisticas():
    """Ejemplo 3: Análisis detallado"""
    print("\n📌 Ejemplo 3: Análisis detallado")
    print("-" * 40)

    try:
        authenticator = GmailAuthenticator()
        credentials = authenticator.authenticate()

        downloader = GmailAttachmentDownloader(credentials)
        stats = downloader.download_all_attachments()

        # Mostrar estadísticas personalizadas
        print(f"📊 Estadísticas:")
        print(f"   - Correos procesados: {stats['total_emails']}")
        print(f"   - Con adjuntos: {stats['emails_with_attachments']}")
        print(f"   - Archivos: {stats['files_downloaded']}")

        # Calcular porcentaje
        if stats['total_emails'] > 0:
            porcentaje = (
                stats['emails_with_attachments'] / stats['total_emails'] * 100
            )
            print(f"   - Porcentaje: {porcentaje:.1f}%")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("📚 Ejemplos de uso - Gmail Attachment Downloader")
    print("=" * 50)

    # Ejecutar ejemplos
    # Descomenta el que quieras usar:

    # ejemplo_basico()
    # ejemplo_carpeta_personalizada()
    # ejemplo_con_estadisticas()

    print("\n💡 Descomenta en el código el ejemplo que quieras ejecutar")
    print("=" * 50)
