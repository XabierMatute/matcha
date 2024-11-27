import psycopg
import os
import logging
from dotenv import load_dotenv

# Configurar el logger
logging.basicConfig(level=logging.INFO)

# Cargar las variables de entorno
load_dotenv()

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
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Crear la tabla de usuarios
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        is_active BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

                # Crear la tabla de perfiles
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS profiles (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
                        birthdate DATE NOT NULL,
                        gender VARCHAR(10),
                        sexual_preferences VARCHAR(100),
                        biography TEXT,
                        fame_rating FLOAT DEFAULT 0.0,
                        profile_picture TEXT,
                        location VARCHAR(100),
                        latitude DOUBLE PRECISION,
                        longitude DOUBLE PRECISION,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

                # Crear la tabla de likes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS likes (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        liked_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, liked_user_id)  -- Evitar likes duplicados
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



