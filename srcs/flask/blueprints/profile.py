from flask import Blueprint, request, jsonify, session, current_app
from manager.profile_manager import (
    get_user_profile,
    update_user_profile,
    get_user_location,
    update_user_location
)
from manager.interests_manager import get_user_interests, update_user_interests
from manager.pictures_manager import upload_picture, fetch_user_pictures


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

# Ruta para obtener el perfil completo
@profile_bp.route('/', methods=['GET'])
def get_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    try:
        profile_data = get_user_profile(user_id)
        return jsonify(profile_data), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching profile for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to fetch user profile."}), 500

# Ruta para actualizar el perfil básico
@profile_bp.route('/update', methods=['POST'])
def update_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    data = request.json
    try:
        updated_profile = update_user_profile(user_id, data)
        return jsonify(updated_profile), 200
    except Exception as e:
        current_app.logger.error(f"Error updating profile for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to update user profile."}), 500

# Ruta para obtener todas las fotos del usuario
@profile_bp.route('/pictures', methods=['GET'])
def get_pictures():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    try:
        pictures = get_user_pictures(user_id)
        return jsonify(pictures), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching pictures for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to fetch user pictures."}), 500

# Ruta para agregar una foto de perfil
@profile_bp.route('/pictures/add', methods=['POST'])
def add_picture():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    picture_file = request.files.get('picture')
    if not picture_file:
        return jsonify({"error": "No picture file provided."}), 400

    try:
        picture_info = add_profile_picture(user_id, picture_file)
        return jsonify(picture_info), 200
    except Exception as e:
        current_app.logger.error(f"Error adding picture for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to add picture."}), 500

# Ruta para obtener la ubicación
@profile_bp.route('/location', methods=['GET'])
def get_location_data():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    try:
        location = get_user_location(user_id)
        return jsonify(location), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching location for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to fetch user location."}), 500

# Ruta para actualizar la ubicación
@profile_bp.route('/location/update', methods=['POST'])
def update_location_data():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    data = request.json
    location = data.get('location')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not location or latitude is None or longitude is None:
        return jsonify({"error": "Missing location data."}), 400

    try:
        updated_location = update_user_location(user_id, location, latitude, longitude)
        return jsonify(updated_location), 200
    except Exception as e:
        current_app.logger.error(f"Error updating location for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to update user location."}), 500

# Ruta para obtener los intereses
@profile_bp.route('/interests', methods=['GET'])
def get_interests():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    try:
        interests = get_user_interests(user_id)
        return jsonify(interests), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching interests for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to fetch user interests."}), 500

# Ruta para actualizar los intereses
@profile_bp.route('/interests/update', methods=['POST'])
def update_interests():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401

    data = request.json
    interests = data.get('interests')

    if not interests or not isinstance(interests, list):
        return jsonify({"error": "Invalid interests data."}), 400

    try:
        updated_interests = update_user_interests(user_id, interests)
        return jsonify(updated_interests), 200
    except Exception as e:
        current_app.logger.error(f"Error updating interests for user ID {user_id}: {e}")
        return jsonify({"error": "Failed to update user interests."}), 500


