from flask import Blueprint, request, jsonify
from models.chat_model import create_message, get_messages_between_users

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/', methods=['POST'])
def send_chat_message():
    """Envía un mensaje a otro usuario."""
    sender_id = request.json.get('sender_id')
    receiver_id = request.json.get('receiver_id')
    message = request.json.get('message')
    
    if not sender_id or not receiver_id or not message:
        return jsonify({"error": "Sender ID, Receiver ID, and message are required"}), 400

    try:
        result = create_message(sender_id, receiver_id, message)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bp.route('/between', methods=['GET'])
def get_chat_messages():
    """Obtiene los mensajes entre dos usuarios."""
    user1_id = request.args.get('user1_id')
    user2_id = request.args.get('user2_id')
    
    if not user1_id or not user2_id:
        return jsonify({"error": "Both user1_id and user2_id are required"}), 400

    try:
        messages = get_messages_between_users(user1_id, user2_id)
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


