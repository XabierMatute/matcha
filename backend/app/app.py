from flask import Flask, render_template  # Asegúrate de importar render_template si lo necesitas
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
import os
from app.auth import auth_bp
from app.database import init_db, db
from app.models import User, Interest, Picture, ProfileView, Like, Notification, Chat
from app.routes import main_bp

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos y otros parámetros
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/matcha.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# Inicializar la base de datos y migraciones
init_db(app)
migrate = Migrate(app, db)

# Inicializar LoginManager
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrar el blueprint de autenticación
app.register_blueprint(auth_bp, url_prefix='/auth')

# # Definir la ruta para el home
# @app.route('/')
# def home():
#     return "¡Finally Welcome to your MatchaXabi !"

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True)












