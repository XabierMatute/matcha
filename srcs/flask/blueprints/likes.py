from flask import Blueprint, request, jsonify
from models.likes_model import like_user, unlike_user, get_liked_users

likes_bp = Blueprint('likes', __name__, url_prefix='/likes')

@likes_bp.route('/<int:liked_user_id>', methods=['POST'])
def like(liked_user_id):
    """
    Da 'like' a un usuario.
    Requiere: user_id en el cuerpo de la solicitud (JSON).
    """
    user_id = request.json.get('user_id')
    if not user_id or not isinstance(user_id, int):
        return jsonify({"error": "Valid user_id is required in the request body"}), 400

    try:
        like_user(user_id, liked_user_id)
        return jsonify({
            "message": "User liked successfully",
            "user_id": user_id,
            "liked_user_id": liked_user_id
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@likes_bp.route('/<int:liked_user_id>', methods=['DELETE'])
def unlike(liked_user_id):
    """
    Elimina el 'like' a un usuario.
    Requiere: user_id en el cuerpo de la solicitud (JSON).
    """
    user_id = request.json.get('user_id')
    if not user_id or not isinstance(user_id, int):
        return jsonify({"error": "Valid user_id is required in the request body"}), 400

    try:
        unlike_user(user_id, liked_user_id)
        return jsonify({
            "message": "Like removed successfully",
            "user_id": user_id,
            "liked_user_id": liked_user_id
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@likes_bp.route('/', methods=['GET'])
def get_likes():
    """
    Obtiene la lista de usuarios que el usuario ha 'likeado'.
    Requiere: user_id como parámetro en la URL.
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "Valid user_id is required as a query parameter"}), 400

    try:
        likes = get_liked_users(user_id)
        return jsonify({
            "message": f"Fetched {len(likes)} liked users.",
            "likes": likes
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

