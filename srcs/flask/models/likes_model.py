from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función utilitaria para validar parámetros
def validate_parameters(*args):
    """Valida que ninguno de los parámetros sea None o vacío."""
    for arg in args:
        if not arg:
            raise ValueError(f"{arg} is required.")
            
# Función común para ejecutar una consulta
def execute_query(query, params):
    """Ejecuta una consulta SQL y maneja la conexión a la base de datos."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return cursor.fetchall()  # Devuelve todos los resultados
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise Exception("Database operation failed.") from e

def create_message(sender_id, receiver_id, message):
    """Crea un nuevo mensaje en el chat."""
    validate_parameters(sender_id, receiver_id, message)
    
    query = '''
        INSERT INTO chats (sender_id, receiver_id, message, timestamp)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        RETURNING id, sender_id, receiver_id, message, timestamp
    '''
    result = execute_query(query, (sender_id, receiver_id, message))
    logger.info(f"Message created: {result}")
    return result

def get_messages_between_users(user1_id, user2_id, limit=None):
    """Obtiene los mensajes entre dos usuarios."""
    validate_parameters(user1_id, user2_id)
    
    query = '''
        SELECT id, sender_id, receiver_id, message, timestamp
        FROM chats
        WHERE (sender_id = %s AND receiver_id = %s)
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
    '''
    if limit:
        query += f" LIMIT {limit}"

    result = execute_query(query, (user1_id, user2_id, user2_id, user1_id))
    logger.info(f"Fetched {len(result)} messages between {user1_id} and {user2_id}")
    return result

def get_recent_messages(user_id, limit=10):
    """Obtiene los mensajes más recientes para un usuario."""
    validate_parameters(user_id)
    
    query = '''
        SELECT id, sender_id, receiver_id, message, timestamp
        FROM chats
        WHERE sender_id = %s OR receiver_id = %s
        ORDER BY timestamp DESC
        LIMIT %s
    '''
    result = execute_query(query, (user_id, user_id, limit))
    logger.info(f"Fetched {len(result)} recent messages for user ID {user_id}")
    return result

def delete_message(message_id):
    """Elimina un mensaje por su ID."""
    validate_parameters(message_id)
    
    query = '''
        DELETE FROM chats
        WHERE id = %s
        RETURNING id, sender_id, receiver_id, message
    '''
    result = execute_query(query, (message_id,))
    
    if result:
        logger.info(f"Message deleted: {result}")
    else:
        logger.info("No message found to delete.")
    
    return result



