from flask import Blueprint, render_template
from flask_login import login_required, current_user

notes_test = Blueprint('notes_test', __name__)

@notes_test.route('/add', methods=['GET', 'POST'])
@login_required
def add_note():
    return render_template('notes.html', user = current_user)