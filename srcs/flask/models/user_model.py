import logging
from typing import Optional, Dict, Any
from .database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches a user by their ID."""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")
    
    logger.info(f"Fetching user with ID {user_id}")
    query = "SELECT id, username, email FROM users WHERE id = %s"
    return Database.execute_query(query, (user_id,))

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Fetches a user by their username."""
    if not username.strip():
        raise ValueError("Username cannot be empty.")
    
    logger.info(f"Fetching user with username {username}")
    query = "SELECT id, username, email FROM users WHERE username = %s"
    return Database.execute_query(query, (username,))

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Fetches a user by their email."""
    if not email.strip():
        raise ValueError("Email cannot be empty.")
    
    logger.info(f"Fetching user with email {email}")
    query = "SELECT id, username, email FROM users WHERE email = %s"
    return Database.execute_query(query, (email,))

def create_user(username: str, email: str, password_hash: str) -> Dict[str, Any]:
    """Creates a new user."""
    logger.info(f"Creating user with username '{username}' and email '{email}'")

    if get_user_by_username(username):
        logger.error(f"Username '{username}' already exists.")
        raise ValueError("Username already exists.")
    if get_user_by_email(email):
        logger.error(f"Email '{email}' already exists.")
        raise ValueError("Email already exists.")
    
    query = '''
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id, username, email
    '''
    return Database.execute_query(query, (username, email, password_hash))

def update_user_password(user_id: int, new_password_hash: str) -> Dict[str, Any]:
    """Updates a user's password."""
    logger.info(f"Updating password for user with ID {user_id}")

    if not get_user_by_id(user_id):
        logger.error(f"User ID {user_id} does not exist.")
        raise ValueError("User ID does not exist.")
    
    query = "UPDATE users SET password_hash = %s WHERE id = %s RETURNING id, username, email"
    return Database.execute_query(query, (new_password_hash, user_id))

def update_user_email(user_id: int, new_email: str) -> Dict[str, Any]:
    """Updates a user's email."""
    logger.info(f"Updating email for user with ID {user_id}")

    if not get_user_by_id(user_id):
        logger.error(f"User ID {user_id} does not exist.")
        raise ValueError("User ID does not exist.")
    if get_user_by_email(new_email):
        logger.error(f"Email '{new_email}' already exists.")
        raise ValueError("Email already exists.")
    
    query = "UPDATE users SET email = %s WHERE id = %s RETURNING id, username, email"
    return Database.execute_query(query, (new_email, user_id))

def delete_user(user_id: int) -> Dict[str, Any]:
    """Deletes a user by their ID."""
    logger.info(f"Deleting user with ID {user_id}")

    if not get_user_by_id(user_id):
        logger.error(f"User ID {user_id} does not exist.")
        raise ValueError("User ID does not exist.")
    
    query = "DELETE FROM users WHERE id = %s RETURNING id"
    return Database.execute_query(query, (user_id,))
