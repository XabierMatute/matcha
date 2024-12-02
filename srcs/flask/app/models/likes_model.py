from .database import Database
import logging

logging.basicConfig(level=logging.INFO)

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
                logging.info(f"Message created: {result}")
                return result
    except Exception as e:
        logging.error(f"Error creating message from {sender_id} to {receiver_id}: {e}")
        raise Exception("Error creating message") from e

def get_messages_between_users(user1_id, user2_id, limit=None):
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
    if limit:
        query += f" LIMIT {limit}"

    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching messages between {user1_id} and {user2_id}: {e}")
        raise Exception("Error fetching messages") from e

def get_recent_messages(user_id, limit=10):
    """Obtiene los mensajes más recientes para un usuario."""
    if not user_id:
        raise ValueError("user_id is required to fetch recent messages.")
    
    query = '''
        SELECT id, sender_id, receiver_id, message, timestamp
        FROM chats
        WHERE sender_id = %s OR receiver_id = %s
        ORDER BY timestamp DESC
        LIMIT %s
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, user_id, limit))
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching recent messages for user ID {user_id}: {e}")
        raise Exception("Error fetching recent messages") from e

def delete_message(message_id):
    """Elimina un mensaje por su ID."""
    if not message_id:
        raise ValueError("message_id is required to delete a message.")
    
    query = '''
        DELETE FROM chats
        WHERE id = %s
        RETURNING id, sender_id, receiver_id, message
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (message_id,))
                result = cursor.fetchone()
                connection.commit()
                if result:
                    logging.info(f"Message deleted: {result}")
                else:
                    logging.info("No message found to delete.")
                return result
    except Exception as e:
        logging.error(f"Error deleting message ID {message_id}: {e}")
        raise Exception("Error deleting message") from e


