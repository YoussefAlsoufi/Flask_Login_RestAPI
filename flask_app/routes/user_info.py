# Import necessary modules
from flask import render_template, redirect, url_for, flash, Blueprint, send_from_directory
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename
from flask_app.models import Note 
from flask_app.helper.upload_photo_form import UploadPhotoForm
import os

# Initialize blueprint and set upload folder path
user_info = Blueprint('user_info', __name__)
photos = UploadSet('photos', IMAGES)

# Ensure that the upload destination folder is set
UPLOADS_DEFAULT_DEST = os.path.join(os.path.dirname(__file__), 'static/uploads')

@user_info.route('/profile')
@login_required
def profile():
    """User profile route displaying user information and notes."""
    form = UploadPhotoForm()
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('user_info.html', current_user=current_user, notes=notes, form = form)

@user_info.route('/static/uploads/<filename>')
def get_file(filename):
    """Serve uploaded files from the uploads directory."""
    return send_from_directory(UPLOADS_DEFAULT_DEST, filename)

@user_info.route('/uploads', methods=['POST', 'GET'])
@login_required
def uploads_image():
    """Handle profile image upload."""
    form = UploadPhotoForm()
    file_url = None
    if form.validate_on_submit():
        # Save file securely
        filename = photos.save(form.photo.data)
        file_url = url_for('user_info.get_file', filename=filename)
    return render_template("user_info.html", form=form, file_url=file_url, current_user=current_user)

