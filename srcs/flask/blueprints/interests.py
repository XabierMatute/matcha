from flask import Blueprint, request, jsonify
from models.interests_model import (
    create_interests,
    list_interests,
    get_interests_by_id,
    add_interests,
    remove_interests,
)

# Definimos el Blueprint con el nombre "interests"
interests_bp = Blueprint('interests', __name__, url_prefix='/interests')

@interests_bp.route('/', methods=['GET'])
def get_all_interests():
    """Obtiene todos los intereses disponibles."""
    try:
        interests = list_interests()
        return jsonify(interests), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interests_bp.route('/<int:interest_id>', methods=['GET'])
def get_interest(interest_id):
    """Obtiene un interés por su ID."""
    try:
        interest = get_interests_by_id(interest_id)
        if interest:
            return jsonify(interest), 200
        else:
            return jsonify({'error': 'Interest not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interests_bp.route('/', methods=['POST'])
def create_interest():
    """Crea un nuevo interés."""
    try:
        data = request.get_json()
        tag = data.get('tag')
        if not tag:
            return jsonify({'error': 'Tag is required'}), 400
        new_interest = create_interests(tag)
        return jsonify(new_interest), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interests_bp.route('/batch', methods=['POST'])
def batch_add_interests():
    """Agrega múltiples intereses."""
    try:
        data = request.get_json()
        tags = data.get('tags', [])
        if not tags:
            return jsonify({'error': 'Tags are required'}), 400
        added_interests = add_interests(tags)
        return jsonify(added_interests), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interests_bp.route('/<int:interest_id>', methods=['DELETE'])
def delete_interest(interest_id):
    """Elimina un interés por su ID."""
    try:
        result = remove_interests([interest_id])
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



