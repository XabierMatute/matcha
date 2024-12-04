from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import create_user, get_user_by_username
from flask_mail import Message
# from yourapp import mail  # Importa la instancia de Flask-Mail configurada

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Página de registro: Muestra el formulario
@users_bp.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')  # Renderiza el formulario de registro

# Manejo del formulario de registro: Procesa los datos enviados por el usuario
@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.form  # Recibe datos del formulario como un diccionario
    required_fields = ['email', 'username', 'first_name', 'last_name', 'password', 'birthdate']
    
    # Validar campos requeridos
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Validar formato de correo electrónico
    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400

    # Validar longitud mínima de la contraseña
    if len(data['password']) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    # Hash de contraseña
    password_hash = generate_password_hash(data['password'])

    # Crear usuario
    try:
        user = create_user(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            birthdate=data['birthdate'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        # Enviar correo de verificación
        send_verification_email(user)
        return redirect(url_for('users.login_form'))  # Redirige al formulario de login
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Página de inicio de sesión: Muestra el formulario
@users_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')  # Renderiza el formulario de login

# Manejo del formulario de inicio de sesión: Procesa los datos
@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.form  # Recibe datos del formulario
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    user = get_user_by_username(data['username'])
    if not user or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.get('is_verified', False):
        return jsonify({"error": "Account not verified. Check your email."}), 403

    session['user_id'] = user['id']  # Inicia sesión
    return redirect(url_for('users.profile'))  # Redirige al perfil

# Enviar correo de verificación
def send_verification_email(user):
    token = "generated_token"  # Aquí generas un token real, como JWT o UUID
    verify_url = f"http://localhost:5000/users/verify_email/{token}"
    msg = Message(
        "Verify your email",
        sender="noreply@matcha.com",
        recipients=[user['email']]
    )
    msg.body = f"Click the link to verify your email: {verify_url}"
    mail.send(msg)

