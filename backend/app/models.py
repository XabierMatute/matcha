import os
import psycopg
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import logging

# Cargar variables de entorno (asegurándote de tener un archivo .env configurado)
load_dotenv()

# Configurar el logger
logging.basicConfig(level=logging.INFO)

class User:
    def __init__(self, id, email, username, first_name, last_name, password_hash, **kwargs):
        self.id = id
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
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

    @staticmethod
    def get_db_connection():
        """Abre una conexión a la base de datos utilizando las variables de entorno."""
        try:
            connection = psycopg.connect(
                database=os.getenv('DATABASE_NAME'),
                user=os.getenv('DATABASE_USER'),
                password=os.getenv('DATABASE_PASSWORD'),
                host=os.getenv('DATABASE_HOST', 'localhost')
            )
            return connection
        except psycopg.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            raise Exception("Database connection failed")

    @staticmethod
    def get_user_by_id(user_id):
        """Obtiene un usuario desde la base de datos usando su ID."""
        query = "SELECT * FROM users WHERE id = %s"
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    result = cursor.fetchone()
            return User(*result) if result else None
        except psycopg.Error as e:
            logging.error(f"Error fetching user by ID: {e}")
            return None

    @staticmethod
    def create_user(email, username, password):
        """Crea un nuevo usuario en la base de datos."""
        password_hash = generate_password_hash(password)
        query = """INSERT INTO users (email, username, password_hash)
                   VALUES (%s, %s, %s) RETURNING id, email, username"""
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (email, username, password_hash))
                    result = cursor.fetchone()
                    connection.commit()
            return User(*result)  # Retorna el objeto User completo
        except psycopg.Error as e:
            logging.error(f"Error creating user: {e}")
            raise Exception("Error creating user")

    @staticmethod
    def user_exists(email=None, username=None):
        """Verifica si el correo o el nombre de usuario ya están registrados."""
        query = "SELECT id FROM users WHERE email = %s OR username = %s"
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (email, username))
                    result = cursor.fetchone()
            return result is not None
        except psycopg.Error as e:
            logging.error(f"Error checking if user exists: {e}")
            return False


# Definición de otros modelos (Interest, Picture) como se hacía antes

class Interest:
    def __init__(self, id, tag):
        self.id = id
        self.tag = tag

    @staticmethod
    def get_interests_by_user(user_id):
        """Obtiene los intereses de un usuario dado su ID."""
        query = """
        SELECT i.id, i.tag FROM interests i
        JOIN user_interests ui ON i.id = ui.interest_id
        WHERE ui.user_id = %s
        """
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    results = cursor.fetchall()
            return [Interest(id=row[0], tag=row[1]) for row in results]
        except psycopg.Error as e:
            logging.error(f"Error fetching interests for user {user_id}: {e}")
            return []

class Picture:
    def __init__(self, id, url, user_id):
        self.id = id
        self.url = url
        self.user_id = user_id

    @staticmethod
    def get_pictures_by_user(user_id):
        """Obtiene las imágenes de un usuario dado su ID."""
        query = "SELECT id, url FROM pictures WHERE user_id = %s"
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    results = cursor.fetchall()
            return [Picture(id=row[0], url=row[1], user_id=user_id) for row in results]
        except psycopg.Error as e:
            logging.error(f"Error fetching pictures for user {user_id}: {e}")
            return []


