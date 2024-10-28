import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("El SECRET_KEY es requerido para producción.")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'postgresql://Beaxabi:Beaxabi12345@db:5433/matcha_dev'  # Cambiado a 'db'
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'postgresql://Beaxabi:Beaxabi12345@db:5433/matcha_prod'  # Cambiado a 'db'
    DEBUG = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    WTF_CSRF_ENABLED = False




