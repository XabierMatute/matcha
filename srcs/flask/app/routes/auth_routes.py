from flask import render_template, redirect, url_for, flash, request, Blueprint, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import os
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import logging
import psycopg

# Configurar el logger
logging.basicConfig(level=logging.INFO)

# Funciones para token
def generate_confirmation_token(email, secret_key):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))

def confirm_token(token, secret_key, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(token, salt=os.getenv('SECURITY_PASSWORD_SALT'), max_age=expiration)
    except Exception as e:
        logging.error(f"Error confirming token: {e}")
        return False
    return email

# Función para enviar correos
def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=os.getenv('MAIL_USERNAME'))
    try:
        mail.send(msg)
        logging.info(f'Email sent to {to}')
    except Exception as e:
        logging.error(f"Failed to send email to {to}: {e}")

# Crear el Blueprint
auth_bp = Blueprint('auth', __name__)

# Rutas de autenticación

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Verificar si el correo o el nombre de usuario ya existen en la base de datos
        connection = g.get('db_connection', None)
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (email, username))
                user = cursor.fetchone()
                if user:
                    flash('El correo o nombre de usuario ya están en uso.', 'danger')
                    return redirect(url_for('auth.register'))

        # Hash de la contraseña antes de almacenarla
        hashed_password = generate_password_hash(password)

        # Crear el usuario con la contraseña hasheada
        connection = g.get('db_connection', None)
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                        (email, username, hashed_password)
                    )
                    connection.commit()
                    
                    # Generar token de confirmación y enviar correo
                    token = generate_confirmation_token(email, os.getenv('SECRET_KEY'))
                    send_email(email, 'Confirm Your Account', 
                               f'Click the link to confirm your account: {url_for("auth.confirm_email", token=token, _external=True)}')
                    flash('A confirmation email has been sent to your email address.', 'success')
                    return redirect(url_for('auth.login'))
            except Exception as e:
                connection.rollback()
                logging.error(f"Error registering user: {e}")
                flash('An error occurred while registering the user. Please try again.', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token, os.getenv('SECRET_KEY'))
    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))

    # Activar el usuario
    connection = g.get('db_connection', None)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                if user[3]:  # Suponiendo que el estado activo está en el índice 3
                    flash('The account has already been confirmed. Please log in.', 'success')
                else:
                    cursor.execute("UPDATE users SET is_active = %s WHERE email = %s", (True, email))
                    connection.commit()
                    flash('You have confirmed your account. Thank you!', 'success')

    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar el usuario y la contraseña
        connection = g.get('db_connection', None)
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                if user and check_password_hash(user[2], password):  # Verificar la contraseña utilizando hash
                    if user[3]:  # Suponiendo que el campo 'is_active' está en el índice 3
                        login_user(user)
                        flash('You have logged in successfully.', 'success')
                        return redirect(url_for('main.home'))
                    else:
                        flash('Account not activated. Check your email.', 'danger')
                else:
                    flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Registrar las rutas en el Blueprint
def register_auth(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')






