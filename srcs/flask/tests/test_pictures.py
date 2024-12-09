import pytest
from unittest.mock import patch
from flask import Flask
from blueprints.pictures import pictures_bp

@pytest.fixture
def app():
    """Crea una aplicación Flask para las pruebas."""
    app = Flask(__name__)
    app.register_blueprint(pictures_bp)
    return app

@pytest.fixture
def client(app):
    """Crea un cliente de pruebas."""
    return app.test_client()

@pytest.fixture
def valid_picture_data():
    """Fixture para datos válidos de imagen."""
    return {
        "user_id": 1,
        "image_id": "image3.jpg",
        "is_profile": True
    }

@pytest.fixture
def valid_profile_data():
    """Fixture para datos válidos de foto de perfil."""
    return {
        "user_id": 1,
        "picture_id": 2
    }

@patch('manager.pictures_manager.fetch_user_pictures')
def test_get_pictures(mock_fetch_user_pictures, client):
    """Prueba el endpoint para obtener todas las fotos de un usuario."""
    mock_fetch_user_pictures.return_value = [
        {"id": 1, "image_id": "image1.jpg", "is_profile": False, "created_at": "2024-01-01T12:00:00"},
        {"id": 2, "image_id": "image2.jpg", "is_profile": True, "created_at": "2024-01-02T12:00:00"}
    ]

    response = client.get('/pictures/1')
    assert response.status_code == 200
    assert response.json == {
        "message": "Fetched 2 pictures for user 1.",
        "pictures": [
            {"id": 1, "image_id": "image1.jpg", "is_profile": False, "created_at": "2024-01-01T12:00:00"},
            {"id": 2, "image_id": "image2.jpg", "is_profile": True, "created_at": "2024-01-02T12:00:00"}
        ]
    }
    mock_fetch_user_pictures.assert_called_once_with(1)

@patch('manager.pictures_manager.fetch_user_pictures')
def test_get_pictures_invalid_user_id(mock_fetch_user_pictures, client):
    """Prueba error al obtener fotos con un user_id inválido."""
    response = client.get('/pictures/not-a-number')
    assert response.status_code == 404  # Flask maneja esto por defecto
    mock_fetch_user_pictures.assert_not_called()

@patch('manager.pictures_manager.upload_picture')
def test_upload_picture(mock_upload_picture, client, valid_picture_data):
    """Prueba el endpoint para subir una foto."""
    mock_upload_picture.return_value = {
        "success": True,
        "picture": {
            "id": 3,
            "user_id": 1,
            "image_id": "image3.jpg",
            "is_profile": True,
            "created_at": "2024-01-03T12:00:00"
        }
    }

    response = client.post('/pictures/upload', json=valid_picture_data)
    assert response.status_code == 201
    assert response.json == mock_upload_picture.return_value
    mock_upload_picture.assert_called_once_with(1, "image3.jpg", True)

@patch('manager.pictures_manager.upload_picture')
def test_upload_picture_exception(mock_upload_picture, client, valid_picture_data):
    """Prueba error inesperado al subir una foto."""
    mock_upload_picture.side_effect = Exception("Unexpected error")

    response = client.post('/pictures/upload', json=valid_picture_data)
    assert response.status_code == 500
    assert "error" in response.json
    assert "Unexpected error" in response.json["error"]
    mock_upload_picture.assert_called_once()

@patch('manager.pictures_manager.remove_picture')
def test_delete_picture(mock_remove_picture, client):
    """Prueba el endpoint para eliminar una foto."""
    mock_remove_picture.return_value = {
        "success": True,
        "picture": {"id": 1, "image_id": "image1.jpg"}
    }

    response = client.delete('/pictures/1/1')
    assert response.status_code == 200
    assert response.json == mock_remove_picture.return_value
    mock_remove_picture.assert_called_once_with(1, 1)

@patch('manager.pictures_manager.change_profile_picture')
def test_set_profile_picture(mock_change_profile_picture, client, valid_profile_data):
    """Prueba el endpoint para establecer una foto como foto de perfil."""
    mock_change_profile_picture.return_value = {
        "success": True,
        "picture": {
            "id": 2,
            "image_id": "image2.jpg",
            "is_profile": True
        }
    }

    response = client.put('/pictures/set-profile', json=valid_profile_data)
    assert response.status_code == 200
    assert response.json == mock_change_profile_picture.return_value
    mock_change_profile_picture.assert_called_once_with(1, 2)

