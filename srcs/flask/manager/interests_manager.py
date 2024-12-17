from models.interests_model import (
    create_interest,
    list_interests,
    get_interest_by_id,
    add_interests,
    remove_interests,
    update_user_interests
)

def add_new_interest(tag):
    """
    Crea un nuevo interés.

    Args:
        tag (str): El nombre del interés.

    Returns:
        dict: Información del interés creado.
    """
    return create_interest(tag)

def fetch_all_interests():
    """
    Obtiene todos los intereses disponibles.

    Returns:
        list: Lista de intereses existentes.
    """
    return list_interests()

def fetch_interest_by_id(interest_id):
    """
    Obtiene un interés por su ID.

    Args:
        interest_id (int): ID del interés.

    Returns:
        dict: Información del interés.
    """
    return get_interest_by_id(interest_id)

def bulk_add_interests(tags):
    """
    Agrega múltiples intereses a la base de datos.

    Args:
        tags (list): Lista de nombres de intereses.

    Returns:
        list: Lista de intereses creados o existentes.
    """
    return add_interests(tags)

def bulk_remove_interests(interest_ids):
    """
    Elimina múltiples intereses de la base de datos.

    Args:
        interest_ids (list): Lista de IDs de intereses a eliminar.

    Returns:
        dict: IDs de los intereses eliminados.
    """
    return remove_interests(interest_ids)

def update_user_interests_list(user_id, new_interests):
    """
    Actualiza los intereses de un usuario.

    Args:
        user_id (int): ID del usuario.
        new_interests (list): Lista de nombres de los nuevos intereses.

    Returns:
        dict: Confirmación de la actualización.
    """
    return update_user_interests(user_id, new_interests)

