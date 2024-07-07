from test_helper.csrf_token_helper import get_csrf_token    

def signup_user(client):
    data = { 'email': 'test@gmail.com',
                'user_name': 'Test', 
                'phone': '0999999999', 
                'password': 'Tt@123', 
                'confirm_password': 'Tt@123' 
                }
    data['csrf_token'] = get_csrf_token(client,'/sign-up')
    return client.post('/sign-up', data=data, follow_redirects=False)