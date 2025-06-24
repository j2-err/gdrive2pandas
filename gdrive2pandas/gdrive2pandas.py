from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
import io
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from pathlib import Path
import pandas as pd


# Alcances de permisos (puedes personalizar)
SCOPES = ['https://www.googleapis.com/auth/drive']

def conectar_drive():
    """Conecta a Google Drive buscando archivos en la raíz del proyecto donde el usuario ejecuta el script."""

    creds = None

    # Buscar archivos en la carpeta donde el usuario ejecuta el código
    base_path = Path.cwd()
    credentials_path = base_path / 'credentials.json'
    token_path = base_path / 'token.json'

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






drive_service = conectar_drive()


def listar_archivos(carpeta_id:str):
    archivos = []
    page_token = None

    while True:
        response = drive_service.files().list(
            q=f"'{carpeta_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000,
            pageToken=page_token
        ).execute()

        archivos.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)

        if page_token is None:
            break

    return archivos

def drive_a_dataframe(archivo_id: str):
    request = drive_service.files().get_media(fileId=archivo_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    file.seek(0)

    # Leer directo a pandas
    df = pd.read_excel(file)
    print('Archivo leído correctamente')
    return df


#print(f"Archivos encontrados en la carpeta: {archivos}")