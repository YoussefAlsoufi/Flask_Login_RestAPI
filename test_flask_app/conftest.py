import pytest
import sys
import os
import logging
logging.basicConfig(filename='test_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


fh = logging.FileHandler('test_log.txt')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logging.getLogger().addHandler(fh)
# Adjust the path to your Flask application directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from flask_app import create_app, db
from flask_app.models import User, Note

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()  # Ensures that any transactions or data manipulations made during the test are discarded, preventing interference with subsequent tests.
        db.drop_all()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def runner(app):
    return app.test_cli_runner()