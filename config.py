import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= os.environ.get('APP_SECRET_KEY')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///tdtest'
    TESTING = True
    SECRET_KEY = 'supersecurepw4testing!'


class StagingConfig(Config):
    TESTING = False
    #SESSION_COOKIE_DOMAIN = 'https://www.google.com'

class DevelopmentConfig(Config):
    APPLICATION_ROOT = '/'
    SECRET_KEY = 'supersecurepw'
