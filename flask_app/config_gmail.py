
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def email_config():    
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://mail.google.com/"]

    """Shows basic usage of the Gmail API. Configures Gmail API."""
    creds = None
    token_key = "token.json"
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_key):
        creds = Credentials.from_authorized_user_file(token_key, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=5001)
        # Save the credentials for the next run
        with open(token_key, "w") as token:
            token.write(creds.to_json())
    
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        # Handle different HTTP errors
        if error.resp.status == 401:
            # Invalid credentials or token expired, delete token.json and retry
            if os.path.exists(token_key):
                os.remove(token_key)
            print("Invalid credentials or token expired. Please restart the application.")
        elif error.resp.status == 403:
            # Insufficient permissions
            print("Access denied. Ensure the application has the necessary permissions.")
        elif error.resp.status == 404:
            # Resource not found
            print("Requested resource not found.")
        else:
            print(f"An HTTP error occurred: {error.resp.status} - {error}")
    except Exception as error:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {error}")
        return None
