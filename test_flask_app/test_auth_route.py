import pytest
from flask_app.models import User
import logging
from flask_app import db
from test_helper.csrf_token_helper import get_csrf_token

@pytest.mark.parametrize("data, expected_status, expected_flash", [
    (
        { 'email': 'test@gmail.com', 'user_name': 'Test', 'phone': '0999999999', 'password': 'Tt@123', 'confirm_password': 'Tt@123' },
        302,  # Expected status code for redirect (302 Found)
        [b'Your account has been created successfully!']  # Expected flash message content
    ),
    (
        { 'email': 'invalid_email', 'user_name': '', 'phone': 'invalid_phone', 'password': 'rr@123', 'confirm_password': 'Tt@123' },
        200,  # Expected status code for validation errors (form re-rendered)
        [b'This field is required.' ,
         b'Email must be a @gmail.com address.',
         b'Password must include at least one uppercase letter, one lowercase letter, one number, and one special character.',
         b'Field must be equal to password.',
         b'Entere a valid phone number.'] 
    ),
    (
        {
            'email': 'existing_user@gmail.com',
            'user_name': 'NewUser',
            'phone': '0999999999',
            'password': 'Tt@123',
            'confirm_password': 'Tt@123'
        },
        200,  # Expected status code for validation errors (form re-rendered)
        [b'That email is already in use. Please choose a different one.']  # Expected error message for duplicate email
    ),
])
def test_signup(client, data, expected_status, expected_flash):
    logging.info("test_signup started!")
    # If testing duplicate email, create a user with the email first
    if data['email'] == 'existing_user@gmail.com':
        logging.debug("new user has added to the db.")
        user = User(email='existing_user@gmail.com', user_name='ExistingUser', phone='0999999999', password='password')
        db.session.add(user)
        db.session.commit()
    
    # Add the CSRF token to the data
    data['csrf_token'] = get_csrf_token(client, '/sign-up')

    # Submit the form with the CSRF token included
    response = client.post('/sign-up', data=data, follow_redirects=False)
    logging.debug(" requesting a new user is done.")
    assert response.status_code == expected_status
    if expected_status == 302:
        assert response.headers['Location'].startswith('/login')

        # Follow the redirect
        follow_response = client.get(response.headers['Location'], follow_redirects=True)
        logging.debug("Follow response status code: %s", follow_response.status_code)
        logging.debug("Follow response data is : %s", follow_response.data)

        # Check the flash message in the response data
        for flash_message in expected_flash:
            assert flash_message in follow_response.data
    else:
        logging.debug("Follow response status code: %s", response.status_code)
        logging.debug("Follow response data is : %s", response.data)
        # Check the flash messages in the response data
        for flash_message in expected_flash:
            assert flash_message in response.data


def test_signup_database_integration(client):
    logging.info("test_signup_database_integration started!")
    initial_user_count = User.query.count()

    data = { 'email': 'test@gmail.com',
             'user_name': 'Test', 
             'phone': '0999999999', 
             'password': 'Tt@123', 
             'confirm_password': 'Tt@123' 
            }
    data['csrf_token'] = get_csrf_token(client,'/sign-up')
    response = client.post('/sign-up', data=data, follow_redirects=False)

    assert response.status_code == 302, f"Expected status code 302, got {response.status_code}"
    assert response.headers['Location'].startswith('/login')
    assert User.query.count() == initial_user_count + 1  # Verify that a new user is added to the database


def test_signup_exception_handling(client, mocker):
    logging.info("test_signup_exception_handling started!")
    # Mock the database session to raise an exception
    mocker.patch('flask_app.db.session.add', side_effect=Exception('Database error'))
    
    data = { 'email': 'test@gmail.com', 'user_name': 'Test', 'phone': '0999999999', 'password': 'Tt@123', 'confirm_password': 'Tt@123' }
    data['csrf_token'] = get_csrf_token(client,'/sign-up')
    response = client.post('/sign-up', data=data, follow_redirects=False)
    
    # Log the actual response content for debugging
    logging.debug("Response status code: %s", response.status_code)
    logging.debug("Response data: %s", response.data.decode())

    assert response.status_code == 200  # Form should be re-rendered on error
    # Check for the error message in the response data
    assert b'Failed to create a user because : Database error' in response.data

    # Ensure that the session is rolled back after the exception
    assert User.query.count() == 0  # No users should be added to the database
    