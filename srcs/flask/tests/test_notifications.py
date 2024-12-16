from unittest.mock import patch
import pytest
from flask import Flask
from blueprints.notifications import notifications_bp
from unittest.mock import MagicMock
from models.database import Database
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

# Mock para evitar la conexión real a la base de datos
from unittest.mock import MagicMock
from models.database import Database

@patch('manager.notifications_manager.Database.get_connection')
@patch('manager.notifications_manager.fetch_user_notifications')
def test_list_notifications(mock_fetch_user_notifications, mock_get_connection, client, sample_notifications):
    # Simular un objeto de conexión
    mock_connection = MagicMock()
    mock_connection.__enter__.return_value = mock_connection  # Simula el comportamiento del contexto `with`
    mock_connection.__exit__.return_value = None  # Simula la salida del contexto `with`
    
    # Configurar el mock para devolver la conexión simulada
    mock_get_connection.return_value = mock_connection
    
    # Configurar el mock para devolver las notificaciones simuladas
    mock_fetch_user_notifications.return_value = sample_notifications
    
    # Realizar la solicitud GET sin parámetros adicionales
    response = client.get('/notifications/?user_id=1')
    
    # Imprimir la respuesta de error para obtener detalles adicionales
    print(response.json)  # Imprime el contenido de la respuesta para ver los detalles del error
    
    # Verificar que el código de estado sea 200
    assert response.status_code == 200
    assert response.json == {"notifications": sample_notifications}
