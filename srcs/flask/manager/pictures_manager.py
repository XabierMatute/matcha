from models.pictures_model import (
    get_pictures_by_user,
    add_picture,
    count_pictures,
    delete_picture,
    set_profile_picture,
)
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Función para validar los parámetros requeridos
def validate_required(*args, **kwargs):
    for name, value in kwargs.items():
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"{name} is required and cannot be empty.")

# Respuesta exitosa
def success_response(data=None, message="Operation successful"):
    return {"success": True, "message": message, "data": data}

# Respuesta de error
def error_response(message="Operation failed"):
    return {"success": False, "message": message}

# Obtener las fotos de un usuario
def fetch_user_pictures(user_id: int) -> Dict:
    try:
        validate_required(UserID=user_id)  # Validar que el ID del usuario esté presente
        pictures = get_pictures_by_user(user_id)  # Obtener las fotos del usuario
        return success_response(data=pictures, message=f"Fetched {len(pictures)} pictures.")
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error fetching pictures for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")

# Subir una nueva foto para el usuario
def upload_picture(user_id: int, image_id: str, is_profile: bool = False) -> Dict:
    try:
        validate_required(UserID=user_id, ImageID=image_id)  # Validar parámetros
        if count_pictures(user_id) >= 5:  # Limitar a 5 fotos
            return error_response("Maximum limit of 5 pictures reached.")

        result = add_picture(user_id, image_id, is_profile)  # Subir la foto
        return success_response(data=result["picture"], message="Picture uploaded successfully.")
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error uploading picture for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")

# Eliminar una foto específica del usuario
def remove_picture(user_id: int, picture_id: int) -> Dict:
    try:
        validate_required(UserID=user_id, PictureID=picture_id)  # Validar parámetros
        result = delete_picture(picture_id, user_id)  # Eliminar la foto
        if result["success"]:
            return success_response(data=result["picture"], message="Picture removed successfully.")
        return error_response(result["message"])
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error removing picture ID {picture_id} for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")

# Cambiar la foto de perfil del usuario
def change_profile_picture(user_id: int, picture_id: int) -> Dict:
    try:
        validate_required(UserID=user_id, PictureID=picture_id)  # Validar parámetros
        result = set_profile_picture(picture_id, user_id)  # Establecer la foto de perfil
        if result["success"]:
            return success_response(data=result["picture"], message="Profile picture updated successfully.")
        return error_response("Failed to update profile picture.")
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error setting profile picture ID {picture_id} for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")

