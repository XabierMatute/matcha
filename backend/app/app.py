from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
import os
from app.auth import auth_bp  # Ajusta según la estructura de tus carpetas
from app.database import init_db, db
from app.models import User
from app.routes import *  # Asegúrate de que tus rutas están definidas correctamente

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos y otros parámetros
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/database_name')
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

if __name__ == "__main__":
    app.run(debug=True)  # Cambia a False en producción










