import pytest
from run import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configura la app en modo testing y crea un cliente de prueba."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'  # Necesario para manejar la sesión
    with app.test_client() as client:
        with app.app_context():
            yield client

# Test para obtener todas las imágenes del usuario
@patch('blueprints.pictures.fetch_user_pictures')
def test_get_pictures_success(mock_fetch_user_pictures, client):
    mock_fetch_user_pictures.return_value = [{"id": 1, "image_id": 123, "is_profile": False}]
    with client.session_transaction() as session:
        session['user_id'] = 1  # Simula un usuario logueado

    response = client.get('/pictures/')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Pictures fetched successfully.",
        "data": [{"id": 1, "image_id": 123, "is_profile": False}]
    }
    mock_fetch_user_pictures.assert_called_once_with(1)

# Test para subir una nueva imagen
@patch('blueprints.pictures.upload_user_picture')
def test_upload_picture_success(mock_upload_picture, client):
    mock_upload_picture.return_value = {"id": 2, "user_id": 1, "image_id": 456, "is_profile": False}
    with client.session_transaction() as session:
        session['user_id'] = 1  # Simula un usuario logueado

    response = client.post('/pictures/upload', json={"image_id": 456, "is_profile": False})
    assert response.status_code == 201
    assert response.get_json() == {
        "success": True,
        "message": "Picture uploaded successfully.",
        "data": {"id": 2, "user_id": 1, "image_id": 456, "is_profile": False}
    }
    mock_upload_picture.assert_called_once_with(1, 456, False)

# Test para eliminar una imagen específica
@patch('blueprints.pictures.remove_user_picture')
def test_delete_picture_success(mock_remove_user_picture, client):
    mock_remove_user_picture.return_value = {"id": 1, "image_id": 123}
    with client.session_transaction() as session:
        session['user_id'] = 1  # Simula un usuario logueado

    response = client.delete('/pictures/1')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Picture deleted successfully.",
        "data": {"id": 1, "image_id": 123}
    }
    mock_remove_user_picture.assert_called_once_with(1, 1)

# Test para establecer una imagen como foto de perfil
@patch('blueprints.pictures.set_user_profile_picture')
def test_set_profile_picture_success(mock_set_profile_picture, client):
    mock_set_profile_picture.return_value = {"id": 1, "image_id": 123, "is_profile": True}
    with client.session_transaction() as session:
        session['user_id'] = 1  # Simula un usuario logueado

    response = client.put('/pictures/set-profile', json={"picture_id": 1})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Profile picture updated successfully.",
        "data": {"id": 1, "image_id": 123, "is_profile": True}
    }
    mock_set_profile_picture.assert_called_once_with(1, 1)







