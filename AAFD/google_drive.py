import os, io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

# Authenticate once
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)

def upload_file_to_drive(stream: io.BytesIO, filename: str, mimetype: str) -> str:
    """
    Uploads the file in `stream` to the configured Drive folder,
    makes it shareable, and returns a public download URL.
    """
    file_metadata = {"name": filename, "parents": [FOLDER_ID]}
    media = MediaIoBaseUpload(stream, mimetype=mimetype)
    uploaded = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webContentLink"
    ).execute()

    # Make it viewable by anyone with link
    drive_service.permissions().create(
        fileId=uploaded["id"],
        body={"role": "reader", "type": "anyone"}
    ).execute()

    return uploaded["webContentLink"]
