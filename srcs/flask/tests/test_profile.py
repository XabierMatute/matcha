import pytest
from flask import Flask, session
from flask.testing import FlaskClient
from blueprints.profile import profile_bp
from unittest.mock import patch

# Configuración básica de prueba para Flask
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.secret_key = 'una_clave_secreta_segura'  # Clave necesaria para la sesión
    app.register_blueprint(profile_bp)
    return app

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def authenticated_user(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Simula un usuario autenticado

# Test: Obtener el perfil del usuario autenticado
def test_get_my_profile(client, authenticated_user):
    with patch('manager.profile_manager.get_user_profile', return_value={"id": 1, "username": "test_user", "biography": "Hello, world!"}):
        response = client.get('/profile/')
        assert response.status_code == 200
        assert response.json['username'] == "test_user"

# Test: Actualizar el perfil básico
def test_update_my_profile(client, authenticated_user):
    with patch('manager.profile_manager.update_user_profile', return_value={"id": 1, "biography": "New bio"}):
        response = client.post('/profile/update', json={"biography": "New bio"})
        assert response.status_code == 200
        assert response.json['biography'] == "New bio"

# Test: Actualizar la ubicación del usuario
def test_update_my_location(client, authenticated_user):
    with patch('manager.profile_manager.update_user_location', return_value={
        "id": 1,
        "location": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060
    }):
        response = client.post('/profile/location/update', json={
            "location": "New York",
            "latitude": 40.7128,
            "longitude": -74.0060
        })
        assert response.status_code == 200
        assert response.json['location'] == "New York"

# Test: Manejar datos malformados en ubicación
def test_update_location_invalid_data(client, authenticated_user):
    response = client.post('/profile/location/update', json={
        "location": "New York"
    })
    assert response.status_code == 400
    assert "error" in response.json

# Test: Obtener intereses del usuario
def test_get_interests(client, authenticated_user):
    with patch('manager.interests_manager.get_user_interests', return_value=["reading", "coding", "traveling"]):
        response = client.get('/profile/interests')
        assert response.status_code == 200
        assert response.json == ["reading", "coding", "traveling"]

# Test: Actualizar intereses del usuario
def test_update_interests(client, authenticated_user):
    with patch('manager.interests_manager.update_user_interests', return_value=["gaming", "music"]):
        response = client.post('/profile/interests/update', json={"interests": ["gaming", "music"]})
        assert response.status_code == 200
        assert response.json == ["gaming", "music"]


