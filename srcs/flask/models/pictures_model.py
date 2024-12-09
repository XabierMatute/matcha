from .database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_id(id_value, name="ID"):
    if not isinstance(id_value, int) or id_value <= 0:
        raise ValueError(f"{name} debe ser un entero positivo.")

def success_response(data=None, message="Operación exitosa"):
    return {"success": True, "message": message, "data": data}

def error_response(message="Operación fallida"):
    return {"success": False, "message": message}

def get_pictures_by_user(user_id):
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
        return success_response(data=pictures, message=f"Se obtuvieron {len(pictures)} imágenes.")
    except Exception as e:
        logger.error(f"Error al obtener imágenes para el usuario {user_id}: {e}")
        return error_response("Error al obtener imágenes.")

def add_picture(user_id, image_id, is_profile=False):
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
            return success_response(data=picture, message="Imagen agregada exitosamente.")
        return error_response("El usuario ya tiene 5 fotos.")
    except Exception as e:
        logger.error(f"Error al agregar imagen para el usuario {user_id}: {e}")
        return error_response("Error al agregar la imagen.")

def delete_picture(picture_id, user_id):
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
        if picture:
            return success_response(data=picture, message="Imagen eliminada exitosamente.")
        return error_response("No se encontró la imagen.")
    except Exception as e:
        logger.error(f"Error al eliminar la imagen con ID {picture_id}: {e}")
        return error_response("Error al eliminar la imagen.")

def set_profile_picture(picture_id, user_id):
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
            return success_response(data=profile_picture, message="Foto de perfil actualizada.")
        return error_response("No se pudo establecer como foto de perfil.")
    except Exception as e:
        logger.error(f"Error al establecer la foto de perfil con ID {picture_id}: {e}")
        return error_response("Error al establecer la foto de perfil.")

def count_pictures(user_id):
    """
    Cuenta el número de imágenes asociadas a un usuario.
    """
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




