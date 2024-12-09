from .database import Database
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función para guardar un mensaje en la base de datos
def save_message(sender_id: int, receiver_id: int, message: str) -> dict:
    """
    Guarda un mensaje en la base de datos.
    """
    if not sender_id or not receiver_id or not message:
        raise ValueError("Sender ID, Receiver ID, and Message are required.")

    query = '''
        INSERT INTO chats (sender_id, receiver_id, message, timestamp)
        VALUES (%s, %s, %s, %s)
        RETURNING id, sender_id, receiver_id, message, timestamp
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (sender_id, receiver_id, message, datetime.utcnow()))
                connection.commit()
                result = cursor.fetchone()
        return {
            "id": result[0],
            "sender_id": result[1],
            "receiver_id": result[2],
            "message": result[3],
            "timestamp": result[4].isoformat()
        }
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        raise Exception("Failed to save message.") from e


# Función para obtener mensajes entre dos usuarios
def get_messages_between(user1_id: int, user2_id: int) -> list:
    """
    Obtiene todos los mensajes intercambiados entre dos usuarios.
    """
    if not user1_id or not user2_id:
        raise ValueError("Both user IDs are required.")

    query = '''
        SELECT id, sender_id, receiver_id, message, timestamp
        FROM chats
        WHERE (sender_id = %s AND receiver_id = %s)
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
                messages = cursor.fetchall()
        return [
            {
                "id": msg[0],
                "sender_id": msg[1],
                "receiver_id": msg[2],
                "message": msg[3],
                "timestamp": msg[4].isoformat()
            } for msg in messages
        ]
    except Exception as e:
        logger.error(f"Error fetching messages between {user1_id} and {user2_id}: {e}")
        raise Exception("Failed to fetch messages.") from e


# Función para eliminar mensajes de un usuario (opcional)
def delete_messages_by_user(user_id: int) -> int:
    """
    Elimina todos los mensajes de un usuario.
    """
    if not user_id:
        raise ValueError("User ID is required.")

    query = '''
        DELETE FROM chats
        WHERE sender_id = %s OR receiver_id = %s
        RETURNING id
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, user_id))
                deleted_messages = cursor.rowcount
                connection.commit()
        return deleted_messages
    except Exception as e:
        logger.error(f"Error deleting messages for user {user_id}: {e}")
        raise Exception("Failed to delete messages.") from e


