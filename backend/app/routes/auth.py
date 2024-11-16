# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from ..models import User  # Importación corregida desde models.py en el directorio superior

# Crear el Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Verificar si el correo o el nombre de usuario ya están registrados
        if User.user_exists(email=email) or User.user_exists(username=username):
            flash('El correo o el nombre de usuario ya están en uso.', 'danger')
            return redirect(url_for('auth.register'))

        # Lógica para registrar el usuario (sin ORM, usando psycopg)
        User.create_user(email, username, password)
        flash('Te has registrado correctamente. Revisa tu correo para confirmar tu cuenta.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar si el usuario existe
        user = User.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Credenciales incorrectas', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('main.home'))



