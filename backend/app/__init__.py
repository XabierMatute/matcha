# app/__init__.py
from flask import Flask, g
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
import psycopg  # Usamos psycopg3 para la conexión a la base de datos
from .routes import register_routes  # Importar la función que registra los blueprints
from .models import User  # Importa la clase User para la carga de usuarios

# Cargar variables de entorno
load_dotenv()

# Inicializar extensiones
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
jwt = JWTManager()  # Inicializa JWTManager

# Configuración de la base de datos (La cadena de conexión puede estar en el archivo .env)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/matcha_dev')

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)

    # Cargar configuración según el entorno
    app.config.from_object(os.getenv('FLASK_CONFIG', 'config.DevelopmentConfig'))

    # Configurar JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  # Asegúrate de que esto esté en tu .env

    # Inicializar extensiones con la app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Ajusta según la ruta de login
    mail.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)

    # Definir la ruta para el home
    @app.route('/')
    def home():
        return "Finalmente bienvenido a MatchaXabi! :)"

    # Función para obtener la conexión a la base de datos (se puede usar en cualquier lugar dentro de la aplicación)
    @app.before_request
    def before_request():
        """Abre una nueva conexión de base de datos por solicitud"""
        g.db_connection = psycopg.connect(DATABASE_URL)
    
    @app.teardown_request
    def teardown_request(exception):
        """Cierra la conexión de base de datos después de cada solicitud"""
        db = getattr(g, 'db_connection', None)
        if db is not None:
            db.close()

    # Registrar los blueprints (rutas)
    register_routes(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    """Función de carga de usuario para Flask-Login"""
    # Usamos la conexión abierta previamente en la solicitud actual
    connection = g.get('db_connection', None)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
        if user:
            # Si el usuario existe, retornar una instancia de la clase User
            return User(*user)
    return None





















