# import pytest
# from unittest.mock import patch, MagicMock
# from models.database import Database

# @patch('models.database.Database.get_connection')
# def test_database_connection(mock_get_connection):
#     """Prueba si la conexión a la base de datos se establece correctamente."""
#     # Configurar el mock para soportar 'with'
#     mock_connection = MagicMock()
#     mock_get_connection.return_value.__enter__.return_value = mock_connection

#     try:
#         with Database.get_connection() as conn:
#             assert conn is not None
#     except Exception as e:
#         pytest.fail(f"Database connection failed: {e}")

# @patch('models.database.Database.get_connection')
# def test_create_tables(mock_get_connection):
#     """Prueba si las tablas se crean correctamente sin errores."""
#     # Configurar el mock para soportar 'with' y el cursor
#     mock_connection = MagicMock()
#     mock_cursor = MagicMock()
#     mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

#     mock_get_connection.return_value.__enter__.return_value = mock_connection

#     try:
#         Database.create_tables()
#         mock_cursor.execute.assert_called()  # Verifica que se hayan ejecutado las consultas
#     except Exception as e:
#         pytest.fail(f"Table creation failed: {e}")

# @patch('models.database.Database.get_connection')
# def test_report_user(mock_get_connection):
#     """Prueba si se puede registrar un reporte correctamente en la base de datos."""
#     # Configurar el mock para soportar 'with' y el cursor
#     mock_connection = MagicMock()
#     mock_cursor = MagicMock()
#     mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

#     mock_get_connection.return_value.__enter__.return_value = mock_connection

#     try:
#         reporter_id = 1
#         reported_id = 2
#         reason = "Spam"

#         query = '''
#         INSERT INTO reports (reporter_id, reported_id, reason, timestamp)
#         VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
#         '''
#         params = (reporter_id, reported_id, reason)

#         Database.execute_query(query, params)

#         mock_cursor.execute.assert_called_once_with(query, params)
#     except Exception as e:
#         pytest.fail(f"Report user test failed: {e}")

# @patch('models.database.Database.get_connection')
# def test_block_user(mock_get_connection):
#     """Prueba si se puede registrar un bloqueo correctamente en la base de datos."""
#     # Configurar el mock para soportar 'with' y el cursor
#     mock_connection = MagicMock()
#     mock_cursor = MagicMock()
#     mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

#     mock_get_connection.return_value.__enter__.return_value = mock_connection

#     try:
#         blocker_id = 1
#         blocked_id = 2

#         query = '''
#         INSERT INTO blocks (blocker_id, blocked_id, timestamp)
#         VALUES (%s, %s, CURRENT_TIMESTAMP)
#         '''
#         params = (blocker_id, blocked_id)

#         Database.execute_query(query, params)

#         mock_cursor.execute.assert_called_once_with(query, params)
#     except Exception as e:
#         pytest.fail(f"Block user test failed: {e}")

# """
# **Importancia de las tablas `reports` y `blocks`:**
# - **`reports`** permite a los usuarios informar actividades sospechosas o inapropiadas, lo que mejora la seguridad y la confianza dentro de la plataforma.
# - **`blocks`** asegura que los usuarios puedan evitar interacciones no deseadas, creando un entorno más seguro y personalizable.
# Estas funcionalidades son fundamentales para cumplir los requisitos de privacidad y moderación en aplicaciones modernas de interacción social.
# """



