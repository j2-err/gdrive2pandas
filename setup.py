# setup.py
from setuptools import setup, find_packages

setup(
    name="gdrive2pandas",
    version="0.1.0",
    description="Conector a Google Drive y librerias para pasar a dataframes",
    author="Tu Nombre",
    url="https://github.com/j2-err/gdrive-conector",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "pandas",
        "openpyxl",
            # Para leer archivos Excel
    ],
)