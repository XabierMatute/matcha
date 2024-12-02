from .database import Database
import logging

logging.basicConfig(level=logging.INFO)

def get_user_by_id(user_id):
    """Obtiene un usuario por su ID."""
    query = "SELECT * FROM users WHERE id = %s"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error fetching user by ID: {e}")
        raise Exception("Error fetching user by ID") from e

def get_user_by_username(username):
    """Obtiene un usuario por su nombre de usuario."""
    query = "SELECT * FROM users WHERE username = %s"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username,))
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error fetching user by username: {e}")
        raise Exception("Error fetching user by username") from e

def create_user(username, email, password_hash, birthdate, first_name=None, last_name=None):
    """Crea un nuevo usuario."""
    query = '''
        INSERT INTO users (username, email, password_hash, birthdate, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, username, email, birthdate, first_name, last_name
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username, email, password_hash, birthdate, first_name, last_name))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise Exception("Error creating user") from e

def update_user(user_id, username=None, email=None, first_name=None, last_name=None):
    """Actualiza los datos de un usuario."""
    updates = []
    params = []

    if username:
        updates.append("username = %s")
        params.append(username)
    if email:
        updates.append("email = %s")
        params.append(email)
    if first_name:
        updates.append("first_name = %s")
        params.append(first_name)
    if last_name:
        updates.append("last_name = %s")
        params.append(last_name)

    if not updates:
        raise ValueError("No fields provided to update.")

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, username, email, first_name, last_name"
    params.append(user_id)

    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error updating user: {e}")
        raise Exception("Error updating user") from e

def delete_user(user_id):
    """Elimina un usuario por su ID."""
    query = "DELETE FROM users WHERE id = %s RETURNING id"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        raise Exception("Error deleting user") from e
