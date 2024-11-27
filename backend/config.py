import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')  # Usa un valor por defecto si no está en las variables de entorno
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY es requerido para producción.")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Si no estás usando SQLAlchemy, puedes omitir esta línea

    # Configuración de correo
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://Beaxabi:Beaxabi12345@localhost:5432/matcha_dev'  # Base de datos para desarrollo
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://Beaxabi:Beaxabi12345@localhost:5432/matcha_prod'  # Base de datos para producción
    DEBUG = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Utiliza SQLite en memoria para pruebas
    TESTING = True
    WTF_CSRF_ENABLED = False  # Corregido el error tipográfico


