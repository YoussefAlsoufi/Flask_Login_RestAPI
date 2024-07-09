from test_helper.login_test_user import login_test_user
from test_helper.signup_user import signup_user
from test_helper.csrf_token_helper import get_csrf_token
from flask_login import current_user
from flask_app.models import Note
import logging

def add_test_note(client):
        note = {
        "note_data": "This is th first note for testing!",
        "user_id" : current_user.id,
        "csrf_token" : get_csrf_token(client, '/notes/add')}
        return client.post('notes/add', data = note, follow_redirects = True)

def test_note_route(client):
    logging.info(" test_note_route has strarted !")
    signup_user(client)
    logging.info("A new user has added to db.")
    logging.debug("Login the new user.")
    response =login_test_user(client, 'test@gmail.com', 'Tt@123')   
    assert b'Login successful!' in response.data 


    
    get_response = client.get('/notes/add', follow_redirects= True)
    logging.debug(f"get note response is {get_response.status_code}")
    assert get_response.status_code == 200 , f"I expected 200 but I got {get_response.status_code}"

    initial_notes_count = Note.query.filter_by(user_id = current_user.id).count()
    post_response = add_test_note(client)
    logging.debug(f"post note response is : {post_response.status_code} ")
    assert post_response.status_code == 200, f"I expected 200 but I got {post_response.status_code}"
    assert b'Note added successfully!' in post_response.data
    # check the notes count: 
    existed_notes = Note.query.filter_by(user_id = current_user.id).count()
    assert existed_notes == initial_notes_count + 1


def test_delete_note(client):
    logging.info("test_delete_note has strated!")
    signup_user(client)
    logging.info("A new user has added to db.")
    logging.debug("Login the new user.")
    response =login_test_user(client, 'test@gmail.com', 'Tt@123')   
    assert b'Login successful!' in response.data 

    # try remove a note from an empty list:
    invalid_delete_note_response = client.post('/notes/delete_last', follow_redirects=True)
    logging.debug(f"invalild deleteing a note from an emptu list is : {invalid_delete_note_response.status_code}")
    assert b'No notes to delete.' in invalid_delete_note_response.data
    assert invalid_delete_note_response.status_code == 200 , f"I expect 200 after invalid deleting a note from an empty list but I got {invalid_delete_note_response.status_code}"

    add_test_note(client)
    existed_notes = Note.query.filter_by(user_id = current_user.id).count()
    delete_reponse = client.post('/notes/delete_last', follow_redirects=True)
    logging.debug("deleting a note.")
    assert delete_reponse.status_code == 200, f"I expected 200 but got {delete_reponse.status_code}"
    logging.debug(f"delete note response is : {delete_reponse.status_code} ")
    notes_after_delete = Note.query.filter_by(user_id = current_user.id).count()
    assert notes_after_delete == existed_notes -1 
    assert b'Last note deleted successfully.' in delete_reponse.data




    




    




