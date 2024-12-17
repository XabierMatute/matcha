from models.pictures_model import (
    get_pictures_by_user,
    add_picture,
    delete_picture,
    set_profile_picture,
    count_pictures
)

def fetch_user_pictures(user_id):
    """
    Obtiene todas las imágenes de un usuario.

    Args:
        user_id (int): ID del usuario.

    Returns:
        list: Lista de imágenes del usuario.
    """
    return get_pictures_by_user(user_id)

def upload_user_picture(user_id, image_id, is_profile=False):
    """
    Agrega una nueva imagen para el usuario.

    Args:
        user_id (int): ID del usuario.
        image_id (int): ID de la imagen.
        is_profile (bool): Indica si la imagen es foto de perfil.

    Returns:
        dict: Información de la imagen agregada.
    """
    return add_picture(user_id, image_id, is_profile)

def remove_user_picture(user_id, picture_id):
    """
    Elimina una imagen específica de un usuario.

    Args:
        user_id (int): ID del usuario.
        picture_id (int): ID de la imagen a eliminar.

    Returns:
        dict: Información de la imagen eliminada.
    """
    return delete_picture(picture_id, user_id)

def set_user_profile_picture(user_id, picture_id):
    """
    Establece una imagen como foto de perfil para el usuario.

    Args:
        user_id (int): ID del usuario.
        picture_id (int): ID de la imagen.

    Returns:
        dict: Información de la foto de perfil actualizada.
    """
    return set_profile_picture(picture_id, user_id)

def get_user_picture_count(user_id):
    """
    Cuenta el número total de imágenes del usuario.

    Args:
        user_id (int): ID del usuario.

    Returns:
        int: Número de imágenes del usuario.
    """
    return count_pictures(user_id)


