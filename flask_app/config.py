from datetime import timedelta
import os 
import os.path
from flask_uploads import UploadSet, IMAGES, configure_uploads

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]

class Config:
    def __init__(self, config_name, app, login_manager) -> None:
        self.config_name = config_name
        self.app = app
        self.login_manager = login_manager

    def env_config(self) -> None: 
        # Configure the uploading images:
        self.app.config["UPLOADS_DEFAULT_DEST"] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
        self.app.config["UPLOADS_PHOTOS_DEST"] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
  
        print("The Path from the config: ", self.app.config["UPLOADS_PHOTOS_DEST"])
        photos = UploadSet('photos', IMAGES)
        configure_uploads(self.app, photos)

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
