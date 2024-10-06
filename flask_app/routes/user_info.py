from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from flask_app.models import Note 

user_info = Blueprint('profile', __name__)

@user_info.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id).all()
        # Render the user_info.html template with current user information
        return render_template('user_info.html', current_user=current_user, notes = notes)
    else:
        # Redirect to login if user is not authenticated
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('home'))
