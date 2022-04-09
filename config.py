import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'top secretXXX' #change this on prod!


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///tdtest'
    TESTING = True

class StagingConfig(Config):
    TESTING = False
    #SESSION_COOKIE_DOMAIN = 'https://www.google.com'

class DevelopmentConfig(Config):
    APPLICATION_ROOT = '/api'
