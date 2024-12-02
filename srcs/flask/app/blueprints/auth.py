from flask import Blueprint, jsonify
from flask_mail import Message
from app import mail  # Importar la instancia de Flask-Mail

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/send-test-email', methods=['GET'])
def send_test_email():
    """Prueba para enviar un correo"""
    try:
        msg = Message(
            subject="Correo de prueba desde Matcha",
            recipients=["beatriz.lamiquizdauden@gmail.com "],  # Cambiar al correo de destino
            body="¡Hola! Este es un correo de prueba enviado desde Flask-Mail."
        )
        mail.send(msg)
        return jsonify({"message": "Correo enviado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
