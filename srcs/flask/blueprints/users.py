from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, current_app
from manager.user_manager import register_user, authenticate_user, get_user_details
from flask_mail import Message
from config import DEBUG
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

users_bp = Blueprint('users', __name__, url_prefix='/users')

def generate_verification_token(email):
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def generate_verification_link(email):
    token = generate_verification_token(email)
    return url_for('test_user.verify', token=token, _external=True)

def send_verification_email(username: str, email: str):
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
    except Exception as e:
        logging.error(f"Error sending verification email: {e}")
        raise Exception("Error sending verification email") from e

@users_bp.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')


# Manejo del registro de usuario
@users_bp.route('/register', methods=['POST'])
def register_user_route():
    data = request.form
    logging.info(f"Received registration data: {data}")
    try:
        register_user(data)
        logging.info(f"User {data['username']} registered successfully.")
        send_verification_email(data["username"], data["email"])
        logging.info(f"Verification email sent to {data['email']}")
        return render_template('registered.html')
    except ValueError as e:
        return render_template('register.html', error_message=str(e))
    except Exception as e:
        return render_template('register.html', error_message=f"Internal Server Error {str(e)}")


# Página de inicio de sesión: Muestra el formulario
@users_bp.route('/login', methods=['GET'])
def login_form():
    """
    Muestra el formulario de inicio de sesión.
    """
    return render_template('login.html')

# Manejo del inicio de sesión
@users_bp.route('/login', methods=['POST'])
def login_user_route():
    """
    Procesa los datos enviados por el formulario de inicio de sesión.
    """
    data = request.form  # Recibe datos del formulario
    try:
        # Intenta autenticar al usuario
        user = authenticate_user(data)
        session['user_id'] = user.id  # Guarda el ID del usuario en la sesión
        return redirect(url_for('profile.profile_page'))  # Redirige al perfil del usuario
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500



