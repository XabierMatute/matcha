from database import get_db_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_profile(user_id, birthdate, gender=None, sexual_preferences=None, biography=None,
                   fame_rating=0.0, profile_picture=None, location=None, latitude=None, longitude=None):
    """
    Crea un perfil para un usuario en la base de datos.

    :param user_id: ID del usuario al que pertenece el perfil.
    :param birthdate: Fecha de nacimiento del usuario.
    :param gender: Género del usuario (opcional).
    :param sexual_preferences: Preferencias sexuales del usuario (opcional).
    :param biography: Biografía del usuario (opcional).
    :param fame_rating: Calificación de fama del usuario (por defecto 0.0).
    :param profile_picture: URL o nombre de la imagen de perfil (opcional).
    :param location: Ubicación del usuario (opcional).
    :param latitude: Latitud (opcional).
    :param longitude: Longitud (opcional).
    :return: Diccionario con los datos del perfil creado.
    """
    query = '''
        INSERT INTO profiles (user_id, birthdate, gender, sexual_preferences, biography, fame_rating,
                              profile_picture, location, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, user_id, birthdate, gender, sexual_preferences, biography, fame_rating, 
                  profile_picture, location, latitude, longitude, updated_at
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, birthdate, gender, sexual_preferences, biography, fame_rating,
                                       profile_picture, location, latitude, longitude))
                result = cursor.fetchone()
                connection.commit()
                logger.info(f"Profile created successfully: {result}")
                return {
                    "id": result[0],
                    "user_id": result[1],
                    "birthdate": result[2],
                    "gender": result[3],
                    "sexual_preferences": result[4],
                    "biography": result[5],
                    "fame_rating": result[6],
                    "profile_picture": result[7],
                    "location": result[8],
                    "latitude": result[9],
                    "longitude": result[10],
                    "updated_at": result[11],
                }
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise Exception("Error creating profile")

def get_profile_by_user_id(user_id):
    """
    Obtiene el perfil de un usuario a partir de su ID.

    :param user_id: ID del usuario.
    :return: Diccionario con los datos del perfil del usuario, o None si no se encuentra.
    """
    query = '''
        SELECT id, user_id, birthdate, gender, sexual_preferences, biography, fame_rating, profile_picture, 
               location, latitude, longitude, updated_at
        FROM profiles
        WHERE user_id = %s
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "user_id": result[1],
                        "birthdate": result[2],
                        "gender": result[3],
                        "sexual_preferences": result[4],
                        "biography": result[5],
                        "fame_rating": result[6],
                        "profile_picture": result[7],
                        "location": result[8],
                        "latitude": result[9],
                        "longitude": result[10],
                        "updated_at": result[11],
                    }
                else:
                    logger.info(f"Profile not found for user_id {user_id}.")
                    return None
    except Exception as e:
        logger.error(f"Error retrieving profile by user_id: {e}")
        raise Exception("Error retrieving profile by user_id")

def update_profile(user_id, **kwargs):
    """
    Actualiza el perfil de un usuario en la base de datos.

    :param user_id: ID del usuario cuyo perfil se actualizará.
    :param kwargs: Parámetros opcionales para actualizar el perfil (pueden incluir gender, biography, etc.).
    :return: Diccionario con los datos actualizados del perfil.
    """
    set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
    values = list(kwargs.values()) + [user_id]

    query = f'''
        UPDATE profiles
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
        RETURNING id, user_id, birthdate, gender, sexual_preferences, biography, fame_rating, 
                  profile_picture, location, latitude, longitude, updated_at
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
                connection.commit()
                if result:
                    logger.info(f"Profile updated successfully: {result}")
                    return {
                        "id": result[0],
                        "user_id": result[1],
                        "birthdate": result[2],
                        "gender": result[3],
                        "sexual_preferences": result[4],
                        "biography": result[5],
                        "fame_rating": result[6],
                        "profile_picture": result[7],
                        "location": result[8],
                        "latitude": result[9],
                        "longitude": result[10],
                        "updated_at": result[11],
                    }
                else:
                    logger.info(f"Profile not found for user_id {user_id}.")
                    return None
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise Exception("Error updating profile")

def delete_profile(user_id):
    """
    Elimina el perfil de un usuario de la base de datos.

    :param user_id: ID del usuario cuyo perfil se eliminará.
    :return: True si el perfil se eliminó con éxito, False si no existía.
    """
    query = '''
        DELETE FROM profiles
        WHERE user_id = %s
        RETURNING id
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                connection.commit()
                if result:
                    logger.info(f"Profile deleted successfully for user_id {user_id}.")
                    return True
                else:
                    logger.info(f"No profile found for user_id {user_id}.")
                    return False
    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        raise Exception("Error deleting profile")


