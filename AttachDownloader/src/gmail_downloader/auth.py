"""
AttachDownloader - Módulo de autenticación para Gmail API
Gestión segura de credenciales OAuth 2.0
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from .config import ConfigManager


class GmailAuthenticator:
    """Clase para manejar la autenticación con Gmail API"""

    def __init__(self, config: ConfigManager = None):
        """
        Inicializa el autenticador

        Args:
            config: Instancia de ConfigManager (si es None, carga la configuración por defecto)
        """
        self.config = config or ConfigManager()
        self.credentials_file = str(self.config.credentials_file)
        self.token_file = str(self.config.token_file)
        self.scopes = self.config.gmail_scopes
        self.creds = None

    def authenticate(self) -> Credentials:
        """
        Autentica con Gmail API

        Returns:
            Credentials: Objeto de credenciales autenticado
        """
        # Cargar token existente si está disponible
        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                self.creds = pickle.load(token)

        # Si no hay credenciales válidas, obtener nuevas
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except RefreshError:
                    self._authorize_new()
            else:
                self._authorize_new()

            # Guardar credenciales para próximas ejecuciones
            with open(self.token_file, "wb") as token:
                pickle.dump(self.creds, token)

        return self.creds

    def _authorize_new(self) -> None:
        """Realiza una nueva autorización interactiva"""
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"El archivo {self.credentials_file} no existe. "
                "Descárgalo desde Google Cloud Console."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_file, self.scopes
        )
        self.creds = flow.run_local_server(port=0)
