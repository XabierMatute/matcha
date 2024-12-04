from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_message(sender_id, receiver_id, message):
    """Crea un nuevo mensaje en el chat."""
    if not sender_id or not receiver_id or not message:
        raise ValueError("sender_id, receiver_id, and message are required to create a message.")
    
    query = '''
        INSERT INTO chats (sender_id, receiver_id, message, timestamp)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        RETURNING id, sender_id, receiver_id, message, timestamp
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (sender_id, receiver_id, message))
                connection.commit()
                result = cursor.fetchone()
                if result:
                    logger.info(f"Message created successfully: {result}")
                else:
                    logger.warning("Message creation returned no result")
                return result
    except Exception as e:
        logger.error(f"Error creating message from {sender_id} to {receiver_id}: {e}")
        raise Exception("Database error while creating message") from e

def get_messages_between_users(user1_id, user2_id):
    """Obtiene los mensajes entre dos usuarios."""
    if not user1_id or not user2_id:
        raise ValueError("Both user1_id and user2_id are required to fetch messages.")
    
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
                if messages:
                    logger.info(f"Fetched {len(messages)} messages between {user1_id} and {user2_id}")
                else:
                    logger.warning(f"No messages found between {user1_id} and {user2_id}")
                return messages
    except Exception as e:
        logger.error(f"Error fetching messages between {user1_id} and {user2_id}: {e}")
        raise Exception("Database error while fetching messages") from e

