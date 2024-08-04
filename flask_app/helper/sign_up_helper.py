from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_app.models import User
import re
import dns.resolver
from validate_email_address import validate_email

def is_email_valid(email):
    if not validate_email(email):
        return False
    # Domain check
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return bool(mx_records)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return False
    
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
        email_data = email.data.strip()

        # Regular expression to check for valid characters and no spaces
        email_regex = re.compile(r'^[a-zA-Z0-9._]')
        if not email_regex.match(email_data):
            raise ValidationError('Email contains invalid characters or spaces.')
        
        user = User.query.filter_by(email=email_data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')
    
    def validate_phone(self, phone):
        if len(phone.data) != 10:
            raise ValidationError("Entere a valid phone number.")
        
        if not phone.data.isdigit():
            raise ValidationError("Enter a valid phone number.")
        
        # Check if the phone number already exists in the database
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone number already exists.')
        

