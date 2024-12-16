from flask import Blueprint, request, jsonify
from manager.pictures_manager import (
    fetch_user_pictures,
    upload_picture,
    remove_picture,
    change_profile_picture
)

pictures_bp = Blueprint("pictures", __name__, url_prefix="/pictures")

@pictures_bp.route("/<int:user_id>", methods=["GET"])
def get_pictures(user_id):
    try:
        result = fetch_user_pictures(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

@pictures_bp.route("/upload", methods=["POST"])
def upload_user_picture():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        image_id = data.get("image_id")
        is_profile = data.get("is_profile", False)

        if not user_id or not image_id:
            return jsonify({"success": False, "message": "user_id and image_id are required."}), 400

        result = upload_picture(user_id, image_id, is_profile)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

@pictures_bp.route("/<int:user_id>/<int:picture_id>", methods=["DELETE"])
def delete_user_picture(user_id, picture_id):
    try:
        result = remove_picture(user_id, picture_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

@pictures_bp.route("/set-profile", methods=["PUT"])
def set_profile_picture():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        picture_id = data.get("picture_id")

        if not user_id or not picture_id:
            return jsonify({"success": False, "message": "user_id and picture_id are required."}), 400

        result = change_profile_picture(user_id, picture_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500




