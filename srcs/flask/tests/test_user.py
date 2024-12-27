

# import pytest
# from run import app
# from unittest.mock import patch

# @pytest.fixture
# def client():
#     """Configura la app en modo testing y crea un cliente de prueba."""
#     app.config['TESTING'] = True
#     app.config['SECRET_KEY'] = 'test_secret'
#     with app.test_client() as client:
#         yield client

# # Test para obtener detalles de un usuario por ID
# @patch('blueprints.users.get_user_details')
# def test_get_user_details_by_id(mock_get_user_details, client):
#     mock_get_user_details.return_value = {"id": 1, "username": "testuser", "email": "test@example.com"}

#     response = client.get('/users/details?user_id=1')
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "message": "User details fetched successfully.",
#         "data": {"id": 1, "username": "testuser", "email": "test@example.com"}
#     }
#     mock_get_user_details.assert_called_once_with(user_id=1, require_verified=True)

# # Test para obtener detalles de un usuario por username
# @patch('blueprints.users.get_user_details')
# def test_get_user_details_by_username(mock_get_user_details, client):
#     mock_get_user_details.return_value = {"id": 2, "username": "john_doe", "email": "john@example.com"}

#     response = client.get('/users/details?username=john_doe')
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "message": "User details fetched successfully.",
#         "data": {"id": 2, "username": "john_doe", "email": "john@example.com"}
#     }
#     mock_get_user_details.assert_called_once_with(username="john_doe", require_verified=True)

# # Test para registrar un nuevo usuario
# @patch('blueprints.users.register_user')
# def test_register_user(mock_register_user, client):
#     mock_register_user.return_value = {"id": 3, "username": "newuser", "email": "new@example.com"}

#     response = client.post('/users/register', json={
#         "username": "newuser",
#         "email": "new@example.com",
#         "password": "securepassword"
#     })
#     assert response.status_code == 201
#     assert response.get_json() == {
#         "success": True,
#         "message": "User registered successfully.",
#         "data": {"id": 3, "username": "newuser", "email": "new@example.com"}
#     }
#     mock_register_user.assert_called_once_with({
#         "username": "newuser",
#         "email": "new@example.com",
#         "password": "securepassword"
#     })

# # Test para actualizar un usuario
# @patch('blueprints.users.update_user_profile')
# def test_update_user(mock_update_user, client):
#     mock_update_user.return_value = {"id": 1, "username": "updateduser", "email": "updated@example.com"}

#     response = client.put('/users/update/1', json={
#         "username": "updateduser",
#         "email": "updated@example.com"
#     })
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "message": "User updated successfully.",
#         "data": {"id": 1, "username": "updateduser", "email": "updated@example.com"}
#     }
#     mock_update_user.assert_called_once_with(1, {
#         "username": "updateduser",
#         "email": "updated@example.com"
#     })

# # Test para eliminar un usuario
# @patch('blueprints.users.delete_user_account')
# def test_delete_user(mock_delete_user, client):
#     mock_delete_user.return_value = {"id": 1}

#     response = client.delete('/users/delete/1')
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "message": "User deleted successfully.",
#         "data": {"id": 1}
#     }
#     mock_delete_user.assert_called_once_with(1)

# # Test para verificar un usuario por email
# @patch('blueprints.users.verify_user')
# def test_verify_user(mock_verify_user, client):
#     mock_verify_user.return_value = {"id": 1, "username": "verifieduser", "email": "verified@example.com"}

#     response = client.post('/users/verify', json={"email": "verified@example.com"})
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "message": "User verified successfully.",
#         "data": {"id": 1, "username": "verifieduser", "email": "verified@example.com"}
#     }
#     mock_verify_user.assert_called_once_with("verified@example.com")

# # Test para error si no se proporciona email en verificación
# def test_verify_user_missing_email(client):
#     response = client.post('/users/verify', json={})
#     assert response.status_code == 400
#     assert response.get_json() == {
#         "success": False,
#         "message": "Email is required."
#     }

# # Test para error si no se proporciona ni ID ni username
# def test_get_user_details_missing_params(client):
#     response = client.get('/users/details')
#     assert response.status_code == 400
#     assert response.get_json() == {
#         "success": False,
#         "message": "Either 'user_id' or 'username' must be provided."
#     }

# # Test para obtener detalles de un usuario no verificado
# @patch('blueprints.users.get_user_details')
# def test_get_user_details_unverified(mock_get_user_details, client):
#     mock_get_user_details.side_effect = ValueError("User 'unverified_user' is not verified.")

#     response = client.get('/users/details?username=unverified_user')
#     assert response.status_code == 400
#     assert response.get_json() == {
#         "success": False,
#         "message": "User 'unverified_user' is not verified."
#     }
#     mock_get_user_details.assert_called_once_with(username="unverified_user", require_verified=True)

# # Test para obtener detalles de un usuario verificado
# @patch('blueprints.users.get_user_details')
# def test_get_user_details_verified(mock_get_user_details, client):
#     mock_get_user_details.return_value = {"id": 2, "username": "verified_user", "email": "verified@example.com"}

#     response = client.get('/users/details?username=verified_user')
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "success": True,
#         "message": "User details fetched successfully.",
#         "data": {"id": 2, "username": "verified_user", "email": "verified@example.com"}
#     }
#     mock_get_user_details.assert_called_once_with(username="verified_user", require_verified=True)

import pytest
from unittest.mock import patch, MagicMock
from models.user_model import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    update_user_password,
    update_user_email,
    delete_user
)

# Mock data
mock_username = "testuser"
mock_email = "test@example.com"
mock_new_email = "new_test@example.com"
mock_password_hash = "hashed_password"
mock_new_password_hash = "new_hashed_password"
mock_user_id = 1

@patch('models.user_model.Database.get_connection')
def test_create_user_success(mock_get_connection):
    """Test if a user is created successfully."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    # Simulate no username/email conflict and a successful insert
    mock_cursor.fetchone.side_effect = [None, None, {"id": mock_user_id, "username": mock_username, "email": mock_email}]

    result = create_user(mock_username, mock_email, mock_password_hash)

    assert result["id"] == mock_user_id
    assert result["username"] == mock_username
    assert result["email"] == mock_email
    assert mock_cursor.execute.call_count == 3

@patch('models.user_model.Database.get_connection')
def test_get_user_by_id(mock_get_connection):
    """Test if a user is fetched by ID."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.return_value = {"id": mock_user_id, "username": mock_username, "email": mock_email}

    result = get_user_by_id(mock_user_id)

    assert result["id"] == mock_user_id
    assert result["username"] == mock_username
    assert result["email"] == mock_email
    mock_cursor.execute.assert_called_once_with("SELECT id, username, email FROM users WHERE id = %s", (mock_user_id,))

@patch('models.user_model.Database.get_connection')
def test_get_user_by_username(mock_get_connection):
    """Test if a user is fetched by username."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.return_value = {"id": mock_user_id, "username": mock_username, "email": mock_email}

    result = get_user_by_username(mock_username)

    assert result["id"] == mock_user_id
    assert result["username"] == mock_username
    assert result["email"] == mock_email
    mock_cursor.execute.assert_called_once_with("SELECT id, username, email FROM users WHERE username = %s", (mock_username,))

@patch('models.user_model.Database.get_connection')
def test_get_user_by_email(mock_get_connection):
    """Test if a user is fetched by email."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.return_value = {"id": mock_user_id, "username": mock_username, "email": mock_email}

    result = get_user_by_email(mock_email)

    assert result["id"] == mock_user_id
    assert result["username"] == mock_username
    assert result["email"] == mock_email
    mock_cursor.execute.assert_called_once_with("SELECT id, username, email FROM users WHERE email = %s", (mock_email,))

@patch('models.user_model.Database.get_connection')
def test_update_user_password(mock_get_connection):
    """Test if a user's password is updated successfully."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.side_effect = [
        {"id": mock_user_id, "username": mock_username, "email": mock_email},
        {"id": mock_user_id, "username": mock_username, "email": mock_email}
    ]

    result = update_user_password(mock_user_id, mock_new_password_hash)

    assert result["id"] == mock_user_id
    assert result["username"] == mock_username
    assert result["email"] == mock_email
    assert mock_cursor.execute.call_count == 2

@patch('models.user_model.Database.get_connection')
def test_update_user_email(mock_get_connection):
    """Test if a user's email is updated successfully."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.side_effect = [
        {"id": mock_user_id, "username": mock_username, "email": mock_email},
        None,
        {"id": mock_user_id, "username": mock_username, "email": mock_new_email}
    ]

    result = update_user_email(mock_user_id, mock_new_email)

    assert result["id"] == mock_user_id
    assert result["username"] == mock_username
    assert result["email"] == mock_new_email
    assert mock_cursor.execute.call_count == 3

@patch('models.user_model.Database.get_connection')
def test_delete_user(mock_get_connection):
    """Test if a user is deleted successfully."""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    mock_cursor.fetchone.side_effect = [
        {"id": mock_user_id, "username": mock_username, "email": mock_email},
        {"id": mock_user_id}
    ]

    result = delete_user(mock_user_id)

    assert result["id"] == mock_user_id
    assert mock_cursor.execute.call_count == 2

if __name__ == "__main__":
    pytest.main(["-v", __file__])





