from flask import Blueprint

# Crear el Blueprint para el módulo de autenticación
auth_bp = Blueprint('auth', __name__)

# Importar las rutas de auth.py
from . import auth_routes  # Asegúrate de que el archivo se llame auth_routes.py

