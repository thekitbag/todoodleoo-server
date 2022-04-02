import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'top secretXXX' #change this on prod!
    CORS_ALLOW_ORIGIN='https://todoodleoo-client.herokuapp.com'
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_HEADERS = 'Content-Type'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///tdtest'
    TESTING = True
