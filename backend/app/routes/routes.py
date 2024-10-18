from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required  # Asegúrate de tener esto si usas Flask-Login

# Crear el Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')  # Cambia según tu plantilla

@main_bp.route('/about')
def about():
    return render_template('about.html')  # Cambia según tu plantilla

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')  # Cambia según tu plantilla

@main_bp.route('/register')
def register():
    return render_template('register.html')  # Cambia según tu plantilla

@main_bp.route('/login')
def login():
    return render_template('login.html')  # Cambia según tu plantilla

@main_bp.route('/logout')
@login_required  # Protege esta ruta
def logout():
    # Lógica para cerrar sesión aquí
    # Ejemplo:
    logout_user()  # Asegúrate de que logout_user esté importado
    return redirect(url_for('main.home'))  # Redirigir a la página de inicio

@main_bp.route('/profile')
@login_required  # Protege esta ruta
def profile():
    return render_template('profile.html')  # Cambia según tu plantilla

@main_bp.route('/profile/<int:user_id>')
@login_required  # Protege esta ruta
def view_profile(user_id):
    return render_template('view_profile.html', user_id=user_id)  # Cambia según tu plantilla

@main_bp.route('/chat/<int:user_id>')
@login_required  # Protege esta ruta
def chat(user_id):
    return render_template('chat.html', user_id=user_id)  # Cambia según tu plantilla

@main_bp.route('/notifications')
@login_required  # Protege esta ruta
def notifications():
    return render_template('notifications.html')  # Cambia según tu plantilla





