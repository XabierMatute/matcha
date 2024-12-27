# from .database import Database
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def validate_user_id(user_id):
#     """Valida que el ID del usuario sea un entero positivo."""
#     if not isinstance(user_id, int) or user_id <= 0:
#         raise ValueError("Invalid user ID. It must be a positive integer.")

# def validate_location_data(location, latitude, longitude):
#     """Valida los datos de ubicación."""
#     if location is not None and not isinstance(location, str):
#         raise ValueError("Location must be a string.")
#     if latitude is not None and not isinstance(latitude, (int, float)):
#         raise ValueError("Latitude must be a number.")
#     if longitude is not None and not isinstance(longitude, (int, float)):
#         raise ValueError("Longitude must be a number.")

# def create_profile(user_id):
#     """
#     Crea un perfil vacío para un usuario.
#     """
#     validate_user_id(user_id)

#     query = '''
#         INSERT INTO profiles (user_id)
#         VALUES (%s)
#         RETURNING user_id
#     '''
#     try:
#         with Database.get_connection() as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, (user_id,))
#                 connection.commit()
#                 created_profile = cursor.fetchone()
#                 if not created_profile:
#                     raise ValueError("Failed to create profile.")
#                 return {"user_id": created_profile[0]}
#     except Exception as e:
#         logger.error(f"Error creating profile for user ID {user_id}: {e}")
#         raise Exception("Error creating profile.") from e

# def get_profile_by_user_id(user_id):
#     """
#     Obtiene el perfil completo de un usuario por su ID.
#     """
#     validate_user_id(user_id)

#     query = '''
#         SELECT user_id, biography, fame_rating, profile_picture, location, latitude, longitude, is_active
#         FROM profiles
#         WHERE user_id = %s
#     '''
#     try:
#         with Database.get_connection() as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, (user_id,))
#                 profile = cursor.fetchone()
#                 if not profile:
#                     raise ValueError("Profile not found for the given user ID.")
                
#                 return {
#                     "user_id": profile[0],
#                     "biography": profile[1],
#                     "fame_rating": profile[2],
#                     "profile_picture": profile[3],
#                     "location": profile[4],
#                     "latitude": profile[5],
#                     "longitude": profile[6],
#                     "is_active": profile[7],
#                 }
#     except Exception as e:
#         logger.error(f"Error fetching profile for user ID {user_id}: {e}")
#         raise Exception("Error fetching profile.") from e

# def update_profile(user_id, **fields):
#     """
#     Actualiza los datos del perfil de un usuario.
#     """
#     validate_user_id(user_id)

#     valid_fields = ['biography', 'location', 'latitude', 'longitude', 'profile_picture']
#     updates = []
#     params = []

#     for field, value in fields.items():
#         if field in valid_fields and value is not None:
#             updates.append(f"{field} = %s")
#             params.append(value)

#     if not updates:
#         raise ValueError("No valid fields provided to update.")

#     query = f"UPDATE profiles SET {', '.join(updates)} WHERE user_id = %s RETURNING user_id, {', '.join(valid_fields)}"
#     params.append(user_id)

#     try:
#         with Database.get_connection() as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, tuple(params))
#                 connection.commit()
#                 updated_profile = cursor.fetchone()
#                 if not updated_profile:
#                     raise ValueError("Failed to update profile. User ID may not exist.")
#                 return dict(zip(["user_id"] + valid_fields, updated_profile))
#     except Exception as e:
#         logger.error(f"Error updating profile for user ID {user_id}: {e}")
#         raise Exception("Error updating profile.") from e

# def get_location(user_id):
#     """
#     Obtiene la ubicación actual de un usuario.
#     """
#     validate_user_id(user_id)

#     query = "SELECT location, latitude, longitude FROM profiles WHERE user_id = %s"
#     try:
#         with Database.get_connection() as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, (user_id,))
#                 location = cursor.fetchone()
#                 if not location:
#                     raise ValueError("Location not found for the given user ID.")
#                 return {
#                     "location": location[0],
#                     "latitude": location[1],
#                     "longitude": location[2]
#                 }
#     except Exception as e:
#         logger.error(f"Error fetching location for user ID {user_id}: {e}")
#         raise Exception("Error fetching location.") from e

# def update_location(user_id, location, latitude, longitude):
#     """
#     Actualiza la ubicación de un usuario.
#     """
#     validate_user_id(user_id)
#     validate_location_data(location, latitude, longitude)

#     query = '''
#         UPDATE profiles
#         SET location = %s, latitude = %s, longitude = %s
#         WHERE user_id = %s
#         RETURNING location, latitude, longitude
#     '''
#     try:
#         with Database.get_connection() as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, (location, latitude, longitude, user_id))
#                 connection.commit()
#                 updated_location = cursor.fetchone()
#                 if not updated_location:
#                     raise ValueError("Failed to update location. User ID may not exist.")
#                 return {
#                     "location": updated_location[0],
#                     "latitude": updated_location[1],
#                     "longitude": updated_location[2]
#                 }
#     except Exception as e:
#         logger.error(f"Error updating location for user ID {user_id}: {e}")
#         raise Exception("Error updating location.") from e
import logging
from typing import Optional, Dict, Any, List
from .database import Database

logger = logging.getLogger(__name__)

def validate_location_data(location: Optional[str], latitude: Optional[float], longitude: Optional[float]):
    """Valida que los datos de ubicación sean correctos."""
    if location is not None and not isinstance(location, str):
        raise ValueError("Location must be a string.")
    if latitude is not None and not isinstance(latitude, (int, float)):
        raise ValueError("Latitude must be a number.")
    if longitude is not None and not isinstance(longitude, (int, float)):
        raise ValueError("Longitude must be a number.")

def get_location_from_ip(ip_address: str) -> Dict[str, Any]:
    """
    Simula obtener la ubicación geográfica basada en la IP.
    (En producción, usar una API como ipstack o GeoIP).
    """
    logger.info(f"Fetching location for IP: {ip_address}")
    # Simulación de datos para una IP
    return {
        "location": "Bilbao, Spain",
        "latitude": 43.263,
        "longitude": -2.935,
    }

def create_profile(user_id: int, profile_data: Dict[str, Any], ip_address: Optional[str] = None) -> Dict[str, Any]:
    """
    Crea un perfil para un usuario.
    Si no se proporciona ubicación, intenta obtenerla desde la IP.
    """
    logger.info(f"Creating profile for user_id={user_id}")
    
    location = profile_data.get("location")
    latitude = profile_data.get("latitude")
    longitude = profile_data.get("longitude")
    
    if not location and ip_address:
        logger.info(f"No location provided. Fetching from IP {ip_address}.")
        ip_location = get_location_from_ip(ip_address)
        location = ip_location["location"]
        latitude = ip_location["latitude"]
        longitude = ip_location["longitude"]
    
    validate_location_data(location, latitude, longitude)
    
    query = '''
    INSERT INTO profiles (user_id, first_name, last_name, birthdate, gender, sexual_preferences, biography, 
                          fame_rating, profile_picture, location, latitude, longitude, is_active, last_seen, is_online)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
    RETURNING *
    '''
    params = (
        user_id, 
        profile_data.get("first_name"), 
        profile_data.get("last_name"), 
        profile_data.get("birthdate"), 
        profile_data.get("gender"), 
        profile_data.get("sexual_preferences"), 
        profile_data.get("biography"), 
        profile_data.get("fame_rating", 0.0), 
        profile_data.get("profile_picture"), 
        location, 
        latitude, 
        longitude, 
        profile_data.get("is_active", False), 
        profile_data.get("is_online", False)
    )
    return Database.execute_query(query, params)

def get_profile_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Recupera el perfil de un usuario.
    """
    logger.info(f"Fetching profile for user_id={user_id}")
    query = "SELECT * FROM profiles WHERE user_id = %s"
    return Database.execute_query(query, (user_id,))

def update_profile(user_id: int, updated_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Actualiza los datos del perfil de un usuario.
    """
    logger.info(f"Updating profile for user_id={user_id}")

    fields = []
    params = []
    for field, value in updated_data.items():
        fields.append(f"{field} = %s")
        params.append(value)

    if not fields:
        raise ValueError("No fields provided to update.")

    params.append(user_id)
    query = f"UPDATE profiles SET {', '.join(fields)} WHERE user_id = %s RETURNING *"
    return Database.execute_query(query, tuple(params))

def delete_profile(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Elimina un perfil de usuario.
    """
    logger.info(f"Deleting profile for user_id={user_id}")
    query = "DELETE FROM profiles WHERE user_id = %s RETURNING *"
    return Database.execute_query(query, (user_id,))



