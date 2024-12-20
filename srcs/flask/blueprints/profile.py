from flask import Blueprint, request, jsonify, session
from manager.profile_manager import (
    fetch_user_profile,
    update_user_profile,
    fetch_user_location,
    update_user_location
)
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    if details:
        response["details"] = details
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
        profile = fetch_user_profile(user_id)
        return jsonify(success_response(data=profile, message="Profile fetched successfully.")), 200
    except Exception as e:
        logger.error(f"Error fetching profile for user ID {user_id}: {e}")
        return error_response("Failed to fetch user profile.", 500, details=str(e))

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
    try:
        updated_profile = update_user_profile(user_id, data)
        return jsonify(success_response(data=updated_profile, message="Profile updated successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error updating profile for user ID {user_id}: {e}")
        return error_response("Failed to update user profile.", 500, details=str(e))

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
        location = fetch_user_location(user_id)
        return jsonify(success_response(data=location, message="Location fetched successfully.")), 200
    except Exception as e:
        logger.error(f"Error fetching location for user ID {user_id}: {e}")
        return error_response("Failed to fetch user location.", 500, details=str(e))

# Ruta para actualizar la ubicación manualmente
@profile_bp.route('/location/manual', methods=['POST'])
def set_manual_location():
    """
    Permite a los usuarios configurar su ubicación manualmente.
    JSON Payload: { "location": "Bilbao", "latitude": 43.262, "longitude": -2.935 }
    """
    user_id = session.get('user_id')
    if not user_id:
        return error_response("User not logged in.", 401)

    data = request.json
    location = data.get("location")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not location and (latitude is None or longitude is None):
        return error_response("Either location or latitude and longitude must be provided.", 400)

    try:
        updated_location = update_user_location(user_id, location, latitude, longitude)
        return jsonify(success_response(data=updated_location, message="Location updated successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error updating location for user ID {user_id}: {e}")
        return error_response("Failed to update user location.", 500, details=str(e))


