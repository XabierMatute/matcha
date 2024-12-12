from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import logging

from manager.user_manager import register_user, authenticate_user, get_user_details
from config import DEBUG

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
    link = url_for('test_user.verify', token=token, _external=True)
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
    data = request.form  # Receive form data
    logging.info(f"Received login data: {data}")
    try:
        # Attempt to authenticate the user
        user = authenticate_user(data)
        session['user_id'] = user.id  # Save the user's ID in the session
        logging.info(f"User {user.id} authenticated successfully.")
        return redirect(url_for('profile.profile_page'))  # Redirect to the user's profile
    except ValueError as e:
        logging.warning(f"ValueError during login: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Exception during login: {e}")
        return jsonify({"error": "Internal Server Error"}), 500