# Helper function to get CSRF token
def get_csrf_token(client, url):
    response = client.get(url)
    csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
    return csrf_token