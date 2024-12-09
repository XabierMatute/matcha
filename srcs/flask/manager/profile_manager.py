from models.profile_model import (
    get_profile_by_user_id,
    update_profile,
    get_location,
    update_location
)
from models.interests_model import get_user_interests, update_user_interests
from models.pictures_model import add_profile_picture, get_user_pictures
from flask import current_app


def get_user_profile(user_id):
    """
    Obtiene el perfil completo de un usuario, incluyendo intereses y fotos.
    """
    try:
        profile = get_profile_by_user_id(user_id)
        if not profile:
            raise ValueError("User profile not found.")

        interests = get_user_interests(user_id)
        pictures = get_user_pictures(user_id)

        return {
            "profile": profile,
            "interests": interests,
            "pictures": pictures
        }
    except Exception as e:
        current_app.logger.error(f"Error fetching profile for user ID {user_id}: {e}")
        raise Exception("Failed to fetch user profile.") from e


def update_user_profile(user_id, data):
    """
    Actualiza los datos básicos del perfil del usuario.
    
    Args:
        user_id (int): ID del usuario.
        data (dict): Campos a actualizar en el perfil.
    
    Returns:
        dict: Perfil actualizado.
    """
    try:
        updated_profile = update_profile(user_id, **data)
        return updated_profile
    except ValueError as e:
        current_app.logger.warning(f"Validation error while updating profile: {e}")
        raise ValueError(str(e))
    except Exception as e:
        current_app.logger.error(f"Error updating profile for user ID {user_id}: {e}")
        raise Exception("Failed to update user profile.") from e


def get_user_location(user_id):
    """
    Obtiene la ubicación actual de un usuario.
    """
    try:
        location = get_location(user_id)
        if not location:
            raise ValueError("Location not found for user.")
        return location
    except Exception as e:
        current_app.logger.error(f"Error fetching location for user ID {user_id}: {e}")
        raise Exception("Failed to fetch user location.") from e


def update_user_location(user_id, location, latitude, longitude):
    """
    Actualiza la ubicación de un usuario.
    """
    try:
        updated_location = update_location(user_id, location, latitude, longitude)
        return updated_location
    except Exception as e:
        current_app.logger.error(f"Error updating location for user ID {user_id}: {e}")
        raise Exception("Failed to update user location.") from e


def update_user_interests(user_id, interests):
    """
    Actualiza los intereses del usuario.
    
    Args:
        user_id (int): ID del usuario.
        interests (list): Lista de intereses a actualizar.
    
    Returns:
        list: Intereses actualizados.
    """
    try:
        updated_interests = update_user_interests(user_id, interests)
        return updated_interests
    except Exception as e:
        current_app.logger.error(f"Error updating interests for user ID {user_id}: {e}")
        raise Exception("Failed to update user interests.") from e


def update_user_profile_picture(user_id, picture_file):
    """
    Actualiza o agrega la foto de perfil del usuario.
    
    Args:
        user_id (int): ID del usuario.
        picture_file (file): Archivo de la foto de perfil.
    
    Returns:
        dict: Información de la foto de perfil actualizada.
    """
    try:
        picture_info = add_profile_picture(user_id, picture_file)
        return picture_info
    except Exception as e:
        current_app.logger.error(f"Error updating profile picture for user ID {user_id}: {e}")
        raise Exception("Failed to update profile picture.") from e
