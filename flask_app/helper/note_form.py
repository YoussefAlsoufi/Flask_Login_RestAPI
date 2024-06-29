from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length

class NoteForm(FlaskForm):
    note_data = TextAreaField('Note', validators=[Length(max=1000)])
    submit = SubmitField('Submit')
