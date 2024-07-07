from test_helper.signup_user import signup_user
from test_helper.csrf_token_helper import get_csrf_token
import logging 

def test_login(client):
    logging.info("Login test started !")
    # Create a user
    signup_user(client)
    logging.debug("a user has created in db.")

    # Attempt to login with a user's creds: 
    data = {
        'email' : 'test@gmail.com',
        'password' : 'Tt@123',
    }
    data['csrf_token'] = get_csrf_token(client, '/login')

    response = client.post('/login', data= data, follow_redirects = False)

    assert response.status_code == 302, f"Expected status code 302, got {response.status_code}"


