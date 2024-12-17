from flask import Blueprint, request, jsonify
from manager.likes_manager import send_like, remove_like, fetch_liked_users, fetch_matches
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear Blueprint para likes
likes_bp = Blueprint('likes', __name__, url_prefix='/likes')

@likes_bp.route('/send', methods=['POST'])
def send_like_route():
    """
    Endpoint para enviar un 'like' de un usuario a otro.
    
    JSON Payload:
        - user_id (int): ID del usuario que da el 'like'.
        - liked_user_id (int): ID del usuario que recibe el 'like'.

    Returns:
        JSON: Resultado del 'like', incluyendo si hubo un 'match'.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'liked_user_id' not in data:
        return jsonify({"error": "Both user_id and liked_user_id are required."}), 400

    try:
        result = send_like(data['user_id'], data['liked_user_id'])
        return jsonify(result), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@likes_bp.route('/remove', methods=['POST'])
def remove_like_route():
    """
    Endpoint para eliminar un 'like' entre usuarios.
    
    JSON Payload:
        - user_id (int): ID del usuario que elimina el 'like'.
        - liked_user_id (int): ID del usuario que recibió el 'like'.

    Returns:
        JSON: Resultado de la eliminación del 'like'.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'liked_user_id' not in data:
        return jsonify({"error": "Both user_id and liked_user_id are required."}), 400

    try:
        result = remove_like(data['user_id'], data['liked_user_id'])
        return jsonify(result), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@likes_bp.route('/liked-users/<int:user_id>', methods=['GET'])
def get_liked_users_route(user_id):
    """
    Endpoint para obtener los usuarios a los que un usuario ha dado 'like'.

    Args:
        user_id (int): ID del usuario que realiza la consulta.

    Returns:
        JSON: Lista de IDs de usuarios que recibieron un 'like'.
    """
    try:
        liked_users = fetch_liked_users(user_id)
        return jsonify({"liked_users": liked_users}), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@likes_bp.route('/matches/<int:user_id>', methods=['GET'])
def get_matches_route(user_id):
    """
    Endpoint para obtener los 'matches' de un usuario.

    Args:
        user_id (int): ID del usuario que realiza la consulta.

    Returns:
        JSON: Lista de IDs de usuarios con los que hay un 'match'.
    """
    try:
        matches = fetch_matches(user_id)
        return jsonify({"matches": matches}), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


