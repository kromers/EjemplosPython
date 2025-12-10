#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AttachDownloader - Herramienta profesional para descargar y organizar adjuntos de Gmail
Estructura inteligente: <Año>/<Trimestre>/<Remitente>/
"""

import sys
from pathlib import Path

# Añadir el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from gmail_downloader.auth import GmailAuthenticator
from gmail_downloader.downloader import GmailAttachmentDownloader
from gmail_downloader.config import ConfigManager


def main():
    """Función principal"""
    print("=" * 90)
    print("🚀 AttachDownloader - Descargador inteligente de adjuntos de Gmail")
    print("     NOTA IMPORTAMTE:")
    print("     Sólo Ricardo Atienza tiene autorización para usar este software.")
    print("     Para autorizar su uso a otra persona u empresa, contacta con kromersoft@gmail.com")
    print("=" * 90)

    try:
        # Paso 0: Cargar configuración
        print("\n⚙️  Cargando configuración...")
        config = ConfigManager()
        config.print_summary()
        
        # Paso 1: Autenticación
        print("📝 Autenticando con Gmail API...")
        authenticator = GmailAuthenticator(config)
        credentials = authenticator.authenticate()
        print("✅ Autenticación exitosa")

        # Paso 2: Descargar adjuntos
        print("\n📥 Iniciando descarga de adjuntos...")
        print(f"   📂 Carpeta destino: {config.download_folder}")
        print(f"   📋 Estructura: {config.folder_structure}")
        print(f"   🔍 Filtros: {config.white_list if config.white_list else 'ninguno'}")
        
        # Mostrar rango de fechas si está configurado
        if config.date_from or config.date_to:
            date_range = f"{config.date_from or '∞'} → {config.date_to or '∞'}"
            print(f"   📅 Rango de fechas: {date_range}")
        
        downloader = GmailAttachmentDownloader(credentials, config)
        stats = downloader.download_all_attachments()

        # Paso 3: Mostrar resultados
        print("\n" + "=" * 70)
        print("📊 ESTADÍSTICAS DE DESCARGA:")
        print("=" * 70)
        print(f"📧 Total de correos procesados: {stats['total_emails']}")
        print(f"📎 Correos con adjuntos: {stats['emails_with_attachments']}")
        print(f"✅ Archivos descargados: {stats['files_downloaded']}")
        print(f"⏭️  Archivos filtrados: {stats.get('files_filtered', 0)}")
        print("=" * 70)
        print("✨ ¡Descarga completada con éxito!")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📌 Pasos para configurar:")
        print("1. Visita: https://console.cloud.google.com/")
        print("2. Crea un nuevo proyecto")
        print("3. Habilita Gmail API")
        print("4. Crea credenciales OAuth 2.0 (Aplicación de escritorio)")
        print("5. Descarga el archivo JSON y guárdalo como:")
        print("   → Ubicación: AttachDownloader/config/credentials.json")
        print("\n6. Edita config/config.cfg con tus preferencias de filtrado")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()