from flask_wtf import FlaskForm
from wtforms import SubmitField

class UpdateUserRoleForm(FlaskForm):
    submit = SubmitField('Update Role')
