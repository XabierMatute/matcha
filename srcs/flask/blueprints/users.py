from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from manager.user_manager import register_user, authenticate_user, get_user_details, delete_user_account
import logging
from config import DEBUG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

users_bp = Blueprint('users', __name__, url_prefix='/users')

def generate_verification_token(email):
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def generate_verification_link(email):
    token = generate_verification_token(email)
    return url_for('users.verify', token=token, _external=True)

def send_verification_email(username: str, email: str):
    try:
        link = generate_verification_link(email)
        msg = Message(
            subject="Verify your email",
            recipients=[email],
            html=render_template('verification_mail.html', username=username, verification_link=link)
        )
        mail = current_app.extensions['mail']
        mail.send(msg)
        logger.info(f"Verification email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send verification email: {e}")
        raise Exception("Error sending verification email") from e

@users_bp.route('/register', methods=['POST'])
def register_user_route():
    data = request.get_json()
    try:
        user = register_user(data)
        send_verification_email(user['username'], user['email'])
        return jsonify({"success": True, "message": "User registered successfully.", "user": user}), 201
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        user = authenticate_user(data['username'], data['password'])
        session['user_id'] = user['id']
        return jsonify({"success": True, "message": "Login successful.", "user": user}), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

@users_bp.route('/verify/<token>', methods=['GET'])
def verify_user(token):
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
        get_user_details(email=email)  # Simulate email validation logic
        return render_template('verified.html')
    except SignatureExpired:
        return render_template('expired_token.html')
    except BadSignature:
        return render_template('invalid_token.html')

@users_bp.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."}), 200

@users_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = delete_user_account(user_id)
        return jsonify({"success": True, "message": "User deleted successfully.", "user": user}), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

        return jsonify({"success": False, "message": "Failed to generate users.", "details": str(e)}), 500
