from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_parameters(*args):
    """Valida que los parámetros no sean None, vacíos y sean enteros."""
    for arg in args:
        if not arg or not isinstance(arg, int):
            raise ValueError("All parameters must be non-empty integers.")

def execute_write_query(query, params):
    """Ejecuta una consulta SQL de escritura (INSERT/DELETE/UPDATE)."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount  # Número de filas afectadas
    except Exception as e:
        logger.error(f"Database error during write operation. Query: {query}, Params: {params}, Error: {e}")
        raise Exception("Database write operation failed.") from e

def execute_read_query(query, params):
    """Ejecuta una consulta SQL de lectura (SELECT)."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()  # Devuelve todos los resultados
    except Exception as e:
        logger.error(f"Database error during read operation. Query: {query}, Params: {params}, Error: {e}")
        raise Exception("Database read operation failed.") from e

def like_user(user_id, liked_user_id):
    """Registra un 'like' de un usuario hacia otro."""
    validate_parameters(user_id, liked_user_id)
    
    # Verificar si ya existe el like
    exists_query = '''
        SELECT 1 FROM likes
        WHERE user_id = %s AND liked_user_id = %s
    '''
    if execute_read_query(exists_query, (user_id, liked_user_id)):
        return {"liked_user_id": liked_user_id, "status": "already_liked"}
    
    # Agregar el like
    insert_query = '''
        INSERT INTO likes (user_id, liked_user_id, timestamp)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
    '''
    try:
        execute_write_query(insert_query, (user_id, liked_user_id))
        return {"liked_user_id": liked_user_id, "status": "like_added"}
    except Exception as e:
        logger.error(f"Error while liking user {liked_user_id} by {user_id}: {e}")
        raise

def unlike_user(user_id, liked_user_id):
    """Elimina un 'like' de un usuario hacia otro."""
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
    """Obtiene una lista de usuarios a los que un usuario ha dado 'like'."""
    validate_parameters(user_id)
    
    query = '''
        SELECT liked_user_id
        FROM likes
        WHERE user_id = %s
    '''
    try:
        results = execute_read_query(query, (user_id,))
        return [row['liked_user_id'] for row in results]
    except Exception as e:
        logger.error(f"Error while fetching liked users for user {user_id}: {e}")
        raise

def get_matches(user_id):
    """Obtiene una lista de usuarios que tienen un 'match' con el usuario."""
    validate_parameters(user_id)
    
    query = '''
        SELECT l1.liked_user_id AS match_id
        FROM likes l1
        JOIN likes l2 ON l1.user_id = l2.liked_user_id
        WHERE l1.user_id = %s AND l2.user_id = l1.liked_user_id
    '''
    try:
        results = execute_read_query(query, (user_id,))
        return [row['match_id'] for row in results]
    except Exception as e:
        logger.error(f"Error while fetching matches for user {user_id}: {e}")
        raise




