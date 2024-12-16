from models.likes_model import like_user, unlike_user, get_liked_users, get_matches
from models.notifications_model import create_notification
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def send_like(user_id: int, liked_user_id: int) -> Dict:
    """
    Envía un 'like' de un usuario hacia otro y verifica si hay un 'match'.

    Args:
        user_id (int): ID del usuario que da el 'like'.
        liked_user_id (int): ID del usuario que recibe el 'like'.

    Returns:
        Dict: Resultado del 'like' y si ocurrió un 'match'.

    Raises:
        ValueError: Si los IDs son inválidos.
    """
    if not user_id or not liked_user_id:
        raise ValueError("Both user_id and liked_user_id are required.")

    # Dar like
    like_result = like_user(user_id, liked_user_id)

    # Verificar si hay un match
    if liked_user_id in get_liked_users(liked_user_id):
        # Notificar a ambos usuarios sobre el match
        create_notification(liked_user_id, "match", f"You matched with user {user_id}")
        create_notification(user_id, "match", f"You matched with user {liked_user_id}")
        like_result["match"] = True
    else:
        like_result["match"] = False

    return like_result

def remove_like(user_id: int, liked_user_id: int) -> Dict:
    """
    Elimina un 'like' de un usuario hacia otro.

    Args:
        user_id (int): ID del usuario que elimina el 'like'.
        liked_user_id (int): ID del usuario que lo recibió.

    Returns:
        Dict: Resultado de la operación.

    Raises:
        ValueError: Si los IDs son inválidos.
    """
    if not user_id or not liked_user_id:
        raise ValueError("Both user_id and liked_user_id are required.")

    return unlike_user(user_id, liked_user_id)

def fetch_liked_users(user_id: int) -> List[int]:
    """
    Obtiene una lista de IDs de usuarios a los que el usuario ha dado 'like'.

    Args:
        user_id (int): ID del usuario.

    Returns:
        List[int]: Lista de IDs de usuarios que recibieron 'like'.

    Raises:
        ValueError: Si el user_id es inválido.
    """
    if not user_id:
        raise ValueError("user_id is required.")
    return get_liked_users(user_id)

def fetch_matches(user_id: int) -> List[int]:
    """
    Obtiene una lista de IDs de usuarios con los que el usuario tiene un 'match'.

    Args:
        user_id (int): ID del usuario.

    Returns:
        List[int]: Lista de IDs de usuarios con 'match'.

    Raises:
        ValueError: Si el user_id es inválido.
    """
    if not user_id:
        raise ValueError("user_id is required.")
    return get_matches(user_id)

def send_match_notifications(user_id: int, match_user_id: int) -> None:
    """
    Envía notificaciones a ambos usuarios cuando ocurre un 'match'.

    Args:
        user_id (int): ID del primer usuario.
        match_user_id (int): ID del segundo usuario.

    Returns:
        None
    """
    create_notification(user_id, "match", f"You matched with user {match_user_id}")
    create_notification(match_user_id, "match", f"You matched with user {user_id}")

