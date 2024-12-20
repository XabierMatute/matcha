from models.chat_model import save_message, get_messages_between

def send_message(sender_id, receiver_id, message):
    """
    Envía un mensaje entre dos usuarios y lo guarda en la base de datos.
    
    Args:
        sender_id (int): ID del usuario que envía el mensaje.
        receiver_id (int): ID del usuario que recibe el mensaje.
        message (str): Contenido del mensaje.
    
    Returns:
        dict: Detalles del mensaje guardado.
    """
    if not sender_id or not receiver_id or not message or not isinstance(message, str) or not message.strip():
        raise ValueError("Sender ID, Receiver ID, and Message are required and Message must be a non-empty string.")

    try:
        saved_message = save_message(sender_id, receiver_id, message.strip())
        return {
            "success": True,
            "message": saved_message
        }
    except ValueError as ve:
        raise ValueError(f"Validation error: {str(ve)}")
    except Exception as e:
        raise Exception(f"An error occurred while sending the message: {str(e)}")


def fetch_chat_history(user1_id, user2_id):
    """
    Obtiene el historial de chat entre dos usuarios, ordenado por fecha.
    
    Args:
        user1_id (int): ID de uno de los usuarios.
        user2_id (int): ID del otro usuario.
    
    Returns:
        dict: Lista de mensajes intercambiados entre los usuarios.
    """
    if not user1_id or not user2_id:
        raise ValueError("Both User IDs are required.")

    try:
        messages = get_messages_between(user1_id, user2_id)
        return {
            "success": True,
            "messages": messages if messages else []
        }
    except ValueError as ve:
        raise ValueError(f"Validation error: {str(ve)}")
    except Exception as e:
        raise Exception(f"An error occurred while fetching the chat history: {str(e)}")





