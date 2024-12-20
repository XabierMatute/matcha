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

# Test para obtener todas las imágenes del usuario
@patch('blueprints.pictures.fetch_user_pictures', return_value=[{"id": 1, "image_id": 123, "is_profile": False}])
def test_get_pictures(mock_fetch_pictures, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.get('/pictures/')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Pictures fetched successfully.",
        "data": [{"id": 1, "image_id": 123, "is_profile": False}]
    }
    mock_fetch_pictures.assert_called_once_with(1)

# Test para subir una nueva imagen
@patch('blueprints.pictures.upload_user_picture', return_value={"id": 2, "user_id": 1, "image_id": 456, "is_profile": False})
def test_upload_picture(mock_upload_picture, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/pictures/upload', json={"image_id": 456})
    assert response.status_code == 201
    assert response.get_json() == {
        "success": True,
        "message": "Picture uploaded successfully.",
        "data": {"id": 2, "user_id": 1, "image_id": 456, "is_profile": False}
    }
    mock_upload_picture.assert_called_once_with(1, 456, False)

# Test para error cuando se intenta subir más de 5 imágenes
@patch('blueprints.pictures.upload_user_picture', return_value=None)
def test_upload_picture_max_limit(mock_upload_picture, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/pictures/upload', json={"image_id": 456})
    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "message": "User already has 5 pictures."
    }
    mock_upload_picture.assert_called_once_with(1, 456, False)

# Test para eliminar una imagen específica
@patch('blueprints.pictures.remove_user_picture', return_value={"id": 1, "image_id": 123})
def test_delete_picture(mock_remove_picture, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.delete('/pictures/1')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Picture deleted successfully.",
        "data": {"id": 1, "image_id": 123}
    }
    mock_remove_picture.assert_called_once_with(1, 1)

# Test para establecer una imagen como foto de perfil
@patch('blueprints.pictures.set_user_profile_picture', return_value={"id": 1, "image_id": 123, "is_profile": True})
def test_set_profile_picture(mock_set_profile_picture, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.put('/pictures/set-profile', json={"picture_id": 1})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Profile picture updated successfully.",
        "data": {"id": 1, "image_id": 123, "is_profile": True}
    }
    mock_set_profile_picture.assert_called_once_with(1, 1)

# Test para contar el número de imágenes del usuario
@patch('blueprints.pictures.get_user_picture_count', return_value=3)
def test_count_pictures(mock_count_pictures, client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.get('/pictures/count')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Picture count fetched successfully.",
        "data": {"count": 3}
    }
    mock_count_pictures.assert_called_once_with(1)

# Test cuando el usuario no está logueado
def test_user_not_logged_in(client):
    response = client.get('/pictures/')
    assert response.status_code == 401
    assert response.get_json() == {
        "success": False,
        "message": "User not logged in."
    }





