# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 10:53:18 by xmatute-         ###   ########.fr        #
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

from flask import render_template

@app.route('/example')
def example():
    return render_template('example.html')




# Registra todos los blueprints
app.register_blueprint(users_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(interests_bp)
# app.register_blueprint(chat_bp)
# app.register_blueprint(profile_bp)
# app.register_blueprint(pictures_bp)

from config import UserConfig
if UserConfig.TESTING:
    from testing.user_testing1 import test_user_bp
    app.register_blueprint(test_user_bp)

from config import CookieConfig
if CookieConfig.TESTING:
    from testing.cookie_testing import test_cookie_bp
    app.register_blueprint(test_cookie_bp)

# app.register_blueprint(chat_bp)
# app.register_blueprint(profile_bp)
# app.register_blueprint(pictures_bp)

from utils.list_routes import list_routes as list_routex

@app.route("/")
def list_routes():
    return render_template('content.html', content=list_routex(app))

# from flask import redirect, url_for

# @app.route("/register")
# def register():
#     return redirect('users/register')

# @app.route("/login")
# def login():
#     return redirect('users/login')

if __name__ == "__main__":
    # Create tables if necessary
    Database.create_tables()
    # Run the application
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)





    
