# setup_db.py
import sys
from flask_app import create_app, db
from flask_migrate import Migrate, upgrade
import logging

def setup_database(config_name='development'):
    app = create_app(config_name)
        # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    with app.app_context():
        try:
            migrate = Migrate(app, db) # with this line, you still need 'flask db migrate -m 'message' when you change you sql db.'
            db.create_all()
            upgrade()
            logger.info("Database upgraded successfully")
        except Exception as e:
            logger.error(f"Database upgrade failed: {e}")
            raise

if __name__ == '__main__':
    config_name = sys.argv[1] if len(sys.argv) > 1 else 'development'
    setup_database(config_name)