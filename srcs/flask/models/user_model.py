import logging
from typing import Optional, Dict

from .database import Database

logging.basicConfig(level=logging.INFO)

# Get user by ID
def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Gets a user by their ID."""
    logging.info(f"Fetching user with ID {user_id}")
    query = "SELECT * FROM users WHERE id = %s"
    user = Database.execute_query(query, (user_id,))
    if not user:
        logging.info(f"User with ID {user_id} not found.")
    return user

# Get user by username
def get_user_by_username(username: str) -> Optional[Dict]:
    """Gets a user by their username."""
    logging.info(f"Fetching user with username {username}")
    query = "SELECT * FROM users WHERE username = %s"
    user = Database.execute_query(query, (username,))
    if not user:
        logging.info(f"User with username {username} not found.")
    return user

# Get user by email
def get_user_by_email(email: str) -> Optional[Dict]:
    """Gets a user by their email."""
    logging.info(f"Fetching user with email {email}")
    query = "SELECT * FROM users WHERE email = %s"
    user = Database.execute_query(query, (email,))
    if not user:
        logging.info(f"User with email {email} not found.")
    return user

# Validate user by email
def validate_user(email: str) -> Optional[Dict]:
    """Validates a user by their email."""
    logging.info(f"Validating user with email {email}")
    user = get_user_by_email(email)
    if not user:
        logging.error(f"No user with email {email} found.")
        raise ValueError(f"No user with email {email} found.")
    query = "UPDATE users SET is_verified = TRUE WHERE email = %s RETURNING id, username, email, first_name, last_name"
    return Database.execute_query(query, (email,))

# Create a new user
def create_user(username: str, email: str, password_hash: str, 
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict:
    """Creates a new user."""
    logging.info(f"Creating user with username {username} and email {email}")
    # Check if the username or email already exists
    if get_user_by_username(username):
        logging.error(f"Username {username} already exists.")
        raise ValueError("Username already exists.")
    if get_user_by_email(email):
        logging.error(f"Email {email} already in use.")
        raise ValueError("Email already in use.") #TODO: make unverified accounts expire?? or something like that so someone can't compromise someone else's email
    if Database.execute_query("SELECT * FROM users WHERE email = %s", (email,)):
        logging.error(f"Email {email} already exists.")
        raise ValueError("Email already exists.")

    query = '''
        INSERT INTO users (username, email, password_hash, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, username, email, first_name, last_name
    '''

    return Database.execute_query(query, (username, email, password_hash, first_name, last_name))

# Update user data
def update_user(user_id: int, username: Optional[str] = None, email: Optional[str] = None, 
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> Optional[Dict]:
    """Updates user data."""
    logging.info(f"Updating user with ID {user_id}")
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        logging.error(f"User ID {user_id} does not exist.")
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
        logging.error("No fields provided to update.")
        raise ValueError("No fields provided to update.")

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, username, email, first_name, last_name"
    params.append(user_id)

    return Database.execute_query(query, tuple(params))

# Delete a user
def delete_user(user_id: int) -> Optional[Dict]:
    """Deletes a user by their ID."""
    logging.info(f"Deleting user with ID {user_id}")
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        logging.error(f"User ID {user_id} does not exist.")
        raise ValueError("User ID does not exist.")

    query = "DELETE FROM users WHERE id = %s RETURNING id"
    return Database.execute_query(query, (user_id,))