import pytest
from run import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configura la app en modo testing y crea un cliente de prueba."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'  # Necesario para la sesión
    with app.test_client() as client:
        with app.app_context():
            yield client

# Test para listar todos los intereses
@patch('blueprints.interests.fetch_all_interests')
def test_list_interests(mock_fetch_all_interests, client):
    mock_fetch_all_interests.return_value = [{"id": 1, "tag": "Music"}, {"id": 2, "tag": "Sports"}]

    response = client.get('/interests/')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Interests fetched successfully.",
        "data": [{"id": 1, "tag": "Music"}, {"id": 2, "tag": "Sports"}]
    }
    mock_fetch_all_interests.assert_called_once()

# Test para obtener un interés por ID
@patch('blueprints.interests.fetch_interest_by_id')
def test_get_interest_success(mock_fetch_interest_by_id, client):
    mock_fetch_interest_by_id.return_value = {"id": 1, "tag": "Music"}

    response = client.get('/interests/1')
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Interest fetched successfully.",
        "data": {"id": 1, "tag": "Music"}
    }
    mock_fetch_interest_by_id.assert_called_once_with(1)

# Test para crear un nuevo interés
@patch('blueprints.interests.add_new_interest')
def test_create_interest_success(mock_add_new_interest, client):
    mock_add_new_interest.return_value = {"id": 3, "tag": "Travel"}

    response = client.post('/interests/add', json={"tag": "Travel"})
    assert response.status_code == 201
    assert response.get_json() == {
        "success": True,
        "message": "Interest created successfully.",
        "data": {"id": 3, "tag": "Travel"}
    }
    mock_add_new_interest.assert_called_once_with("Travel")

# Test para agregar múltiples intereses
@patch('blueprints.interests.bulk_add_interests')
def test_add_multiple_interests(mock_bulk_add_interests, client):
    mock_bulk_add_interests.return_value = [{"id": 4, "tag": "Cooking"}, {"id": 5, "tag": "Reading"}]

    response = client.post('/interests/add-batch', json={"tags": ["Cooking", "Reading"]})
    assert response.status_code == 201
    assert response.get_json() == {
        "success": True,
        "message": "Interests added successfully.",
        "data": [{"id": 4, "tag": "Cooking"}, {"id": 5, "tag": "Reading"}]
    }
    mock_bulk_add_interests.assert_called_once_with(["Cooking", "Reading"])

# Test para eliminar múltiples intereses
@patch('blueprints.interests.bulk_remove_interests')
def test_remove_interests(mock_bulk_remove_interests, client):
    mock_bulk_remove_interests.return_value = {"deleted_ids": [1, 2]}

    response = client.delete('/interests/remove', json={"interest_ids": [1, 2]})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "Interests removed successfully.",
        "data": {"deleted_ids": [1, 2]}
    }
    mock_bulk_remove_interests.assert_called_once_with([1, 2])

# Test para actualizar los intereses de un usuario
@patch('blueprints.interests.update_user_interests_list')
def test_update_user_interests(mock_update_user_interests_list, client):
    mock_update_user_interests_list.return_value = {"success": True, "message": "User interests updated successfully."}

    with client.session_transaction() as session:
        session['user_id'] = 1  # Simula un usuario logueado

    response = client.post('/interests/user/update', json={"interests": ["Music", "Travel"]})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "message": "User interests updated successfully.",
        "data": {"success": True, "message": "User interests updated successfully."}
    }
    mock_update_user_interests_list.assert_called_once_with(1, ["Music", "Travel"])

# Test para error cuando el usuario no está logueado
def test_update_user_interests_not_logged_in(client):
    response = client.post('/interests/user/update', json={"interests": ["Music", "Travel"]})
    assert response.status_code == 401
    assert response.get_json() == {
        "success": False,
        "message": "User not logged in."
    }

