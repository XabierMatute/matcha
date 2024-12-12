import logging
from models.user_model import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    update_user,
    delete_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict, Optional
from config import UserConfig as config
from email_validator import validate_email, EmailNotValidError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_user(data: Dict) -> Dict:
    """
    Registers a new user in the system.
    
    Args:
        data (Dict): Dictionary with fields 'username', 'email', 'password',
                     'birthdate', 'first_name', and 'last_name'.
                     
    Returns:
        Dict: Registered user data.
        
    Raises:
        ValueError: If any required field is missing or the email/username already exists.
    """
    logger.info("Registering user with data: %s", data)
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            logger.error("Missing required field: %s", field)
            raise ValueError(f"Missing required field: {field}")

    # Additional validations
    # username
    username = data['username']
    if not username:
        logger.error("No username provided.")
        raise ValueError("No username provided.")
    for i in username:
        if not i.isalnum() and i != "_":
            logger.error("Invalid username: %s", username)
            raise ValueError("Username must contain only letters, numbers, and underscores.")
    if len(username) < config.USERNAME_MIN_LENGTH:
        logger.error("Username too short: %s", username)
        raise ValueError(f"Username must be at least {config.USERNAME_MIN_LENGTH} characters long.")

    # email
    if not data['email']:
        logger.error("No email provided.")
        raise ValueError("No email provided.")
    mail = data['email']

    try:
        # validate and get info
        v = validate_email(mail)
        mail = v["email"]  # replace with normalized form
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        logger.error("Invalid email: %s", mail)
        if config.DEBUG:
            logger.debug("Ignoring: %s", str(e))
        else:
            raise ValueError(f"Invalid email: {str(e)}")

    if not data['password']:
        logger.error("No password provided.")
        raise ValueError("No password provided.")
    password = data['password']
    if len(password) < config.PASSWORD_MIN_LENGTH:
        logger.error("Password too short.")
        raise ValueError(f"Password must be at least {config.PASSWORD_MIN_LENGTH} characters long.")

    # Create password hash
    password_hash = generate_password_hash(data['password'])

    user = create_user(
        username=username,
        email=mail,
        password_hash=password_hash
    )

    logger.info("User registered successfully: %s", user)
    return user

def authenticate_user(username: str, password: str) -> Dict:
    """
    Authenticates a user with their username and password.
    
    Args:
        username (str): Username.
        password (str): Password.
        
    Returns:
        Dict: Authenticated user data.
        
    Raises:
        ValueError: If the username/password are incorrect or the account is not verified.
    """
    logger.info("Authenticating user: %s", username)
    user = get_user_by_username(username)
    if not user:
        logger.error("Invalid username: %s", username)
        raise ValueError("Invalid username")
    if not check_password_hash(user['password_hash'], password):
        logger.error("Invalid password for user: %s", username)
        raise ValueError("Invalid password")
    logger.info("User authenticated successfully: %s", username)
    return user

def update_user_profile(user_id: int, updates: Dict) -> Optional[Dict]:
    """
    Updates a user's profile data.
    
    Args:
        user_id (int): ID of the user to update.
        updates (Dict): Fields to update (username, email, first_name, last_name).
        
    Returns:
        Optional[Dict]: Updated user data.
        
    Raises:
        ValueError: If no valid fields are provided or the user does not exist.
    """
    logger.info("Updating user profile for user_id: %d with updates: %s", user_id, updates)
    if not updates:
        logger.error("No fields provided for update.")
        raise ValueError("No fields provided for update.")
    updated_user = update_user(user_id, **updates)
    logger.info("User profile updated successfully: %s", updated_user)
    return updated_user

def delete_user_account(user_id: int) -> Optional[Dict]:
    """
    Deletes a user's account.
    
    Args:
        user_id (int): ID of the user to delete.
        
    Returns:
        Optional[Dict]: Deleted user data.
        
    Raises:
        ValueError: If the user does not exist.
    """
    logger.info("Deleting user account for user_id: %d", user_id)
    deleted_user = delete_user(user_id)
    logger.info("User account deleted successfully: %s", deleted_user)
    return deleted_user

def get_user_details(user_id: int) -> Dict:
    """
    Retrieves a user's details.
    
    Args:
        user_id (int): ID of the user.
        
    Returns:
        Optional[Dict]: User details.
        
    Raises:
        ValueError: If the user does not exist.
    """
    logger.info("Retrieving user details for user_id: %d", user_id)
    user = get_user_by_id(user_id)
    if not user:
        logger.error("User with ID %d not found.", user_id)
        raise ValueError(f"User with ID {user_id} not found.")
    logger.info("User details retrieved successfully: %s", user)
    return user