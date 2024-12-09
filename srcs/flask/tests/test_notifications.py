import pytest
from unittest.mock import patch
from flask import Flask
from blueprints.notifications import notifications_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(notifications_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_notifications():
    return [
        {"id": 1, "type": "message_received", "message": "You have a new message.", "is_read": False},
        {"id": 2, "type": "liked", "message": "Someone liked your profile.", "is_read": True}
    ]

@patch('manager.notifications_manager.fetch_user_notifications')
def test_list_notifications(mock_fetch_user_notifications, client, sample_notifications):
    mock_fetch_user_notifications.return_value = sample_notifications
    response = client.get('/notifications/?user_id=1')
    assert response.status_code == 200
    assert response.json == {"notifications": sample_notifications}
    mock_fetch_user_notifications.assert_called_once_with(1, None, None)

@patch('manager.notifications_manager.fetch_user_notifications')
def test_list_notifications_with_pagination(mock_fetch_user_notifications, client):
    mock_fetch_user_notifications.return_value = [
        {"id": 1, "type": "message_received", "message": "You have a new message.", "is_read": False}
    ]
    response = client.get('/notifications/?user_id=1&limit=10&offset=5')
    assert response.status_code == 200
    mock_fetch_user_notifications.assert_called_once_with(1, 10, 5)

@patch('manager.notifications_manager.fetch_unread_notifications')
def test_list_unread_notifications(mock_fetch_unread_notifications, client):
    mock_fetch_unread_notifications.return_value = [
        {"id": 1, "type": "message_received", "message": "You have a new message.", "is_read": False}
    ]
    response = client.get('/notifications/unread?user_id=1')
    assert response.status_code == 200
    mock_fetch_unread_notifications.assert_called_once_with(1)

@patch('manager.notifications_manager.mark_notification_as_read')
def test_mark_notification_as_read(mock_mark_notification_as_read, client):
    mock_mark_notification_as_read.return_value = {
        "id": 1,
        "type": "message_received",
        "message": "You have a new message.",
        "is_read": True
    }
    response = client.put('/notifications/1')
    assert response.status_code == 200
    mock_mark_notification_as_read.assert_called_once_with(1)

@patch('manager.notifications_manager.remove_notification')
def test_delete_notification(mock_remove_notification, client):
    mock_remove_notification.return_value = {"id": 1}
    response = client.delete('/notifications/1')
    assert response.status_code == 200
    mock_remove_notification.assert_called_once_with(1)

@patch('manager.notifications_manager.remove_multiple_notifications')
def test_delete_notifications_batch(mock_remove_multiple_notifications, client):
    mock_remove_multiple_notifications.return_value = [{"id": 1}, {"id": 2}]
    response = client.delete('/notifications/batch', json={"notification_ids": [1, 2]})
    assert response.status_code == 200
    mock_remove_multiple_notifications.assert_called_once_with([1, 2])

@patch('manager.notifications_manager.remove_multiple_notifications')
def test_delete_notifications_batch_invalid_data(mock_remove_multiple_notifications, client):
    response = client.delete('/notifications/batch', json={})
    assert response.status_code == 400
    mock_remove_multiple_notifications.assert_not_called()

@patch('manager.notifications_manager.remove_multiple_notifications')
def test_delete_notifications_batch_empty_list(mock_remove_multiple_notifications, client):
    response = client.delete('/notifications/batch', json={"notification_ids": []})
    assert response.status_code == 400
    mock_remove_multiple_notifications.assert_not_called()

