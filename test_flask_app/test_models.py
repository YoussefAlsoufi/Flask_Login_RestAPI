from flask_app.models import User, Note
from flask_app import db
from test_flask_app.conftest import app

def test_user_model(app):
    with app.app_context():
        # Create a user object
        user = User(user_name='TestUser', email='test@example.com',password='Tt@123', phone='1234567890', role='user')

        # Add user to session and commit to database
        db.session.add(user)
        db.session.commit()

        # Query the user from the database
        queried_user = User.query.filter_by(email='test@example.com').first()

        # Assertions
        assert queried_user is not None
        assert queried_user.user_name == 'TestUser'
        assert queried_user.phone == '1234567890'
        assert queried_user.role == 'user'

def test_note_model(app):
    with app.app_context():
        # Create a note object associated with a user (assuming user exists)
        user = User(user_name='TestUser', email='test@example.com', password='Tt@123', phone='1234567890', role='user')
        db.session.add(user)
        db.session.commit()

        note = Note(note_data='Test Note', user_id=user.id)

        # Add note to session and commit to database
        db.session.add(note)
        db.session.commit()

        # Query the note from the database
        queried_note = Note.query.filter_by(note_data='Test Note').first()

        # Assertions
        assert queried_note is not None
        assert queried_note.user_id == user.id