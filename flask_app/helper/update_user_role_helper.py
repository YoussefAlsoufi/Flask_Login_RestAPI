from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class UpdateUserRoleForm(FlaskForm):
    submit = SubmitField('Update Role')
