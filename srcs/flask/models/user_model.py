from .database import Database
import logging
from typing import Optional, Dict, Tuple

logging.basicConfig(level=logging.INFO)

# Función auxiliar para ejecutar consultas y manejar errores
# PQ no está en database.py?
def execute_query(query: str, params: Tuple = (), fetchone: bool = True) -> Optional[Dict]:
    """Ejecuta una consulta en la base de datos y maneja el cursor."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:  # Solo intenta obtener resultados si la consulta los devuelve.
                    return cursor.fetchone() if fetchone else cursor.fetchall()
                connection.commit()  # Confirma transacción en INSERT, UPDATE o DELETE.
    except Exception as e:
        logging.error(f"Error executing query: {query}, params: {params}, error: {e}")
        raise Exception("Database query error") from e

# Obtener usuario por ID
def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Obtiene un usuario por su ID."""
    query = "SELECT * FROM users WHERE id = %s"
    user = execute_query(query, (user_id,))
    if not user:
        logging.info(f"User with ID {user_id} not found.")
    return user

# Obtener usuario por nombre de usuario
def get_user_by_username(username: str) -> Optional[Dict]:
    """Obtiene un usuario por su nombre de usuario."""
    query = "SELECT * FROM users WHERE username = %s"
    user = execute_query(query, (username,))
    if not user:
        logging.info(f"User with username {username} not found.")
    return user

def get_user_by_email(email: str) -> Optional[Dict]:
    """Obtiene un usuario por su email."""
    query = "SELECT * FROM users WHERE email = %s"
    user = execute_query(query, (email,))
    if not user:
        logging.info(f"User with email {email} not found.")
    return user

def validate_user(email: str) -> Optional[Dict]:
    """Valida un usuario por su email."""
    user = get_user_by_email(email)
    if not user:
        raise ValueError(f"No user with email {email} found.")
    query = "UPDATE users SET is_verified = TRUE WHERE email = %s RETURNING id, username, email, first_name, last_name"
    return execute_query(query, (email,))


# Crear un nuevo usuario
def create_user(username: str, email: str, password_hash: str, 
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict:
    """Crea un nuevo usuario."""
    # Verificar si el username o email ya existen
    if get_user_by_username(username):
        raise ValueError("Username already exists.")
    if get_user_by_email(email):
        raise ValueError("Email already in use.") #TODO: hacer que las cuentas sin verificar caduquen?? o algo así para que alguien no pueda compromenter un correo ajeno
    if execute_query("SELECT * FROM users WHERE email = %s", (email,)):
        raise ValueError("Email already exists.")

    query = '''
        INSERT INTO users (username, email, password_hash, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, username, email, birthdate, first_name, last_name
    '''
    return execute_query(query, (username, email, password_hash, first_name, last_name))

# Actualizar datos del usuario
def update_user(user_id: int, username: Optional[str] = None, email: Optional[str] = None, 
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> Optional[Dict]:
    """Actualiza los datos de un usuario."""
    existing_user = get_user_by_id(user_id)
    if not existing_user:
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

    return execute_query(query, tuple(params))

# Eliminar un usuario
def delete_user(user_id: int) -> Optional[Dict]:
    """Elimina un usuario por su ID."""
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise ValueError("User ID does not exist.")

    query = "DELETE FROM users WHERE id = %s RETURNING id"
    return execute_query(query, (user_id,))

