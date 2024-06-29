from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_app.models import Note
from flask_app import db
from sqlalchemy.sql import func

notes = Blueprint('notes', __name__)

@notes.route('/add', methods=['GET', 'POST'])
@login_required
def add_note():
    if request.method == 'POST':
        note_content = request.form.get('note')
        if note_content.strip():
            new_note = Note(note_data=note_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', 'success')
        else:
            flash('Note cannot be empty.', 'danger')
        return redirect(url_for('notes.add_note'))
    
    # For GET request, fetch and display user's notes
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', user=current_user, notes=user_notes)
