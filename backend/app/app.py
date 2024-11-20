import os
from flask import Flask
from flask_login import LoginManager
from app.auth import auth_bp
from app.routes import main_bp
import psycopg

# Crear la app
app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# Inicializar LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Definir la ruta de login

@login_manager.user_loader
def load_user(user_id):
    """Función de carga de usuario para Flask-Login"""
    conn = app.config.get('DB_CONNECTION')  # Usando una conexión configurada en __init__.py
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    if user:
        return User(id=user[0], email=user[1], username=user[2], first_name=user[3], last_name=user[4])
    return None

# Registrar el blueprint de autenticación y de rutas principales
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)  # Ruta principal de la aplicación

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True)


