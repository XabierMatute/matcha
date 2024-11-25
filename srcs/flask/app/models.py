from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg
import os
import logging
from dotenv import load_dotenv
import re

# Configurar el logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cargar las variables de entorno
load_dotenv()

class User:
    def __init__(self, id, email, username, first_name, last_name, password_hash, birthdate, **kwargs):
        if not birthdate:
            raise ValueError("Birthdate is required")  # Si no se pasa birthdate, lanzamos un error
        
        self.id = id
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.birthdate = birthdate  # Fecha de nacimiento
        self.gender = kwargs.get('gender')
        self.sexual_preferences = kwargs.get('sexual_preferences')
        self.biography = kwargs.get('biography')
        self.fame_rating = kwargs.get('fame_rating', 0.0)
        self.profile_picture = kwargs.get('profile_picture')
        self.location = kwargs.get('location')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.is_active = kwargs.get('is_active', False)

    def set_password(self, password):
        """Genera un hash para la contraseña y lo asigna al campo password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Compara la contraseña ingresada con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def calculate_age(self):
        """Calcula la edad del usuario basándose en su fecha de nacimiento."""
        if self.birthdate:
            today = datetime.today()
            age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            return age
        return None  # Si no tiene fecha de nacimiento, no se puede calcular la edad

    @staticmethod
    def get_db_connection():
        """Obtiene una nueva conexión a la base de datos."""
        try:
            connection = psycopg.connect(os.getenv('DATABASE_URL'))
            return connection
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise Exception("Database connection failed")

    @staticmethod
    def is_valid_email(email):
        """Valida el formato del correo electrónico."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    @staticmethod
    def get_user_by_id(user_id):
        """Obtiene un usuario por su ID desde la base de datos."""
        query = """
        SELECT id, email, username, first_name, last_name, password_hash, birthdate, gender, sexual_preferences, biography, fame_rating, profile_picture, location, latitude, longitude, is_active 
        FROM users 
        WHERE id = %s
        """
        connection = User.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()  # Obtiene un único resultado
            if result:
                return User(*result)  # Crea una instancia de User con los datos obtenidos
            else:
                return None  # Si no se encuentra el usuario
        except psycopg.Error as e:
            logger.error(f"Error fetching user with ID {user_id}: {e}")
            raise Exception(f"Error fetching user with ID {user_id}: {e}")
        finally:
            connection.close()

    @staticmethod
    def create_user(email, username, password, birthdate, **kwargs):
        """Crea un nuevo usuario en la base de datos, validando email y username únicos."""
        if not User.is_valid_email(email):
            raise ValueError("Invalid email format")

        # Validación de email y username único
        connection = User.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM users WHERE email = %s OR username = %s", (email, username))
                if cursor.fetchone():
                    raise ValueError("Email or Username already taken.")
            
            password_hash = generate_password_hash(password)
            query = """INSERT INTO users (email, username, password_hash, birthdate, gender, sexual_preferences, biography, fame_rating, profile_picture, location, latitude, longitude, is_active)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, email, username, birthdate, gender, sexual_preferences, biography, fame_rating, profile_picture, location, latitude, longitude, is_active"""
            
            user_data = (
                email, username, password_hash, birthdate, kwargs.get('gender'), kwargs.get('sexual_preferences'), kwargs.get('biography'),
                kwargs.get('fame_rating', 0.0), kwargs.get('profile_picture', None), kwargs.get('location', None), 
                kwargs.get('latitude', None), kwargs.get('longitude', None), kwargs.get('is_active', False)
            )
            with connection.cursor() as cursor:
                cursor.execute(query, user_data)
                result = cursor.fetchone()
                connection.commit()
            
            return User(*result)  # Retorna el objeto User creado
        except psycopg.Error as e:
            logger.error(f"Error creating user: {e}")
            raise Exception("Error creating user")
        finally:
            connection.close()  # Asegúrate de cerrar la conexión

    # Otros métodos como create_notification, get_notifications, etc., se mantienen igual.







