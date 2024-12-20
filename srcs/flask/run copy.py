# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/12 16:58:27 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
from config import RunConfig as Config, SecretConfig, MailConfig, UserConfig
from flask import Flask
from flask_mail import Mail, Message
from models.database import Database

# Agregar el directorio raíz al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Importación de blueprints
from blueprints.users import users_bp
from blueprints.likes import likes_bp
from blueprints.notifications import notifications_bp
from blueprints.interests import interests_bp
from blueprints.chat import chat_bp
from blueprints.profile import profile_bp
from blueprints.pictures import pictures_bp
from blueprints.database_bp import database_bp

# Inicialización de la app Flask
app = Flask(__name__)
app.config.update(SecretConfig.config)

# Configuración del correo
mail = None
if MailConfig.ACTIVE:
    app.config.update(MailConfig.config)
    mail = Mail(app)
    from blueprints.mail import mail_bp
    app.register_blueprint(mail_bp)


@app.route('/mail')
def send_test_mail():
    """Ruta de prueba para enviar un correo."""
    try:
        msg = Message(
            subject="¡Hola desde Flask!",
            recipients=["tobovaf835@rustetic.com"],  # Lista de destinatarios
            body="Este es un correo de prueba enviado desde Flask.",
        )
        mail.send(msg)
        return "Correo enviado exitosamente"
    except Exception as e:
        return f"Error enviando correo: {e}"


# Registro de todos los blueprints
app.register_blueprint(users_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(interests_bp)
app.register_blueprint(database_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(pictures_bp)

# Registro de rutas de prueba si el modo TESTING está habilitado
if UserConfig.TESTING:
    from testing.user_testing1 import test_user_bp
    app.register_blueprint(test_user_bp)

# Ruta para listar todas las rutas registr







    
