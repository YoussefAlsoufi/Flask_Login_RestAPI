from datetime import timedelta
from dotenv import load_dotenv
import os 

class Config:
    def __init__(self, config_name, app, login_manager) -> None:
        self.config_name = config_name
        self.app = app
        self.login_manager = login_manager

    def env_config(self):    
            # Load configurations based on the environment
        if self.config_name == 'development':
            self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_DEV')
            self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
            # Set session protection to strong
            self.login_manager.session_protection = "strong"
        elif self.config_name == 'testing':
            self.app.config['TESTING'] = True
            self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_TEST')
            self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')
        elif self.config_name == 'production':
            self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_PROD')
            self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')
        else:
            raise ValueError(f"Invalid FLASK_CONFIG value: {self.config_name}")
    
    def time_config(self):
        self.app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=60) 
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)

    def email_config(self):    
        MAIL_SERVER = os.getenv('MAIL_SERVER')
        MAIL_PORT = os.getenv('MAIL_PORT')
        MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
        MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', False)
'''        MAIL_USERNAME = 
        MAIL_PASSWORD = 
        MAIL_DEFAULT_SENDER = '''