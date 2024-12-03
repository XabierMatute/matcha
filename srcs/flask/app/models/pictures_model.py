import logging
from .database import Database

# Configura el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_pictures_by_user(user_id):
    """Obtiene todas las imágenes de un usuario."""
    query = 'SELECT * FROM pictures WHERE user_id = %s'
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                pictures = cursor.fetchall()
        return pictures
    except Exception as e:
        logger.error(f"Error al obtener imágenes para el usuario {user_id}: {e}")
        return []

def add_picture(user_id, image_id):
    """Agrega una nueva imagen para un usuario si no supera las 5."""
    if count_pictures(user_id) >= 5:
        return {"success": False, "message": "El usuario ya tiene 5 fotos."}

    query = 'INSERT INTO pictures (user_id, image_id) VALUES (%s, %s)'
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, image_id))
                conn.commit()
        logger.info(f"Imagen agregada para el usuario {user_id} con ID de imagen {image_id}.")
        return {"success": True, "message": "Imagen agregada exitosamente."}
    except Exception as e:
        logger.error(f"Error al agregar imagen para el usuario {user_id}: {e}")
        return {"success": False, "message": "Hubo un error al agregar la imagen."}

def count_pictures(user_id):
    """Cuenta la cantidad de imágenes de un usuario."""
    query = 'SELECT COUNT(*) FROM pictures WHERE user_id = %s'
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                count = cursor.fetchone()[0]
        return count
    except Exception as e:
        logger.error(f"Error al contar imágenes para el usuario {user_id}: {e}")
        return 0

def delete_picture(picture_id):
    """Elimina una imagen por su ID."""
    query = 'DELETE FROM pictures WHERE id = %s'
    try:
        with Database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (picture_id,))
                conn.commit()
        logger.info(f"Imagen con ID {picture_id} eliminada exitosamente.")
        return {"success": True, "message": "Imagen eliminada exitosamente."}
    except Exception as e:
        logger.error(f"Error al eliminar la imagen con ID {picture_id}: {e}")
        return {"success": False, "message": "Hubo un error al eliminar la imagen."}



