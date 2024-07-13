from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
class ChatRoomform(FlaskForm):
    name = StringField('Email', validators=[DataRequired()])
    code = StringField('Room Code')
    join = SubmitField('Join The Room')
    create = SubmitField('Create a Chat Room')

class LiveChatRoom(FlaskForm):
    message = TextAreaField('Messages')
    send = SubmitField('Send')

    