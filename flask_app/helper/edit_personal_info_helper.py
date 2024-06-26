from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from flask_wtf import FlaskForm
from .sign_up_helper import PasswordValidator
from flask_app.models import User
from flask_login import current_user
from flask_app import bcrypt


class NewPasswordValidator(PasswordValidator):
    def __init__(self, message=None):
        super().__init__(message)
        self.additional_message = "New password cannot be the same as the current password."

    def __call__(self, form, field):
        # Perform the base validations
        super().__call__(form, field)
        
        # Additional check to ensure the new password is not the same as the current password
        new_password = field.data
        if current_user and current_user.password and bcrypt.check_password_hash(current_user.password, new_password):
            raise ValidationError(self.additional_message)


class EditPersonalInfo(FlaskForm):
    email = StringField('Email', validators=[Optional(),Email()])
    user_name = StringField('First Name')
    phone = StringField('Phone', validators=[Optional()])
    password = PasswordField('Password', validators=[ NewPasswordValidator(), Optional()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    save_changes = SubmitField('Save')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already in use. Please choose a different one.')
        
    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('Phone number already exists.') 