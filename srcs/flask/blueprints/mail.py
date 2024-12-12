# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mail.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/10 17:16:36 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/11 19:24:47 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# from flask import Blueprint, current_app
# from flask_mail import Message



# mail_bp = Blueprint('mail', __name__, url_prefix='/mail')

# @mail_bp.route('/hi', methods=['GET'])
# def send_hi_mail():
#     return "Hi!"

# #send test mail
# @mail_bp.route('/test', methods=['GET'])
# def send_test_mail():
#     try:
#         msg = Message(
#             subject="¡Hola desde Flask!",
#             recipients=["tobovaf835@rustetic.com"],  # Lista de destinatarios
#             body="Este es un correo de prueba enviado desde Flask.",
#         )
#         mail = current_app.extensions['mail']
#         mail.send(msg)
#         return "Correo enviado exitosamente"
#     except Exception as e:
#         return f"Error enviando correo: {e}"

# @mail_bp.route('/test2', methods=['GET'])

from flask import Blueprint, current_app, request, jsonify
from flask_mail import Message

mail_bp = Blueprint('mail', __name__, url_prefix='/mail')

# Ruta para probar el envío de correos
@mail_bp.route('/test', methods=['GET'])
def send_test_mail():
    """Envía un correo de prueba a una dirección especificada."""
    try:
        msg = Message(
            subject="¡Hola desde Flask!",
            recipients=["tobovaf835@rustetic.com"],  # Dirección de prueba
            body="Este es un correo de prueba enviado desde Flask.",
        )
        mail = current_app.extensions['mail']
        mail.send(msg)
        return "Correo enviado exitosamente"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para enviar un correo de verificación
@mail_bp.route('/verification', methods=['POST'])
def send_verification_mail():
    """Envía un correo de verificación al usuario."""
    data = request.get_json()
    email = data.get('email')
    verification_code = data.get('verification_code')

    if not email or not verification_code:
        return jsonify({"error": "Faltan campos necesarios: email o verification_code"}), 400

    try:
        msg = Message(
            subject="Verifica tu cuenta",
            recipients=[email],
            body=f"Hola, por favor verifica tu cuenta usando este código: {verification_code}"
        )
        mail = current_app.extensions['mail']
        mail.send(msg)
        return jsonify({"message": "Correo de verificación enviado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para enviar notificaciones
@mail_bp.route('/notification', methods=['POST'])
def send_notification_mail():
    """Envía una notificación al usuario."""
    data = request.get_json()
    email = data.get('email')
    notification_message = data.get('message')

    if not email or not notification_message:
        return jsonify({"error": "Faltan campos necesarios: email o message"}), 400

    try:
        msg = Message(
            subject="Tienes una nueva notificación",
            recipients=[email],
            body=f"Hola, tienes una nueva notificación: {notification_message}"
        )
        mail = current_app.extensions['mail']
        mail.send(msg)
        return jsonify({"message": "Correo de notificación enviado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para manejar correos personalizados
@mail_bp.route('/custom', methods=['POST'])
def send_custom_mail():
    """Envía un correo con contenido personalizado."""
    data = request.get_json()
    email = data.get('email')
    subject = data.get('subject')
    body = data.get('body')

    if not email or not subject or not body:
        return jsonify({"error": "Faltan campos necesarios: email, subject o body"}), 400

    try:
        msg = Message(
            subject=subject,
            recipients=[email],
            body=body
        )
        mail = current_app.extensions['mail']
        mail.send(msg)
        return jsonify({"message": "Correo personalizado enviado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Nota: Asegúrate de configurar Flask-Mail correctamente en tu app principal.
# Ejemplo de configuración:
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'
# app.config['MAIL_PASSWORD'] = 'tu_contraseña'
# app.extensions['mail'] = Mail(app)
