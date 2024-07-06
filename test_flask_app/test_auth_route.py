import pytest
from flask_app.models import User

@pytest.mark.parametrize("data, expected_status, expected_flash", [
    (
        { 'email': 'test@gmail.com', 'user_name': 'Test', 'phone': '0999999999', 'password': 'Tt@123', 'confirm_password': 'Tt@123' },
        200,  # Expected status code for redirect (302 Found)
        b'Your account has been created successfully!'  # Expected flash message content
    ),
    (
        { 'email': 'invalid_email', 'user_name': '', 'phone': 'invalid_phone', 'password': 'Tt@123', 'confirm_password': 'Tt@123' },
        200,  # Expected status code for validation errors (form re-rendered)
        b'This field is required.'  # Expected error message content (adjust as needed based on your form validation)
    ),
])
def test_signup(client, data, expected_status, expected_flash):
        # Get the CSRF token from the form
    response = client.get('/sign-up')
    csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
    
    # Add the CSRF token to the data
    data['csrf_token'] = csrf_token

    response = client.post('/sign-up', data=data, follow_redirects=True)
    
    print("Response status code:", response.status_code)
    print("Response data:", response.data)
    
    assert response.status_code == expected_status
    if expected_flash:
        assert expected_flash in response.data


"""def test_signup_database_integration(client):
    initial_user_count = User.query.count()

    data = { 'email': 'test@gmail.com', 'user_name': 'Test', 'phone': '0999999999', 'password': 'Tt@123', 'confirm_password': 'Tt@123' }
    response = client.post('/sign-up', data=data, follow_redirects=True)

    assert response.status_code == 200  # Redirected after successful signup
    assert User.query.count() == initial_user_count + 1  # Verify that a new user is added to the database

def test_signup_exception_handling(client, mocker):
    # Mock the database session to raise an exception
    mocker.patch('flask_app.db.session.add', side_effect=Exception('Database error'))
    
    data = { 'email': 'test@gmail.com', 'user_name': 'Test', 'phone': '0999999999', 'password': 'Tt@123', 'confirm_password': 'Tt@123' }
    response = client.post('/sign-up', data=data, follow_redirects=True)
    
    assert response.status_code == 302  # Form should be re-rendered
    assert b'Failed to create a user because' in response.data  # Check for error message

    # Ensure that the session is rolled back after the exception
    assert User.query.count() == 0  # No users should be added to the database

"""