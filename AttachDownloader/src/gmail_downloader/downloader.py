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
from .config import ConfigManager


class GmailAttachmentDownloader:
    """Clase para descargar adjuntos de Gmail"""

    def __init__(self, credentials: Credentials, config: ConfigManager = None):
        """
        Inicializa el descargador

        Args:
            credentials: Credenciales de Gmail API
            config: Instancia de ConfigManager (si es None, carga la configuración por defecto)
        """
        self.config = config or ConfigManager()
        self.service = build("gmail", "v1", credentials=credentials)
        self.download_folder = self.config.download_folder
        self.download_folder.mkdir(parents=True, exist_ok=True)
        self.stats = {
            "total_emails": 0,
            "emails_with_attachments": 0,
            "files_downloaded": 0,
            "files_filtered": 0,
        }

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
            max_emails = self.config.max_emails_to_process
            
            results = self.service.users().messages().list(userId="me").execute()
            messages = results.get("messages", [])

            # Manejar paginación
            while "nextPageToken" in results:
                if max_emails > 0 and len(messages) >= max_emails:
                    break
                results = (
                    self.service.users()
                    .messages()
                    .list(userId="me", pageToken=results["nextPageToken"])
                    .execute()
                )
                messages.extend(results.get("messages", []))

            # Aplicar límite
            if max_emails > 0:
                messages = messages[:max_emails]

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
            
            # Filtrar por remitente si está configurado
            if self.config.whitelist_senders:
                sender_lower = sender.lower()
                if not any(allowed in sender_lower for allowed in self.config.whitelist_senders):
                    return
            
            if self.config.blacklist_senders:
                sender_lower = sender.lower()
                if any(blocked in sender_lower for blocked in self.config.blacklist_senders):
                    return
            
            # Obtener fecha del correo
            date_str = next(
                (h["value"] for h in headers if h["name"] == "Date"), None
            )
            email_date = self._parse_email_date(date_str) if date_str else datetime.now()

            # Filtrar por rango de fechas si está configurado
            if not self._is_date_in_range(email_date):
                return

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
            
            if not filename:
                return
            
            # Verificar extensión permitida
            if self.config.allowed_extensions:
                file_ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
                if file_ext not in self.config.allowed_extensions:
                    self.stats["files_filtered"] += 1
                    return
            
            # Aplicar filtros de lista blanca y negra
            filename_check = filename if self.config.case_sensitive_filters else filename.lower()
            
            # Verificar lista blanca
            if self.config.white_list:
                white_list = self.config.white_list if self.config.case_sensitive_filters else [w.lower() for w in self.config.white_list]
                if not any(word in filename_check for word in white_list):
                    self.stats["files_filtered"] += 1
                    return
            
            # Verificar lista negra
            if self.config.black_list:
                black_list = self.config.black_list if self.config.case_sensitive_filters else [b.lower() for b in self.config.black_list]
                if any(word in filename_check for word in black_list):
                    self.stats["files_filtered"] += 1
                    return
            
            # Extraer año y trimestre
            year = email_date.year
            trimester = self._get_trimester(email_date.month)
            
            # Obtener nombre de la carpeta del remitente
            sender_folder = sender
            if self.config.use_domain_only and "@" in sender:
                sender_folder = sender.split("@")[1].replace(">", "").strip()
            
            # Crear estructura: <download_folder>/<Año>/<Trimestre>/<Remitente>/
            folder_path = self.download_folder / str(year) / trimester / self._sanitize_filename(sender_folder)
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
                
                # Manejar duplicados si está configurado
                if filepath.exists() and self.config.add_timestamp_on_duplicate:
                    name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_filename = f"{name}_{timestamp}.{ext}" if ext else f"{name}_{timestamp}"
                    filepath = folder_path / self._sanitize_filename(new_filename)

                with open(filepath, "wb") as f:
                    f.write(data)

                if self.config.log_successful_downloads:
                    print(f"✅ Descargado: {filename} -> {filepath}")
                self.stats["files_downloaded"] += 1

        except Exception as e:
            print(f"⚠️ Error descargando adjunto {filename}: {e}")

    def _is_date_in_range(self, email_date: datetime) -> bool:
        """
        Verifica si la fecha del correo está dentro del rango configurado

        Args:
            email_date: Fecha del correo

        Returns:
            bool: True si la fecha está en rango o no hay rango configurado, False si está fuera
        """
        # Si no hay rango configurado, aceptar todas las fechas
        if not self.config.date_from and not self.config.date_to:
            return True
        
        try:
            # Convertir fecha del correo a naive si es aware para comparación consistente
            if email_date.tzinfo is not None:
                email_date = email_date.replace(tzinfo=None)
            
            # Parsear fecha_desde si está configurada
            if self.config.date_from:
                date_from = datetime.strptime(self.config.date_from, "%Y-%m-%d")
                if email_date < date_from:
                    return False
            
            # Parsear fecha_hasta si está configurada
            if self.config.date_to:
                date_to = datetime.strptime(self.config.date_to, "%Y-%m-%d")
                # Incluir todo el día: hasta las 23:59:59
                date_to = date_to.replace(hour=23, minute=59, second=59)
                if email_date > date_to:
                    return False
            
            return True
        except Exception as e:
            print(f"⚠️ Error al parsear rango de fechas: {e}")
            return True

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
        
        # Limitar longitud si está configurado
        max_length = 255  # Por defecto
        if len(filename) > max_length:
            if "." in filename:
                name, ext = filename.rsplit(".", 1)
                filename = name[: max_length - len(ext) - 1] + "." + ext
            else:
                filename = filename[:max_length]
        
        return filename
