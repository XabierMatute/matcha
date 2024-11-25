from flask import Flask, g, current_app
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
import psycopg
from psycopg.rows import namedtuple_row  # Para devolver resultados como tuplas nombradas
from .routes import register_routes  # Importar las rutas
from app.models import User  # Importar el modelo User para la carga de usuarios

# Cargar las variables de entorno desde el archivo .env ubicado en srcs
load_dotenv(os.path.join(os.path.dirname(__file__), 'srcs', '.env'))

# Inicializar extensiones
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
jwt = JWTManager()

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://usuario:secret@localhost:5432/BAXM_db')

# Aquí ya no usaremos ConnectionPool, sino conexiones directas en el modelo




def create_app() -> Flask:
    """Crea e inicializa la aplicación Flask."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

    # Inicializar extensiones con la app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)

    @app.before_request
    def before_request():
        """Abre una nueva conexión de base de datos por solicitud desde el pool."""
        g.db_connection = pool.getconn()
        g.db_connection.row_factory = namedtuple_row  # Devolver resultados como tuplas nombradas

    @app.teardown_request
    def teardown_request(exception):
        """Cierra la conexión de base de datos después de cada solicitud."""
        db = getattr(g, 'db_connection', None)
        if db is not None:
            pool.putconn(db)

    # Registrar los blueprints
    register_routes(app)

    # Configurar logs
    configure_logging(app)

    return app


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """Función de carga de usuario para Flask-Login."""
    connection = getattr(g, 'db_connection', None)
    if connection:
        try:
            with connection.cursor() as cursor:
                query = '''
                    SELECT id, username, email, password_hash, birthdate, gender,
                           sexual_preferences, biography, fame_rating, profile_picture,
                           location, latitude, longitude, is_active
                    FROM users
                    WHERE id = %s
                '''
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    # Crear instancia de User desde los datos devueltos
                    return User(*user_data)
        except psycopg.Error as e:
            # Logueamos el error
            current_app.logger.error(f"Error loading user with ID {user_id}: {e}")
    return None


def configure_logging(app: Flask):
    """Configura el sistema de logs para la aplicación."""
    import logging
    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)























