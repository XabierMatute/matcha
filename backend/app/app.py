import os
from flask import Flask
from flask_login import LoginManager
from app.auth import auth_bp
from dotenv import load_dotenv
from app.models import User, Interest, Picture, ProfileView, Like, Notification, Chat  # Asegúrate de que estos modelos estén configurados adecuadamente
from app.routes import main_bp
import psycopg

# Cargar las variables de entorno
load_dotenv()

# Crear la app
app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# Función para obtener la conexión a la base de datos utilizando psycopg3
def get_db_connection():
    conn = psycopg.connect(os.getenv('DATABASE_URL'))  # Aquí se usa la URL de la base de datos desde el .env
    return conn

# Inicializar LoginManager
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # Obtener el usuario directamente con psycopg3
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    conn.close()
    
    if user:
        return User(id=user[0], email=user[1], username=user[2], first_name=user[3], last_name=user[4])  # Asegúrate de que estos sean los campos correctos
    return None

# Registrar el blueprint de autenticación
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)  # Asegúrate de registrar el blueprint de 'main'

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True)
