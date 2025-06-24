from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from pathlib import Path

# Alcances de permisos (solo lectura de archivos de Drive)
SCOPES = ['https://www.googleapis.com/auth/drive']

def conectar_drive(credentials_file='credentials.json', token_file='token.json'):
    """Conecta a Google Drive usando archivos en la raíz del proyecto o ruta especificada.

    Args:
        credentials_file (str): Nombre o ruta del archivo de credenciales.
        token_file (str): Nombre o ruta del archivo del token.

    Returns:
        Google Drive service object.
    """
    creds = None
    credentials_path = Path(credentials_file)
    token_path = Path(token_file)

    # Si ya existe un token de sesión previa, lo carga
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # Si no hay credenciales válidas, inicia el flujo de autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Guarda el token para reutilizarlo
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Crear el servicio de Drive
    service = build('drive', 'v3', credentials=creds)

    return service
