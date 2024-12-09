from models.notifications_model import (
    create_notification,
    get_all_notifications,
    get_unread_notifications,
    mark_as_read,
    delete_notification,
    delete_notifications
)
from typing import List, Dict
import logging

def validate_required_field(field, field_name: str):
    """Valida que un campo requerido no sea nulo o vacío."""
    if not field:
        raise ValueError(f"{field_name} is required.")

def send_notification(user_id: int, notification_type: str, message: str) -> Dict:
    """Crea una nueva notificación para un usuario."""
    try:
        validate_required_field(user_id, "User ID")
        validate_required_field(notification_type, "Notification type")
        validate_required_field(message, "Message")
        return create_notification(user_id, notification_type, message)
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
        raise Exception("Unable to send notification") from e

def fetch_user_notifications(user_id: int, limit: int = None, offset: int = None) -> List[Dict]:
    """Obtiene todas las notificaciones de un usuario."""
    validate_required_field(user_id, "User ID")
    return get_all_notifications(user_id, limit, offset)

def fetch_unread_notifications(user_id: int, limit: int = None, offset: int = None) -> List[Dict]:
    """Obtiene todas las notificaciones no leídas de un usuario."""
    validate_required_field(user_id, "User ID")
    return get_unread_notifications(user_id, limit, offset)

def mark_notification_as_read(notification_id: int) -> Dict:
    """Marca una notificación como leída."""
    validate_required_field(notification_id, "Notification ID")
    return mark_as_read(notification_id)

def remove_notification(notification_id: int) -> Dict:
    """Elimina una notificación por su ID."""
    validate_required_field(notification_id, "Notification ID")
    return delete_notification(notification_id)

def remove_multiple_notifications(notification_ids: List[int]) -> List[Dict]:
    """Elimina múltiples notificaciones por sus IDs."""
    if not notification_ids or len(notification_ids) == 0:
        raise ValueError("Notification IDs are required to remove notifications.")
    return delete_notifications(notification_ids)

def group_notifications_by_type(user_id: int) -> Dict[str, List[Dict]]:
    """Agrupa las notificaciones de un usuario por tipo."""
    notifications = fetch_user_notifications(user_id)
    grouped = {}
    for notification in notifications:
        grouped.setdefault(notification['type'], []).append(notification)
    return grouped
 
