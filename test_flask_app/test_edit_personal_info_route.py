from flask_login import current_user
from test_helper.signup_user import signup_user
from test_helper.csrf_token_helper import get_csrf_token
from flask_app import db
from test_helper.login_test_user import login_test_user
import logging

def test_edit_personal_info_route(client):
    logging.info("test_edit_personal_info has started!")
    signup_user(client)
    logging.info("A new user has added to db.")
    logging.debug("Login the new user.")
    response =login_test_user(client, 'test@gmail.com', 'Tt@123')   
    assert b'Login successful!' in response.data 

    not_accepted_data = { 'email': 'test@gmail.com',
                'user_name': 'Test', 
                'phone': '0999999999', 
                'password': 'Tt@123', 
                'confirm_password': 'Tt@123' 
                }
    not_accepted_data['csrf_token'] = get_csrf_token(client,'/edit_personal_info')

    response = client.get('/edit_personal_info', follow_redirects = False)
    logging.debug(f"the response status code for get edit personal info is : {response.status_code}")
    assert response.status_code == 200, f"expected status code is 200 , but I got {response.status_code}"

    response = client.post('/edit_personal_info', data = not_accepted_data, follow_redirects = True)
    assert response.status_code == 200, f"expected status code is 200 , but I got {response.status_code}"
    assert b'New password cannot be the same as the current password.' in response.data

    # Update user info correctly:
    logging.debug("Update user's values correctly!")
    accepted_data = { 'email': 'test@gmail.com',
                'user_name': 'Test_user', 
                'phone': '0999999999', 
                'password': '', 
                'confirm_password': '',
                'csrf_token' : get_csrf_token(client,'/edit_personal_info')
                }
    response = client.post('/edit_personal_info', data = accepted_data, follow_redirects = True)
    assert response.status_code == 200, f"expected status code is 200 , but I got {response.status_code}"
    assert b'Your information has been updated!' in response.data
    db.session.commit()
    # check if the updated info has committed successfully:
    updated_user_name = current_user.user_name
    assert updated_user_name == "Test_user" , f" 'Test_user' is expected however I got {updated_user_name}"

    # incorrect phone number:
    logging.debug("Edit info with invalid phone number")
    accepted_data = { 'email': 'test@gmail.com',
                'user_name': 'Test_user', 
                'phone': '0999999999e', 
                'password': '', 
                'confirm_password': '',
                'csrf_token' : get_csrf_token(client,'/edit_personal_info')
                }
    response = client.post('/edit_personal_info', data = accepted_data, follow_redirects = True)
    assert response.status_code == 200, f"expected status code is 200 , but I got {response.status_code}"
    assert b'Failed to save changes.' in response.data



