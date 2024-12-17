import pytest
from unittest.mock import patch, MagicMock
from models.database import Database

@patch('models.database.Database.get_connection')
def test_database_connection(mock_get_connection):
    """Prueba si la conexión a la base de datos se establece correctamente."""
    # Configurar el mock para soportar 'with'
    mock_connection = MagicMock()
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    try:
        with Database.get_connection() as conn:
            assert conn is not None
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

@patch('models.database.Database.get_connection')
def test_create_tables(mock_get_connection):
    """Prueba si las tablas se crean correctamente sin errores."""
    # Configurar el mock para soportar 'with' y el cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    mock_get_connection.return_value.__enter__.return_value = mock_connection

    try:
        Database.create_tables()
    except Exception as e:
        pytest.fail(f"Table creation failed: {e}")


