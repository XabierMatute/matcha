# /app/config/__init__.py
from flask import Flask
import os

# Asegúrate de que las configuraciones están siendo importadas correctamente
from config import DevelopmentConfig, TestingConfig, ProductionConfig

def create_app():
    """Crea la instancia de la aplicación Flask con la configuración correspondiente."""
    app = Flask(__name__)

    # Obtener el entorno de configuración desde la variable de entorno FLASK_ENV
    env = os.getenv('FLASK_ENV', 'development')  # Valor por defecto 'development'

    # Selecciona la configuración apropiada según el entorno
    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    elif env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError(f"Unknown FLASK_ENV value: {env}")

    # Definir rutas de ejemplo (esto podría moverse a un archivo routes.py en aplicaciones más grandes)
    @app.route('/')
    def home():
        return "¡Welcome to Matcha!"

    # (Opcional) Si deseas registrar blueprints para rutas o módulos adicionales:
    # from .routes import main_bp
    # app.register_blueprint(main_bp)

    return app



