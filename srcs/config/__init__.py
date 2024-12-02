from flask import Flask
from flask_mail import Mail
import os
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# Instancia global de Flask-Mail
mail = Mail()

def create_app():
    """Crea e inicializa la instancia de la aplicación Flask"""
    app = Flask(__name__)

    # Obtener el entorno desde la variable de entorno FLASK_ENV
    env = os.getenv('FLASK_ENV', 'development')

    # Cargar la configuración correspondiente
    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    elif env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError(f"Unknown FLASK_ENV value: {env}")

    # Inicializar Flask-Mail con la configuración cargada
    mail.init_app(app)

    return app

