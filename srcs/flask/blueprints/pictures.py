from flask import Blueprint, request, jsonify
from manager.pictures_manager import (
    fetch_user_pictures,
    upload_picture,
    remove_picture,
    change_profile_picture
)
import logging

logger = logging.getLogger(__name__)
pictures_bp = Blueprint('pictures', __name__, url_prefix='/pictures')

def success_response(data=None, message="Operation successful"):
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed"):
    return {"success": False, "message": message}

def validate_request_data(data, required_fields):
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"{field} is required.")

@pictures_bp.route('/<int:user_id>', methods=['GET'])
def get_pictures(user_id):
    try:
        pictures = fetch_user_pictures(user_id)
        return jsonify(success_response(data=pictures, message=f"Fetched {len(pictures)} pictures.")), 200
    except ValueError as ve:
        return jsonify(error_response(str(ve))), 400
    except Exception as e:
        logger.error(f"Unexpected error in {request.path}: {e}")
        return jsonify(error_response("An unexpected error occurred.")), 500

@pictures_bp.route('/upload', methods=['POST'])
def upload_user_picture():
    data = request.get_json()
    try:
        validate_request_data(data, ["user_id", "image_id"])
        result = upload_picture(data["user_id"], data["image_id"], data.get("is_profile", False))
        status_code = 201 if result.get("success") else 400
        return jsonify(result), status_code
    except ValueError as ve:
        return jsonify(error_response(str(ve))), 400
    except Exception as e:
        logger.error(f"Unexpected error in {request.path}: {e}")
        return jsonify(error_response("An unexpected error occurred.")), 500

@pictures_bp.route('/<int:user_id>/<int:picture_id>', methods=['DELETE'])
def delete_user_picture(user_id, picture_id):
    try:
        result = remove_picture(user_id, picture_id)
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code
    except ValueError as ve:
        return jsonify(error_response(str(ve))), 400
    except Exception as e:
        logger.error(f"Unexpected error in {request.path}: {e}")
        return jsonify(error_response("An unexpected error occurred.")), 500

@pictures_bp.route('/set-profile', methods=['PUT'])
def set_profile_picture():
    data = request.get_json()
    try:
        validate_request_data(data, ["user_id", "picture_id"])
        result = change_profile_picture(data["user_id"], data["picture_id"])
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code
    except ValueError as ve:
        return jsonify(error_response(str(ve))), 400
    except Exception as e:
        logger.error(f"Unexpected error in {request.path}: {e}")
        return jsonify(error_response("An unexpected error occurred.")), 500

