from unittest.mock import patch
import pytest
from flask import Flask
from blueprints.notifications import notifications_bp

@pytest.fixture
def app():
    """Configura la aplicación Flask para pruebas."""
    app = Flask(__name__)
    app.config['TESTING'] = True  # Modo prueba
    app.register_blueprint(notifications_bp)
    return app

@pytest.fixture
def client(app):
    """Devuelve un cliente de prueba de Flask."""
    return app.test_client()

@pytest.fixture
def sample_notifications():
    """Datos simulados de notificaciones."""
    return [
        {"id": 1, "type": "message_received", "message": "You have a new message.", "is_read": False},
        {"id": 2, "type": "liked", "message": "Someone liked your profile.", "is_read": True}
    ]

@patch('blueprints.notifications.fetch_user_notifications')
def test_list_notifications(mock_fetch_user_notifications, client, sample_notifications):
    """Test para listar todas las notificaciones."""
    mock_fetch_user_notifications.return_value = sample_notifications
    response = client.get('/notifications/', query_string={"user_id": 1, "limit": 10, "offset": 0})
    assert response.status_code == 200
    assert response.json == {
        "success": True,
        "message": "Notifications fetched successfully",
        "data": sample_notifications
    }
    mock_fetch_user_notifications.assert_called_once_with(1, 10, 0)

@patch('blueprints.notifications.fetch_unread_notifications')
def test_list_unread_notifications(mock_fetch_unread_notifications, client, sample_notifications):
    """Test para listar las notificaciones no leídas."""
    mock_fetch_unread_notifications.return_value = [sample_notifications[0]]
    response = client.get('/notifications/unread', query_string={"user_id": 1})
    assert response.status_code == 200
    assert response.json == {
        "success": True,
        "message": "Unread notifications fetched successfully",
        "data": [sample_notifications[0]]
    }
    mock_fetch_unread_notifications.assert_called_once_with(1)

@patch('blueprints.notifications.mark_notification_as_read')
def test_mark_notification_as_read(mock_mark_as_read, client):
    """Test para marcar una notificación como leída."""
    mock_mark_as_read.return_value = {"id": 1, "type": "message_received", "is_read": True}
    response = client.put('/notifications/1')
    assert response.status_code == 200
    assert response.json == {
        "success": True,
        "message": "Notification marked as read",
        "data": {"id": 1, "type": "message_received", "is_read": True}
    }
    mock_mark_as_read.assert_called_once_with(1)

@patch('blueprints.notifications.remove_notification')
def test_delete_notification(mock_remove_notification, client):
    """Test para eliminar una notificación."""
    mock_remove_notification.return_value = {"id": 1}
    response = client.delete('/notifications/1')
    assert response.status_code == 200
    assert response.json == {
        "success": True,
        "message": "Notification deleted successfully",
        "data": {"id": 1}
    }
    mock_remove_notification.assert_called_once_with(1)

@patch('blueprints.notifications.remove_multiple_notifications')
def test_delete_notifications_batch(mock_remove_multiple_notifications, client):
    """Test para eliminar múltiples notificaciones."""
    mock_remove_multiple_notifications.return_value = [1, 2]
    payload = {"notification_ids": [1, 2]}
    response = client.delete('/notifications/batch', json=payload)
    assert response.status_code == 200
    assert response.json == {
        "success": True,
        "message": "Notifications deleted successfully",
        "data": {"deleted_ids": [1, 2]}
    }
    mock_remove_multiple_notifications.assert_called_once_with([1, 2])

@patch('blueprints.notifications.send_notification')
def test_send_notification(mock_send_notification, client):
    """Test para enviar una nueva notificación."""
    mock_send_notification.return_value = {"id": 3, "type": "liked", "message": "Someone liked your profile."}
    payload = {
        "user_id": 1,
        "type": "liked",
        "message": "Someone liked your profile."
    }
    response = client.post('/notifications/send', json=payload)
    assert response.status_code == 201
    assert response.json == {
        "success": True,
        "message": "Notification sent successfully",
        "data": {"id": 3, "type": "liked", "message": "Someone liked your profile."}
    }
    mock_send_notification.assert_called_once_with(1, "liked", "Someone liked your profile.")




