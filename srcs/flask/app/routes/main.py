from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import get_user_by_id  # Asegúrate de tener esta función definida para obtener usuarios de la base de datos

# Crear el Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('main/home.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@main_bp.route('/profile')
@login_required
def profile():
    # Pasamos el usuario logueado a la plantilla para mostrar su información
    return render_template('main/profile.html', user=current_user)

@main_bp.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    # Aquí obtienes al usuario por su ID
    user = get_user_by_id(user_id)  # Asumiendo que tienes esta función que consulta la base de datos
    if user is None:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('main.home'))  # Redirigir a la página de inicio si el usuario no existe
    return render_template('main/view_profile.html', user=user)

@main_bp.route('/chat/<int:user_id>')
@login_required
def chat(user_id):
    # Pasamos el ID del usuario a la plantilla para establecer la conversación
    return render_template('main/chat.html', user_id=user_id)

@main_bp.route('/notifications')
@login_required
def notifications():
    # Aquí podrías pasar las notificaciones del usuario si las tienes en la base de datos
    return render_template('main/notifications.html')

