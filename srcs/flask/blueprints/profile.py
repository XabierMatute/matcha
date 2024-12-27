from flask import Blueprint, request, jsonify, session
from manager.profile_manager import (
    get_user_profile,
    update_user_profile,
    get_user_location,
    update_user_location,
    get_location_from_ip
)
import logging
import requests

# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    return jsonify(response), status_code

# Ruta para obtener el perfil completo
@profile_bp.route('/', methods=['GET'])
def get_profile():
    """
    Obtiene el perfil completo del usuario.
    """
    user_id = session.get('user_id')
    if not user_id:
        return error_response("User not logged in.", 401)
    try:
        profile = get_user_profile(user_id)
        return jsonify(success_response(data=profile, message="Profile fetched successfully.")), 200
    except Exception as e:
        logger.error(f"Error fetching profile for user ID {user_id}: {e}")
        return error_response("Failed to fetch user profile.", 500)

# Ruta para actualizar el perfil
@profile_bp.route('/update', methods=['POST'])
def update_profile():
    """
    Actualiza el perfil del usuario.
    """
    user_id = session.get('user_id')
    if not user_id:
        return error_response("User not logged in.", 401)

    data = request.json
    if not data or not isinstance(data, dict):
        return error_response("Invalid input data.", 400)
    try:
        updated_profile = update_user_profile(user_id, data)
        return jsonify(success_response(data=updated_profile, message="Profile updated successfully.")), 200
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error updating profile for user ID {user_id}: {e}")
        return error_response("Failed to update user profile.", 500)

# Ruta para obtener la ubicación
@profile_bp.route('/location', methods=['GET'])
def get_location():
    """
    Obtiene la ubicación actual del usuario.
    """
    user_id = session.get('user_id')
    if not user_id:
        return error_response("User not logged in.", 401)
    try:
        location = get_user_location(user_id)
        return jsonify(success_response(data=location, message="Location fetched successfully.")), 200
    except Exception as e:
        logger.error(f"Error fetching location for user ID {user_id}: {e}")
        return error_response("Failed to fetch user location.", 500)

# Ruta para actualizar la ubicación manualmente
@profile_bp.route('/location/update', methods=['POST'])
def set_manual_location():
    """
    Permite a los usuarios configurar su ubicación manualmente.
    JSON Payload: { "location": "Bilbao", "latitude": 43.262, "longitude": -2.935 }
    """
    user_id = session.get('user_id')
    if not user_id:
        return error_response("User not logged in.", 401)

    data = request.json
    if not data or not isinstance(data, dict):
        return error_response("Invalid input data.", 400)

    location = data.get("location")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if location is None and (latitude is None or longitude is None):
        return error_response("You must provide either a location or both latitude and longitude.", 400)

    if latitude is not None and not isinstance(latitude, (int, float)):
        return error_response("Latitude must be a number.", 400)
    if longitude is not None and not isinstance(longitude, (int, float)):
        return error_response("Longitude must be a number.", 400)

    try:
        updated_location = update_user_location(user_id, location, latitude, longitude)
        return jsonify(success_response(data=updated_location, message="Location updated successfully.")), 200
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error updating location for user ID {user_id}: {e}")
        return error_response("Failed to update user location.", 500)

# Ruta para obtener la ubicación basada en IP
@profile_bp.route('/location/ip', methods=['GET'])
def get_location_by_ip():
    """
    Obtiene la ubicación basada en la dirección IP del cliente.
    """
    user_id = session.get('user_id')
    if not user_id:
        return error_response("User not logged in.", 401)

    ip_address = request.remote_addr  # Obtiene la IP del cliente
    logger.debug(f"Fetching location for IP: {ip_address}")

    location_data = get_location_from_ip(ip_address)
    if location_data["location"] is None:
        return error_response("Failed to fetch location from IP.", 400)

    try:
        updated_location = update_user_location(
            user_id,
            location=location_data["location"],
            latitude=location_data["latitude"],
            longitude=location_data["longitude"]
        )
        return jsonify(success_response(data=updated_location, message="Location updated successfully.")), 200
    except Exception as e:
        logger.error(f"Error updating location for user ID {user_id}: {e}")
        return error_response("Failed to update location.", 500)
