from flask_app.models import User, Note
from flask_app import db

def test_user_model():
    user = User(user_name='lolo', email='lolo@gmail.com', password='Lolo@123', phone='0933234345', role='user')
    db.session.add(user)
    db.session.commit()
    assert User.query.count() == 1

def test_note_model():
    note = Note(note_data='This is a test note.', user_id=7)
    db.session.add(note)
    db.session.commit()
    assert Note.query.count() == 1
