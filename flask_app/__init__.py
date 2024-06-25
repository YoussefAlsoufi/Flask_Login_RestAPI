from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .environments_configuration import DevelopmentConfig, TestConfig, ProductionConfig
from sqlalchemy import text
from dotenv import load_dotenv
from flask_login import LoginManager
import os 

load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_name= 'development'):
    app = Flask(__name__)
        # Load configurations based on the environment
    if config_name == 'development':
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_DEV')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
    elif config_name == 'testing':
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_TEST')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')
    elif config_name == 'production':
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_PROD')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')
    else:
        raise ValueError(f"Invalid FLASK_CONFIG value: {config_name}")
    
    print (config_name)
    print ("The sceretKey: " , app.config["SECRET_KEY"])

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    # Initialize Flask-Migrate
    # command in terminal required :flask db init (once you init db) ,  flask db migrate -m "Description of changes", flask db upgrade
    migrate = Migrate(app,db)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix = '/')

    return app


def check_database_connection(app):
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print ("success data base")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")
            raise
