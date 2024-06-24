from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder":"Enter your email"})
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    