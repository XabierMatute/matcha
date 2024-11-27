import logging
from database import get_db_connection

# Configurar el logger
logging.basicConfig(level=logging.INFO)

def add_like(user_id, liked_user_id):
    """
    Agrega un like de un usuario a otro.
    
    :param user_id: ID del usuario que da el like.
    :param liked_user_id: ID del usuario que recibe el like.
    :return: Diccionario con los datos del like si se agregó correctamente, o None si ya existía.
    """
    query = '''
        INSERT INTO likes (user_id, liked_user_id)
        VALUES (%s, %s)
        ON CONFLICT (user_id, liked_user_id) DO NOTHING
        RETURNING id, user_id, liked_user_id, timestamp
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, liked_user_id))
                result = cursor.fetchone()
                connection.commit()
                if result:
                    logging.info(f"Like added successfully: {result}")
                    return {
                        "id": result[0],
                        "user_id": result[1],
                        "liked_user_id": result[2],
                        "timestamp": result[3],
                    }
                else:
                    logging.info("Like already exists.")
                    return None
    except Exception as e:
        logging.error(f"Error adding like: {e}")
        raise Exception("Error adding like")

def remove_like(user_id, liked_user_id):
    """
    Elimina un like de un usuario a otro.
    
    :param user_id: ID del usuario que da el like.
    :param liked_user_id: ID del usuario que recibió el like.
    :return: True si se eliminó, False si no existía.
    """
    query = '''
        DELETE FROM likes
        WHERE user_id = %s AND liked_user_id = %s
        RETURNING id
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, liked_user_id))
                result = cursor.fetchone()
                connection.commit()
                if result:
                    logging.info(f"Like removed successfully: {result}")
                    return True
                else:
                    logging.info("No like found to remove.")
                    return False
    except Exception as e:
        logging.error(f"Error removing like: {e}")
        raise Exception("Error removing like")

def get_likes(user_id):
    """
    Obtiene todos los likes que un usuario ha dado.
    
    :param user_id: ID del usuario.
    :return: Lista de diccionarios con los likes.
    """
    query = '''
        SELECT id, liked_user_id, timestamp
        FROM likes
        WHERE user_id = %s
        ORDER BY timestamp DESC
    '''
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                results = cursor.fetchall()
                likes = [
                    {"id": row[0], "liked_user_id": row[1], "timestamp": row[2]}
                    for row in results
                ]
                logging.info(f"Likes retrieved successfully for user_id {user_id}: {likes}")
                return likes
    except Exception as e:
        logging.error(f"Error retrieving likes: {e}")
        raise Exception("Error retrieving likes")
