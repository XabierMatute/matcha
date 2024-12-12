from models.database import Database
import logging
# from psycopg.extras import execute_values

logging.basicConfig(level=logging.INFO)

def create_interest(tag):
    """Crea un nuevo interés."""
    query = '''
        INSERT INTO interests (tag)
        VALUES (%s)
        RETURNING id, tag
    '''
    return execute_query(query, (tag,))

def list_interests():
    """Obtiene todos los intereses disponibles."""
    query = '''
        SELECT id, tag
        FROM interests
        ORDER BY tag ASC
    '''
    return execute_query(query, fetchone=False)

def get_interest_by_id(interest_id):
    """Obtiene un interés por su ID."""
    query = '''
        SELECT id, tag
        FROM interests
        WHERE id = %s
    '''
    return execute_query(query, (interest_id,))

def add_interests(tags):
    """Agrega múltiples intereses a la base de datos, evitando duplicados."""
    if not tags or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        raise ValueError("Tags must be a non-empty list of strings.")

    query = '''
        INSERT INTO interests (tag)
        VALUES %s
        ON CONFLICT (tag) DO NOTHING
        RETURNING id, tag
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                # execute_values(cursor, query, [(tag,) for tag in tags])
                connection.commit()
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error adding interests: {e}")
        raise Exception("Error adding interests") from e

def remove_interests(interest_ids):
    """Elimina múltiples intereses de la base de datos."""
    if not interest_ids:
        raise ValueError("Interest IDs list cannot be empty.")

    query = '''
        DELETE FROM interests
        WHERE id = ANY(%s)
    '''
    return execute_query(query, (interest_ids,))
def update_user_interests(user_id, new_interests):
    """
    Actualiza los intereses de un usuario.
    Reemplaza los intereses existentes con los proporcionados.
    """
    if not new_interests or not all(isinstance(tag, str) and tag.strip() for tag in new_interests):
        raise ValueError("New interests must be a non-empty list of strings.")

    # Eliminar intereses actuales
    delete_query = '''
        DELETE FROM user_interests
        WHERE user_id = %s
    '''

    # Insertar nuevos intereses
    insert_query = '''
        INSERT INTO user_interests (user_id, interest_id)
        VALUES %s
    '''

    # Asegúrate de que los nuevos intereses existan en la tabla de intereses
    get_interest_ids_query = '''
        SELECT id
        FROM interests
        WHERE tag = ANY(%s)
    '''

    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                # Eliminar intereses actuales
                cursor.execute(delete_query, (user_id,))

                # Obtener IDs de los nuevos intereses
                cursor.execute(get_interest_ids_query, (new_interests,))
                interest_ids = cursor.fetchall()

                if not interest_ids:
                    raise ValueError("None of the provided interests exist in the database.")

                # Formatear datos para la inserción
                interest_values = [(user_id, interest_id[0]) for interest_id in interest_ids]

                # Insertar nuevos intereses
                execute_values(cursor, insert_query, interest_values)
                connection.commit()

                return {"success": True, "message": "User interests updated successfully."}
    except Exception as e:
        logging.error(f"Error updating interests for user ID {user_id}: {e}")
        raise Exception("Error updating user interests") from e




