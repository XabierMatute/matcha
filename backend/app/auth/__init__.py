from flask import Blueprint

# Crear el Blueprint para el módulo de autenticación
auth_bp = Blueprint('auth', __name__)

# Importar las rutas de auth_routes
from .auth_routes import *  # Asegúrate de que el archivo se llame auth_routes.py

# Función para registrar las rutas en la aplicación
def register_auth(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')


