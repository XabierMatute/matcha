import logging
from typing import Optional, Dict, Any
from .database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario por su ID."""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")
    
    logger.info(f"Fetching user with ID {user_id}")
    query = "SELECT * FROM users WHERE id = %s"
    return Database.execute_query(query, (user_id,))

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario por su nombre de usuario."""
    if not username.strip():
        raise ValueError("Username cannot be empty.")
    
    logger.info(f"Fetching user with username {username}")
    query = "SELECT * FROM users WHERE username = %s"
    return Database.execute_query(query, (username,))

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario por su email."""
    if not email.strip():
        raise ValueError("Email cannot be empty.")
    
    logger.info(f"Fetching user with email {email}")
    query = "SELECT * FROM users WHERE email = %s"
    return Database.execute_query(query, (email,))

def validate_user(email: str) -> Dict[str, Any]:
    """Valida y verifica un usuario por su email."""
    logger.info(f"Validating user with email {email}")
    user = get_user_by_email(email)
    if not user:
        logger.error(f"No user found with email {email}")
        raise ValueError("No user with this email exists.")
    
    query = "UPDATE users SET is_verified = TRUE WHERE email = %s RETURNING id, username, email, first_name, last_name"
    return Database.execute_query(query, (email,))

def create_user(username: str, email: str, password_hash: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict[str, Any]:
    """Crea un nuevo usuario."""
    logger.info(f"Creating user with username '{username}' and email '{email}'")

    if get_user_by_username(username):
        logger.error(f"Username '{username}' already exists.")
        raise ValueError("Username already exists.")
    if get_user_by_email(email):
        logger.error(f"Email '{email}' already exists.")
        raise ValueError("Email already exists.")
    
    query = '''
        INSERT INTO users (username, email, password_hash, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, username, email, first_name, last_name
    '''
    return Database.execute_query(query, (username, email, password_hash, first_name, last_name))

def update_user(user_id: int, username: Optional[str] = None, email: Optional[str] = None,
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Actualiza los datos de un usuario."""
    logger.info(f"Updating user with ID {user_id}")
    if not get_user_by_id(user_id):
        logger.error(f"User ID {user_id} does not exist.")
        raise ValueError("User ID does not exist.")

    updates = []
    params = []

    if username:
        updates.append("username = %s")
        params.append(username)
    if email:
        updates.append("email = %s")
        params.append(email)
    if first_name:
        updates.append("first_name = %s")
        params.append(first_name)
    if last_name:
        updates.append("last_name = %s")
        params.append(last_name)

    if not updates:
        raise ValueError("No fields provided to update.")

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, username, email, first_name, last_name"
    params.append(user_id)

    return Database.execute_query(query, tuple(params))

def delete_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Elimina un usuario por su ID."""
    logger.info(f"Deleting user with ID {user_id}")
    if not get_user_by_id(user_id):
        logger.error(f"User ID {user_id} does not exist.")
        raise ValueError("User ID does not exist.")

    query = "DELETE FROM users WHERE id = %s RETURNING id"
    return Database.execute_query(query, (user_id,))
