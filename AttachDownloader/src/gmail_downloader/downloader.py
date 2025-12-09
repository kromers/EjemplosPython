"""
AttachDownloader - Módulo para descargar y organizar adjuntos de Gmail
Estructura inteligente: <Año>/<Trimestre>/<Remitente>/
"""

import base64
import os
from typing import List
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class GmailAttachmentDownloader:
    """Clase para descargar adjuntos de Gmail"""

    def __init__(self, credentials: Credentials, download_folder: str = "downloads"):
        """
        Inicializa el descargador

        Args:
            credentials: Credenciales de Gmail API
            download_folder: Carpeta donde guardar los adjuntos
        """
        self.service = build("gmail", "v1", credentials=credentials)
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(exist_ok=True)
        self.stats = {"total_emails": 0, "emails_with_attachments": 0, "files_downloaded": 0}

    def download_all_attachments(self) -> dict:
        """
        Descarga todos los adjuntos de todos los correos

        Returns:
            dict: Estadísticas de la descarga
        """
        try:
            # Obtener lista de mensajes
            messages = self._get_all_messages()
            print(f"📧 Total de correos encontrados: {len(messages)}")
            self.stats["total_emails"] = len(messages)

            # Procesar cada mensaje
            for msg_id in messages:
                self._download_message_attachments(msg_id)

            return self.stats

        except Exception as e:
            print(f"❌ Error al descargar adjuntos: {e}")
            raise

    def _get_all_messages(self) -> List[str]:
        """
        Obtiene IDs de todos los mensajes

        Returns:
            List[str]: Lista de IDs de mensajes
        """
        try:
            results = self.service.users().messages().list(userId="me").execute()
            messages = results.get("messages", [])

            # Manejar paginación
            while "nextPageToken" in results:
                results = (
                    self.service.users()
                    .messages()
                    .list(userId="me", pageToken=results["nextPageToken"])
                    .execute()
                )
                messages.extend(results.get("messages", []))

            return [msg["id"] for msg in messages]

        except Exception as e:
            print(f"❌ Error al obtener mensajes: {e}")
            return []

    def _download_message_attachments(self, msg_id: str) -> None:
        """
        Descarga adjuntos de un mensaje específico

        Args:
            msg_id: ID del mensaje
        """
        try:
            message = self.service.users().messages().get(userId="me", id=msg_id).execute()
            headers = message["payload"].get("headers", [])

            # Obtener asunto y remitente
            subject = next(
                (h["value"] for h in headers if h["name"] == "Subject"), "Sin asunto"
            )
            sender = next((h["value"] for h in headers if h["name"] == "From"), "Desconocido")
            
            # Obtener fecha del correo
            date_str = next(
                (h["value"] for h in headers if h["name"] == "Date"), None
            )
            email_date = self._parse_email_date(date_str) if date_str else datetime.now()

            # Procesar partes del mensaje
            parts = message["payload"].get("parts", [])
            if not parts:
                # Sin partes, no hay adjuntos
                return

            has_attachments = False
            for part in parts:
                if part["filename"]:
                    has_attachments = True
                    self._download_attachment(part, msg_id, subject, sender, email_date)

            if has_attachments:
                self.stats["emails_with_attachments"] += 1

        except Exception as e:
            print(f"⚠️ Error procesando mensaje {msg_id}: {e}")

    def _download_attachment(self, part: dict, msg_id: str, subject: str, sender: str, email_date: datetime) -> None:
        """
        Descarga un adjunto específico

        Args:
            part: Parte del mensaje con adjunto
            msg_id: ID del mensaje
            subject: Asunto del correo
            sender: Remitente del correo
            email_date: Fecha del correo
        """
        try:
            filename = part["filename"]
            
            if filename and filename.lower().endswith('.pdf'):
                # Listas de filtrado
                white_list = ["factura", "invoice"]
                black_list = ["proforma"]
                
                filename_lower = filename.lower()
                
                # Verificar que contiene una palabra de la whitelist y no contiene palabras de la blacklist
                has_white_list_word = any(word in filename_lower for word in white_list)
                has_black_list_word = any(word in filename_lower for word in black_list)
                
                if not (has_white_list_word and not has_black_list_word):
                    return
                
                # Extraer año y trimestre
                year = email_date.year
                trimester = self._get_trimester(email_date.month)
                
                # Crear estructura: adjuntos/<Año>/<Trimestre>/<Remitente>/
                folder_path = self.download_folder / str(year) / trimester / self._sanitize_filename(sender)
                folder_path.mkdir(parents=True, exist_ok=True)

                # Obtener datos del adjunto
                att_id = part["body"].get("attachmentId")
                if att_id:
                    attachment = (
                        self.service.users()
                        .messages()
                        .attachments()
                        .get(userId="me", messageId=msg_id, id=att_id)
                        .execute()
                    )

                    data = base64.urlsafe_b64decode(attachment["data"])
                    filepath = folder_path / self._sanitize_filename(filename)

                    with open(filepath, "wb") as f:
                        f.write(data)

                    print(f"✅ Descargado: {filename} -> {filepath}")
                    self.stats["files_downloaded"] += 1

        except Exception as e:
            print(f"⚠️ Error descargando adjunto {filename}: {e}")

    @staticmethod
    def _get_trimester(month: int) -> str:
        """
        Obtiene el trimestre basado en el mes

        Args:
            month: Número del mes (1-12)

        Returns:
            str: Trimestre (Q1, Q2, Q3, Q4)
        """
        trimester_map = {
            1: "T1", 2: "T1", 3: "T1",
            4: "T2", 5: "T2", 6: "T2",
            7: "T3", 8: "T3", 9: "T3",
            10: "T4", 11: "T4", 12: "T4"
        }
        return trimester_map.get(month, "T1")

    @staticmethod
    def _parse_email_date(date_str: str) -> datetime:
        """
        Parsea la fecha del correo en formato RFC 2822

        Args:
            date_str: Fecha en formato RFC 2822 (ej: "Mon, 15 Dec 2024 10:30:45 +0000")

        Returns:
            datetime: Objeto datetime con la fecha
        """
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except Exception:
            return datetime.now()

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """
        Sanitiza nombres de archivo para evitar caracteres inválidos

        Args:
            filename: Nombre original

        Returns:
            str: Nombre sanitizado
        """
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        return filename
