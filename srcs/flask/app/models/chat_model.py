from .database import Database
import logging

def create_message(sender_id, receiver_id, message):
    """Crea un nuevo mensaje en el chat."""
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
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error creating message: {e}")
        raise

def get_messages_between_users(user1_id, user2_id):
    """Obtiene los mensajes entre dos usuarios."""
    query = '''
        SELECT * FROM chats
        WHERE (sender_id = %s AND receiver_id = %s)
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching messages: {e}")
        raise
