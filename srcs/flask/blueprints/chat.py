from flask import Blueprint, request, jsonify
from manager.chat_manager import send_message, fetch_chat_history

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

def validate_ids(*ids):
    """
    Valida que los IDs sean enteros y no nulos.
    """
    for id in ids:
        if not id or not str(id).isdigit():
            raise ValueError("All IDs must be integers and non-empty")

@chat_bp.route('/', methods=['POST'])
def send_chat_message():
    """
    Envía un mensaje a otro usuario.
    """
    data = request.json
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')

    try:
        # Validar IDs
        validate_ids(sender_id, receiver_id)
        sender_id = int(sender_id)
        receiver_id = int(receiver_id)

        # Validar mensaje
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        # Enviar mensaje
        result = send_message(sender_id, receiver_id, message)
        return jsonify({"success": True, "message": result}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Internal Server Error: {str(e)}"}), 500

@chat_bp.route('/between', methods=['GET'])
def get_chat_messages():
    """
    Obtiene el historial de chat entre dos usuarios.
    """
    user1_id = request.args.get('user1_id')
    user2_id = request.args.get('user2_id')

    try:
        # Validar IDs
        validate_ids(user1_id, user2_id)
        user1_id = int(user1_id)
        user2_id = int(user2_id)

        # Obtener historial
        messages = fetch_chat_history(user1_id, user2_id)
        return jsonify({"success": True, "messages": messages}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Internal Server Error: {str(e)}"}), 500

@chat_bp.route('/real-time', methods=['GET'])
def real_time_chat_placeholder():
    """
    Placeholder para implementar chat en tiempo real con WebSocket.
    """
    return jsonify({"success": False, "info": "Real-time chat is not implemented yet"}), 501


