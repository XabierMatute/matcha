import psycopg
import logging
from database import get_db_connection

# Configurar el logger
logging.basicConfig(level=logging.INFO)

def create_user(username, email, password_hash):
    """
    Crea un nuevo usuario en la base de datos.

    :param username: Nombre de usuario del nuevo usuario.
    :param email: Correo electrónico del nuevo usuario.
    :param password_hash: Hash de la contraseña del nuevo usuario.
    :return: Diccionario con los datos del usuario creado.
    """
    query = '''
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id, username, email, is_active, created_at
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username, email, password_hash))
                result = cursor.fetchone()
                connection.commit()
                logging.info(f"User created successfully: {result}")
                return {
                    "id": result[0],
                    "username": result[1],
                    "email": result[2],
                    "is_active": result[3],
                    "created_at": result[4],
                }
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise Exception("Error creating user")

def get_user_by_id(user_id):
    """
    Obtiene los datos de un usuario por su ID.

    :param user_id: ID del usuario.
    :return: Diccionario con los datos del usuario.
    """
    query = '''
        SELECT id, username, email, is_active, created_at
        FROM users
        WHERE id = %s
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "username": result[1],
                        "email": result[2],
                        "is_active": result[3],
                        "created_at": result[4],
                    }
                else:
                    logging.info("User not found.")
                    return None
    except Exception as e:
        logging.error(f"Error retrieving user by ID: {e}")
        raise Exception("Error retrieving user by ID")

def update_user_status(user_id, is_active):
    """
    Actualiza el estado de un usuario (activo/inactivo).

    :param user_id: ID del usuario.
    :param is_active: Estado de actividad del usuario (True o False).
    :return: Diccionario con los datos actualizados del usuario.
    """
    query = '''
        UPDATE users
        SET is_active = %s
        WHERE id = %s
        RETURNING id, username, email, is_active, created_at
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (is_active, user_id))
                result = cursor.fetchone()
                connection.commit()
                if result:
                    logging.info(f"User status updated successfully: {result}")
                    return {
                        "id": result[0],
                        "username": result[1],
                        "email": result[2],
                        "is_active": result[3],
                        "created_at": result[4],
                    }
                else:
                    logging.info("User not found.")
                    return None
    except Exception as e:
        logging.error(f"Error updating user status: {e}")
        raise Exception("Error updating user status")

