

def test_signup_route(client):
    data =  { 'email' : 'test@gmail.com',
              'user_name' : 'Test',
              'phone' : '0999999999',
              'password':'Tt@123',
              'confirm_password': 'Tt@123'
    }
    response = client.post('/sign-up', data=data, follow_redirects = False)

    assert response.status_code == 200 

def test_signup_validation (client):
        data =  { 'email' : 'test@gail.com',
              'user_name' : 'Test',
              'phone' : '0999999999',
              'password':'Tt@123',
              'confirm_password': 'Tt@123'
    }
        response = client.post('/sign-up', data=data, follow_redirects=True)
        
        assert response.status_code ==200
