from test_helper.csrf_token_helper import get_csrf_token    
from flask_app import db
from flask_app.models import User

def signup_user(client):
    data = { 'email': 'test@gmail.com',
                'user_name': 'Test', 
                'phone': '0999999999', 
                'password': 'Tt@123', 
                'confirm_password': 'Tt@123' ,
                }
    data['csrf_token'] = get_csrf_token(client,'/sign-up')
    return client.post('/sign-up', data=data, follow_redirects=False)

def signup_admin(client):
    data = { 'email': 'admin@gmail.com',
            'user_name': 'Test', 
            'phone': '0999999997', 
            'password': 'Admin@123', 
            'confirm_password': 'Admin@123',
                }
    data['csrf_token'] = get_csrf_token(client,'/sign-up')
    return client.post('/sign-up', data=data, follow_redirects=False)

def signup_super_admin(client):
    data = { 
            'email': 'superadmin@gmail.com',
            'user_name': 'Test', 
            'phone': '0999999996', 
            'password': 'SuperAdmin@123', 
            'confirm_password': 'SuperAdmin@123',
                }
    data['csrf_token'] = get_csrf_token(client,'/sign-up')
    client.post('/sign-up', data=data, follow_redirects=False)
    admin = User.query.filter_by(email='superadmin@gmail.com').first()
    admin.role = 'admin'
    db.session.commit()
    return admin