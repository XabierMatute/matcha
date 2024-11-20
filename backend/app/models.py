from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg
import os
import logging
from dotenv import load_dotenv

# Configurar el logger
logging.basicConfig(level=logging.ERROR)

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
        """Abre una conexión a la base de datos utilizando las variables de entorno."""
        load_dotenv()  # Cargar las variables de entorno
        try:
            connection_string = os.getenv('DATABASE_URL')
            return psycopg.connect(connection_string)
        except psycopg.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise Exception("Database connection failed")

    @staticmethod
    def create_user(email, username, password, birthdate, **kwargs):
        """Crea un nuevo usuario en la base de datos."""
        password_hash = generate_password_hash(password)
        query = """INSERT INTO users (email, username, password_hash, birthdate, gender, sexual_preferences, biography, fame_rating, profile_picture, location, latitude, longitude, is_active)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, email, username, birthdate, gender, sexual_preferences, biography, fame_rating, profile_picture, location, latitude, longitude, is_active"""
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (email, username, password_hash, birthdate, kwargs.get('gender'), kwargs.get('sexual_preferences'), kwargs.get('biography'),
                                           kwargs.get('fame_rating', 0.0), kwargs.get('profile_picture'), kwargs.get('location'), kwargs.get('latitude'), kwargs.get('longitude'), kwargs.get('is_active', False)))
                    result = cursor.fetchone()
                    connection.commit()
            return User(*result)  # Retorna el objeto User creado
        except psycopg.Error as e:
            logging.error(f"Error creating user: {e}")
            raise Exception("Error creating user")

    @staticmethod
    def create_notification(user_id, message, notification_type):
        """Crea una nueva notificación para un usuario"""
        query = '''
            INSERT INTO notifications (user_id, message, type)
            VALUES (%s, %s, %s) RETURNING id, user_id, message, type, timestamp
        '''
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id, message, notification_type))
                    result = cursor.fetchone()
                    connection.commit()
            return result
        except psycopg.Error as e:
            logging.error(f"Error creating notification: {e}")
            raise Exception("Error creating notification")

    @staticmethod
    def get_notifications(user_id, is_read=False):
        """Obtiene las notificaciones de un usuario, filtradas por 'is_read'."""
        query = '''
            SELECT id, message, type, timestamp
            FROM notifications 
            WHERE user_id = %s AND is_read = %s 
            ORDER BY timestamp DESC
        '''
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id, is_read))
                    results = cursor.fetchall()
            return results
        except psycopg.Error as e:
            logging.error(f"Error fetching notifications for user {user_id}: {e}")
            return []

    @staticmethod
    def mark_notification_as_read(notification_id):
        """Marca una notificación como leída."""
        query = '''
            UPDATE notifications
            SET is_read = TRUE
            WHERE id = %s
        '''
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (notification_id,))
                    connection.commit()
        except psycopg.Error as e:
            logging.error(f"Error marking notification as read: {e}")
            raise Exception("Error marking notification as read")


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

    @staticmethod
    def create_interest(tag):
        """Crea un nuevo interés en la base de datos."""
        query = "INSERT INTO interests (tag) VALUES (%s) RETURNING id, tag"
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (tag,))
                    result = cursor.fetchone()
                    connection.commit()
            return Interest(*result)
        except psycopg.Error as e:
            logging.error(f"Error creating interest: {e}")
            raise Exception("Error creating interest")


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

    @staticmethod
    def create_picture(url, user_id):
        """Agrega una nueva imagen para un usuario."""
        query = "INSERT INTO pictures (url, user_id) VALUES (%s, %s) RETURNING id, url"
        try:
            with User.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (url, user_id))
                    result = cursor.fetchone()
                    connection.commit()
            return Picture(*result)
        except psycopg.Error as e:
            logging.error(f"Error creating picture: {e}")
            raise Exception("Error creating picture")



