from .database import Database
import logging

logging.basicConfig(level=logging.INFO)

def get_profile_by_user_id(user_id):
    """Obtiene el perfil de un usuario desde la tabla users."""
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
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error fetching profile for user ID {user_id}: {e}")
        raise Exception("Error fetching profile") from e

def update_profile(user_id, biography=None, location=None, latitude=None, longitude=None, profile_picture=None):
    """Actualiza los datos del perfil de un usuario en la tabla users."""
    updates = []
    params = []

    if biography:
        updates.append("biography = %s")
        params.append(biography)
    if location:
        updates.append("location = %s")
        params.append(location)
    if latitude:
        updates.append("latitude = %s")
        params.append(latitude)
    if longitude:
        updates.append("longitude = %s")
        params.append(longitude)
    if profile_picture:
        updates.append("profile_picture = %s")
        params.append(profile_picture)

    if not updates:
        raise ValueError("No fields provided to update.")

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, biography, location, latitude, longitude, profile_picture"
    params.append(user_id)

    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error updating profile for user ID {user_id}: {e}")
        raise Exception("Error updating profile") from e

def get_location(user_id):
    """Obtiene la ubicación actual de un usuario."""
    query = "SELECT location, latitude, longitude FROM users WHERE id = %s"
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error fetching location for user ID {user_id}: {e}")
        raise Exception("Error fetching location") from e

def update_location(user_id, location, latitude, longitude):
    """Actualiza la ubicación de un usuario."""
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
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error updating location for user ID {user_id}: {e}")
        raise Exception("Error updating location") from e

