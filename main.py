from flask_app import create_app, check_database_connection
import sys
from flask_migrate import upgrade

if __name__ == '__main__':
        # Get the configuration name from the command line argument
    config_name = sys.argv[1] if len(sys.argv) > 1 else 'development'
    print ("Config_name", config_name)
    app = create_app(config_name)
    check_database_connection(app)
    app.run(debug=(config_name == 'development'))



