from flask import Blueprint, request, jsonify
from manager.likes_manager import send_like, remove_like, fetch_liked_users, fetch_matches

likes_bp = Blueprint('likes', __name__, url_prefix='/likes')


@likes_bp.route('/<int:liked_user_id>', methods=['POST'])
def like(liked_user_id):
    """Da 'like' a un usuario."""
    user_id = request.json.get('user_id')
    if not user_id or not isinstance(user_id, int):
        return jsonify({"error": "Valid user_id is required in the request body"}), 400

    try:
        result = send_like(user_id, liked_user_id)
        return jsonify({
            "message": "User liked successfully",
            "like_status": result
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@likes_bp.route('/<int:liked_user_id>', methods=['DELETE'])
def unlike(liked_user_id):
    """Elimina el 'like' a un usuario."""
    user_id = request.json.get('user_id')
    if not user_id or not isinstance(user_id, int):
        return jsonify({"error": "Valid user_id is required in the request body"}), 400

    try:
        result = remove_like(user_id, liked_user_id)
        return jsonify({
            "message": "Like removed successfully",
            "like_status": result
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@likes_bp.route('/', methods=['GET'])
def get_likes():
    """Obtiene la lista de usuarios a los que el usuario ha dado 'like'."""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "Valid user_id is required as a query parameter"}), 400

    try:
        likes = fetch_liked_users(user_id)
        return jsonify({
            "message": f"Fetched {len(likes)} liked users.",
            "likes": likes
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@likes_bp.route('/matches', methods=['GET'])
def get_matches():
    """Obtiene la lista de usuarios con los que el usuario tiene un 'match'."""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "Valid user_id is required as a query parameter"}), 400

    try:
        matches = fetch_matches(user_id)
        return jsonify({
            "message": f"Fetched {len(matches)} matches.",
            "matches": matches
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

