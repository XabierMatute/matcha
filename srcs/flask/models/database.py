import logging
import psycopg
from psycopg.rows import dict_row  # Opcional: para trabajar con resultados como diccionarios
from config import DatabaseConfig as Config
from typing import Tuple, Optional, Dict, Any, Union, List

logging.basicConfig(level=logging.INFO)


class Database:
    """Clase para manejar la conexión, creación de tablas y consultas en la base de datos."""

    @staticmethod
    def validate_config():
        """Valida que las variables de configuración estén definidas."""
        required_vars = ["POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST"]
        for var in required_vars:
            if not getattr(Config, var, None):
                raise ValueError(f"{var} is not set")

    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos."""
        try:
            Database.validate_config()

            if Config.DEBUG:
                logging.debug(
                    f"Connecting to database {Config.POSTGRES_DB} as {Config.POSTGRES_USER} at {Config.POSTGRES_HOST}"
                )

            return psycopg.connect(
                dbname=Config.POSTGRES_DB,
                user=Config.POSTGRES_USER,
                password=Config.POSTGRES_PASSWORD,
                host=Config.POSTGRES_HOST,
                row_factory=dict_row,  # Opcional: devuelve resultados como diccionarios
            )

        except (psycopg.Error, ValueError) as e:
            logging.error(f"Error connecting to the database: {e}")
            raise Exception(f"Database connection failed: {e}") from e

    @staticmethod
    def execute_query(
        query: str,
        params: Union[Tuple, List] = (),
        fetchone: bool = True
    ) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]:
        """
        Ejecuta una consulta en la base de datos y maneja el cursor.
        
        Args:
            query (str): Consulta SQL a ejecutar.
            params (Tuple | List): Parámetros para la consulta SQL.
            fetchone (bool): Si es True, devuelve una fila; de lo contrario, devuelve todas las filas.

        Returns:
            Optional[Dict | List[Dict]]: Resultados de la consulta (si aplica).
        """
        try:
            with Database.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    if cursor.description:  # Solo intenta obtener resultados si la consulta los devuelve.
                        return cursor.fetchone() if fetchone else cursor.fetchall()
                    connection.commit()  # Confirma transacción en INSERT, UPDATE o DELETE.
        except Exception as e:
            logging.error(f"Error executing query: {query}, params: {params}, error: {e}")
            raise Exception("Database query error") from e

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
                birthdate DATE,
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
                is_online BOOLEAN DEFAULT FALSE,
                is_verified BOOLEAN DEFAULT FALSE
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
            ''',
            '''
            CREATE TABLE IF NOT EXISTS pictures (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                image_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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



