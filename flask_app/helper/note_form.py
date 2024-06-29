from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired

class NoteForm(FlaskForm):
    note_data = TextAreaField('Note')