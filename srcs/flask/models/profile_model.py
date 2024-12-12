from .database import Database
import logging

logging.basicConfig(level=logging.INFO)

def get_profile_by_user_id(user_id):
    """
    Obtiene el perfil completo de un usuario por su ID.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID. It must be a positive integer.")

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
                
                # Estructurar el retorno
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
        logging.error(f"Error fetching profile for user ID {user_id}: {e}")
        raise Exception("Error fetching profile") from e



def update_profile(user_id, **fields):
    """
    Actualiza los datos del perfil de un usuario.
    Solo se actualizan los campos que están presentes en fields.
    """
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
                return updated_profile
    except Exception as e:
        logging.error(f"Error updating profile for user ID {user_id}: {e}")
        raise Exception("Error updating profile") from e


def get_location(user_id):
    """
    Obtiene la ubicación actual de un usuario.
    """
    query = "SELECT location, latitude, longitude FROM users WHERE id = %s"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                location = cursor.fetchone()
                if not location:
                    raise ValueError("Location not found for the given user ID.")
                return location
    except Exception as e:
        logging.error(f"Error fetching location for user ID {user_id}: {e}")
        raise Exception("Error fetching location") from e


def update_location(user_id, location, latitude, longitude):
    """
    Actualiza la ubicación de un usuario.
    """
    query = '''
        UPDATE users
        SET location = %s, latitude = %s, longitude = %s
        WHERE id = %s
        RETURNING id, location, latitude, longitude
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (location, latitude, longitude, user_id))
                connection.commit()
                updated_location = cursor.fetchone()
                if not updated_location:
                    raise ValueError("Failed to update location. User ID may not exist.")
                return updated_location
    except Exception as e:
        logging.error(f"Error updating location for user ID {user_id}: {e}")
        raise Exception("Error updating location") from e


