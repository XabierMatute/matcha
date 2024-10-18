import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("El SECRET_KEY es requerido para producción.")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://Beaxabi:Beaxabi12345@localhost:5432/matcha_dev'
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://Beaxabi:Beaxabi12345@localhost:5432/matcha_prod'
    DEBUG = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    WTF_CSRF_ENABLED = False




