"""
Módulo para descargar adjuntos de Gmail
"""

import base64
import os
from typing import List
from pathlib import Path
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

            # Procesar partes del mensaje
            parts = message["payload"].get("parts", [])
            if not parts:
                # Sin partes, no hay adjuntos
                return

            has_attachments = False
            for part in parts:
                if part["filename"]:
                    has_attachments = True
                    self._download_attachment(part, msg_id, subject, sender)

            if has_attachments:
                self.stats["emails_with_attachments"] += 1

        except Exception as e:
            print(f"⚠️ Error procesando mensaje {msg_id}: {e}")

    def _download_attachment(self, part: dict, msg_id: str, subject: str, sender: str) -> None:
        """
        Descarga un adjunto específico

        Args:
            part: Parte del mensaje con adjunto
            msg_id: ID del mensaje
            subject: Asunto del correo
            sender: Remitente del correo
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
                
                # Crear carpeta con nombre del remitente
                sender_folder = self.download_folder / self._sanitize_filename(sender)
                sender_folder.mkdir(exist_ok=True)

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
                    filepath = sender_folder / self._sanitize_filename(filename)

                    with open(filepath, "wb") as f:
                        f.write(data)

                    print(f"✅ Descargado: {filename} -> {filepath}")
                    self.stats["files_downloaded"] += 1

        except Exception as e:
            print(f"⚠️ Error descargando adjunto {filename}: {e}")

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
