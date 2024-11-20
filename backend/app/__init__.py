from flask import Flask, g
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
import psycopg
from .routes import register_routes  # Importar las rutas
from .models import User  # Importar el modelo User para la carga de usuarios

# Cargar las variables de entorno (solo aquí, una vez)
load_dotenv()

# Inicializar extensiones
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
jwt = JWTManager()

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/matcha_dev')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

    # Inicializar extensiones con la app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Ajusta la ruta de login según sea necesario
    mail.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)

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

    # Registrar los blueprints
    register_routes(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    """Función de carga de usuario para Flask-Login"""
    connection = g.get('db_connection', None)
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id, username, email, password_hash, birthdate, gender, sexual_preferences, biography, fame_rating, profile_picture, location, latitude, longitude, is_active FROM users WHERE id = %s', (user_id,))
                user = cursor.fetchone()
                if user:
                    return User(*user)  # Aquí es donde mapeamos los valores a la clase User
        except psycopg.Error as e:
            # Logueamos el error y devolvemos None si ocurre un problema con la consulta
            app.logger.error(f"Error loading user: {e}")
    return None






















