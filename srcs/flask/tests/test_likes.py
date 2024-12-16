from unittest.mock import patch
import pytest
from flask import Flask
from blueprints.likes import likes_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(likes_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_likes():
    return [{"user_id": 1, "liked_user_id": 2}, {"user_id": 1, "liked_user_id": 3}]

@pytest.fixture
def sample_matches():
    return [{"match_id": 2}, {"match_id": 3}]

@patch('manager.likes_manager.send_like')  # Ruta correcta para el mock
def test_like_user(mock_send_like, client):
    mock_send_like.return_value = {"liked_user_id": 2, "status": "like_added"}
    payload = {"user_id": 1}
    response = client.post('/likes/2', json=payload)
    assert response.status_code == 201
    assert response.json == {
        "message": "User liked successfully",
        "like_status": {"liked_user_id": 2, "status": "like_added"}
    }
    mock_send_like.assert_called_once_with(1, 2)

@patch('manager.likes_manager.remove_like')  # Ruta correcta para el mock
def test_unlike_user(mock_remove_like, client):
    mock_remove_like.return_value = {"liked_user_id": 2, "status": "like_removed"}
    payload = {"user_id": 1}
    response = client.delete('/likes/2', json=payload)
    assert response.status_code == 200
    assert response.json == {
        "message": "Like removed successfully",
        "like_status": {"liked_user_id": 2, "status": "like_removed"}
    }
    mock_remove_like.assert_called_once_with(1, 2)

@patch('manager.likes_manager.fetch_liked_users')  # Ruta correcta para el mock
def test_get_likes(mock_fetch_liked_users, client):
    mock_fetch_liked_users.return_value = [2, 3]
    response = client.get('/likes/', query_string={"user_id": 1})
    assert response.status_code == 200
    assert response.json == {
        "message": "Fetched 2 liked users.",
        "likes": [2, 3]
    }
    mock_fetch_liked_users.assert_called_once_with(1)

@patch('manager.likes_manager.fetch_matches')  # Ruta correcta para el mock
def test_get_matches(mock_fetch_matches, client):
    mock_fetch_matches.return_value = [2, 3]
    response = client.get('/likes/matches', query_string={"user_id": 1})
    assert response.status_code == 200
    assert response.json == {
        "message": "Fetched 2 matches.",
        "matches": [2, 3]
    }
    mock_fetch_matches.assert_called_once_with(1)

# Casos negativos
def test_like_user_invalid_user_id(client):
    payload = {"user_id": "invalid"}
    response = client.post('/likes/2', json=payload)
    assert response.status_code == 400
    assert response.json == {"error": "Valid user_id is required in the request body"}

def test_unlike_user_invalid_user_id(client):
    payload = {"user_id": "invalid"}
    response = client.delete('/likes/2', json=payload)
    assert response.status_code == 400
    assert response.json == {"error": "Valid user_id is required in the request body"}

def test_get_likes_missing_user_id(client):
    response = client.get('/likes/')
    assert response.status_code == 400
    assert response.json == {"error": "Valid user_id is required as a query parameter"}

def test_get_matches_missing_user_id(client):
    response = client.get('/likes/matches')
    assert response.status_code == 400
    assert response.json == {"error": "Valid user_id is required as a query parameter"}





