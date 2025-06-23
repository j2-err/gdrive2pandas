from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


import os

# Alcances de permisos (solo lectura de archivos de Drive)
SCOPES = ['https://www.googleapis.com/auth/drive']

def conectar_drive():
    creds = None

    # Si ya existe un token de sesión previa, lo carga
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Si no hay credenciales válidas, inicia el flujo de autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Guarda el token para reutilizarlo
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Crear el servicio de Drive
    service = build('drive', 'v3', credentials=creds)

    return service

