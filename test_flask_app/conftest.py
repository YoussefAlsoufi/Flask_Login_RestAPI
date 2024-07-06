import pytest
import sys
import os

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
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()