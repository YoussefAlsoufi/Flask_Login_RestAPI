from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .environments_configuration import DevelopmentConfig, TestConfig, ProductionConfig
from sqlalchemy import text
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_app.config import Config


load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_name= 'development'):
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # Create an instance of Config
    config = Config(config_name, app, login_manager)
    # Load configurations
    config.env_config()
    config.time_config()

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
    socketio.init_app(app)
    
    # Initialize Flask-Migrate
    # command in terminal required :flask db init (once you init db) ,  flask db migrate -m "Description of changes", flask db upgrade
    migrate = Migrate(app,db)
    
    from .routes.update_role_route import update_role
    from .routes.home_route import home_bp
    from .routes.auth_route import auth
    from .routes.notes_route import notes
    from .routes.edit_personal_info_route import edit_personal_info_bp
    from .routes.chat_room_route import chat_room
    from .routes.email_token_route import email_token
    from .routes.user_info import user_info
    

    app.register_blueprint(update_role)
    app.register_blueprint(home_bp)
    app.register_blueprint(edit_personal_info_bp)
    app.register_blueprint(auth)
    app.register_blueprint(notes, url_prefix='/notes')
    app.register_blueprint(chat_room)
    app.register_blueprint(email_token)
    app.register_blueprint(user_info)


    return app


def check_database_connection(app):
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print ("success data base")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")
            raise
