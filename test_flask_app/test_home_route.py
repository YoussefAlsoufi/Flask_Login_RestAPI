
def test_home_page(client):
    response = client.get('/', follow_redirects =False)
    assert response.status_code == 302
    assert response.headers['Location'].startswith('/login')

