# database.py
import psycopg
import os

# Función para obtener la conexión a la base de datos
def get_db_connection():
    connection_string = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/matcha_dev')
    return psycopg.connect(connection_string)

# Función para crear las tablas necesarias en la base de datos
def create_tables():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                email VARCHAR(100) UNIQUE,
                password_hash TEXT
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interests (
                id SERIAL PRIMARY KEY,
                tag VARCHAR(100) UNIQUE
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_interests (
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                interest_id INTEGER REFERENCES interests(id) ON DELETE CASCADE,
                PRIMARY KEY (user_id, interest_id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pictures (
                id SERIAL PRIMARY KEY,
                url TEXT,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            );
        ''')
        connection.commit()  # Guardamos los cambios
    connection.close()

# Función para insertar un nuevo usuario
def insert_user(username, email, password_hash):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        ''', (username, email, password_hash))
        connection.commit()  # Guardamos los cambios
    connection.close()







