from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import logging

from manager.user_manager import register_user, authenticate_user, get_user_details
from config import DEBUG

from models.user_model import validate_user

users_bp = Blueprint('users', __name__, url_prefix='/users')

def generate_verification_token(email):
    """
    Generates a verification token for the given email.

    Args:
        email (str): The email address to generate the token for.

    Returns:
        str: The generated verification token.
    """
    logging.debug(f"Generating verification token for email: {email}")
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
    logging.debug(f"Generated token: {token}")
    return token

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
        link = generate_verification_link(email)
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

@users_bp.route('/register', methods=['POST'])
def register_user_route():
    """
    Handles user registration.

    Returns:
        str: The rendered template after registration.
    """
    data = request.form
    logging.info(f"Received registration data: {data}")
    try:
        register_user(data)
        logging.info(f"User {data['username']} registered successfully.")
        send_verification_email(data["username"], data["email"])
        logging.info(f"Verification email sent to {data['email']}")
        return render_template('registered.html')
    except ValueError as e:
        logging.warning(f"ValueError during registration: {e}")
        return render_template('register.html', error_message=str(e))
    except Exception as e:
        logging.error(f"Exception during registration: {e}")
        return render_template('register.html', error_message=f"Internal Server Error {str(e)}")

@users_bp.route('/login', methods=['GET'])
def login_form():
    """
    Renders the login form.

    Returns:
        str: The rendered login form template.
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
            # return render_template('content.html', content=user)
            return render_template('account.html', user=user)
        else:
            return redirect(url_for('users.account', username=session.get('username')))
    else:
        return redirect('/login')











def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code

from flask import Blueprint, request, jsonify

logger = logging.getLogger(__name__)

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
