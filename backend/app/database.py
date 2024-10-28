from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask App
app = Flask(__name__)

# Cargar la configuración según el entorno
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Extensiones de Flask
db = SQLAlchemy(app)  # Inicializa SQLAlchemy
migrate = Migrate(app, db)  # Inicializa Flask-Migrate

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Define la vista de inicio de sesión

mail = Mail(app)
csrf = CSRFProtect(app)

# Función para inicializar la base de datos
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea todas las tablas

# Importar rutas y modelos
from app import routes, models  # Mover al final para evitar importación circular




