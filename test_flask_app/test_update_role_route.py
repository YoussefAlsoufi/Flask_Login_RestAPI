from flask import url_for
from test_helper.signup_user import signup_user, signup_admin, signup_super_admin
from test_helper.login_test_user import login_test_user
from test_helper.csrf_token_helper import get_csrf_token
import logging 
from flask_login import current_user

def test_get_users_list(client):
    logging.info("test_get_users_list has started!")
    signup_user(client)
    logging.info("A new user has been added to the database.")
    
    # Login the user
    response = login_test_user(client, 'test@gmail.com', 'Tt@123')   
    assert b'Login successful!' in response.data 

    # Check the role of the logged-in user
    logging.debug(f"Current user role: {current_user.role}")

    # Make GET request to /users_list
    get_users_list = client.get('/users_list', follow_redirects=False)
    logging.debug(f"Status code of getting the users list response: {get_users_list.status_code}")
    if current_user.role == 'admin':
            # Assert that admin can access the users list
            assert get_users_list.status_code == 200, f"Expected status code 200 for admin, but got {get_users_list.status_code}"
    else:
        # Assert that non-admins are redirected and access is restricted
        assert get_users_list.status_code == 302, f"Expected status code 302 for non-admin, but got {get_users_list.status_code}"
        
        # Check the redirection location
        assert get_users_list.location.endswith(url_for('home_bp.home')), "Expected redirection to home page"
        
        # Check for the flash message indicating restricted access
        with client.session_transaction() as session:
            flash_messages = dict(session['_flashes'])
            assert 'info' in flash_messages
            assert 'Access to user list is restricted to admins only' in flash_messages['info']



def test_update_user_role_admin(client):
    logging.info("test_update_user_role with admin role has started!")
    signup_user(client)
    signup_admin(client)
    logging.info("A new user with admin role has added to db.")
    logging.debug("Login the new user.")
    response =login_test_user(client, 'admin@gmail.com', 'Admin@123')   
    assert b'Login successful!' in response.data
    data = {
         "id":1,
        "role":"admin"
        }
    
    # Check the role of the logged-in user
    logging.debug(f"Current user info: email: {current_user.email} , role: {current_user.role}")

    # Make post request to /users_list/update
    update_role_response = client.post('/users_list/update', data = data, follow_redirects = True )
    logging.debug(f" the status code of updating user role response is {update_role_response.status_code}")

    assert update_role_response.status_code == 200, f" I expected 200 as status_code of updating user's role response from non super admin, but I got {update_role_response.status_code}"
    assert b'Access to update roles only for super admins' in update_role_response.data


def test_update_user_role_super_admin(client):
    logging.info("test_update_user_role with super-admin role has started!")
    signup_user(client)
    signup_super_admin(client)

    logging.info("A new user with super-admin role has added to db.")
    logging.debug("Login the new user.")
    response =login_test_user(client, 'superadmin@gmail.com', 'SuperAdmin@123')   
    assert b'Login successful!' in response.data
    # Prepare data for role update
    data = {
        "id": 1, 
        "role": "admin"
    }

    # Check the role of the logged-in user
    logging.debug(f"Current user info: email: {current_user.email}, role: {current_user.role}")

    # Make GET request to /users_list/update
    update_role_response = client.post('/users_list/update', data = data, follow_redirects = True )
    logging.debug(f" the status code of updating user role response is {update_role_response.status_code}")
    logging.debug(update_role_response.data.decode()) 
    assert update_role_response.status_code == 200, f" I expected 200 as status_code of updating user's role response from super-admin, but I got {update_role_response.status_code}"
    assert b'Roles updated successfully.' in update_role_response.data
