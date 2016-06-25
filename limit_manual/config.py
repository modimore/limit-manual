'''
Defines possible configuration objects for application.
'''

class Config(object):
    DEBUG = False
    TESTING = False

    DB_NAME = 'limit_manual'
    DB_USER = 'modimore'

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True
