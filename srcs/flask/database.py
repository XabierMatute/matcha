import psycopg
import os
import logging
from config import DEBUG

# Configurar el logger
logging.basicConfig(level=logging.INFO)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        postgres_db = os.getenv('POSTGRES_DB')
        if not postgres_db:
            raise ValueError("POSTGRES_DB is not set")
        postgres_user = os.getenv('POSTGRES_USER')
        if not postgres_user:
            raise ValueError("POSTGRES_USER is not set")
        postgres_password = os.getenv('POSTGRES_PASSWORD')
        if not postgres_password:
            raise ValueError("POSTGRES_PASSWORD is not set")
        postgres_host = os.getenv('POSTGRES_HOST')
        if not postgres_host:
            raise ValueError("POSTGRES_DB is not set")

        if DEBUG:
            print(f"Connecting to database {postgres_db} as {postgres_user} ...")
            print(f"Password: {postgres_password}")
            print(f"Host: {postgres_db}")

        return psycopg.connect(dbname=postgres_db, user=postgres_user, password=postgres_password, host=postgres_host)

    except (psycopg.Error, ValueError) as e:
        logging.error(f"Error connecting to the database: {e}")
        raise Exception(f"Database connection failed: {e}")

def create_tables():
    try:
        # Intentar obtener la conexión a la base de datos
        with get_db_connection() as connection:
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

# Función para agregar un like
def add_like(user_id, liked_user_id):
    """Agrega un like de un usuario a otro."""
    query = '''
        INSERT INTO likes (user_id, liked_user_id)
        VALUES (%s, %s)
        ON CONFLICT (user_id, liked_user_id) DO NOTHING
        RETURNING id, user_id, liked_user_id, timestamp
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, liked_user_id))
                result = cursor.fetchone()
                connection.commit()
                if result:
                    logging.info(f"Like added: {result}")
                    return result
                else:
                    logging.info("Like already exists.")
                    return None  # Si el like ya existe
    except psycopg.Error as e:
        logging.error(f"Error adding like: {e}")
        raise Exception("Error adding like")