from models.database import Database
import logging
from psycopg2.extras import execute_values


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_interest(tag):
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
                interest = cursor.fetchone()
                return {"id": interest[0], "tag": interest[1]}
    except Exception as e:
        logger.error(f"Error creating interest '{tag}': {e}")
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
                interests = cursor.fetchall()
                return [{"id": row[0], "tag": row[1]} for row in interests]
    except Exception as e:
        logger.error(f"Error listing interests: {e}")
        raise Exception("Error listing interests") from e

def get_interest_by_id(interest_id):
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
                interest = cursor.fetchone()
                if not interest:
                    raise ValueError("Interest not found.")
                return {"id": interest[0], "tag": interest[1]}
    except Exception as e:
        logger.error(f"Error fetching interest with ID {interest_id}: {e}")
        raise Exception("Error fetching interest") from e

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
                execute_values(cursor, query, [(tag,) for tag in tags])
                connection.commit()
                interests = cursor.fetchall()
                return [{"id": row[0], "tag": row[1]} for row in interests]
    except Exception as e:
        logger.error(f"Error adding interests: {e}")
        raise Exception("Error adding interests") from e

def remove_interests(interest_ids):
    """Elimina múltiples intereses de la base de datos."""
    if not interest_ids or not all(isinstance(i, int) and i > 0 for i in interest_ids):
        raise ValueError("Interest IDs must be a non-empty list of positive integers.")

    query = '''
        DELETE FROM interests
        WHERE id = ANY(%s)
        RETURNING id
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (interest_ids,))
                connection.commit()
                deleted = cursor.fetchall()
                return {"deleted_ids": [row[0] for row in deleted]}
    except Exception as e:
        logger.error(f"Error removing interests: {e}")
        raise Exception("Error removing interests") from e

def update_user_interests(user_id, new_interests):
    """Actualiza los intereses de un usuario."""
    if not new_interests or not all(isinstance(tag, str) and tag.strip() for tag in new_interests):
        raise ValueError("New interests must be a non-empty list of strings.")

    delete_query = '''DELETE FROM user_interests WHERE user_id = %s'''
    get_interest_ids_query = '''SELECT id FROM interests WHERE tag = ANY(%s)'''
    insert_query = '''INSERT INTO user_interests (user_id, interest_id) VALUES %s'''

    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(delete_query, (user_id,))
                cursor.execute(get_interest_ids_query, (new_interests,))
                interest_ids = cursor.fetchall()

                if not interest_ids:
                    raise ValueError("None of the provided interests exist in the database.")

                interest_values = [(user_id, interest_id[0]) for interest_id in interest_ids]
                execute_values(cursor, insert_query, interest_values)
                connection.commit()

                return {"success": True, "message": "User interests updated successfully."}
    except Exception as e:
        logger.error(f"Error updating interests for user ID {user_id}: {e}")
        raise Exception("Error updating user interests") from e





