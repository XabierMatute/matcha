import psycopg
import os
import logging
from dotenv import load_dotenv

# Configurar el logger
logging.basicConfig(level=logging.ERROR)

# Cargar las variables de entorno (esto solo se debe hacer una vez en la aplicación)
load_dotenv()  # Cargar las variables de entorno desde el archivo .env

# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        connection_string = os.getenv('DATABASE_URL')
        if not connection_string:
            raise ValueError("DATABASE_URL environment variable is not set.")
        return psycopg.connect(connection_string)
    except (psycopg.Error, ValueError) as e:
        logging.error(f"Error connecting to the database: {e}")
        raise Exception("Database connection failed")

# Función para crear las tablas necesarias en la base de datos
def create_tables():
    connection = None
    try:
        # Intentar obtener la conexión a la base de datos
        connection = get_db_connection()

        # Crear un cursor para ejecutar las consultas
        with connection.cursor() as cursor:
            # Crear la tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    birthdate DATE NOT NULL,
                    gender VARCHAR(10),
                    sexual_preferences VARCHAR(100),
                    biography TEXT,
                    fame_rating FLOAT DEFAULT 0.0,
                    profile_picture TEXT,
                    location VARCHAR(100),
                    latitude DOUBLE PRECISION,
                    longitude DOUBLE PRECISION,
                    is_active BOOLEAN DEFAULT FALSE
                );
            ''')

            # Crear la tabla de intereses
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interests (
                    id SERIAL PRIMARY KEY,
                    tag VARCHAR(100) UNIQUE NOT NULL
                );
            ''')

            # Crear la tabla de relaciones muchos a muchos (usuario-intereses)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_interests (
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    interest_id INTEGER REFERENCES interests(id) ON DELETE CASCADE,
                    PRIMARY KEY (user_id, interest_id)
                );
            ''')

            # Crear la tabla de imágenes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pictures (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
                );
            ''')

            # Crear la tabla de notificaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    type VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT FALSE
                );
            ''')

            # Confirmar la creación de las tablas
            connection.commit()
            logging.info("Tables created successfully.")

    except psycopg.Error as e:
        logging.error(f"Error during table creation: {e}")
        raise Exception("Error creating tables")
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    
    finally:
        # Asegúrate de cerrar la conexión si está abierta
        if connection:
            connection.close()
            logging.info("Database connection closed.")






