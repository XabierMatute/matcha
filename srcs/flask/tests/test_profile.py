import pytest
from run import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configura la app en modo testing y crea un cliente de prueba."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

# Test para obtener el perfil completo
@patch('blueprints.profile.fetch_user_profile', return_value={"username": "testuser", "email": "test@test.com"})
def test_get_profile(mock_fetch_profile, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.get('/profile/')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Profile fetched successfully.",
        "data": {"username": "testuser", "email": "test@test.com"}
    }
    mock_fetch_profile.assert_called_once_with(1)

# Test para actualizar el perfil
@patch('blueprints.profile.update_user_profile', return_value={"username": "updateduser", "email": "updated@test.com"})
def test_update_profile(mock_update_profile, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/profile/update', json={"username": "updateduser"})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Profile updated successfully.",
        "data": {"username": "updateduser", "email": "updated@test.com"}
    }
    mock_update_profile.assert_called_once_with(1, {"username": "updateduser"})

# Test para obtener la ubicación
@patch('blueprints.profile.fetch_user_location', return_value={"location": "City", "latitude": 40.0, "longitude": -3.0})
def test_get_location(mock_fetch_location, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.get('/profile/location')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Location fetched successfully.",
        "data": {"location": "City", "latitude": 40.0, "longitude": -3.0}
    }
    mock_fetch_location.assert_called_once_with(1)

# Test para actualizar la ubicación
@patch('blueprints.profile.update_user_location', return_value={"location": "New City", "latitude": 42.0, "longitude": -2.0})
def test_update_location(mock_update_location, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/profile/location/update', json={
        "location": "New City",
        "latitude": 42.0,
        "longitude": -2.0
    })
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Location updated successfully.",
        "data": {"location": "New City", "latitude": 42.0, "longitude": -2.0}
    }
    mock_update_location.assert_called_once_with(1, "New City", 42.0, -2.0)

# Test para error cuando el usuario no está logueado
def test_get_profile_not_logged_in(client):
    response = client.get('/profile/')
    assert response.status_code == 401
    assert response.get_json() == {
        "success": False,
        "message": "User not logged in."
    }

# Test para error de validación en actualización de ubicación
def test_update_location_missing_data(client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/profile/location/update', json={"latitude": 42.0})
    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "message": "Missing location data."
    }





