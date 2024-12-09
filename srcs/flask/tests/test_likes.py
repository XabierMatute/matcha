import pytest
from unittest.mock import patch
from flask import Flask
from blueprints.likes import likes_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(likes_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_like_result():
    return {"liked_user_id": 2, "status": "like_added", "match": False}

@pytest.fixture
def sample_liked_users():
    return [2, 3, 4]

@pytest.fixture
def sample_matches():
    return [3, 5]

@patch('manager.likes_manager.send_like')
def test_like_user(mock_send_like, client, sample_like_result):
    mock_send_like.return_value = sample_like_result

    response = client.post('/likes/2', json={"user_id": 1})
    assert response.status_code == 201
    assert response.json == {
        "message": "User liked successfully",
        "like_status": sample_like_result
    }
    mock_send_like.assert_called_once_with(1, 2)

@patch('manager.likes_manager.remove_like')
def test_unlike_user(mock_remove_like, client):
    mock_remove_like.return_value = {"liked_user_id": 2, "status": "like_removed"}

    response = client.delete('/likes/2', json={"user_id": 1})
    assert response.status_code == 200
    assert response.json == {
        "message": "Like removed successfully",
        "like_status": {"liked_user_id": 2, "status": "like_removed"}
    }
    mock_remove_like.assert_called_once_with(1, 2)

@patch('manager.likes_manager.fetch_liked_users')
def test_get_liked_users(mock_fetch_liked_users, client, sample_liked_users):
    mock_fetch_liked_users.return_value = sample_liked_users

    response = client.get('/likes/?user_id=1')
    assert response.status_code == 200
    assert response.json == {
        "message": "Fetched 3 liked users.",
        "likes": sample_liked_users
    }
    mock_fetch_liked_users.assert_called_once_with(1)

@patch('manager.likes_manager.fetch_matches')
def test_get_matches(mock_fetch_matches, client, sample_matches):
    mock_fetch_matches.return_value = sample_matches

    response = client.get('/likes/matches?user_id=1')
    assert response.status_code == 200
    assert response.json == {
        "message": "Fetched 2 matches.",
        "matches": sample_matches
    }
    mock_fetch_matches.assert_called_once_with(1)

