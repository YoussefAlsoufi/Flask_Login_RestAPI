from email.mime.multipart import MIMEMultipart
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


def create_verification_email(to_email, verification_link):

    message = MIMEMultipart('alternative')

    # Plain-text version
    text = f"""
    Welcome to Insights,
    Please verify your account by clicking on the following link: {verification_link}
    """

    # HTML version with larger, centered text
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; max-width: 600px; margin: auto;">
                <h1 style="font-size: 24px;">Welcome to Insights,</h1>
                <p style="font-size: 18px;">Please verify your account by clicking on the link below:</p>
                <p><a href="{verification_link}" style="display: inline-block; padding: 10px 20px; font-size: 18px; color: white; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Verify Account</a></p>
            </div>
        </body>
    </html>
    """

    # Attach both plain-text and HTML parts to the message
    message.attach(MIMEText(text, 'plain'))
    message.attach(MIMEText(html, 'html'))

    # Set email headers
    message['to'] = to_email
    message['from'] = "youssefalsoufi.1@gmail.com"
    message['subject'] = "User Verification"

    # Encode the message in base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {'raw': raw_message}

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