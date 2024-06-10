from flask_app import create_app, check_database_connection


if __name__ == '__main__':
    app = create_app()
    check_database_connection(app)
    app.run(debug= True)


