import unittest 
from flask_app import create_app, db
from flask_migrate import Migrate, upgrade

def run_tests():
    app = create_app('testing')

# This line creates an app context, which allows you to interact with the Flask app and its extension within a specific scope.
# it's necessary because certain operations like interacting with db, requires the app context to be active.
    with app.app_context():
        
        # Discover and run tests
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner().run(tests)

if __name__ == '__main__':
    run_tests()