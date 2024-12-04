from flask import Blueprint, request, jsonify
from models.notifications_model import get_notifications, mark_as_read

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@notifications_bp.route('/', methods=['GET'])
def list_notifications():
    """Obtiene todas las notificaciones del usuario."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        notifications = get_notifications(user_id)
        return jsonify({"notifications": notifications}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/<int:notification_id>', methods=['PUT'])
def mark_notification_as_read(notification_id):
    """Marca una notificación como leída."""
    try:
        mark_as_read(notification_id)
        return jsonify({"message": "Notification marked as read"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
