from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_app.helper.note_form import NoteForm
from flask_app.models import Note
from flask_app import db
from sqlalchemy.sql import func

notes = Blueprint('notes', __name__)

@notes.route('/add', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():      
        note_content = form.note_data.data
        if note_content:
            new_note = Note(note_data=note_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', 'success')
            return redirect(url_for('notes.add_note'))  # Redirect after POST to prevent resubmission
    
    # For GET request, fetch and display user's notes
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.note_date.desc()).all()
    return render_template('notes.html', user=current_user, notes=user_notes, form = form)

@notes.route('/delete_last', methods=['POST'])
@login_required
def delete_last_note():
    last_note = Note.query.filter_by(user_id=current_user.id).order_by(Note.note_date.desc()).first()
    if last_note:
        db.session.delete(last_note)
        db.session.commit()
        flash('Last note deleted successfully.', 'success')
    else:
        flash('No notes to delete.', 'danger')
    return redirect(url_for('notes.add_note'))