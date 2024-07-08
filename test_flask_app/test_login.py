from test_helper.signup_user import signup_user
from test_helper.csrf_token_helper import get_csrf_token
import logging 

def test_login(client):
    logging.info("Login test started !")
    # Create a user
    signup_user(client)
    logging.debug("a user has created in db.")

    # Attempt to login with a correct user's creds: 
    correct_data = {
        'email' : 'test@gmail.com',
        'password' : 'Tt@123',
    }
    correct_data['csrf_token'] = get_csrf_token(client, '/login')

    # Attempt to login with a incorerct user's creds: 
    incorrect_data = {
        'email' : 'test@gmail.com',
        'password' : 'TT@123',
    }
    incorrect_data['csrf_token'] = get_csrf_token(client, '/login')

    response = client.post('/login', data= correct_data, follow_redirects = False)
    logging.debug("Follow response status code with correct creds: %s", response.status_code)
    logging.debug("Follow response data with correct creds is : %s", response.data)
    assert response.status_code == 302, f"Expected status code 302 with correct creds, got {response.status_code}"

    response = client.post('/login', data = incorrect_data, follow_redirects = True)
    logging.debug("Follow response status code with incorrect creds: %s", response.status_code)
    logging.debug("Follow response data with incorrect creds is : %s", response.data)
    assert response.status_code == 200, f"Expected status code 200 're-rendered' with incorrect creds, got {response.status_code}"
    




