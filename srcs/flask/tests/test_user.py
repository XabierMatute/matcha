import pytest
from unittest.mock import patch
from manager.user_manager import (
    register_user,
    authenticate_user,
    update_user_profile,
    delete_user_account,
    get_user_details
)

# Fixture para datos de usuario simulados
@pytest.fixture
def mock_user_data():
    return {
        "id": 1,
        "username": "test_user",
        "password_hash": "hashedpassword",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "is_verified": True
    }

# Fixture para datos del formulario
@pytest.fixture
def user_form_data():
    return {
        "username": "test_user",
        "email": "test@example.com",
        "password": "securepassword",
        "birthdate": "1990-01-01",
        "first_name": "Test",
        "last_name": "User"
    }

# Test para registrar un usuario exitosamente
@patch('manager.user_manager.create_user')
@patch('manager.user_manager.get_user_by_username', return_value=None)
def test_register_user(mock_get_user_by_username, mock_create_user, user_form_data):
    mock_create_user.return_value = {
        **user_form_data,
        "id": 1
    }

    result = register_user(user_form_data)

    assert result["username"] == "test_user"
    assert result["email"] == "test@example.com"
    mock_create_user.assert_called_once()

# Test para error al registrar un usuario existente
@patch('manager.user_manager.get_user_by_username')
def test_register_user_existing_username(mock_get_user_by_username, user_form_data):
    mock_get_user_by_username.return_value = {"id": 1, "username": "test_user"}

    with pytest.raises(ValueError) as exc_info:
        register_user(user_form_data)

    assert str(exc_info.value) == "Username or email already exists."

# Test para autenticar un usuario exitosamente
@patch('manager.user_manager.get_user_by_username')
@patch('werkzeug.security.check_password_hash', return_value=True)
def test_authenticate_user_success(mock_check_password_hash, mock_get_user_by_username, mock_user_data):
    mock_get_user_by_username.return_value = mock_user_data

    result = authenticate_user("test_user", "correctpassword")

    assert result["username"] == "test_user"
    assert mock_check_password_hash.called

# Test para error al autenticar con contraseña incorrecta
@patch('manager.user_manager.get_user_by_username')
@patch('werkzeug.security.check_password_hash', return_value=False)
def test_authenticate_user_invalid_password(mock_check_password_hash, mock_get_user_by_username, mock_user_data):
    mock_get_user_by_username.return_value = mock_user_data

    with pytest.raises(ValueError) as exc_info:
        authenticate_user("test_user", "wrongpassword")

    assert str(exc_info.value) == "Invalid username or password."

# Test para obtener detalles del usuario
@patch('manager.user_manager.get_user_by_id')
def test_get_user_details(mock_get_user_by_id, mock_user_data):
    mock_get_user_by_id.return_value = mock_user_data

    result = get_user_details(1)

    assert result["username"] == "test_user"
    assert result["email"] == "test@example.com"
    mock_get_user_by_id.assert_called_once_with(1)

# Test para error al obtener un usuario inexistente
@patch('manager.user_manager.get_user_by_id', return_value=None)
def test_get_user_details_not_found(mock_get_user_by_id):
    with pytest.raises(ValueError) as exc_info:
        get_user_details(99)

    assert str(exc_info.value) == "User not found."

# Test para actualizar el perfil de un usuario
@patch('manager.user_manager.update_user')
def test_update_user_profile(mock_update_user):
    mock_update_user.return_value = {
        "id": 1,
        "username": "updated_user",
        "email": "updated@example.com",
        "first_name": "Updated",
        "last_name": "User"
    }

    updates = {"username": "updated_user", "email": "updated@example.com"}
    result = update_user_profile(1, updates)

    assert result["username"] == "updated_user"
    assert result["email"] == "updated@example.com"
    mock_update_user.assert_called_once_with(1, **updates)

# Test para eliminar una cuenta de usuario
@patch('manager.user_manager.delete_user')
def test_delete_user_account(mock_delete_user):
    mock_delete_user.return_value = {"id": 1, "username": "test_user"}

    result = delete_user_account(1)

    assert result["id"] == 1
    assert result["username"] == "test_user"
    mock_delete_user.assert_called_once_with(1)

