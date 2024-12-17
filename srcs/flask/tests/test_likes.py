import pytest
from run import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configura la app en modo testing y crea un cliente de prueba."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test para enviar un like
@patch('blueprints.likes.send_like', return_value={"liked_user_id": 2, "status": "like_added", "match": False})
def test_send_like(mock_send_like, client):
    response = client.post('/likes/send', json={"user_id": 1, "liked_user_id": 2})
    assert response.status_code == 200
    assert response.get_json() == {"liked_user_id": 2, "status": "like_added", "match": False}
    mock_send_like.assert_called_once_with(1, 2)

# Test para eliminar un like
@patch('blueprints.likes.remove_like', return_value={"liked_user_id": 2, "status": "like_removed"})
def test_remove_like(mock_remove_like, client):
    response = client.post('/likes/remove', json={"user_id": 1, "liked_user_id": 2})
    assert response.status_code == 200
    assert response.get_json() == {"liked_user_id": 2, "status": "like_removed"}
    mock_remove_like.assert_called_once_with(1, 2)

# Test para obtener usuarios con likes
@patch('blueprints.likes.fetch_liked_users', return_value=[2, 3, 4])
def test_get_liked_users(mock_fetch_liked_users, client):
    response = client.get('/likes/liked-users/1')
    assert response.status_code == 200
    assert response.get_json() == {"liked_users": [2, 3, 4]}
    mock_fetch_liked_users.assert_called_once_with(1)

# Test para obtener matches
@patch('blueprints.likes.fetch_matches', return_value=[2, 5])
def test_get_matches(mock_fetch_matches, client):
    response = client.get('/likes/matches/1')
    assert response.status_code == 200
    assert response.get_json() == {"matches": [2, 5]}
    mock_fetch_matches.assert_called_once_with(1)

# Test para error de validación
def test_send_like_missing_params(client):
    response = client.post('/likes/send', json={"user_id": 1})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Both user_id and liked_user_id are required."}

# Test para manejar errores inesperados
@patch('blueprints.likes.send_like', side_effect=Exception("Unexpected Error"))
def test_send_like_unexpected_error(mock_send_like, client):
    response = client.post('/likes/send', json={"user_id": 1, "liked_user_id": 2})
    assert response.status_code == 500
    assert response.get_json() == {"error": "An unexpected error occurred."}







