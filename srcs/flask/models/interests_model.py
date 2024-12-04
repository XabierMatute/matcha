from .database import Database
import logging

logging.basicConfig(level=logging.INFO)

def create_interests(tag):
    """Crea un nuevo interés."""
    query = '''
        INSERT INTO interests (tag)
        VALUES (%s)
        RETURNING id, tag
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (tag,))
                connection.commit()
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error creating interest '{tag}': {e}")
        raise Exception("Error creating interest") from e

def list_interests():
    """Obtiene todos los intereses disponibles."""
    query = '''
        SELECT id, tag
        FROM interests
        ORDER BY tag ASC
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching interests: {e}")
        raise Exception("Error fetching interests") from e

def get_interests_by_id(interest_id):
    """Obtiene un interés por su ID."""
    query = '''
        SELECT id, tag
        FROM interests
        WHERE id = %s
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (interest_id,))
                return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error fetching interest ID {interest_id}: {e}")
        raise Exception("Error fetching interest") from e

def add_interests(tags):
    """Agrega múltiples intereses a la base de datos."""
    query = '''
        INSERT INTO interests (tag)
        VALUES (%s)
        ON CONFLICT (tag) DO NOTHING
        RETURNING id, tag
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                added_interests = []
                for tag in tags:
                    cursor.execute(query, (tag,))
                    result = cursor.fetchone()
                    if result:
                        added_interests.append(result)
                connection.commit()
                return added_interests
    except Exception as e:
        logging.error(f"Error adding interests: {e}")
        raise Exception("Error adding interests") from e

def remove_interests(interest_ids):
    """Elimina múltiples intereses de la base de datos."""
    query = '''
        DELETE FROM interests
        WHERE id = %s
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                for interest_id in interest_ids:
                    cursor.execute(query, (interest_id,))
                connection.commit()
                return f"Removed {len(interest_ids)} interests."
    except Exception as e:
        logging.error(f"Error removing interests: {e}")
        raise Exception("Error removing interests") from e



