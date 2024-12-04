from .database import Database
import logging

logging.basicConfig(level=logging.INFO)

def create_notification(user_id, notification_type, message):
    """Crea una nueva notificación para un usuario."""
    if not user_id or not notification_type or not message:
        raise ValueError("user_id, notification_type, and message are required to create a notification.")
    
    query = '''
        INSERT INTO notifications (user_id, type, message)
        VALUES (%s, %s, %s)
        RETURNING id, user_id, type, message, timestamp, is_read
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, notification_type, message))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error creating notification for user ID {user_id}: {e}")
        raise Exception("Error creating notification") from e

def get_notifications(user_id):
    """Obtiene todas las notificaciones de un usuario."""
    if not user_id:
        raise ValueError("user_id is required to fetch notifications.")
    
    query = "SELECT * FROM notifications WHERE user_id = %s ORDER BY timestamp DESC"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching notifications for user ID {user_id}: {e}")
        raise Exception("Error fetching notifications") from e


def get_unread_notifications(user_id):
    """Obtiene todas las notificaciones no leídas de un usuario."""
    if not user_id:
        raise ValueError("user_id is required to fetch unread notifications.")
    
    query = "SELECT * FROM notifications WHERE user_id = %s AND is_read = FALSE ORDER BY timestamp DESC"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching unread notifications for user ID {user_id}: {e}")
        raise Exception("Error fetching unread notifications") from e

def mark_as_read(notification_id):
    """Marca una notificación como leída."""
    if not notification_id:
        raise ValueError("notification_id is required to mark notification as read.")
    
    query = '''
        UPDATE notifications
        SET is_read = TRUE
        WHERE id = %s
        RETURNING id, user_id, type, message, timestamp, is_read
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (notification_id,))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error marking notification ID {notification_id} as read: {e}")
        raise Exception("Error marking notification as read") from e
def delete_notification(notification_id):
    """Elimina una notificación."""
    if not notification_id:
        raise ValueError("notification_id is required to delete a notification.")
    
    query = "DELETE FROM notifications WHERE id = %s RETURNING id"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (notification_id,))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error deleting notification ID {notification_id}: {e}")
        raise Exception("Error deleting notification") from e
