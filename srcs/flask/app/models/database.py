import os
import logging
import psycopg
from config import DEBUG

logging.basicConfig(level=logging.INFO)

class Database:
    """Clase para manejar la conexión y la creación de tablas en la base de datos."""
    
    @staticmethod
    def get_connection():
        """Establece una conexión con la base de datos."""
        try:
            postgres_db = os.getenv('POSTGRES_DB')
            postgres_user = os.getenv('POSTGRES_USER')
            postgres_password = os.getenv('POSTGRES_PASSWORD')
            postgres_host = os.getenv('POSTGRES_HOST')

            if DEBUG:
                print(f"Connecting to database {postgres_db} at {postgres_host} as {postgres_user}")

            return psycopg.connect(
                dbname=postgres_db, 
                user=postgres_user, 
                password=postgres_password, 
                host=postgres_host
            )
        except (psycopg.Error, ValueError) as e:
            logging.error(f"Error connecting to the database: {e}")
            raise Exception("Database connection failed") from e

    @staticmethod
    def create_tables():
        """Crea las tablas necesarias para la aplicación."""
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                birthdate DATE NOT NULL,
                gender VARCHAR(10),
                sexual_preferences VARCHAR(100),
                biography TEXT,
                fame_rating FLOAT DEFAULT 0.0,
                profile_picture TEXT,
                location VARCHAR(100),
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                is_active BOOLEAN DEFAULT FALSE,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_online BOOLEAN DEFAULT FALSE
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS likes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                liked_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, liked_user_id)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                type VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS interests (
                id SERIAL PRIMARY KEY,
                tag VARCHAR(100) UNIQUE NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS user_interests (
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                interest_id INTEGER REFERENCES interests(id) ON DELETE CASCADE,
                PRIMARY KEY (user_id, interest_id)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS chats (
                id SERIAL PRIMARY KEY,
                sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                receiver_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''
        ]
        
        try:
            with Database.get_connection() as connection:
                with connection.cursor() as cursor:
                    for query in queries:
                        cursor.execute(query)
                    connection.commit()
                    logging.info("Tables created successfully.")
        except psycopg.Error as e:
            logging.error(f"Error during table creation: {e}")
            raise Exception("Error creating tables") from e

# Llamar a create_tables() si se ejecuta directamente
if __name__ == "__main__":
    try:
        Database.create_tables()
        logging.info("Database setup completed.")
    except Exception as e:
        logging.error(f"Database setup failed: {e}")
