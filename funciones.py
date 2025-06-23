from connect import conectar_drive
from googleapiclient.http import MediaIoBaseDownload
import io

import pandas as pd

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