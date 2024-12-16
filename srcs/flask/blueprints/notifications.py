from flask import Blueprint, request, jsonify
from manager.notifications_manager import (
    fetch_user_notifications,
    fetch_unread_notifications,
    mark_notification_as_read,
    remove_notification,
    remove_multiple_notifications,
    send_notification
)

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

def error_response(message, status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"error": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code

def validate_user_id(user_id):
    """Valida que el 'user_id' esté presente y sea un número entero positivo."""
    if not user_id:
        raise ValueError("User ID is required")
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("User ID must be a positive integer")
    return user_id

@notifications_bp.route('/', methods=['GET'])
def list_notifications():
    """Obtiene todas las notificaciones del usuario con soporte para paginación."""
    user_id = request.args.get('user_id', type=int)
    limit = request.args.get('limit', type=int, default=10)
    offset = request.args.get('offset', type=int, default=0)

    if not user_id:
        return error_response("User ID is required")

    try:
        notifications = fetch_user_notifications(user_id, limit, offset)
        return jsonify({"notifications": notifications}), 200
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response("Failed to fetch notifications", details=str(e))


@notifications_bp.route('/unread', methods=['GET'])
def list_unread_notifications():
    """Obtiene todas las notificaciones no leídas del usuario."""
    try:
        user_id = validate_user_id(request.args.get('user_id', type=int))
        notifications = fetch_unread_notifications(user_id)
        return jsonify({"notifications": notifications}), 200
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response("Failed to fetch unread notifications", details=str(e))

@notifications_bp.route('/<int:notification_id>', methods=['PUT'])
def mark_as_read_route(notification_id):
    """Marca una notificación como leída."""
    try:
        notification = mark_notification_as_read(notification_id)
        return jsonify({"message": "Notification marked as read", "notification": notification}), 200
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response("Failed to mark notification as read", details=str(e))

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification_route(notification_id):
    """Elimina una notificación por su ID."""
    try:
        deleted_notification = remove_notification(notification_id)
        return jsonify({"message": "Notification deleted", "notification": deleted_notification}), 200
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response("Failed to delete notification", details=str(e))

@notifications_bp.route('/batch', methods=['DELETE'])
def delete_notifications_batch():
    """Elimina múltiples notificaciones."""
    try:
        data = request.get_json()
        notification_ids = data.get('notification_ids')

        # Validar que notification_ids sea una lista de enteros
        if not notification_ids or not isinstance(notification_ids, list) or not all(isinstance(id, int) for id in notification_ids):
            return error_response("A list of valid notification IDs is required")

        # Llamar a la función del manager para eliminar las notificaciones
        deleted_notifications = remove_multiple_notifications(notification_ids)
        return jsonify({
            "message": f"{len(deleted_notifications)} notifications deleted successfully"
        }), 200
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response("Failed to delete notifications", details=str(e))



