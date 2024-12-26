from models.profile_model import (
    get_profile_by_user_id,
    update_profile,
    get_location,
    update_location
)
import logging

logger = logging.getLogger(__name__)

# Obtener perfil completo
def fetch_user_profile(user_id):
    """
    Obtiene el perfil completo de un usuario.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        logger.warning("Invalid user ID provided for fetching profile.")
        raise ValueError("User ID must be a positive integer.")

    try:
        return get_profile_by_user_id(user_id)
    except ValueError as ve:
        logger.warning(f"Validation error while fetching profile: {ve}")
        raise ValueError(str(ve))
    except Exception as e:
        logger.error(f"Error fetching profile for user ID {user_id}: {e}")
        raise Exception("Failed to fetch user profile.") from e

# Actualizar perfil
def update_user_profile(user_id, data):
    """
    Actualiza el perfil del usuario con los datos proporcionados.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        logger.warning("Invalid user ID provided for updating profile.")
        raise ValueError("User ID must be a positive integer.")

    if not isinstance(data, dict) or not data:
        logger.warning("Invalid data provided for updating profile.")
        raise ValueError("Profile data must be a non-empty dictionary.")

    try:
        return update_profile(user_id, **data)
    except ValueError as ve:
        logger.warning(f"Validation error while updating profile: {ve}")
        raise ValueError(str(ve))
    except Exception as e:
        logger.error(f"Error updating profile for user ID {user_id}: {e}")
        raise Exception("Failed to update user profile.") from e

# Obtener ubicación
def fetch_user_location(user_id):
    """
    Obtiene la ubicación actual del usuario.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        logger.warning("Invalid user ID provided for fetching location.")
        raise ValueError("User ID must be a positive integer.")

    try:
        return get_location(user_id)
    except ValueError as ve:
        logger.warning(f"Validation error while fetching location: {ve}")
        raise ValueError(str(ve))
    except Exception as e:
        logger.error(f"Error fetching location for user ID {user_id}: {e}")
        raise Exception("Failed to fetch user location.") from e

# Actualizar ubicación
def update_user_location(user_id, location, latitude, longitude):
    """
    Actualiza la ubicación del usuario.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        logger.warning("Invalid user ID provided for updating location.")
        raise ValueError("User ID must be a positive integer.")

    if location is not None and not isinstance(location, str):
        logger.warning("Invalid location provided for updating location.")
        raise ValueError("Location must be a string.")

    if latitude is not None and not isinstance(latitude, (int, float)):
        logger.warning("Invalid latitude provided for updating location.")
        raise ValueError("Latitude must be a number.")

    if longitude is not None and not isinstance(longitude, (int, float)):
        logger.warning("Invalid longitude provided for updating location.")
        raise ValueError("Longitude must be a number.")

    try:
        return update_location(user_id, location, latitude, longitude)
    except ValueError as ve:
        logger.warning(f"Validation error while updating location: {ve}")
        raise ValueError(str(ve))
    except Exception as e:
        logger.error(f"Error updating location for user ID {user_id}: {e}")
        raise Exception("Failed to update user location.") from e


