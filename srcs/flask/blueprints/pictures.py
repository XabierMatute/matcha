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
    return jsonify(fetch_user_pictures(user_id))

@pictures_bp.route("/upload", methods=["POST"])
def upload_user_picture():
    data = request.get_json()
    return jsonify(upload_picture(data["user_id"], data["image_id"], data.get("is_profile", False)))

@pictures_bp.route("/<int:user_id>/<int:picture_id>", methods=["DELETE"])
def delete_user_picture(user_id, picture_id):
    return jsonify(remove_picture(user_id, picture_id))

@pictures_bp.route("/set-profile", methods=["PUT"])
def set_profile_picture():
    data = request.get_json()
    return jsonify(change_profile_picture(data["user_id"], data["picture_id"]))



