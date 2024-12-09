import pytest
from unittest.mock import patch
from flask import Flask
from blueprints.interests import interests_bp

@pytest.fixture
def app():
    """Crea una aplicación Flask para las pruebas."""
    app = Flask(__name__)
    app.register_blueprint(interests_bp)
    return app

@pytest.fixture
def client(app):
    """Crea un cliente de pruebas."""
    return app.test_client()

@patch('manager.interests_manager.get_all_interests')
def test_get_all_interests(mock_get_all_interests, client):
    """Prueba obtener todos los intereses."""
    mock_get_all_interests.return_value = [
        {"id": 1, "tag": "music"},
        {"id": 2, "tag": "travel"}
    ]

    response = client.get('/interests/')
    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "tag": "music"},
        {"id": 2, "tag": "travel"}
    ]

@patch('manager.interests_manager.get_interest_by_id')
def test_get_interest(mock_get_interest_by_id, client):
    """Prueba obtener un interés por ID."""
    mock_get_interest_by_id.return_value = {"id": 1, "tag": "music"}

    response = client.get('/interests/1')
    assert response.status_code == 200
    assert response.json == {"id": 1, "tag": "music"}

    mock_get_interest_by_id.return_value = None
    response = client.get('/interests/999')
    assert response.status_code == 404
    assert response.json == {"error": "Interest not found"}

@patch('manager.interests_manager.add_new_interest')
def test_create_interest(mock_add_new_interest, client):
    """Prueba crear un interés."""
    mock_add_new_interest.return_value = {"id": 3, "tag": "art"}

    response = client.post('/interests/', json={"tag": "art"})
    assert response.status_code == 201
    assert response.json == {"id": 3, "tag": "art"}

    mock_add_new_interest.side_effect = ValueError("Interest tag cannot be empty.")
    response = client.post('/interests/', json={"tag": ""})
    assert response.status_code == 400
    assert response.json == {"error": "Interest tag cannot be empty."}

@patch('manager.interests_manager.add_multiple_interests')
def test_batch_add_interests(mock_add_multiple_interests, client):
    """Prueba agregar intereses en lote."""
    mock_add_multiple_interests.return_value = [
        {"id": 1, "tag": "music"},
        {"id": 2, "tag": "travel"}
    ]

    response = client.post('/interests/batch', json={"tags": ["music", "travel"]})
    assert response.status_code == 201
    assert response.json == [
        {"id": 1, "tag": "music"},
        {"id": 2, "tag": "travel"}
    ]

    mock_add_multiple_interests.side_effect = ValueError("No tags provided to add.")
    response = client.post('/interests/batch', json={"tags": []})
    assert response.status_code == 400
    assert response.json == {"error": "No tags provided to add."}

@patch('manager.interests_manager.remove_interests_by_ids')
def test_delete_interest(mock_remove_interests_by_ids, client):
    """Prueba eliminar un interés."""
    mock_remove_interests_by_ids.return_value = "Removed 1 interests."

    response = client.delete('/interests/1')
    assert response.status_code == 200
    assert response.json == {"message": "Removed 1 interests."}

    mock_remove_interests_by_ids.side_effect = ValueError("No interest IDs provided to remove.")
    response = client.delete('/interests/999')
    assert response.status_code == 400
    assert response.json == {"error": "No interest IDs provided to remove."}
