from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
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
jwt = JWTManager()  # Inicializa JWTManager

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)

    # Cargar la configuración según el entorno
    app.config.from_object(os.getenv('FLASK_CONFIG', 'config.DevelopmentConfig'))

    # Configurar JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  # Asegúrate de que esto esté en tu .env

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)  # Inicializa JWTManager

    # Definir la ruta para el home
    @app.route('/')
    def home():
        return "Finally Welcome to our MatchaXabi! :)"

    # Importar rutas y modelos dentro del contexto de la aplicación
    with app.app_context():
        from . import models  # Importar modelos para asegurar que se registren
        from .routes import main_bp  # Importar el blueprint de rutas

        # Registrar el blueprint de las rutas
        app.register_blueprint(main_bp)  # Asegúrate de que el nombre coincida con el definido en routes.py

        from .auth import register_auth  # Importar la función para registrar las rutas de autenticación
        register_auth(app)  # Registrar las rutas de autenticación

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

















