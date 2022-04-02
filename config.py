import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'top secretXXX' #change this on prod!
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_HEADERS = 'Content-Type'
    SESSION_REFRESH_EACH_REQUEST: False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///tdtest'
    TESTING = True

class StagingConfig(Config):
    CORS_ALLOW_ORIGIN='https://todoodleoo-client.herokuapp.com'
    SESSION_COOKIE_DOMAIN='https://todoodleoo-client.herokuapp.com'

class DevelopmentConfig(Config):
    CORS_ALLOW_ORIGIN='http://localhost:3000'
