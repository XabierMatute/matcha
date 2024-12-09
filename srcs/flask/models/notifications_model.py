from .database import Database
import logging

logging.basicConfig(level=logging.INFO)

ERROR_MESSAGES = {
    "missing_user_id": "user_id is required.",
    "missing_notification_id": "notification_id is required.",
    "missing_required_fields": "user_id, notification_type, and message are required."
}

def create_notification(user_id, notification_type, message):
    if not user_id or not notification_type or not message:
        raise ValueError(ERROR_MESSAGES["missing_required_fields"])
    query = '''
        INSERT INTO notifications (user_id, type, message)
        VALUES (%s, %s, %s)
        RETURNING id, user_id, type, message, timestamp, is_read
    '''
    return _execute_query(query, (user_id, notification_type, message), fetchone=True)

def get_all_notifications(user_id, limit=None, offset=None):
    if not user_id:
        raise ValueError(ERROR_MESSAGES["missing_user_id"])
    query = '''
        SELECT * FROM notifications
        WHERE user_id = %s
        ORDER BY timestamp DESC
    '''
    params = [user_id]
    if limit and offset is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
    return _execute_query(query, tuple(params), fetchone=False)

def get_unread_notifications(user_id):
    if not user_id:
        raise ValueError(ERROR_MESSAGES["missing_user_id"])
    query = '''
        SELECT * FROM notifications
        WHERE user_id = %s AND is_read = FALSE
        ORDER BY timestamp DESC
    '''
    return _execute_query(query, (user_id,), fetchone=False)

def mark_as_read(notification_id):
    if not notification_id:
        raise ValueError(ERROR_MESSAGES["missing_notification_id"])
    query = '''
        UPDATE notifications
        SET is_read = TRUE
        WHERE id = %s
        RETURNING id, user_id, type, message, timestamp, is_read
    '''
    return _execute_query(query, (notification_id,), fetchone=True)

def delete_notification(notification_id):
    if not notification_id:
        raise ValueError(ERROR_MESSAGES["missing_notification_id"])
    query = "DELETE FROM notifications WHERE id = %s RETURNING id"
    return _execute_query(query, (notification_id,), fetchone=True)

def delete_notifications(notification_ids):
    if not notification_ids:
        raise ValueError("notification_ids cannot be empty.")
    query = '''
        DELETE FROM notifications
        WHERE id = ANY(%s)
        RETURNING id
    '''
    return _execute_query(query, (notification_ids,), fetchone=False)

def _execute_query(query, params, fetchone=False):
    """Centraliza la ejecución de consultas con manejo de errores."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetchone:
                    return cursor.fetchone()
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Database query error: {e}")
        raise Exception("An unexpected error occurred") from e


