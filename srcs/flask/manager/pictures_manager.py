from models.pictures_model import (
    get_pictures_by_user,
    add_picture,
    count_pictures,
    delete_picture,
    set_profile_picture
)
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def validate_required(value, name="Value"):
    if not value:
        raise ValueError(f"{name} is required.")

def success_response(data=None, message="Operation successful"):
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed"):
    return {"success": False, "message": message}

def fetch_user_pictures(user_id: int) -> Dict:
    try:
        validate_required(user_id, "User ID")
        pictures = get_pictures_by_user(user_id)
        return success_response(data=pictures, message=f"Fetched {len(pictures)} pictures.")
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error fetching pictures for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")

def upload_picture(user_id: int, image_id: str, is_profile: bool = False) -> Dict:
    try:
        validate_required(user_id, "User ID")
        validate_required(image_id, "Image ID")

        if count_pictures(user_id) >= 5:
            return error_response("Maximum limit of 5 pictures reached.")

        result = add_picture(user_id, image_id, is_profile)

        if is_profile and result.get("success"):
            set_profile_picture(result["picture"]["id"], user_id)

        return success_response(data=result["picture"], message="Picture uploaded successfully.")
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error uploading picture for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")

def remove_picture(user_id: int, picture_id: int) -> Dict:
    try:
        validate_required(user_id, "User ID")
        validate_required(picture_id, "Picture ID")

        result = delete_picture(picture_id, user_id)
        if result["success"]:
            return success_response(data=result["picture"], message="Picture removed successfully.")
        return error_response(result["message"])
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error removing picture ID {picture_id} for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")

def change_profile_picture(user_id: int, picture_id: int) -> Dict:
    try:
        validate_required(user_id, "User ID")
        validate_required(picture_id, "Picture ID")

        result = set_profile_picture(picture_id, user_id)
        if result["success"]:
            return success_response(data=result["picture"], message="Profile picture updated successfully.")
        return error_response(result["message"])
    except ValueError as ve:
        return error_response(str(ve))
    except Exception as e:
        logger.error(f"Error setting profile picture ID {picture_id} for user {user_id}: {e}")
        return error_response("An unexpected error occurred.")
