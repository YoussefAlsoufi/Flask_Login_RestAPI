from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .environments_configuration import DevelopmentConfig, TestConfig, ProductionConfig
from sqlalchemy import text
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import timedelta
from flask_login import current_user
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
        # Set session protection to strong
        login_manager.session_protection = "strong"
    elif config_name == 'testing':
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_TEST')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')
    elif config_name == 'production':
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_PROD')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')
    else:
        raise ValueError(f"Invalid FLASK_CONFIG value: {config_name}")
    
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=60) 
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)
    
    print (config_name)
    print ("The sceretKey: " , app.config["SECRET_KEY"])

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please, Login to access this page!."
    login_manager.login_message_category = "info"

    login_manager.refresh_view = "auth.login"  
    login_manager.needs_refresh_message = " Please, refresh your Login first !."
    login_manager.needs_refresh_message_category = "info" 

    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Initialize Flask-Migrate
    # command in terminal required :flask db init (once you init db) ,  flask db migrate -m "Description of changes", flask db upgrade
    migrate = Migrate(app,db)
    
    from .views import views
    from .routes.home_route import home_bp
    from .routes.auth_route import auth
    from .routes.notes_route import notes
    from .routes.edit_personal_info_route import edit_personal_info_bp
    

    app.register_blueprint(views)
    app.register_blueprint(home_bp)
    app.register_blueprint(edit_personal_info_bp)
    app.register_blueprint(auth)
    app.register_blueprint(notes, url_prefix='/notes')


    return app


def check_database_connection(app):
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print ("success data base")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")
            raise
