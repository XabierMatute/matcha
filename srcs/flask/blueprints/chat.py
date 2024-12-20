from flask import Blueprint, request, jsonify
from manager.chat_manager import send_message, fetch_chat_history
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

def success_response(data=None, message="Operation successful"):
    """Genera una respuesta de éxito consistente."""
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed", status_code=400, details=None):
    """Genera una respuesta de error consistente."""
    response = {"success": False, "message": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code

@chat_bp.route("/send", methods=["POST"])
def send_chat_message():
    """
    Endpoint para enviar un mensaje entre dos usuarios.
    
    JSON Payload:
        - sender_id (int): ID del usuario que envía el mensaje.
        - receiver_id (int): ID del usuario que recibe el mensaje.
        - message (str): Contenido del mensaje.

    Returns:
        JSON: Mensaje enviado correctamente o error.
    """
    data = request.get_json()
    try:
        if not data:
            raise ValueError("Invalid or missing JSON payload.")

        # Validar datos requeridos
        sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")
        message = data.get("message")

        if not sender_id or not receiver_id or not message:
            raise ValueError("Sender ID, Receiver ID, and Message are required.")

        # Enviar el mensaje usando el manager
        result = send_message(sender_id, receiver_id, message)
        return jsonify(success_response(data=result["message"], message="Message sent successfully.")), 201
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return error_response("An unexpected error occurred.", 500, details=str(e))

@chat_bp.route("/history", methods=["GET"])
def get_chat_history():
    """
    Endpoint para obtener el historial de chat entre dos usuarios.

    Query Params:
        - user1_id (int): ID de uno de los usuarios.
        - user2_id (int): ID del otro usuario.

    Returns:
        JSON: Historial de mensajes entre los dos usuarios.
    """
    sender_id = request.args.get("user1_id", type=int)
    receiver_id = request.args.get("user2_id", type=int)
    try:
        if not sender_id or not receiver_id:
            raise ValueError("Both User IDs are required.")

        # Obtener historial de mensajes usando el manager
        result = fetch_chat_history(sender_id, receiver_id)
        return jsonify(success_response(data=result["messages"], message="Chat history fetched successfully.")), 200
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return error_response(str(ve), 400)
    except Exception as e:
        logger.error(f"Failed to fetch chat history: {e}")
        return error_response("An unexpected error occurred.", 500, details=str(e))



