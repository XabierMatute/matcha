from flask import Blueprint, request, jsonify
from manager.interests_manager import (
    get_all_interests,
    add_new_interest,
    add_multiple_interests,
    remove_interests_by_ids,
    get_interest_by_id
)

# Definimos el Blueprint con el nombre "interests"
interests_bp = Blueprint('interests', __name__, url_prefix='/interests')

def error_response(message, status_code=500, details=None):
    """Genera una respuesta de error consistente."""
    response = {'error': message}
    if details:
        response['details'] = details
    return jsonify(response), status_code

@interests_bp.route('/', methods=['GET'])
def get_interests():
    """Obtiene todos los intereses disponibles."""
    try:
        interests = get_all_interests()
        return jsonify(interests), 200
    except Exception as e:
        return error_response('Failed to fetch interests', details=str(e))

@interests_bp.route('/<int:interest_id>', methods=['GET'])
def get_interest(interest_id):
    """Obtiene un interés por su ID."""
    try:
        interest = get_interest_by_id(interest_id)
        if interest:
            return jsonify(interest), 200
        return error_response('Interest not found', status_code=404)
    except Exception as e:
        return error_response('Failed to fetch interest', details=str(e))

@interests_bp.route('/', methods=['POST'])
def create_interest():
    """Crea un nuevo interés."""
    try:
        data = request.get_json()
        if not data or not data.get('tag'):
            return error_response('Tag is required', status_code=400)
        
        new_interest = add_new_interest(data['tag'])
        return jsonify(new_interest), 201
    except ValueError as e:
        return error_response(str(e), status_code=400)
    except Exception as e:
        return error_response('Failed to create interest', details=str(e))

@interests_bp.route('/batch', methods=['POST'])
def batch_add_interests():
    """Agrega múltiples intereses."""
    try:
        data = request.get_json()
        if not data or not data.get('tags'):
            return error_response('Tags are required', status_code=400)
        
        added_interests = add_multiple_interests(data['tags'])
        return jsonify(added_interests), 201
    except ValueError as e:
        return error_response(str(e), status_code=400)
    except Exception as e:
        return error_response('Failed to add interests', details=str(e))

@interests_bp.route('/<int:interest_id>', methods=['DELETE'])
def delete_interest(interest_id):
    """Elimina un interés por su ID."""
    try:
        if not get_interest_by_id(interest_id):
            return error_response('Interest not found', status_code=404)

        result = remove_interests_by_ids([interest_id])
        return jsonify({'message': result}), 200
    except ValueError as e:
        return error_response(str(e), status_code=400)
    except Exception as e:
        return error_response('Failed to delete interest', details=str(e))


