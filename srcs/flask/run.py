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

from config import RunConfig as Config
from flask import Flask

# Importa todos los blueprints de la carpeta blueprints
from blueprints.users import users_bp
from blueprints.likes import likes_bp
from blueprints.notifications import notifications_bp
from blueprints.interests import interests_bp
from blueprints.chat import chat_bp
from blueprints.profile import profile_bp
from blueprints.pictures import pictures_bp
from models.database import Database

app = Flask(__name__)

from config import SecretConfig
app.config.update(SecretConfig.config)

from flask_mail import Mail, Message

# Configuración del correo
from config import MailConfig
mail = None
if MailConfig.ACTIVE:
    app.config.update(MailConfig.config)
    mail = Mail(app)
    from blueprints.mail import mail_bp
    app.register_blueprint(mail_bp)

@app.route('/mail')
def send_test_mail():
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

# Registra todos los blueprints
app.register_blueprint(users_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(interests_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(pictures_bp)

from config import UserConfig
if UserConfig.TESTING:
    from testing.user_testing1 import test_user_bp
    app.register_blueprint(test_user_bp)

from utils.list_routes import list_routes as list_routex

@app.route("/")
def helloworld():
    return list_routex(app)

if __name__ == "__main__":
    # Crea las tablas si es necesario
    Database.create_tables()
    # Ejecuta la aplicación
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)







    
