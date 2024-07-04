from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_app.models import User
import re

class PasswordValidator:
    def __init__(self, message=None):
        if message is None:
            message = 'Password must include at least one uppercase letter, one lowercase letter, one number, and one special character.'
        self.message = message

    def __call__(self, form, field):
        password = field.data
        if (not re.search(r'[A-Z]', password) or
                not re.search(r'[a-z]', password) or
                not re.search(r'\d', password) or
                not re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
            raise ValidationError(self.message)

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder":"Enter your email"})
    user_name = StringField('First Name', validators=[DataRequired()],render_kw={"placeholder":"Enter your Name"})
    phone = StringField('Phone', validators=[DataRequired()],render_kw={"placeholder":"Enter your Name"})
    password = PasswordField('Password', validators=[DataRequired(), PasswordValidator()], render_kw={"placeholder":"create a strong password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder":"Confirm your password"})
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')
        
    def validate_phone(self, phone):
        if len(phone.data) != 10:
            raise ValidationError("Enter a valid phone number.")
        
        # Check if the phone number already exists in the database
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone number already exists.')   
