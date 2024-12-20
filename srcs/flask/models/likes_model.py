from .database import Database
import logging
from datetime import datetime

# Configuración básica del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Excepción personalizada para errores de base de datos
class DatabaseError(Exception):
    """Excepción personalizada para errores de base de datos."""
    pass

def validate_parameters(*args):
    """
    Valida que los parámetros no sean None, vacíos y sean enteros positivos.
    
    Args:
        *args: Lista de parámetros a validar.
    
    Raises:
        ValueError: Si algún parámetro no cumple con las validaciones.
    """
    for arg in args:
        if not isinstance(arg, int) or arg <= 0:
            raise ValueError("All parameters must be non-empty positive integers.")

def execute_write_query(query, params):
    """
    Ejecuta una consulta SQL de escritura (INSERT/DELETE/UPDATE).
    
    Args:
        query (str): La consulta SQL a ejecutar.
        params (tuple): Los parámetros para la consulta.
    
    Returns:
        int: El número de filas afectadas por la consulta.
    
    Raises:
        DatabaseError: Si ocurre un error durante la operación de escritura.
    """
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount  # Devuelve el número de filas afectadas
    except Exception as e:
        logger.error(f"Database error during write operation. Query: {query}, Params: {params}, Error: {e}")
        raise DatabaseError("Database write operation failed.") from e

def execute_read_query(query, params):
    """
    Ejecuta una consulta SQL de lectura (SELECT).
    
    Args:
        query (str): La consulta SQL a ejecutar.
        params (tuple): Los parámetros para la consulta.
    
    Returns:
        list: Una lista de resultados de la consulta.
    
    Raises:
        DatabaseError: Si ocurre un error durante la operación de lectura.
    """
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()  # Devuelve todos los resultados obtenidos
    except Exception as e:
        logger.error(f"Database error during read operation. Query: {query}, Params: {params}, Error: {e}")
        raise DatabaseError("Database read operation failed.") from e

def like_user(user_id, liked_user_id):
    """
    Registra un 'like' de un usuario hacia otro.
    
    Args:
        user_id (int): ID del usuario que da el 'like'.
        liked_user_id (int): ID del usuario que recibe el 'like'.
    
    Returns:
        dict: Un diccionario con el estado del 'like'.
    """
    validate_parameters(user_id, liked_user_id)

    # Consulta para insertar un 'like' sin duplicados
    insert_query = '''
        INSERT INTO likes (user_id, liked_user_id, timestamp)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    '''
    try:
        timestamp = datetime.utcnow()
        rowcount = execute_write_query(insert_query, (user_id, liked_user_id, timestamp))
        status = "like_added" if rowcount > 0 else "already_liked"
        return {"liked_user_id": liked_user_id, "status": status}
    except Exception as e:
        logger.error(f"Error while liking user {liked_user_id} by {user_id}: {e}")
        raise

def unlike_user(user_id, liked_user_id):
    """
    Elimina un 'like' de un usuario hacia otro.
    
    Args:
        user_id (int): ID del usuario que elimina el 'like'.
        liked_user_id (int): ID del usuario al que se quitó el 'like'.
    
    Returns:
        dict: Un diccionario con el estado de la eliminación del 'like'.
    """
    validate_parameters(user_id, liked_user_id)

    query = '''
        DELETE FROM likes
        WHERE user_id = %s AND liked_user_id = %s
    '''
    try:
        rowcount = execute_write_query(query, (user_id, liked_user_id))
        return {"liked_user_id": liked_user_id, "status": "like_removed" if rowcount > 0 else "no_like_found"}
    except Exception as e:
        logger.error(f"Error while unliking user {liked_user_id} by {user_id}: {e}")
        raise

def get_liked_users(user_id):
    """
    Obtiene una lista de usuarios a los que un usuario ha dado 'like'.
    
    Args:
        user_id (int): ID del usuario.
    
    Returns:
        list: Lista de IDs de usuarios que recibieron un 'like'.
    """
    validate_parameters(user_id)

    query = '''
        SELECT liked_user_id
        FROM likes
        WHERE user_id = %s
    '''
    try:
        results = execute_read_query(query, (user_id,))
        return [row["liked_user_id"] for row in results]
    except Exception as e:
        logger.error(f"Error while fetching liked users for user {user_id}: {e}")
        raise

def get_matches(user_id):
    """
    Obtiene una lista de usuarios que tienen un 'match' con el usuario.
    
    Args:
        user_id (int): ID del usuario.
    
    Returns:
        list: Lista de IDs de usuarios con los que hay un 'match'.
    """
    validate_parameters(user_id)

    query = '''
        SELECT l1.liked_user_id AS match_id
        FROM likes l1
        JOIN likes l2 ON l1.user_id = l2.liked_user_id
        WHERE l1.user_id = %s AND l2.user_id = l1.liked_user_id
    '''
    try:
        results = execute_read_query(query, (user_id,))
        return [row["match_id"] for row in results]
    except Exception as e:
        logger.error(f"Error while fetching matches for user {user_id}: {e}")
        raise
