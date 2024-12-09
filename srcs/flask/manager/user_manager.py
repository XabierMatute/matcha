from models.user_model import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    update_user,
    delete_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict, Optional


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
    required_fields = ['username', 'email', 'password', 'birthdate', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validaciones adicionales
    if '@' not in data['email']:
        raise ValueError("Invalid email format.")
    if len(data['password']) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    # Crear hash de contraseña
    password_hash = generate_password_hash(data['password'])

    # Registrar usuario
    return create_user(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        birthdate=data['birthdate'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )


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
    if not user or not check_password_hash(user['password_hash'], password):
        raise ValueError("Invalid username or password.")
    if not user.get('is_verified', False):
        raise ValueError("Account is not verified.")
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


def get_user_details(user_id: int) -> Optional[Dict]:
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
        raise ValueError("User not found.")
    return user

