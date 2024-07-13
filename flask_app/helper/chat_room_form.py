from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class ChatRoomform(FlaskForm):
    name = StringField('Email', validators=[DataRequired()])
    code = StringField('Room Code')
    join = SubmitField('Join The Room')
    create = SubmitField('Create a Chat Room')