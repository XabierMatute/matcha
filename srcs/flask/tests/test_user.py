import pytest
from run import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configura la app en modo testing y crea un cliente de prueba."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'
    with app.test_client() as client:
        yield client

# Test para obtener detalles de un usuario por ID
@patch('blueprints.users.get_user_details')
def test_get_user_details_by_id(mock_get_user_details, client):
    mock_get_user_details.return_value = {"id": 1, "username": "testuser", "email": "test@example.com"}

    response = client.get('/users/details?user_id=1')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "User details fetched successfully.",
        "data": {"id": 1, "username": "testuser", "email": "test@example.com"}
    }
    mock_get_user_details.assert_called_once_with(user_id=1, require_verified=True)

# Test para obtener detalles de un usuario por username
@patch('blueprints.users.get_user_details')
def test_get_user_details_by_username(mock_get_user_details, client):
    mock_get_user_details.return_value = {"id": 2, "username": "john_doe", "email": "john@example.com"}

    response = client.get('/users/details?username=john_doe')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "User details fetched successfully.",
        "data": {"id": 2, "username": "john_doe", "email": "john@example.com"}
    }
    mock_get_user_details.assert_called_once_with(username="john_doe", require_verified=True)

# Test para registrar un nuevo usuario
@patch('blueprints.users.register_user')
def test_register_user(mock_register_user, client):
    mock_register_user.return_value = {"id": 3, "username": "newuser", "email": "new@example.com"}

    response = client.post('/users/register', json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert response.get_json() == {
        "success": True,
        "message": "User registered successfully.",
        "data": {"id": 3, "username": "newuser", "email": "new@example.com"}
    }
    mock_register_user.assert_called_once_with({
        "username": "newuser",
        "email": "new@example.com",
        "password": "securepassword"
    })

# Test para actualizar un usuario
@patch('blueprints.users.update_user_profile')
def test_update_user(mock_update_user, client):
    mock_update_user.return_value = {"id": 1, "username": "updateduser", "email": "updated@example.com"}

    response = client.put('/users/update/1', json={
        "username": "updateduser",
        "email": "updated@example.com"
    })
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "User updated successfully.",
        "data": {"id": 1, "username": "updateduser", "email": "updated@example.com"}
    }
    mock_update_user.assert_called_once_with(1, {
        "username": "updateduser",
        "email": "updated@example.com"
    })

# Test para eliminar un usuario
@patch('blueprints.users.delete_user_account')
def test_delete_user(mock_delete_user, client):
    mock_delete_user.return_value = {"id": 1}

    response = client.delete('/users/delete/1')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "User deleted successfully.",
        "data": {"id": 1}
    }
    mock_delete_user.assert_called_once_with(1)

# Test para verificar un usuario por email
@patch('blueprints.users.verify_user')
def test_verify_user(mock_verify_user, client):
    mock_verify_user.return_value = {"id": 1, "username": "verifieduser", "email": "verified@example.com"}

    response = client.post('/users/verify', json={"email": "verified@example.com"})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "User verified successfully.",
        "data": {"id": 1, "username": "verifieduser", "email": "verified@example.com"}
    }
    mock_verify_user.assert_called_once_with("verified@example.com")

# Test para error si no se proporciona email en verificación
def test_verify_user_missing_email(client):
    response = client.post('/users/verify', json={})
    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "message": "Email is required."
    }

# Test para error si no se proporciona ni ID ni username
def test_get_user_details_missing_params(client):
    response = client.get('/users/details')
    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "message": "Either 'user_id' or 'username' must be provided."
    }

# Test para obtener detalles de un usuario no verificado
@patch('blueprints.users.get_user_details')
def test_get_user_details_unverified(mock_get_user_details, client):
    mock_get_user_details.side_effect = ValueError("User 'unverified_user' is not verified.")

    response = client.get('/users/details?username=unverified_user')
    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "message": "User 'unverified_user' is not verified."
    }
    mock_get_user_details.assert_called_once_with(username="unverified_user", require_verified=True)

# Test para obtener detalles de un usuario verificado
@patch('blueprints.users.get_user_details')
def test_get_user_details_verified(mock_get_user_details, client):
    mock_get_user_details.return_value = {"id": 2, "username": "verified_user", "email": "verified@example.com"}

    response = client.get('/users/details?username=verified_user')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "User details fetched successfully.",
        "data": {"id": 2, "username": "verified_user", "email": "verified@example.com"}
    }
    mock_get_user_details.assert_called_once_with(username="verified_user", require_verified=True)






