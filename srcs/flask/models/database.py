import logging
import psycopg
from psycopg.rows import dict_row
from config import DatabaseConfig as Config
from typing import Tuple, Optional, Dict, Any, Union, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """Class to handle database connection, table creation, and queries."""

    @staticmethod
    def validate_config():
        """Validates that the configuration variables are defined."""
        required_vars = ["POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST"]
        for var in required_vars:
            if not getattr(Config, var, None):
                raise ValueError(f"{var} is not set")

    @staticmethod
    def get_connection():
        """Gets a connection to the database."""
        try:
            Database.validate_config()

            logger.debug(
                f"Connecting to database {Config.POSTGRES_DB} as {Config.POSTGRES_USER} at {Config.POSTGRES_HOST}"
            )

            return psycopg.connect(
                dbname=Config.POSTGRES_DB,
                user=Config.POSTGRES_USER,
                password=Config.POSTGRES_PASSWORD,
                host=Config.POSTGRES_HOST,
                row_factory=dict_row  # Returns results as dictionaries
            )

        except (psycopg.Error, ValueError) as e:
            logger.error(f"Error connecting to the database: {e}")
            raise Exception(f"Database connection failed: {e}") from e

    @staticmethod
    def execute_query(
        query: str,
        params: Union[Tuple, List] = (),
        fetchone: bool = True
    ) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]:
        """
        Executes a query on the database and handles the cursor.

        Args:
            query (str): SQL query to execute.
            params (Tuple | List): Parameters for the SQL query.
            fetchone (bool): If True, returns one row; otherwise, returns all rows.

        Returns:
            Optional[Dict | List[Dict]]: Query results (if applicable).
        """
        try:
            with Database.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    if cursor.description:  # Only attempt to fetch results if the query returns something
                        return cursor.fetchone() if fetchone else cursor.fetchall()
                    connection.commit()  # Commit transaction on INSERT, UPDATE, or DELETE.
        except Exception as e:
            logger.error(f"Error executing query: {query}, params: {params}, error: {e}")
            raise Exception("Database query error") from e

    @staticmethod
    def create_tables():
        """Creates the necessary tables for the application."""
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
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
            ''',
            '''
            CREATE TABLE IF NOT EXISTS pictures (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                image_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                reporter_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                reported_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                reason TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS blocks (
                id SERIAL PRIMARY KEY,
                blocker_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                blocked_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(blocker_id, blocked_id)
            );
            '''
        ]

        try:
            with Database.get_connection() as connection:
                with connection.cursor() as cursor:
                    for query in queries:
                        cursor.execute(query)
                    connection.commit()
                    logger.info("Tables created successfully.")
        except psycopg.Error as e:
            logger.error(f"Error during table creation: {e}")
            raise Exception("Error creating tables") from e


# Call create_tables() if run directly
if __name__ == "__main__":
    try:
        Database.create_tables()
        logger.info("Database setup completed.")
    except Exception as e:
        logger.error(f"Database setup failed: {e}")