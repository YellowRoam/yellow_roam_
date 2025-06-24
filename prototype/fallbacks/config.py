
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-should-set-a-secret-key')
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = os.environ.get('FLASK_ENV', 'production')

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ENV = 'testing'
