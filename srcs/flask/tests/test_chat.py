import pytest
from unittest.mock import patch, Mock
from manager.chat_manager import send_message, fetch_chat_history

# Prueba para enviar mensaje
@patch('manager.chat_manager.save_message')
def test_send_message(mock_save_message):
    mock_message = Mock(
        id=1,
        sender_id=101,
        receiver_id=202,
        message="Hello!",
        timestamp="2024-01-01T10:00:00"
    )
    mock_save_message.return_value = mock_message

    result = send_message(101, 202, "Hello!")

    assert result["id"] == 1
    assert result["sender_id"] == 101
    assert result["receiver_id"] == 202
    assert result["message"] == "Hello!"
    assert result["timestamp"] == "2024-01-01T10:00:00"
    mock_save_message.assert_called_once_with(101, 202, "Hello!")

# Prueba para obtener historial de chat
@patch('manager.chat_manager.get_messages_between')
def test_fetch_chat_history(mock_get_messages_between):
    mock_messages = [
        Mock(
            id=1,
            sender_id=101,
            receiver_id=202,
            message="Hello!",
            timestamp="2024-01-01T10:00:00"
        ),
        Mock(
            id=2,
            sender_id=202,
            receiver_id=101,
            message="Hi!",
            timestamp="2024-01-01T10:01:00"
        )
    ]
    mock_get_messages_between.return_value = mock_messages

    result = fetch_chat_history(101, 202)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["message"] == "Hello!"
    assert result[1]["id"] == 2
    assert result[1]["message"] == "Hi!"
    mock_get_messages_between.assert_called_once_with(101, 202)

# Prueba para historial vacío
@patch('manager.chat_manager.get_messages_between')
def test_fetch_chat_history_empty(mock_get_messages_between):
    mock_get_messages_between.return_value = []

    result = fetch_chat_history(101, 202)

    assert result == []
    mock_get_messages_between.assert_called_once_with(101, 202)

# Prueba para error en base de datos
@patch('manager.chat_manager.get_messages_between')
def test_fetch_chat_history_error(mock_get_messages_between):
    mock_get_messages_between.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        fetch_chat_history(101, 202)

# Pruebas para errores de send_message
def test_send_message_invalid_input():
    with pytest.raises(ValueError, match="Invalid sender, receiver, or message"):
        send_message(None, 202, "Hello!")
    with pytest.raises(ValueError, match="Invalid sender, receiver, or message"):
        send_message(101, None, "Hello!")
    with pytest.raises(ValueError, match="Invalid sender, receiver, or message"):
        send_message(101, 202, None)

# Prueba para errores de fetch_chat_history
def test_fetch_chat_history_invalid_input():
    with pytest.raises(ValueError, match="Invalid user IDs"):
        fetch_chat_history(None, 202)
    with pytest.raises(ValueError, match="Invalid user IDs"):
        fetch_chat_history(101, None)


