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

# Test para reportar un usuario
@patch('blueprints.likes.send_report', return_value={"success": True, "message": "User reported successfully."})
def test_report_user(mock_send_report, client):
    response = client.post('/reports/report', json={"reporter_id": 1, "reported_id": 2, "reason": "Spam"})
    assert response.status_code == 200
    assert response.get_json() == {"success": True, "message": "User reported successfully."}
    mock_send_report.assert_called_once_with(1, 2, "Spam")

# Test para bloquear un usuario
@patch('blueprints.likes.block_user_account', return_value={"success": True, "message": "User blocked successfully."})
def test_block_user(mock_block_user_account, client):
    response = client.post('/reports/block', json={"blocker_id": 1, "blocked_id": 2})
    assert response.status_code == 200
    assert response.get_json() == {"success": True, "message": "User blocked successfully."}
    mock_block_user_account.assert_called_once_with(1, 2)

# Test para error de validación al enviar like
def test_send_like_missing_params(client):
    response = client.post('/likes/send', json={"user_id": 1})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Both user_id and liked_user_id are required."}

# Test para manejar errores inesperados en like
@patch('blueprints.likes.send_like', side_effect=Exception("Unexpected Error"))
def test_send_like_unexpected_error(mock_send_like, client):
    response = client.post('/likes/send', json={"user_id": 1, "liked_user_id": 2})
    assert response.status_code == 500
    assert response.get_json() == {"error": "An unexpected error occurred."}

# Test para manejar errores inesperados en reporte
@patch('blueprints.likes.send_report', side_effect=Exception("Unexpected Error"))
def test_report_user_unexpected_error(mock_send_report, client):
    response = client.post('/reports/report', json={"reporter_id": 1, "reported_id": 2, "reason": "Spam"})
    assert response.status_code == 500
    assert response.get_json() == {"error": "An unexpected error occurred."}

# Test para manejar errores inesperados en bloqueo
@patch('blueprints.likes.block_user_account', side_effect=Exception("Unexpected Error"))
def test_block_user_unexpected_error(mock_block_user_account, client):
    response = client.post('/reports/block', json={"blocker_id": 1, "blocked_id": 2})
    assert response.status_code == 500
    assert response.get_json() == {"error": "An unexpected error occurred."}











