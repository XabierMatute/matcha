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




