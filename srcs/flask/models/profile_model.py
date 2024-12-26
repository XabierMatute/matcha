from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_user_id(user_id):
    """Valida que el ID del usuario sea un entero positivo."""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID. It must be a positive integer.")

def validate_location_data(location, latitude, longitude):
    """Valida los datos de ubicación."""
    if location is not None and not isinstance(location, str):
        raise ValueError("Location must be a string.")
    if latitude is not None and not isinstance(latitude, (int, float)):
        raise ValueError("Latitude must be a number.")
    if longitude is not None and not isinstance(longitude, (int, float)):
        raise ValueError("Longitude must be a number.")

def get_profile_by_user_id(user_id):
    """
    Obtiene el perfil completo de un usuario por su ID.
    """
    validate_user_id(user_id)

    query = '''
        SELECT id, username, email, first_name, last_name, gender, sexual_preferences,
               biography, fame_rating, profile_picture, location, latitude, longitude, is_active
        FROM users
        WHERE id = %s
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                profile = cursor.fetchone()
                if not profile:
                    raise ValueError("Profile not found for the given user ID.")
                
                return {
                    "id": profile[0],
                    "username": profile[1],
                    "email": profile[2],
                    "first_name": profile[3],
                    "last_name": profile[4],
                    "gender": profile[5],
                    "sexual_preferences": profile[6],
                    "biography": profile[7],
                    "fame_rating": profile[8],
                    "profile_picture": profile[9],
                    "location": profile[10],
                    "latitude": profile[11],
                    "longitude": profile[12],
                    "is_active": profile[13],
                }
    except Exception as e:
        logger.error(f"Error fetching profile for user ID {user_id}: {e}")
        raise Exception("Error fetching profile.") from e

def update_profile(user_id, **fields):
    """
    Actualiza los datos del perfil de un usuario.
    """
    validate_user_id(user_id)

    valid_fields = ['biography', 'location', 'latitude', 'longitude', 'profile_picture']
    updates = []
    params = []

    for field, value in fields.items():
        if field in valid_fields and value is not None:
            updates.append(f"{field} = %s")
            params.append(value)

    if not updates:
        raise ValueError("No valid fields provided to update.")

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, {', '.join(valid_fields)}"
    params.append(user_id)

    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                connection.commit()
                updated_profile = cursor.fetchone()
                if not updated_profile:
                    raise ValueError("Failed to update profile. User ID may not exist.")
                return dict(zip(["id"] + valid_fields, updated_profile))
    except Exception as e:
        logger.error(f"Error updating profile for user ID {user_id}: {e}")
        raise Exception("Error updating profile.") from e

def get_location(user_id):
    """
    Obtiene la ubicación actual de un usuario.
    """
    validate_user_id(user_id)

    query = "SELECT location, latitude, longitude FROM users WHERE id = %s"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                location = cursor.fetchone()
                if not location:
                    raise ValueError("Location not found for the given user ID.")
                return {
                    "location": location[0],
                    "latitude": location[1],
                    "longitude": location[2]
                }
    except Exception as e:
        logger.error(f"Error fetching location for user ID {user_id}: {e}")
        raise Exception("Error fetching location.") from e

def update_location(user_id, location, latitude, longitude):
    """
    Actualiza la ubicación de un usuario.
    """
    validate_user_id(user_id)
    validate_location_data(location, latitude, longitude)

    query = '''
        UPDATE users
        SET location = %s, latitude = %s, longitude = %s
        WHERE id = %s
        RETURNING location, latitude, longitude
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (location, latitude, longitude, user_id))
                connection.commit()
                updated_location = cursor.fetchone()
                if not updated_location:
                    raise ValueError("Failed to update location. User ID may not exist.")
                return {
                    "location": updated_location[0],
                    "latitude": updated_location[1],
                    "longitude": updated_location[2]
                }
    except Exception as e:
        logger.error(f"Error updating location for user ID {user_id}: {e}")
        raise Exception("Error updating location.") from e


