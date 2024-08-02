import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def create_message(to,verification_link):
    message = MIMEText(f"Welcome in Insights, Please verify your account by clicking on the link: {verification_link}")
    message['to'] = to
    message['from'] = "youssefalsoufi.1@gmail.com"
    message['subject'] = "User verification"
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
    
def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = serializer.loads(token, salt=os.getenv('SECURITY_PASSWORD_SALT'), max_age=expiration)
    except:
        return False
    return email