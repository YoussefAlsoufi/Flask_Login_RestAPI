from flask_app.helper.note_form import NoteForm

def test_note_form_valid():
    form = NoteForm(note_data='This is a test note.')
    assert form.validate() is True

def test_note_form_invalid():
    form = NoteForm(note_data='')
    assert form.validate() is False
    assert 'This field is required.' in form.note_data.errors