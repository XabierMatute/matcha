from models.likes_model import like_user, unlike_user, get_liked_users, get_matches
from models.notifications_model import create_notification
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_like(user_id, liked_user_id):
    """
    Envía un 'like' de un usuario hacia otro y verifica si hay un 'match'.

    Args:
        user_id (int): ID del usuario que da el 'like'.
        liked_user_id (int): ID del usuario que recibe el 'like'.

    Returns:
        dict: Resultado del 'like' y si ocurrió un 'match'.

    Raises:
        ValueError: Si los IDs son inválidos.
    """
    if not user_id or not liked_user_id:
        raise ValueError("Both user_id and liked_user_id are required.")

    # Registrar el like
    like_result = like_user(user_id, liked_user_id)

    # Verificar si existe un 'match'
    if like_result["status"] == "like_added" and liked_user_id in get_liked_users(liked_user_id):
        # Crear notificaciones para ambos usuarios
        create_notification(user_id, "match", f"You matched with user {liked_user_id}!")
        create_notification(liked_user_id, "match", f"You matched with user {user_id}!")
        like_result["match"] = True
    else:
        like_result["match"] = False

    return like_result

def remove_like(user_id, liked_user_id):
    """
    Elimina un 'like' de un usuario hacia otro.

    Args:
        user_id (int): ID del usuario que elimina el 'like'.
        liked_user_id (int): ID del usuario que lo recibió.

    Returns:
        dict: Resultado de la eliminación.
    """
    if not user_id or not liked_user_id:
        raise ValueError("Both user_id and liked_user_id are required.")

    return unlike_user(user_id, liked_user_id)

def fetch_liked_users(user_id):
    """
    Obtiene una lista de usuarios a los que un usuario ha dado 'like'.

    Args:
        user_id (int): ID del usuario.

    Returns:
        list: Lista de IDs de usuarios que recibieron 'like'.
    """
    if not user_id:
        raise ValueError("user_id is required.")
    return get_liked_users(user_id)

def fetch_matches(user_id):
    """
    Obtiene una lista de usuarios que tienen un 'match' con el usuario.

    Args:
        user_id (int): ID del usuario.

    Returns:
        list: Lista de IDs de usuarios con los que hay un 'match'.
    """
    if not user_id:
        raise ValueError("user_id is required.")
    return get_matches(user_id)

def send_match_notifications(user_id, matched_user_id):
    """
    Envía notificaciones a ambos usuarios cuando ocurre un 'match'.

    Args:
        user_id (int): ID del primer usuario.
        matched_user_id (int): ID del segundo usuario.
    """
    create_notification(user_id, "match", f"You matched with user {matched_user_id}!")
    create_notification(matched_user_id, "match", f"You matched with user {user_id}!")


