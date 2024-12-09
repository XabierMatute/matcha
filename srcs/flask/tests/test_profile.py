import pytest
from flask import Flask
from flask.testing import FlaskClient
from blueprints.profile import profile_bp

# Configuración básica de prueba para Flask
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(profile_bp)
    return app

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def authenticated_user(monkeypatch):
    monkeypatch.setattr('flask.session', {'user_id': 1})  # Simula un usuario autenticado

# Test: Obtener el perfil del usuario autenticado
def test_get_my_profile(client, monkeypatch):
    def mock_get_user_profile(user_id):
        return {"id": 1, "username": "test_user", "biography": "Hello, world!"}
    monkeypatch.setattr('manager.profile_manager.get_user_profile', mock_get_user_profile)

    response = client.get('/profile/')
    assert response.status_code == 200
    assert response.json['username'] == "test_user"

# Test: Actualizar el perfil básico
def test_update_my_profile(client, monkeypatch):
    def mock_update_user_profile(user_id, data):
        return {"id": 1, "biography": data.get("biography", "Default bio")}
    monkeypatch.setattr('manager.profile_manager.update_user_profile', mock_update_user_profile)

    response = client.post('/profile/update', json={"biography": "New bio"})
    assert response.status_code == 200
    assert response.json['biography'] == "New bio"

# Test: Actualizar la ubicación del usuario
def test_update_my_location(client, monkeypatch):
    def mock_update_user_location(user_id, location, latitude, longitude):
        return {"id": 1, "location": location, "latitude": latitude, "longitude": longitude}
    monkeypatch.setattr('manager.profile_manager.update_user_location', mock_update_user_location)

    response = client.post('/profile/location/update', json={
        "location": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060
    })
    assert response.status_code == 200
    assert response.json['location'] == "New York"

# Test: Manejar datos malformados en ubicación
def test_update_location_invalid_data(client):
    response = client.post('/profile/location/update', json={
        "location": "New York"
    })
    assert response.status_code == 400
    assert "error" in response.json

# Test: Obtener intereses del usuario
def test_get_interests(client, monkeypatch):
    def mock_get_user_interests(user_id):
        return ["reading", "coding", "traveling"]
    monkeypatch.setattr('manager.interests_manager.get_user_interests', mock_get_user_interests)

    response = client.get('/profile/interests')
    assert response.status_code == 200
    assert response.json == ["reading", "coding", "traveling"]

# Test: Actualizar intereses del usuario
def test_update_interests(client, monkeypatch):
    def mock_update_user_interests(user_id, interests):
        return interests
    monkeypatch.setattr('manager.interests_manager.update_user_interests', mock_update_user_interests)

    response = client.post('/profile/interests/update', json={"interests": ["gaming", "music"]})
    assert response.status_code == 200
    assert response.json == ["gaming", "music"]
