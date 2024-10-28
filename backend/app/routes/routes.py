from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user  

# Crear el Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('main/home.html')  # Asegúrate de que la plantilla existe

@main_bp.route('/about')
def about():
    return render_template('main/about.html')  # Asegúrate de que la plantilla existe

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')  # Asegúrate de que la plantilla existe

@main_bp.route('/register')
def register():
    return render_template('auth/register.html')  # Asegúrate de que la plantilla existe

@main_bp.route('/login')  
def login():
    return render_template('auth/login.html')  # Asegúrate de que la plantilla existe

@main_bp.route('/logout')
@login_required  
def logout():
    logout_user()  
    return redirect(url_for('main.home'))  # Redirigir a la página de inicio después de cerrar sesión

@main_bp.route('/profile')
@login_required  
def profile():
    return render_template('main/profile.html')  # Asegúrate de que la plantilla existe

@main_bp.route('/profile/<int:user_id>')
@login_required  
def view_profile(user_id):
    return render_template('main/view_profile.html', user_id=user_id)  # Asegúrate de que la plantilla existe

@main_bp.route('/chat/<int:user_id>')
@login_required  
def chat(user_id):
    return render_template('main/chat.html', user_id=user_id)  # Asegúrate de que la plantilla existe

@main_bp.route('/notifications')
@login_required  
def notifications():
    return render_template('main/notifications.html')  # Asegúrate de que la plantilla existe






