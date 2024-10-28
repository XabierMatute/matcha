from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import db, mail
from app.models import User
from app.forms import RegistrationForm, LoginForm
from flask_mail import Message
import os
from itsdangerous import URLSafeTimedSerializer
import logging

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
def register_routes(auth_bp):
    @auth_bp.route('/')
    def home():
        return "Welcome to Matcha!"

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.username.data).first():
                flash('El correo o nombre de usuario ya están en uso.', 'danger')
                return redirect(url_for('auth.register'))

            user = User(
                email=form.email.data,
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                token = generate_confirmation_token(user.email, os.getenv('SECRET_KEY'))
                send_email(user.email, 'Confirm Your Account', 
                           f'Click the link to confirm your account: {url_for("auth.confirm_email", token=token, _external=True)}')
                flash('A confirmation email has been sent to your email address.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error registering user: {e}")
                flash('An error occurred while registering the user. Please try again.', 'danger')

        return render_template('auth/register.html', form=form)

    @auth_bp.route('/confirm/<token>')
    def confirm_email(token):
        email = confirm_token(token, os.getenv('SECRET_KEY'))
        if not email:
            flash('The confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first_or_404()
        if user.is_active:
            flash('The account has already been confirmed. Please log in.', 'success')
        else:
            user.is_active = True
            db.session.commit()
            flash('You have confirmed your account. Thank you!', 'success')
        
        return redirect(url_for('auth.login'))

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                if user.is_active:
                    login_user(user)
                    flash('You have logged in successfully.', 'success')
                    return redirect(url_for('auth.profile'))  
                else:
                    flash('Account not activated. Check your email.', 'danger')
            else:
                flash('Invalid username or password.', 'danger')
        return render_template('auth/login.html', form=form)

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
    register_routes(auth_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')



