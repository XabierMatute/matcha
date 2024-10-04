from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

def create_app():
    # Inicializar Flask App
    app = Flask(__name__)

    # Cargar la configuración según el entorno
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object('config.ProductionConfig')
    elif os.getenv('FLASK_ENV') == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Asegúrate de que la vista de login esté correctamente referenciada
    mail.init_app(app)
    csrf.init_app(app)

    # Importar rutas y modelos dentro del contexto de la aplicación
    with app.app_context():
        from . import models  # Importar modelos primero para que estén disponibles para migraciones
        from .routes import register_auth  # Importar la función para registrar las rutas

        register_auth(app)  # Registrar las rutas en la aplicación

        db.create_all()  # Crear las tablas en la base de datos, si es necesario

    return app










