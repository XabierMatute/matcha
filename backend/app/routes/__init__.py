from app.auth.auth_routes import register_auth


def create_app():
    app = Flask(__name__)
    # Otras configuraciones...

    register_auth(app)  # Asegúrate de que esto se llame después de inicializar app

    return app
