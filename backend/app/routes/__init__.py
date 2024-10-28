from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from .routes import *  # Importar las rutas definidas en routes.py

def register_auth(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Asegúrate de usar auth_bp


