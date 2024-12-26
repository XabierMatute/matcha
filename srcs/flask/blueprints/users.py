from faker import Faker
from flask import Blueprint, request, jsonify
from manager.user_manager import (
    fetch_user_by_id,
    fetch_user_by_username,
    fetch_user_by_email,
    verify_user,
    register_new_user,
    modify_user,
    remove_user,
    get_user_details
)
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

users_bp = Blueprint("users", __name__, url_prefix="/users")

def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code

# Ruta para obtener detalles de usuario por ID o nombre de usuario
@users_bp.route('/details', methods=['GET'])
def get_user_details_route():
    """
    Obtiene detalles de usuario por ID o nombre de usuario.
    Parámetros de consulta: ?user_id=<id> o ?username=<username>
    """
    user_id = request.args.get("user_id", type=int)
    username = request.args.get("username", type=str)

    try:
        if user_id:
            user = get_user_details(user_id, require_verified=True)
        elif username:
            user = get_user_details(username, require_verified=True)
        else:
            return error_response("Either 'user_id' or 'username' must be provided.", 400)

        if not user:
            return error_response("User not found.", 404)
        return jsonify(success_response(data=user, message="User details fetched successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error fetching user details: {e}")
        return error_response("Failed to fetch user details.", 500, details=str(e))

# Ruta para registrar un nuevo usuario
@users_bp.route('/register', methods=['POST'])
def register_user():
    """
    Crea un nuevo usuario.
    JSON Payload: { "username": "...", "email": "...", "password_hash": "...", "first_name": "...", "last_name": "..." }
    """
    data = request.json
    try:
        username = data.get("username")
        email = data.get("email")
        password_hash = data.get("password_hash")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if not username or not email or not password_hash:
            return error_response("Username, email, and password_hash are required.", 400)

        new_user = register_new_user(username, email, password_hash, first_name, last_name)
        return jsonify(success_response(data=new_user, message="User registered successfully.")), 201
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return error_response("Failed to register user.", 500, details=str(e))

# Ruta para actualizar un usuario
@users_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Actualiza la información de un usuario.
    JSON Payload: { "username": "...", "email": "...", "first_name": "...", "last_name": "..." }
    """
    data = request.json
    try:
        updated_user = modify_user(
            user_id,
            data.get("username"),
            data.get("email"),
            data.get("first_name"),
            data.get("last_name")
        )
        return jsonify(success_response(data=updated_user, message="User updated successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error updating user with ID {user_id}: {e}")
        return error_response("Failed to update user.", 500, details=str(e))

# Ruta para eliminar un usuario
@users_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Elimina un usuario por su ID.
    """
    try:
        deleted_user = remove_user(user_id)
        return jsonify(success_response(data=deleted_user, message="User deleted successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}")
        return error_response("Failed to delete user.", 500, details=str(e))

# Ruta para verificar un usuario por email
@users_bp.route('/verify', methods=['POST'])
def verify_user_email():
    """
    Verifica un usuario por su email.
    JSON Payload: { "email": "..." }
    """
    data = request.json
    try:
        email = data.get("email")
        if not email:
            return error_response("Email is required.", 400)

        verified_user = verify_user(email)
        return jsonify(success_response(data=verified_user, message="User verified successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Error verifying user with email '{email}': {e}")
        return error_response("Failed to verify user.", 500, details=str(e))

@users_bp.route('/generate_example_data', methods=['POST'])
def generate_example_data():
    try:
        example_user = {
            "username": "exampleuser",
            "email": "example@example.com",
            "password_hash": "examplepassword",
            "first_name": "Example",
            "last_name": "User"
        }
        register_new_user(
            example_user["username"],
            example_user["email"],
            example_user["password_hash"],
            example_user["first_name"],
            example_user["last_name"]
        )
        return jsonify({"success": True, "message": "Example user generated."}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@users_bp.route('/generate_fake_users', methods=['POST'])
def generate_fake_users():
    """
    Genera 10 usuarios ficticios y los inserta en la base de datos.
    """
    fake = Faker()
    created_users = []
    
    try:
        for _ in range(10):
            username = fake.user_name()
            email = fake.email()
            password_hash = fake.password()  # Genera un hash ficticio
            first_name = fake.first_name()
            last_name = fake.last_name()

            # Inserta el usuario en la base de datos
            new_user = register_new_user(
                username=username,
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name
            )
            created_users.append(new_user)
        
        return jsonify({"success": True, "message": "10 fake users generated.", "users": created_users}), 201
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to generate users.", "details": str(e)}), 500