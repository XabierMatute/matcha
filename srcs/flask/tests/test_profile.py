# import pytest
# from run import app
# from unittest.mock import patch

# @pytest.fixture
# def client():
#     """Configura la app en modo testing y crea un cliente de prueba."""
#     app.config['TESTING'] = True
#     app.config['SECRET_KEY'] = 'test_secret'
#     app.config['SESSION_TYPE'] = 'filesystem'
#     with app.test_client() as client:
#         yield client

# # Test para actualizar la ubicación manualmente
# @patch('blueprints.profile.update_user_location')
# def test_set_manual_location_valid_data(mock_update_user_location, client):
#     """Prueba la actualización manual de ubicación con datos válidos."""
#     mock_update_user_location.return_value = {
#         "location": "Bilbao",
#         "latitude": 43.262,
#         "longitude": -2.935
#     }

#     with client.session_transaction() as session:
#         session['user_id'] = 1

#     response = client.post('/profile/location/manual', json={
#         "location": "Bilbao",
#         "latitude": 43.262,
#         "longitude": -2.935
#     })

#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "message": "Location updated successfully.",
#         "data": {
#             "location": "Bilbao",
#             "latitude": 43.262,
#             "longitude": -2.935
#         }
#     }
#     mock_update_user_location.assert_called_once_with(
#         1, "Bilbao", 43.262, -2.935
#     )

# @patch('blueprints.profile.update_user_location')
# def test_set_manual_location_missing_latitude(mock_update_user_location, client):
#     """Prueba la actualización manual de ubicación sin latitud."""
#     mock_update_user_location.side_effect = ValueError("You must provide either a location or both latitude and longitude.")

#     with client.session_transaction() as session:
#         session['user_id'] = 1

#     response = client.post('/profile/location/manual', json={
#         "location": "Bilbao",
#         "longitude": -2.935
#     })

#     assert response.status_code == 400
#     assert response.get_json() == {
#         "success": False,
#         "message": "You must provide either a location or both latitude and longitude."
#     }

# @patch('blueprints.profile.update_user_location')
# def test_set_manual_location_invalid_latitude(mock_update_user_location, client):
#     """Prueba la actualización manual de ubicación con una latitud inválida."""
#     mock_update_user_location.side_effect = ValueError("Latitude must be a number.")

#     with client.session_transaction() as session:
#         session['user_id'] = 1

#     response = client.post('/profile/location/manual', json={
#         "location": "Bilbao",
#         "latitude": "invalid_latitude",
#         "longitude": -2.935
#     })

#     assert response.status_code == 400
#     assert response.get_json() == {
#         "success": False,
#         "message": "Latitude must be a number."
#     }
#     mock_update_user_location.assert_not_called()

# @patch('blueprints.profile.get_user_location')
# def test_get_location_success(mock_get_user_location, client):
#     """Prueba obtener la ubicación del usuario con éxito."""
#     mock_get_user_location.return_value = {
#         "location": "Bilbao",
#         "latitude": 43.262,
#         "longitude": -2.935
#     }

#     with client.session_transaction() as session:
#         session['user_id'] = 1

#     response = client.get('/profile/location')
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "data": {
#             "location": "Bilbao",
#             "latitude": 43.262,
#             "longitude": -2.935
#         },
#         "message": "Location fetched successfully."
#     }
#     mock_get_user_location.assert_called_once_with(1)

# def test_get_location_not_logged_in(client):
#     """Prueba obtener la ubicación cuando no se ha iniciado sesión."""
#     response = client.get('/profile/location')
#     assert response.status_code == 401
#     assert response.get_json() == {
#         "success": False,
#         "message": "User not logged in."
#     }
import pytest
from unittest.mock import patch, MagicMock
from models.profile_model import create_profile, get_profile_by_user_id, update_profile, delete_profile

# Mock data
mock_user_id = 1
mock_profile_data = {
    "first_name": "John",
    "last_name": "Doe",
    "birthdate": "1990-01-01",
    "gender": "Male",
    "location": None,
    "latitude": None,
    "longitude": None,
    "is_active": True,
    "is_online": True
}

@patch('models.profile_model.Database.get_connection')
@patch('models.profile_model.get_location_from_ip')
def test_create_profile(mock_get_location_from_ip, mock_get_connection):
    """Test creating a profile."""
    mock_get_location_from_ip.return_value = {
        "location": "Bilbao, Spain",
        "latitude": 43.263,
        "longitude": -2.935
    }

    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.return_value = {
        "user_id": mock_user_id,
        "first_name": "John",
        "last_name": "Doe",
        "birthdate": "1990-01-01",
        "gender": "Male",
        "location": "Bilbao, Spain",
        "latitude": 43.263,
        "longitude": -2.935,
        "is_active": True,
        "is_online": True
    }

    result = create_profile(mock_user_id, mock_profile_data, ip_address="8.8.8.8")

    assert result["user_id"] == mock_user_id
    assert result["location"] == "Bilbao, Spain"
    mock_cursor.execute.assert_called_once()
    mock_get_location_from_ip.assert_called_once_with("8.8.8.8")

@patch('models.profile_model.Database.get_connection')
def test_get_profile_by_user_id(mock_get_connection):
    """Test fetching a profile by user ID."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.return_value = {
        "user_id": mock_user_id,
        "first_name": "John",
        "last_name": "Doe",
    }

    result = get_profile_by_user_id(mock_user_id)

    assert result["user_id"] == mock_user_id
    assert result["first_name"] == "John"
    mock_cursor.execute.assert_called_once_with("SELECT * FROM profiles WHERE user_id = %s", (mock_user_id,))

@patch('models.profile_model.Database.get_connection')
def test_update_profile(mock_get_connection):
    """Test updating a profile."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    updated_data = {"first_name": "Jane", "is_online": False}
    mock_cursor.fetchone.return_value = {
        "user_id": mock_user_id,
        "first_name": "Jane",
        "is_online": False
    }

    result = update_profile(mock_user_id, updated_data)

    assert result["user_id"] == mock_user_id
    assert result["first_name"] == "Jane"
    mock_cursor.execute.assert_called_once()

@patch('models.profile_model.Database.get_connection')
def test_delete_profile(mock_get_connection):
    """Test deleting a profile."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.return_value = {"user_id": mock_user_id}

    result = delete_profile(mock_user_id)

    assert result["user_id"] == mock_user_id
    mock_cursor.execute.assert_called_once()

if __name__ == "__main__":
    pytest.main(["-v", __file__])






