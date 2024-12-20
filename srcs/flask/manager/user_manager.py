import logging
from models.user_model import (
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    validate_user,
    create_user,
    update_user,
    delete_user
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_user_by_id(user_id, require_verified=False):
    """
    Obtiene un usuario por su ID.

    Args:
        user_id (int): ID del usuario.
        require_verified (bool): Si se debe validar que el usuario esté verificado.

    Returns:
        dict: Información del usuario.

    Raises:
        ValueError: Si el usuario no está verificado y se requiere verificación.
    """
    try:
        user = get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        if require_verified and not user.get('is_verified', False):
            raise ValueError(f"User with ID {user_id} is not verified.")
        return user
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}")
        raise

def fetch_user_by_username(username, require_verified=False):
    """
    Obtiene un usuario por su nombre de usuario.

    Args:
        username (str): Nombre del usuario.
        require_verified (bool): Si se debe validar que el usuario esté verificado.

    Returns:
        dict: Información del usuario.

    Raises:
        ValueError: Si el usuario no está verificado y se requiere verificación.
    """
    try:
        user = get_user_by_username(username)
        if not user:
            raise ValueError(f"User '{username}' not found.")
        if require_verified and not user.get('is_verified', False):
            raise ValueError(f"User '{username}' is not verified.")
        return user
    except Exception as e:
        logger.error(f"Error fetching user by username '{username}': {e}")
        raise

def fetch_user_by_email(email, require_verified=False):
    """
    Obtiene un usuario por su email.

    Args:
        email (str): Email del usuario.
        require_verified (bool): Si se debe validar que el usuario esté verificado.

    Returns:
        dict: Información del usuario.

    Raises:
        ValueError: Si el usuario no está verificado y se requiere verificación.
    """
    try:
        user = get_user_by_email(email)
        if not user:
            raise ValueError(f"User with email '{email}' not found.")
        if require_verified and not user.get('is_verified', False):
            raise ValueError(f"User with email '{email}' is not verified.")
        return user
    except Exception as e:
        logger.error(f"Error fetching user by email '{email}': {e}")
        raise

def verify_user(email):
    """
    Verifica un usuario por su email.

    Args:
        email (str): Email del usuario.

    Returns:
        dict: Información del usuario verificado.
    """
    try:
        return validate_user(email)
    except Exception as e:
        logger.error(f"Error verifying user by email '{email}': {e}")
        raise

def register_new_user(username, email, password_hash, first_name=None, last_name=None):
    """
    Crea un nuevo usuario.

    Args:
        username (str): Nombre de usuario.
        email (str): Email del usuario.
        password_hash (str): Hash de la contraseña.
        first_name (str, optional): Nombre del usuario.
        last_name (str, optional): Apellido del usuario.

    Returns:
        dict: Información del usuario creado.
    """
    try:
        return create_user(username, email, password_hash, first_name, last_name)
    except Exception as e:
        logger.error(f"Error registering user '{username}' with email '{email}': {e}")
        raise

def modify_user(user_id, username=None, email=None, first_name=None, last_name=None):
    """
    Actualiza los datos de un usuario.

    Args:
        user_id (int): ID del usuario.
        username (str, optional): Nuevo nombre de usuario.
        email (str, optional): Nuevo email del usuario.
        first_name (str, optional): Nuevo nombre.
        last_name (str, optional): Nuevo apellido.

    Returns:
        dict: Información del usuario actualizado.
    """
    try:
        return update_user(user_id, username, email, first_name, last_name)
    except Exception as e:
        logger.error(f"Error updating user with ID {user_id}: {e}")
        raise

def remove_user(user_id):
    """
    Elimina un usuario por su ID.

    Args:
        user_id (int): ID del usuario.

    Returns:
        dict: Información del usuario eliminado.
    """
    try:
        return delete_user(user_id)
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}")
        raise

def get_user_details(user_identifier, require_verified=False):
    """
    Obtiene los detalles de un usuario por ID o nombre de usuario.

    Args:
        user_identifier (int | str): ID del usuario o nombre de usuario.
        require_verified (bool): Si se debe validar que el usuario esté verificado.

    Returns:
        dict: Información del usuario.
    """
    try:
        if isinstance(user_identifier, int):
            return fetch_user_by_id(user_identifier, require_verified=require_verified)
        elif isinstance(user_identifier, str):
            return fetch_user_by_username(user_identifier, require_verified=require_verified)
        else:
            raise ValueError("Invalid user identifier. Must be an integer (ID) or string (username).")
    except Exception as e:
        logger.error(f"Error fetching user details for '{user_identifier}': {e}")
        raise


