from flask import Blueprint, request, jsonify, session
from manager.pictures_manager import (
    fetch_user_pictures,
    upload_user_picture,
    remove_user_picture,
    set_user_profile_picture,
    get_user_picture_count
)
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pictures_bp = Blueprint("pictures", __name__, url_prefix="/pictures")

def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code

# Ruta para obtener todas las imágenes del usuario
@pictures_bp.route("/", methods=["GET"])
def get_pictures():
    """
    Obtiene todas las imágenes del usuario.
    """
    user_id = session.get("user_id")
    if not user_id:
        return error_response("User not logged in.", 401)
    try:
        pictures = fetch_user_pictures(user_id)
        return jsonify(success_response(data=pictures, message="Pictures fetched successfully.")), 200
    except Exception as e:
        logger.error(f"Error fetching pictures for user ID {user_id}: {e}")
        return error_response("Failed to fetch pictures.", 500, details=str(e))

# Ruta para subir una nueva imagen
@pictures_bp.route("/upload", methods=["POST"])
def upload_picture():
    """
    Sube una nueva imagen del usuario.
    """
    user_id = session.get("user_id")
    if not user_id:
        return error_response("User not logged in.", 401)

    data = request.json
    image_id = data.get("image_id")
    is_profile = data.get("is_profile", False)

    if not image_id:
        return error_response("Image ID is required.", 400)

    try:
        new_picture = upload_user_picture(user_id, image_id, is_profile)
        if not new_picture:
            return error_response("User already has 5 pictures.", 400)
        return jsonify(success_response(data=new_picture, message="Picture uploaded successfully.")), 201
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error uploading picture for user ID {user_id}: {e}")
        return error_response("Failed to upload picture.", 500, details=str(e))

# Ruta para eliminar una imagen específica
@pictures_bp.route("/<int:picture_id>", methods=["DELETE"])
def delete_picture(picture_id):
    """
    Elimina una imagen específica del usuario.
    """
    user_id = session.get("user_id")
    if not user_id:
        return error_response("User not logged in.", 401)
    try:
        deleted_picture = remove_user_picture(user_id, picture_id)
        if not deleted_picture:
            return error_response("Picture not found.", 404)
        return jsonify(success_response(data=deleted_picture, message="Picture deleted successfully.")), 200
    except Exception as e:
        logger.error(f"Error deleting picture ID {picture_id} for user ID {user_id}: {e}")
        return error_response("Failed to delete picture.", 500, details=str(e))

# Ruta para establecer una imagen como foto de perfil
@pictures_bp.route("/set-profile", methods=["PUT"])
def set_profile_picture():
    """
    Establece una imagen como foto de perfil.
    """
    user_id = session.get("user_id")
    if not user_id:
        return error_response("User not logged in.", 401)

    data = request.json
    picture_id = data.get("picture_id")

    if not picture_id:
        return error_response("Picture ID is required.", 400)

    try:
        profile_picture = set_user_profile_picture(user_id, picture_id)
        if not profile_picture:
            return error_response("Failed to set profile picture.", 400)
        return jsonify(success_response(data=profile_picture, message="Profile picture updated successfully.")), 200
    except Exception as e:
        logger.error(f"Error setting profile picture ID {picture_id} for user ID {user_id}: {e}")
        return error_response("Failed to update profile picture.", 500, details=str(e))

# Ruta para contar las imágenes del usuario
@pictures_bp.route("/count", methods=["GET"])
def count_pictures():
    """
    Cuenta el número de imágenes del usuario.
    """
    user_id = session.get("user_id")
    if not user_id:
        return error_response("User not logged in.", 401)
    try:
        count = get_user_picture_count(user_id)
        return jsonify(success_response(data={"count": count}, message="Picture count fetched successfully.")), 200
    except Exception as e:
        logger.error(f"Error counting pictures for user ID {user_id}: {e}")
        return error_response("Failed to count pictures.", 500, details=str(e))



