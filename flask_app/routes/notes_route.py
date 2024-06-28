from flask import Blueprint, render_template
from flask_login import login_required, current_user

notes = Blueprint('notes', __name__)

@notes.route('/add', methods=['GET', 'POST'])
@login_required
def add_note():
    return render_template('notes.html', user = current_user)