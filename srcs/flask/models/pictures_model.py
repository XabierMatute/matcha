from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_id(id_value, name="ID"):
    """Valida que el ID sea un entero positivo."""
    if not isinstance(id_value, int) or id_value <= 0:
        raise ValueError(f"{name} debe ser un entero positivo.")

def get_pictures_by_user(user_id):
    """Obtiene todas las imágenes de un usuario."""
    validate_id(user_id, "user_id")
    query = '''
        SELECT id, image_id, is_profile, created_at
        FROM pictures
        WHERE user_id = %s
        ORDER BY created_at DESC
    '''
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                pictures = cursor.fetchall()
                return [{"id": p[0], "image_id": p[1], "is_profile": p[2], "created_at": p[3]} for p in pictures]
    except Exception as e:
        logger.error(f"Error al obtener imágenes para el usuario {user_id}: {e}")
        raise Exception("Error al obtener imágenes") from e

def add_picture(user_id, image_id, is_profile=False):
    """Agrega una nueva imagen para un usuario, limitado a 5 imágenes."""
    validate_id(user_id, "user_id")
    validate_id(image_id, "image_id")

    query = '''
        INSERT INTO pictures (user_id, image_id, is_profile, created_at)
        SELECT %s, %s, %s, CURRENT_TIMESTAMP
        WHERE (SELECT COUNT(*) FROM pictures WHERE user_id = %s) < 5
        RETURNING id, user_id, image_id, is_profile, created_at
    '''
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, image_id, is_profile, user_id))
                conn.commit()
                picture = cursor.fetchone()
                if picture:
                    return {"id": picture[0], "user_id": picture[1], "image_id": picture[2],
                            "is_profile": picture[3], "created_at": picture[4]}
                return None
    except Exception as e:
        logger.error(f"Error al agregar imagen para el usuario {user_id}: {e}")
        raise Exception("Error al agregar la imagen") from e

def delete_picture(picture_id, user_id):
    """Elimina una imagen específica de un usuario."""
    validate_id(picture_id, "picture_id")
    validate_id(user_id, "user_id")

    query = '''
        DELETE FROM pictures
        WHERE id = %s AND user_id = %s
        RETURNING id, image_id
    '''
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (picture_id, user_id))
                conn.commit()
                picture = cursor.fetchone()
                return {"id": picture[0], "image_id": picture[1]} if picture else None
    except Exception as e:
        logger.error(f"Error al eliminar imagen con ID {picture_id} para el usuario {user_id}: {e}")
        raise Exception("Error al eliminar la imagen") from e

def set_profile_picture(picture_id, user_id):
    """Establece una imagen como foto de perfil."""
    validate_id(picture_id, "picture_id")
    validate_id(user_id, "user_id")

    query_reset = '''
        UPDATE pictures
        SET is_profile = FALSE
        WHERE user_id = %s
    '''
    query_set = '''
        UPDATE pictures
        SET is_profile = TRUE
        WHERE id = %s AND user_id = %s
        RETURNING id, image_id, is_profile
    '''
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_reset, (user_id,))
                cursor.execute(query_set, (picture_id, user_id))
                conn.commit()
                profile_picture = cursor.fetchone()
                if profile_picture:
                    return {"id": profile_picture[0], "image_id": profile_picture[1], "is_profile": profile_picture[2]}
                return None
    except Exception as e:
        logger.error(f"Error al establecer foto de perfil con ID {picture_id} para el usuario {user_id}: {e}")
        raise Exception("Error al establecer foto de perfil") from e

def count_pictures(user_id):
    """Cuenta el número de imágenes de un usuario."""
    validate_id(user_id, "user_id")
    query = '''
        SELECT COUNT(*)
        FROM pictures
        WHERE user_id = %s
    '''
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                count = cursor.fetchone()
                return count[0] if count else 0
    except Exception as e:
        logger.error(f"Error al contar imágenes para el usuario {user_id}: {e}")
        raise Exception("Error al contar imágenes") from e





