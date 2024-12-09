from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, current_app
from manager.user_manager import register_user, authenticate_user, get_user_details
from flask_mail import Message

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Función para enviar el correo de verificación
def send_verification_email(user):
    """
    Envía un correo de verificación al usuario después de registrarse.
    """
    verification_link = url_for('users.verify_email', token=user.verification_token, _external=True)
    
    
    msg = Message('Verificación de Correo',
                  recipients=[user.email])
    msg.body = f'Por favor, haz clic en el siguiente enlace para verificar tu correo: {verification_link}'
    try:
        # Usa `current_app` para acceder a la instancia de Mail
        mail = current_app.extensions['mail']
        mail.send(msg)
    except Exception as e:
        raise ValueError(f"Error al enviar el correo: {str(e)}")

# Página de registro: Muestra el formulario
@users_bp.route('/register', methods=['GET'])
def register_form():
    """
    Muestra el formulario de registro.
    """
    return render_template('register.html')

# Manejo del registro de usuario
@users_bp.route('/register', methods=['POST'])
def register_user_route():
    """
    Procesa los datos enviados por el formulario de registro.
    """
    data = request.form  # Recibe datos del formulario
    try:
        user = register_user(data)  # Intenta registrar al usuario
        send_verification_email(user)  # Enviar correo de verificación
        return redirect(url_for('users.login_form'))  # Redirige al login
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

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



