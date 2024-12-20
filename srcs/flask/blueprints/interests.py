from flask import Blueprint, request, jsonify, session
from manager.interests_manager import (
    add_new_interest,
    fetch_all_interests,
    fetch_interest_by_id,
    bulk_add_interests,
    bulk_remove_interests,
    update_user_interests_list
)
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

interests_bp = Blueprint("interests", __name__, url_prefix="/interests")

def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code

# Ruta para obtener todos los intereses
@interests_bp.route('/', methods=['GET'])
def list_interests():
    """
    Obtiene todos los intereses disponibles.
    """
    try:
        interests = fetch_all_interests()
        return jsonify(success_response(data=interests, message="Interests fetched successfully.")), 200
    except Exception as e:
        logger.error(f"Error fetching interests: {e}")
        return error_response("Failed to fetch interests.", 500, details=str(e))

# Ruta para obtener un interés por ID
@interests_bp.route('/<int:interest_id>', methods=['GET'])
def get_interest(interest_id):
    """
    Obtiene un interés por su ID.
    """
    try:
        interest = fetch_interest_by_id(interest_id)
        return jsonify(success_response(data=interest, message="Interest fetched successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error fetching interest with ID {interest_id}: {e}")
        return error_response("Failed to fetch interest.", 500, details=str(e))

# Ruta para crear un nuevo interés
@interests_bp.route('/add', methods=['POST'])
def create_interest():
    """
    Crea un nuevo interés.
    """
    data = request.json
    tag = data.get("tag")

    if not tag:
        return error_response("Tag is required.", 400)

    try:
        new_interest = add_new_interest(tag)
        return jsonify(success_response(data=new_interest, message="Interest created successfully.")), 201
    except Exception as e:
        logger.error(f"Error creating interest '{tag}': {e}")
        return error_response("Failed to create interest.", 500, details=str(e))

# Ruta para agregar múltiples intereses
@interests_bp.route('/add-batch', methods=['POST'])
def add_multiple_interests():
    """
    Agrega múltiples intereses a la base de datos.
    """
    data = request.json
    tags = data.get("tags")

    if not tags or not isinstance(tags, list):
        return error_response("Tags must be a non-empty list of strings.", 400)

    try:
        new_interests = bulk_add_interests(tags)
        return jsonify(success_response(data=new_interests, message="Interests added successfully.")), 201
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error adding interests: {e}")
        return error_response("Failed to add interests.", 500, details=str(e))

# Ruta para eliminar múltiples intereses
@interests_bp.route('/remove', methods=['DELETE'])
def remove_interests():
    """
    Elimina múltiples intereses por sus IDs.
    """
    data = request.json
    interest_ids = data.get("interest_ids")

    if not interest_ids or not isinstance(interest_ids, list):
        return error_response("Interest IDs must be a non-empty list of integers.", 400)

    try:
        deleted_interests = bulk_remove_interests(interest_ids)
        return jsonify(success_response(data=deleted_interests, message="Interests removed successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error removing interests: {e}")
        return error_response("Failed to remove interests.", 500, details=str(e))

# Ruta para actualizar los intereses de un usuario
@interests_bp.route('/user/update', methods=['POST'])
def update_user_interests():
    """
    Actualiza los intereses de un usuario.
    """
    user_id = session.get("user_id")
    if not user_id:
        return error_response("User not logged in.", 401)

    data = request.json
    new_interests = data.get("interests")

    if not new_interests or not isinstance(new_interests, list):
        return error_response("Interests must be a non-empty list of strings.", 400)

    try:
        result = update_user_interests_list(user_id, new_interests)
        return jsonify(success_response(data=result, message="User interests updated successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error updating interests for user ID {user_id}: {e}")
        return error_response("Failed to update user interests.", 500, details=str(e))



