from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)
class UploadPhotoForm (FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, "only images you can upload!"),
            FileRequired( "File Field should not be empty!")
        ]
    )
    submit = SubmitField('Update')
