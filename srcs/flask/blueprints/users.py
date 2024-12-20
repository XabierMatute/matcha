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

<<<<<<< HEAD


users_bp = Blueprint('users', __name__, url_prefix='/users')
=======
users_bp = Blueprint("users", __name__, url_prefix="/users")
>>>>>>> origin/contablas

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

def generate_verification_link(email):
    """
    Generates a verification link for the given email.

    Args:
        email (str): The email address to generate the link for.

    Returns:
        str: The generated verification link.
    """
    logging.debug(f"Generating verification link for email: {email}")
    token = generate_verification_token(email)
    link = url_for('users.verify', token=token, _external=True)
    logging.debug(f"Generated verification link: {link}")
    return link

def send_verification_email(username: str, email: str):
    """
    Sends a verification email to the given email address.

    Args:
        username (str): The username of the recipient.
        email (str): The email address of the recipient.

    Raises:
        Exception: If there is an error generating the verification link or sending the email.
    """
    logging.info(f"Sending verification email to {email}")
    
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
        logging.error(f"Error generating verification link: {e}")
        raise Exception("Error generating verification link") from e
    
    try:
        msg = Message(
            subject="Verify your email",
            recipients=[email],
            html=render_template('verification_mail.html', username=username, verification_link=link, email=email)
        )
        mail = current_app.extensions['mail']
        mail.send(msg)
        logging.info(f"Verification email sent to {email}")
    except Exception as e:
        logging.error(f"Error sending verification email: {e}")
        raise Exception("Error sending verification email") from e

def generate_login_cookie(user_id):
    """
    Generates a login cookie for the given user ID.

    Args:
        user_id (int): The ID of the user to generate the cookie for.

    Returns:
        str: The generated login cookie.
    """
    logging.debug(f"Generating login cookie for user ID: {user_id}")
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    cookie = serializer.dumps(user_id, salt=app.config['SECURITY_PASSWORD_SALT'])
    logging.debug(f"Generated cookie: {cookie}")
    return cookie

@users_bp.route('/register', methods=['GET'])
def register_form():
    """
    Renders the user registration form.

    Returns:
        str: The rendered registration form template.
    """
    logging.debug("Rendering registration form")
    return render_template('register.html')
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
    logging.debug("Rendering login form")
    return render_template('login.html')

@users_bp.route('/login', methods=['POST'])
def login_user_route():
    """
    Processes login form data.

    Returns:
        Response: A redirect to the user's profile page or an error message.
    """
    data = request.form
    logging.info(f"Received login data: {data}")
    try:
        username = data['username']
        password = data['password']
        logging.info(f"Authenticating user {username}")
        user = authenticate_user(username, password)
        logging.info(f"User {user['id']} authenticated successfully.")
        if not user['is_verified']:
            logging.warning("User account not verified")
            return render_template('login.html', error_message="Account not verified. Please check your email.")
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['logged_in'] = True
        return redirect('/')
        return user
    except ValueError as e:
        logging.warning(f"ValueError during login: {e}")
        return render_template('login.html', error_message=str(e))

# @users_bp.route('/login', methods=['POST'])
# def login_user_route():
#     """
#     Processes login form data.

#     Returns:
#         Response: A redirect to the user's profile page or an error message.
#     """
#     data = request.form  # Receive form data
#     logging.info(f"Received login data: {data}")
#     try:
#         # Attempt to authenticate the user
#         username = data['username']
#         password = data['password']
#         logging.info(f"Authenticating user {username}")
#         user = authenticate_user(username, password)
#         logging.info(f"User {user['id']} authenticated successfully.")
#         session['user_id'] = user['id']  # Store user ID in session
#         return redirect(url_for('profile.profile_page'))  # Redirect to the user's profile
#     except ValueError as e:
#         logging.warning(f"ValueError during login: {e}")
#         return jsonify({"error": str(e)}), 400
#     except Exception as e:
#         logging.error(f"Exception during login: {e}")
#         return jsonify({"error": "Internal Server Error"}), 500

from itsdangerous import SignatureExpired, BadSignature

def check_verification_token(token):
    """
    Check the verification token and return the associated email if valid.

    Args:
        token (str): The verification token.

    Returns:
        str: The email associated with the token if valid, or an error message if invalid or expired.
    """
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
        logging.info("Token is valid for email: %s", email)
        return email
    except SignatureExpired:
        logging.warning("The token is expired.")
        return "The token is expired."
    except BadSignature:
        logging.warning("The token is invalid.")
        return "The token is invalid."

@users_bp.route('/verify/<token>', methods=['GET'])
def verify(token):
    """
    Verify the user account using the provided token.

    Args:
        token (str): The verification token.

    Returns:
        Response: The rendered template based on the token validation result.
    """
    email = check_verification_token(token)
    if email == "The token is expired.":
        logging.info("Rendering expired_token.html for expired token.")
        return render_template('expired_token.html') # TODO: Create template and add link to resend email
    elif email == "The token is invalid.":
        logging.info("Rendering invalid_token.html for invalid token.")
        return render_template('invalid_token.html') # TODO: Create template
    else:
        validate_user(email)
        logging.info("User validated for email: %s", email)
        return render_template('verified.html')

@users_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

from manager.user_manager import get_user_by_username

@users_bp.route('/account/<username>', methods=['GET'])
def account(username):
    if session.get('logged_in'):
        if session.get('username') == username:
            user = get_user_by_username(username)
            return render_template('content.html', content=user)
            return render_template('account.html', user=user)
        else:
            return redirect(url_for('users.account', username=session.get('username')))
    else:
        return redirect('/login')
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
