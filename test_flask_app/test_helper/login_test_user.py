from test_helper.csrf_token_helper import get_csrf_token

def login_test_user (client, email, password):
    return client.post('/login', data = dict(email=email, password=password, csrf_token=get_csrf_token(client,'/login')), follow_redirects=True)
