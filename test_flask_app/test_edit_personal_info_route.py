from flask_login import current_user
from test_helper.signup_user import signup_user
from test_helper.csrf_token_helper import get_csrf_token
import logging

def login_test_user (client, email, password):
    return client.post('/login', data = dict(email=email, password=password, csrf_token=get_csrf_token(client,'/login')), follow_redirects=True)

def test_edit_personal_info_route(client):
    logging.info("test_edit_personal_info has started!")
    signup_user(client)
    logging.info("A new user has added to db.")
    logging.debug("Login the new user.")
    response =login_test_user(client, 'test@gmail.com', 'Tt@123')   
    assert b'Login successful!' in response.data 

    user = { 'email': 'test@gmail.com',
                'user_name': 'Test', 
                'phone': '0999999999', 
                'password': 'Tt@123', 
                'confirm_password': 'Tt@123' 
                }
    user['csrf_token'] = get_csrf_token(client,'/edit_personal_info')

    response = client.get('/edit_personal_info', follow_redirects = False)
    logging.debug(f"the response status code for get edit personal info is : {response.status_code}")
    assert response.status_code == 200, f"expected status code is 200 , but I got {response.status_code}"

    response = client.post('/edit_personal_info', data = user, follow_redirects = True)
    assert response.status_code == 200, f"expected status code is 200 , but I got {response.status_code}"
    assert b'' in response.data




