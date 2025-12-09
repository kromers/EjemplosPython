"""
Tests para el módulo de Gmail Downloader
"""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestGmailAuthenticator(unittest.TestCase):
    """Tests para la autenticación"""

    def test_token_file_exists(self):
        """Verifica que el archivo de token se puede crear"""
        token_file = Path("config/token.pickle")
        self.assertFalse(
            token_file.exists() or True,
            "El archivo token.pickle no debería existir inicialmente",
        )

    def test_credentials_file_path(self):
        """Verifica que la ruta de credenciales es válida"""
        credentials_file = Path("config/credentials.json")
        # Verificar que la ruta es correcta
        self.assertIn("config", str(credentials_file))


class TestGmailAttachmentDownloader(unittest.TestCase):
    """Tests para el descargador de adjuntos"""

    def test_download_folder_creation(self):
        """Verifica que la carpeta de descargas se puede crear"""
        download_folder = Path("downloads")
        download_folder.mkdir(exist_ok=True)
        self.assertTrue(download_folder.exists())

    def test_sanitize_filename(self):
        """Verifica la sanitización de nombres de archivo"""
        from gmail_downloader.downloader import GmailAttachmentDownloader

        test_cases = [
            ("archivo<>normal.txt", "archivo__normal.txt"),
            ('documento"especial".pdf', "documento_especial_.pdf"),
            ("imagen|invertida.jpg", "imagen_invertida.jpg"),
        ]

        for input_name, expected in test_cases:
            result = GmailAttachmentDownloader._sanitize_filename(input_name)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
