from models.profile_model import (
    get_profile_by_user_id,
    update_profile,
    get_location,
    update_location
)

def fetch_user_profile(user_id):
    """
    Obtiene el perfil completo del usuario.
    
    Args:
        user_id (int): ID del usuario.

    Returns:
        dict: Información del perfil del usuario.
    """
    return get_profile_by_user_id(user_id)

def update_user_profile(user_id, data):
    """
    Actualiza el perfil del usuario con los campos proporcionados.

    Args:
        user_id (int): ID del usuario.
        data (dict): Campos a actualizar.

    Returns:
        dict: Perfil del usuario actualizado.
    """
    return update_profile(user_id, **data)

def fetch_user_location(user_id):
    """
    Obtiene la ubicación del usuario.

    Args:
        user_id (int): ID del usuario.

    Returns:
        dict: Información de la ubicación del usuario.
    """
    return get_location(user_id)

def update_user_location(user_id, location, latitude, longitude):
    """
    Actualiza la ubicación del usuario.

    Args:
        user_id (int): ID del usuario.
        location (str): Dirección de ubicación.
        latitude (float): Latitud.
        longitude (float): Longitud.

    Returns:
        dict: Información de la ubicación actualizada.
    """
    return update_location(user_id, location, latitude, longitude)
