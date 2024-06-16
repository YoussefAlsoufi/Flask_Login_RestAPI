import os

class DevelopmentConfig :
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY_DEV')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    print ("Youssef , this is the scret key :", SECRET_KEY)

class TestConfig: 
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY_TEST')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

class ProductionConfig:
    SECRET_KEY = os.getenv('SECRET_KEY_PROD')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')    