from flask import Blueprint, request, jsonify
from manager.notifications_manager import (
    fetch_user_notifications,
    fetch_unread_notifications,
    mark_notification_as_read,
    remove_notification,
    remove_multiple_notifications,
    send_notification
)
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code

def validate_user_id():
    """Valida y obtiene el 'user_id' del request."""
    user_id = request.args.get('user_id', type=int)
    if not user_id or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")
    return user_id

@notifications_bp.route('/', methods=['GET'])
def list_notifications():
    """Obtiene todas las notificaciones del usuario con soporte para paginación."""
    try:
        user_id = validate_user_id()
        limit = request.args.get('limit', type=int, default=10)
        offset = request.args.get('offset', type=int, default=0)

        notifications = fetch_user_notifications(user_id, limit, offset)
        return jsonify(success_response(data=notifications, message="Notifications fetched successfully")), 200
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return error_response(str(e))
    except Exception as e:
        logger.error(f"Failed to fetch notifications: {e}")
        return error_response("Failed to fetch notifications", details=str(e))

@notifications_bp.route('/unread', methods=['GET'])
def list_unread_notifications():
    """Obtiene todas las notificaciones no leídas del usuario."""
    try:
        user_id = validate_user_id()
        notifications = fetch_unread_notifications(user_id)
        return jsonify(success_response(data=notifications, message="Unread notifications fetched successfully")), 200
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return error_response(str(e))
    except Exception as e:
        logger.error(f"Failed to fetch unread notifications: {e}")
        return error_response("Failed to fetch unread notifications", details=str(e))

@notifications_bp.route('/<int:notification_id>', methods=['PUT'])
def mark_as_read_route(notification_id):
    """Marca una notificación como leída."""
    try:
        if notification_id <= 0:
            raise ValueError("Notification ID must be a positive integer.")

        notification = mark_notification_as_read(notification_id)
        return jsonify(success_response(data=notification, message="Notification marked as read")), 200
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return error_response(str(e))
    except Exception as e:
        logger.error(f"Failed to mark notification as read: {e}")
        return error_response("Failed to mark notification as read", details=str(e))

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification_route(notification_id):
    """Elimina una notificación por su ID."""
    try:
        if notification_id <= 0:
            raise ValueError("Notification ID must be a positive integer.")

        deleted_notification = remove_notification(notification_id)
        return jsonify(success_response(data=deleted_notification, message="Notification deleted successfully")), 200
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return error_response(str(e))
    except Exception as e:
        logger.error(f"Failed to delete notification: {e}")
        return error_response("Failed to delete notification", details=str(e))

@notifications_bp.route('/batch', methods=['DELETE'])
def delete_notifications_batch():
    """Elimina múltiples notificaciones."""
    try:
        data = request.get_json()
        notification_ids = data.get('notification_ids')

        if not notification_ids or not isinstance(notification_ids, list) or not all(isinstance(id, int) and id > 0 for id in notification_ids):
            raise ValueError("A valid list of positive integer notification IDs is required.")

        deleted_notifications = remove_multiple_notifications(notification_ids)
        return jsonify(success_response(data={"deleted_ids": deleted_notifications}, message="Notifications deleted successfully")), 200
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return error_response(str(e))
    except Exception as e:
        logger.error(f"Failed to delete notifications: {e}")
        return error_response("Failed to delete notifications", details=str(e))

@notifications_bp.route('/send', methods=['POST'])
def send_notification_route():
    """Crea y envía una notificación a un usuario."""
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        notification_type = data.get("type")
        message = data.get("message")

        if not user_id or not notification_type or not message:
            raise ValueError("User ID, notification type, and message are required.")

        notification = send_notification(user_id, notification_type, message)
        return jsonify(success_response(data=notification, message="Notification sent successfully")), 201
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return error_response(str(e))
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        return error_response("Failed to send notification", details=str(e))





