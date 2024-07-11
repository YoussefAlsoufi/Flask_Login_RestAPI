from test_helper.signup_user import signup_user
from test_helper.csrf_token_helper import get_csrf_token
import logging 

def test_valid_login(client):
    logging.info("test_valid_login test started !")
    # Create a user
    signup_user(client)
    logging.debug("a user has created in db.")

    # Attempt to login with a correct user's creds: 
    correct_data = {
        'email' : 'test@gmail.com',
        'password' : 'Tt@123',
    }
    correct_data['csrf_token'] = get_csrf_token(client, '/login')

    # Test with correct credentials
    response = client.post('/login', data=correct_data, follow_redirects=False)
    logging.debug("Response status code with correct creds: %s", response.status_code)
    logging.debug("Response data with correct creds: %s", response.data)
    assert response.status_code == 302, f"Expected status code 302 for redirect with correct creds, got {response.status_code}"

    # Follow the redirect
    response = client.get(response.headers['Location'], follow_redirects=True)
    logging.debug("Follow redirect status code: %s", response.status_code)
    logging.debug("Follow redirect data: %s", response.data)
    assert response.status_code == 200, "Expected status code 200 after following redirect with correct creds"
    assert b'Login successful!' in response.data, "Expected flash message 'Login successful!' not found in response data."


def test_invalid_login(client):
    logging.info("test_invalid_login test started !")
    # Create a user
    signup_user(client)
    logging.debug("a user has created in db.")

    # Attempt to login with a incorerct user's creds: 
    incorrect_data = {
        'email' : 'test@gmail.com',
        'password' : 'TT@123',
    }
    incorrect_data['csrf_token'] = get_csrf_token(client, '/login')
    
    # Test with incorrect credentials
    response = client.post('/login', data=incorrect_data, follow_redirects=True)
    logging.debug("Response status code with incorrect creds: %s", response.status_code)
    logging.debug("Response data with incorrect creds: %s", response.data)
    assert response.status_code == 200, f"Expected status code 200 're-rendered' with incorrect creds, got {response.status_code}"
    assert b'Login unsuccessful. Please check email and password.' in response.data, "Expected flash message 'Login unsuccessful. Please check email and password.' not found in response data."


