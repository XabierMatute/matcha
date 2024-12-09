from flask import Blueprint, request, jsonify
from manager.chat_manager import send_message, fetch_chat_history

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

def success_response(data=None, message="Operation successful"):
    return {"success": True, "message": message, "data": data}

def error_response(message="Operation failed"):
    return {"success": False, "message": message}

# Ruta para enviar un mensaje
@chat_bp.route("/send", methods=["POST"])
def send_chat_message():
    """
    Endpoint para enviar un mensaje entre dos usuarios.
    """
    data = request.get_json()
    try:
        if not data:
            return jsonify(error_response("Invalid or missing JSON payload.")), 400
        
        # Validar datos requeridos
        sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")
        message = data.get("message")
        
        if not sender_id or not receiver_id or not message:
            return jsonify(error_response("Sender ID, Receiver ID, and Message are required.")), 400
        
        # Enviar el mensaje usando el manager
        result = send_message(sender_id, receiver_id, message)
        return jsonify(success_response(data=result["message"], message="Message sent successfully.")), 201
    except ValueError as ve:
        return jsonify(error_response(str(ve))), 400
    except Exception as e:
        return jsonify(error_response("An unexpected error occurred.")), 500

# Ruta para obtener el historial de chat
@chat_bp.route("/history", methods=["GET"])
def get_chat_history():
    """
    Endpoint para obtener el historial de chat entre dos usuarios.
    """
    sender_id = request.args.get("user1_id", type=int)
    receiver_id = request.args.get("user2_id", type=int)
    try:
        if not sender_id or not receiver_id:
            return jsonify(error_response("Both User IDs are required.")), 400
        
        # Obtener historial de mensajes usando el manager
        result = fetch_chat_history(sender_id, receiver_id)
        return jsonify(success_response(data=result["messages"], message="Chat history fetched successfully.")), 200
    except ValueError as ve:
        return jsonify(error_response(str(ve))), 400
    except Exception as e:
        return jsonify(error_response("An unexpected error occurred.")), 500



