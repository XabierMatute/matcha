from .database import Database
import logging
from typing import Optional, Dict, Tuple

logging.basicConfig(level=logging.INFO)

# Función auxiliar para ejecutar consultas y manejar errores
def execute_query(query: str, params: Tuple = (), fetchone: bool = True) -> Optional[dict]:
    """Ejecuta una consulta en la base de datos y maneja el cursor."""
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetchone:
                    return cursor.fetchone()
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error executing query: {query}, params: {params}, error: {e}")
        raise Exception("Database query error") from e

# Obtener usuario por ID
def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Obtiene un usuario por su ID."""
    query = "SELECT * FROM users WHERE id = %s"
    return execute_query(query, (user_id,))

# Obtener usuario por nombre de usuario
def get_user_by_username(username: str) -> Optional[Dict]:
    """Obtiene un usuario por su nombre de usuario."""
    query = "SELECT * FROM users WHERE username = %s"
    return execute_query(query, (username,))

# Crear un nuevo usuario
def create_user(username: str, email: str, password_hash: str, birthdate: str, 
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict:
    """Crea un nuevo usuario."""
    query = '''
        INSERT INTO users (username, email, password_hash, birthdate, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, username, email, birthdate, first_name, last_name
    '''
    return execute_query(query, (username, email, password_hash, birthdate, first_name, last_name))

# Actualizar datos del usuario
def update_user(user_id: int, username: Optional[str] = None, email: Optional[str] = None, 
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> Optional[Dict]:
    """Actualiza los datos de un usuario."""
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
    query = "DELETE FROM users WHERE id = %s RETURNING id"
    return execute_query(query, (user_id,))

