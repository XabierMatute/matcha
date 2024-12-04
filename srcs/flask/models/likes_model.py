from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función utilitaria para validar parámetros
def validate_parameters(*args):
    """Valida que ninguno de los parámetros sea None o vacío."""
    for arg in args:
        if not arg:
            raise ValueError("All parameters are required and cannot be None.")

# Función común para ejecutar consultas de escritura
def execute_write_query(query, params):
    """Ejecuta una consulta SQL de escritura (INSERT/DELETE/UPDATE)."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount  # Número de filas afectadas
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise Exception("Database write operation failed.") from e

# Función común para ejecutar consultas de lectura
def execute_read_query(query, params):
    """Ejecuta una consulta SQL de lectura (SELECT)."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()  # Devuelve todos los resultados
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise Exception("Database read operation failed.") from e

# Función para dar "like" a un usuario
def like_user(user_id, liked_user_id):
    """Registra un 'like' de un usuario hacia otro."""
    validate_parameters(user_id, liked_user_id)
    
    query = '''
        INSERT INTO likes (user_id, liked_user_id, timestamp)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT DO NOTHING
    '''
    rowcount = execute_write_query(query, (user_id, liked_user_id))
    if rowcount > 0:
        logger.info(f"User {user_id} liked user {liked_user_id}.")
    else:
        logger.info(f"User {user_id} already liked user {liked_user_id}.")
    return rowcount

# Función para eliminar un "like"
def unlike_user(user_id, liked_user_id):
    """Elimina un 'like' de un usuario hacia otro."""
    validate_parameters(user_id, liked_user_id)
    
    query = '''
        DELETE FROM likes
        WHERE user_id = %s AND liked_user_id = %s
    '''
    rowcount = execute_write_query(query, (user_id, liked_user_id))
    if rowcount > 0:
        logger.info(f"User {user_id} unliked user {liked_user_id}.")
    else:
        logger.info(f"No like found for user {user_id} to unlike user {liked_user_id}.")
    return rowcount

# Función para obtener usuarios a los que se les ha dado "like"
def get_liked_users(user_id):
    """Obtiene una lista de usuarios a los que un usuario ha dado 'like'."""
    validate_parameters(user_id)
    
    query = '''
        SELECT liked_user_id
        FROM likes
        WHERE user_id = %s
    '''
    results = execute_read_query(query, (user_id,))
    liked_users = [row[0] for row in results]  # Extrae los IDs de los usuarios
    logger.info(f"User {user_id} has liked {len(liked_users)} users.")
    return liked_users


