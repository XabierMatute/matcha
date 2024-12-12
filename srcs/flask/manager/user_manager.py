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


# def valid_username(username: str) -> bool:
#     """
#     Comprueba si un nombre de usuario es válido.
#     Un nombre de usuario válido debe tener al menos USERNAME_MIN_LENGTH caracteres y estar compuesto unicamente por letras, números y guiones bajos.
    
#     Args:
#         username (str): Nombre de usuario.
        
#     Returns:
#         bool: True si es válido, False en caso contrario.
#     """
#     if not username:
#         return False
#     # numeros y letras y barras bajas
#     for i in username:
#         if not i.isalnum() and i != "_":
#             return False
#     if len(username) < config.USERNAME_MIN_LENGTH:
#         return False
#     return True

def register_user(data: Dict) -> Dict:
    """
    Registra un nuevo usuario en el sistema.
    
    Args:
        data (Dict): Diccionario con los campos 'username', 'email', 'password',
                     'birthdate', 'first_name', y 'last_name'.
                     
    Returns:
        Dict: Datos del usuario registrado.
        
    Raises:
        ValueError: Si falta algún campo requerido o el email/username ya existen.
    """
    # required_fields = ['username', 'email', 'password', 'birthdate', 'first_name', 'last_name']
    # birthdate no está en el formulario, podría estar en perfil por ser info de perfil, pero estaría guay poder comprovar que es mayor de edad
    # required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validaciones adicionales
    #username
    username = data['username']
    if not username:
        raise ValueError("Not username provided.")
    for i in username:
        if not i.isalnum() and i != "_":
            raise ValueError("Username must contain only letters, numbers, and underscores.")
    if len(username) < config.USERNAME_MIN_LENGTH:
        raise ValueError(f"Username must be at least {config.USERNAME_MIN_LENGTH} characters long.")

    # email
    if not data['email']:
        raise ValueError("No email provided.")
    mail = data['email']

    from email_validator import validate_email, EmailNotValidError

    try:
        # validate and get info
        v = validate_email(mail)
        mail = v["email"]  # replace with normalized form
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        if config.DEBUG:
            print("ignoring: ",str(e))
        else:
            raise ValueError(f"Invalid email: {str(e)}")

    if not data['password']:
        raise ValueError("No password provided.")
    password = data['password']
    if len(password) < config.PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {config.PASSWORD_MIN_LENGTH} characters long.")

    # Crear hash de contraseña
    password_hash = generate_password_hash(data['password'])

    user = create_user(
        username=username,
        email=mail,
        password_hash=password_hash
    )

    return user

def authenticate_user(username: str, password: str) -> Dict:
    """
    Autentica un usuario con su username y contraseña.
    
    Args:
        username (str): Nombre de usuario.
        password (str): Contraseña.
        
    Returns:
        Dict: Datos del usuario autenticado.
        
    Raises:
        ValueError: Si el username/contraseña son incorrectos o la cuenta no está verificada.
    """
    user = get_user_by_username(username)
    if not user:
        raise ValueError("Invalid username")
    if not check_password_hash(user['password_hash'], password):
        raise ValueError("Invalid password")
    # if not user.get('is_verified', False):
    #     raise ValueError("Account is not verified.")
    return user


def update_user_profile(user_id: int, updates: Dict) -> Optional[Dict]:
    """
    Actualiza los datos de perfil de un usuario.
    
    Args:
        user_id (int): ID del usuario a actualizar.
        updates (Dict): Campos a actualizar (username, email, first_name, last_name).
        
    Returns:
        Optional[Dict]: Datos del usuario actualizado.
        
    Raises:
        ValueError: Si no se proporcionan campos válidos o el usuario no existe.
    """
    if not updates:
        raise ValueError("No fields provided for update.")
    return update_user(user_id, **updates)


def delete_user_account(user_id: int) -> Optional[Dict]:
    """
    Elimina la cuenta de un usuario.
    
    Args:
        user_id (int): ID del usuario a eliminar.
        
    Returns:
        Optional[Dict]: Datos del usuario eliminado.
        
    Raises:
        ValueError: Si el usuario no existe.
    """
    return delete_user(user_id)


def get_user_details(user_id: int) -> Dict:
    """
    Obtiene los detalles de un usuario.
    
    Args:
        user_id (int): ID del usuario.
        
    Returns:
        Optional[Dict]: Detalles del usuario.
        
    Raises:
        ValueError: Si el usuario no existe.
    """
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")
    return user

