import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("El SECRET_KEY es requerido para producción.")
    
    # Eliminar la configuración de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración para el correo
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_SERVER = 'smtp.gmail.com'
    
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    if not MAIL_USERNAME:
        raise ValueError("MAIL_USERNAME es requerido para el envío de correos.")
    
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    if not MAIL_PASSWORD:
        raise ValueError("MAIL_PASSWORD es requerido para el envío de correos.")
    
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    if not MAIL_DEFAULT_SENDER:
        raise ValueError("MAIL_DEFAULT_SENDER es requerido para el envío de correos.")

class DevelopmentConfig(Config):
    # Aquí puedes gestionar la base de datos manualmente, sin SQLAlchemy
    DATABASE_URL = os.getenv('DATABASE_URL') or 'postgresql://username:password@db:5433/matcha_dev'
    DEBUG = True

class ProductionConfig(Config):
    DATABASE_URL = os.getenv('DATABASE_URL') or 'postgresql://username:password@db:5433/matcha_prod'
    DEBUG = False

class TestingConfig(Config):
    DATABASE_URL = 'sqlite:///:memory:'
    TESTING = True
    WTF_CSRF_ENABLED = False






