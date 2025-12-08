"""
Módulo de autenticación para Gmail API
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow


class GmailAuthenticator:
    """Clase para manejar la autenticación con Gmail API"""

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    TOKEN_FILE = "config/token.pickle"
    # CREDENTIALS_FILE = "config/credentials.json"
    CREDENTIALS_FILE = "config/GmailKromers_credentials.json"

    def __init__(self, credentials_file: str = CREDENTIALS_FILE):
        """
        Inicializa el autenticador

        Args:
            credentials_file: Ruta al archivo de credenciales JSON
        """
        self.credentials_file = credentials_file
        self.creds = None

    def authenticate(self) -> Credentials:
        """
        Autentica con Gmail API

        Returns:
            Credentials: Objeto de credenciales autenticado
        """
        # Cargar token existente si está disponible
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, "rb") as token:
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
            with open(self.TOKEN_FILE, "wb") as token:
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
            self.credentials_file, self.SCOPES
        )
        self.creds = flow.run_local_server(port=0)
