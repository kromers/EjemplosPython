"""
AttachDownloader - Módulo de configuración
Gestiona la lectura y parseo del archivo config.cfg
"""

import os
from configparser import ConfigParser
from pathlib import Path
from typing import List, Optional, Dict, Any


class ConfigManager:
    """Gestor centralizado de configuración"""

    def __init__(self, config_file: str = "config/config.cfg"):
        """
        Inicializa el gestor de configuración

        Args:
            config_file: Ruta al archivo de configuración
        """
        self.config_file = Path(config_file)
        self.config = ConfigParser()
        self._load_config()

    def _load_config(self) -> None:
        """Carga y valida el archivo de configuración"""
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Archivo de configuración no encontrado: {self.config_file}\n"
                "Asegúrate de que config/config.cfg existe en el directorio del proyecto."
            )

        try:
            self.config.read(self.config_file)
        except Exception as e:
            raise ValueError(f"Error al parsear config.cfg: {e}")

    # ========================================================================
    # GENERAL
    # ========================================================================

    @property
    def project_name(self) -> str:
        """Nombre del proyecto"""
        return self._get("GENERAL", "project_name", "AttachDownloader")

    @property
    def version(self) -> str:
        """Versión del proyecto"""
        return self._get("GENERAL", "version", "1.0.0")

    @property
    def mode(self) -> str:
        """Modo de ejecución (debug o production)"""
        return self._get("GENERAL", "mode", "production")

    # ========================================================================
    # DOWNLOADS
    # ========================================================================

    @property
    def download_folder(self) -> Path:
        """Carpeta de descargas (relativa o absoluta)"""
        folder = self._get("DOWNLOADS", "download_folder", "./downloads")
        path = Path(folder).expanduser().resolve()
        return path

    @property
    def folder_structure(self) -> str:
        """Estructura de carpetas (year/trimester/sender)"""
        return self._get("DOWNLOADS", "folder_structure", "year/trimester/sender")

    @property
    def create_folders_if_not_exist(self) -> bool:
        """Crear carpetas automáticamente"""
        return self._get_bool("DOWNLOADS", "create_folders_if_not_exist", True)

    @property
    def max_folders_to_create(self) -> int:
        """Máximo de carpetas a crear (0 = sin límite)"""
        return self._get_int("DOWNLOADS", "max_folders_to_create", 0)

    # ========================================================================
    # GMAIL API
    # ========================================================================

    @property
    def credentials_file(self) -> Path:
        """Ruta al archivo de credenciales"""
        filename = self._get("GMAIL_API", "credentials_file", "credentials.json")
        return Path("config") / filename

    @property
    def token_file(self) -> Path:
        """Ruta al archivo de token"""
        filename = self._get("GMAIL_API", "token_file", "token.pickle")
        return Path("config") / filename

    @property
    def gmail_scopes(self) -> List[str]:
        """Ámbitos de Gmail API"""
        scopes_str = self._get(
            "GMAIL_API",
            "gmail_scopes",
            "https://www.googleapis.com/auth/gmail.readonly",
        )
        return [scope.strip() for scope in scopes_str.split(",")]

    @property
    def max_emails_to_process(self) -> int:
        """Máximo de correos a procesar (0 = todos)"""
        return self._get_int("GMAIL_API", "max_emails_to_process", 0)

    @property
    def max_attachments_to_download(self) -> int:
        """Máximo de adjuntos a descargar (0 = todos)"""
        return self._get_int("GMAIL_API", "max_attachments_to_download", 0)

    # ========================================================================
    # FILTERS
    # ========================================================================

    @property
    def allowed_extensions(self) -> List[str]:
        """Extensiones permitidas"""
        ext_str = self._get("FILTERS", "allowed_extensions", "pdf")
        if not ext_str.strip():
            return []
        return [ext.strip().lower() for ext in ext_str.split(",")]

    @property
    def white_list(self) -> List[str]:
        """Lista blanca de palabras clave"""
        wl_str = self._get("FILTERS", "white_list", "factura, invoice, receipt")
        if not wl_str.strip():
            return []
        return [word.strip().lower() for word in wl_str.split(",")]

    @property
    def black_list(self) -> List[str]:
        """Lista negra de palabras clave"""
        bl_str = self._get("FILTERS", "black_list", "proforma, draft, borrador, temporal")
        if not bl_str.strip():
            return []
        return [word.strip().lower() for word in bl_str.split(",")]

    @property
    def case_sensitive_filters(self) -> bool:
        """Filtros sensibles a mayúsculas"""
        return self._get_bool("FILTERS", "case_sensitive_filters", False)

    # ========================================================================
    # SENDERS
    # ========================================================================

    @property
    def whitelist_senders(self) -> List[str]:
        """Lista blanca de remitentes"""
        senders_str = self._get("SENDERS", "whitelist_senders", "")
        if not senders_str.strip():
            return []
        return [sender.strip().lower() for sender in senders_str.split(",")]

    @property
    def blacklist_senders(self) -> List[str]:
        """Lista negra de remitentes"""
        senders_str = self._get("SENDERS", "blacklist_senders", "noreply@, notification@")
        if not senders_str.strip():
            return []
        return [sender.strip().lower() for sender in senders_str.split(",")]

    @property
    def use_domain_only(self) -> bool:
        """Usar solo dominio en nombre de carpeta"""
        return self._get_bool("SENDERS", "use_domain_only", False)

    # ========================================================================
    # DATES
    # ========================================================================

    @property
    def date_format(self) -> str:
        """Formato de fecha"""
        return self._get("DATES", "date_format", "%Y-%m-%d")

    @property
    def use_email_date(self) -> bool:
        """Usar fecha del correo"""
        return self._get_bool("DATES", "use_email_date", True)

    @property
    def date_from(self) -> Optional[str]:
        """Fecha inicial de filtrado"""
        return self._get("DATES", "date_from", "") or None

    @property
    def date_to(self) -> Optional[str]:
        """Fecha final de filtrado"""
        return self._get("DATES", "date_to", "") or None

    # ========================================================================
    # SANITIZATION
    # ========================================================================

    @property
    def max_filename_length(self) -> int:
        """Longitud máxima de nombre de archivo"""
        return self._get_int("SANITIZATION", "max_filename_length", 255)

    @property
    def replace_spaces_with_underscores(self) -> bool:
        """Reemplazar espacios con guiones bajos"""
        return self._get_bool("SANITIZATION", "replace_spaces_with_underscores", False)

    @property
    def add_timestamp_on_duplicate(self) -> bool:
        """Agregar timestamp si el archivo existe"""
        return self._get_bool("SANITIZATION", "add_timestamp_on_duplicate", True)

    # ========================================================================
    # LOGGING
    # ========================================================================

    @property
    def log_level(self) -> str:
        """Nivel de logging"""
        return self._get("LOGGING", "log_level", "INFO")

    @property
    def log_file(self) -> Path:
        """Ubicación del archivo de log"""
        log_path = self._get("LOGGING", "log_file", "logs/attachdownloader.log")
        return Path(log_path)

    @property
    def console_output(self) -> bool:
        """Mostrar logs en consola"""
        return self._get_bool("LOGGING", "console_output", True)

    @property
    def log_successful_downloads(self) -> bool:
        """Registrar descargas exitosas"""
        return self._get_bool("LOGGING", "log_successful_downloads", True)

    # ========================================================================
    # NOTIFICATIONS
    # ========================================================================

    @property
    def send_notification(self) -> bool:
        """Enviar notificación al terminar"""
        return self._get_bool("NOTIFICATIONS", "send_notification", False)

    @property
    def notification_type(self) -> str:
        """Tipo de notificación (email, slack, webhook)"""
        return self._get("NOTIFICATIONS", "notification_type", "email")

    @property
    def notification_recipient(self) -> str:
        """Destinatario o webhook URL"""
        return self._get("NOTIFICATIONS", "notification_recipient", "")

    # ========================================================================
    # ADVANCED
    # ========================================================================

    @property
    def execution_mode(self) -> str:
        """Modo de ejecución (full o incremental)"""
        return self._get("ADVANCED", "execution_mode", "full")

    @property
    def retry_attempts(self) -> int:
        """Intentos de reintento"""
        return self._get_int("ADVANCED", "retry_attempts", 3)

    @property
    def connection_timeout(self) -> int:
        """Timeout de conexión (segundos)"""
        return self._get_int("ADVANCED", "connection_timeout", 30)

    # ========================================================================
    # BACKUP
    # ========================================================================

    @property
    def backup_folder(self) -> Path:
        """Carpeta de backup"""
        folder = self._get("BACKUP", "backup_folder", "./backups")
        return Path(folder).expanduser().resolve()

    @property
    def compress_downloads(self) -> bool:
        """Comprimir descargas en ZIP"""
        return self._get_bool("BACKUP", "compress_downloads", False)

    # ========================================================================
    # UTILIDADES PRIVADAS
    # ========================================================================

    def _get(self, section: str, option: str, default: str = "") -> str:
        """Obtiene valor de configuración (string)"""
        try:
            return self.config.get(section, option)
        except Exception:
            return default

    def _get_bool(self, section: str, option: str, default: bool = False) -> bool:
        """Obtiene valor de configuración (booleano)"""
        try:
            value = self.config.get(section, option).lower().strip()
            return value in ("true", "1", "yes", "on")
        except Exception:
            return default

    def _get_int(self, section: str, option: str, default: int = 0) -> int:
        """Obtiene valor de configuración (entero)"""
        try:
            return int(self.config.get(section, option))
        except Exception:
            return default

    def to_dict(self) -> Dict[str, Any]:
        """Convierte toda la configuración a diccionario"""
        return {
            # GENERAL
            "project_name": self.project_name,
            "version": self.version,
            "mode": self.mode,
            # DOWNLOADS
            "download_folder": str(self.download_folder),
            "folder_structure": self.folder_structure,
            "create_folders_if_not_exist": self.create_folders_if_not_exist,
            # GMAIL_API
            "credentials_file": str(self.credentials_file),
            "token_file": str(self.token_file),
            "gmail_scopes": self.gmail_scopes,
            "max_emails_to_process": self.max_emails_to_process,
            # FILTERS
            "allowed_extensions": self.allowed_extensions,
            "white_list": self.white_list,
            "black_list": self.black_list,
            "case_sensitive_filters": self.case_sensitive_filters,
            # SENDERS
            "whitelist_senders": self.whitelist_senders,
            "blacklist_senders": self.blacklist_senders,
            # LOGGING
            "log_level": self.log_level,
            "log_file": str(self.log_file),
        }

    def print_summary(self) -> None:
        """Imprime un resumen de la configuración actual"""
        print("\n" + "=" * 70)
        print("⚙️  CONFIGURACIÓN ACTUAL")
        print("=" * 70)
        print(f"Proyecto: {self.project_name} v{self.version}")
        print(f"Modo: {self.mode}")
        print(f"Carpeta de descargas: {self.download_folder}")
        print(f"Estructura: {self.folder_structure}")
        print(f"Extensiones permitidas: {self.allowed_extensions if self.allowed_extensions else 'todas'}")
        print(f"Lista blanca: {self.white_list if self.white_list else 'ninguna'}")
        print(f"Lista negra: {self.black_list if self.black_list else 'ninguna'}")
        if self.whitelist_senders:
            print(f"Remitentes (incluir): {self.whitelist_senders}")
        print("=" * 70 + "\n")
