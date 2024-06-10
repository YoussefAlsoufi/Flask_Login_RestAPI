from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    # Initialize Flask-Migrate
    migrate = Migrate(app, db) # we need for shema changes in future 
                                # command in terminal required :flask db init ,  flask db migrate -m "Description of changes", flask db upgrade
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
