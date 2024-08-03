import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://mail.google.com/"]
token_file = "token.json"
CREDENTIALS_FILE = "credentials.json"

def load_credentials(token_file, scopes):
    if os.path.exists(token_file):
        return Credentials.from_authorized_user_file(token_file, scopes)
    return None

def refresh_credentials(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

def obtain_new_credentials(credentials_file, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
    creds = flow.run_local_server(port=5001)
    with open(token_file, "w") as token:
        token.write(creds.to_json())
    return creds

def handle_http_error(error, token_file):
    if error.resp.status == 401:
        if os.path.exists(token_file):
            os.remove(token_file)
        print("Invalid credentials or token expired. Please restart the application.")
    elif error.resp.status == 403:
        print("Access denied. Ensure the application has the necessary permissions.")
    elif error.resp.status == 404:
        print("Requested resource not found.")
    else:
        print(f"An HTTP error occurred: {error.resp.status} - {error}")

def email_config():
    """Shows basic usage of the Gmail API. Configures Gmail API."""
    creds = load_credentials(token_file, SCOPES)
    creds = refresh_credentials(creds) if creds else obtain_new_credentials(CREDENTIALS_FILE, SCOPES)

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        handle_http_error(error, token_file)
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        return None
