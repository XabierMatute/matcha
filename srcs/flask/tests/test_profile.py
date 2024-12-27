import pytest
from run import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configura la app en modo testing y crea un cliente de prueba."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'
    app.config['SESSION_TYPE'] = 'filesystem'
    with app.test_client() as client:
        yield client

# Test para actualizar la ubicación manualmente
@patch('blueprints.profile.update_user_location')
def test_set_manual_location_valid_data(mock_update_user_location, client):
    """Prueba la actualización manual de ubicación con datos válidos."""
    mock_update_user_location.return_value = {
        "location": "Bilbao",
        "latitude": 43.262,
        "longitude": -2.935
    }

    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/profile/location/update', json={
        "location": "Bilbao",
        "latitude": 43.262,
        "longitude": -2.935
    })

    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Location updated successfully.",
        "data": {
            "location": "Bilbao",
            "latitude": 43.262,
            "longitude": -2.935
        }
    }
    mock_update_user_location.assert_called_once_with(
        1, "Bilbao", 43.262, -2.935
    )

@patch('blueprints.profile.update_user_location')
def test_set_manual_location_missing_latitude(mock_update_user_location, client):
    """Prueba la actualización manual de ubicación sin latitud."""
    mock_update_user_location.side_effect = ValueError("You must provide either a location or both latitude and longitude.")

    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/profile/location/update', json={
        "location": "Bilbao",
        "longitude": -2.935
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "message": "You must provide either a location or both latitude and longitude."
    }

@patch('blueprints.profile.update_user_location')
def test_set_manual_location_invalid_latitude(mock_update_user_location, client):
    """Prueba la actualización manual de ubicación con una latitud inválida."""
    mock_update_user_location.side_effect = ValueError("Latitude must be a number.")

    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/profile/location/update', json={
        "location": "Bilbao",
        "latitude": "invalid_latitude",
        "longitude": -2.935
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "message": "Latitude must be a number."
    }
    mock_update_user_location.assert_not_called()

@patch('blueprints.profile.get_user_location')
def test_get_location_success(mock_get_user_location, client):
    """Prueba obtener la ubicación del usuario con éxito."""
    mock_get_user_location.return_value = {
        "location": "Bilbao",
        "latitude": 43.262,
        "longitude": -2.935
    }

    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.get('/profile/location')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "data": {
            "location": "Bilbao",
            "latitude": 43.262,
            "longitude": -2.935
        },
        "message": "Location fetched successfully."
    }
    mock_get_user_location.assert_called_once_with(1)

def test_get_location_not_logged_in(client):
    """Prueba obtener la ubicación cuando no se ha iniciado sesión."""
    response = client.get('/profile/location')
    assert response.status_code == 401
    assert response.get_json() == {
        "success": False,
        "message": "User not logged in."
    }





