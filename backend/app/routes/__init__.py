# app/routes/__init__.py

from .main import main_bp  # Importar el Blueprint desde main.py
from .auth import auth_bp  # Importar el Blueprint desde auth.py

# Registrar los Blueprints en la aplicación Flask
def register_routes(app):
    app.register_blueprint(main_bp)  # Registrar las rutas principales
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Registrar las rutas de autenticación






