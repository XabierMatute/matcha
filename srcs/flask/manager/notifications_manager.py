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

logging.basicConfig(level=logging.INFO)

def validate_required_field(field, field_name: str):
    """Valida que un campo requerido no sea nulo o vacío."""
    if not field:
        raise ValueError(f"{field_name} is required.")

def send_notification(user_id: int, notification_type: str, message: str) -> Dict:
    """
    Crea una nueva notificación para un usuario.
    
    Args:
        user_id (int): ID del usuario receptor.
        notification_type (str): Tipo de notificación.
        message (str): Mensaje de la notificación.

    Returns:
        Dict: Información de la notificación creada.
    
    Raises:
        ValueError: Si algún campo requerido está vacío.
        Exception: Si ocurre un error al crear la notificación.
    """
    try:
        validate_required_field(user_id, "User ID")
        validate_required_field(notification_type, "Notification type")
        validate_required_field(message, "Message")

        return create_notification(user_id, notification_type, message)
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
        raise Exception("Unable to send notification") from e

def fetch_user_notifications(user_id: int, limit: int = None, offset: int = None) -> List[Dict]:
    """
    Obtiene todas las notificaciones de un usuario con soporte para paginación.

    Args:
        user_id (int): ID del usuario.
        limit (int, opcional): Número máximo de resultados.
        offset (int, opcional): Desplazamiento inicial.

    Returns:
        List[Dict]: Lista de notificaciones.
    
    Raises:
        ValueError: Si el user_id no es válido.
        Exception: Si ocurre un error al obtener las notificaciones.
    """
    validate_required_field(user_id, "User ID")
    return get_all_notifications(user_id, limit, offset)

def fetch_unread_notifications(user_id: int) -> List[Dict]:
    """
    Obtiene todas las notificaciones no leídas de un usuario.

    Args:
        user_id (int): ID del usuario.

    Returns:
        List[Dict]: Lista de notificaciones no leídas.
    
    Raises:
        ValueError: Si el user_id no es válido.
        Exception: Si ocurre un error al obtener las notificaciones no leídas.
    """
    validate_required_field(user_id, "User ID")
    return get_unread_notifications(user_id)

def mark_notification_as_read(notification_id: int) -> Dict:
    """
    Marca una notificación como leída.

    Args:
        notification_id (int): ID de la notificación.

    Returns:
        Dict: Información de la notificación actualizada.
    
    Raises:
        ValueError: Si el notification_id no es válido.
        Exception: Si ocurre un error al marcar la notificación como leída.
    """
    validate_required_field(notification_id, "Notification ID")
    return mark_as_read(notification_id)

def remove_notification(notification_id: int) -> Dict:
    """
    Elimina una notificación por su ID.

    Args:
        notification_id (int): ID de la notificación.

    Returns:
        Dict: Información de la notificación eliminada.
    
    Raises:
        ValueError: Si el notification_id no es válido.
        Exception: Si ocurre un error al eliminar la notificación.
    """
    validate_required_field(notification_id, "Notification ID")
    return delete_notification(notification_id)

def remove_multiple_notifications(notification_ids: List[int]) -> List[Dict]:
    """
    Elimina múltiples notificaciones por sus IDs.

    Args:
        notification_ids (List[int]): Lista de IDs de notificaciones.

    Returns:
        List[Dict]: Lista de notificaciones eliminadas.
    
    Raises:
        ValueError: Si la lista de notification_ids está vacía.
        Exception: Si ocurre un error al eliminar las notificaciones.
    """
    if not notification_ids or not all(isinstance(id, int) and id > 0 for id in notification_ids):
        raise ValueError("A valid list of positive integer notification IDs is required.")
    return delete_notifications(notification_ids)

def group_notifications_by_type(user_id: int) -> Dict[str, List[Dict]]:
    """
    Agrupa las notificaciones de un usuario por tipo.

    Args:
        user_id (int): ID del usuario.

    Returns:
        Dict[str, List[Dict]]: Notificaciones agrupadas por tipo.
    
    Raises:
        ValueError: Si el user_id no es válido.
        Exception: Si ocurre un error al agrupar las notificaciones.
    """
    notifications = fetch_user_notifications(user_id)
    grouped = {}
    for notification in notifications:
        grouped.setdefault(notification['type'], []).append(notification)
    return grouped

