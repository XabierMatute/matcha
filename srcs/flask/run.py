# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 15:34:29 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



# Importa todos los blueprints de la carpeta blueprints
# from blueprints.users import users_bp
# from blueprints.likes import likes_bp
# from blueprints.notifications import notifications_bp
# from blueprints.interests import interests_bp
# from blueprints.chat import chat_bp
# from blueprints.profile import profile_bp
# from blueprints.pictures import pictures_bp


# from config import SecretConfig
# app.config.update(SecretConfig.config)

# from flask_mail import Mail, Message

# from flask import render_template

# @app.route('/example')
# def example():
#     return render_template('example.html')

# # Registra todos los blueprints
# app.register_blueprint(users_bp)
# app.register_blueprint(likes_bp)
# app.register_blueprint(notifications_bp)
# app.register_blueprint(interests_bp)
# app.register_blueprint(chat_bp)
# app.register_blueprint(profile_bp)
# app.register_blueprint(pictures_bp)

# from config import UserConfig
# if UserConfig.TESTING:
#     from testing.user_testing1 import test_user_bp
#     app.register_blueprint(test_user_bp)

# from config import CookieConfig
# if CookieConfig.TESTING:
#     from testing.cookie_testing import test_cookie_bp
#     app.register_blueprint(test_cookie_bp)

# app.register_blueprint(chat_bp)
# app.register_blueprint(profile_bp)
# app.register_blueprint(pictures_bp)

# from utils.list_routes import list_routes as list_routex

# @app.route("/")
# def list_routes():
#     return render_template('content.html', content=list_routex(app))

# from flask import redirect, url_for

# @app.route("/register")
# def register():
#     return redirect('users/register')

# @app.route("/login")
# def login():
#     if session.get('logged_in'):
#         return redirect('users/account/' + session.get('username'))
#     return redirect('users/login')

# @app.route("/logout")
# def logout():
#     return redirect('users/logout')

# from flask import session

# @app.route("/account")
# def account():
#     if session.get('logged_in'):
#         return redirect('users/account/' + session.get('username'))
#     else:
#         return redirect('users/login')

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

from config import DatabaseConfig, MailConfig
from config import RunConfig as Config
from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Create tables if necessary
if DatabaseConfig.ACTIVE:
    from models.database import Database
    Database.create_tables()

# Configurate the mail
mail = None
if MailConfig.ACTIVE:
    from flask_mail import Mail
    app.config.update(MailConfig.config)
    mail = Mail(app)

from blueprints.master import master_bp
app.register_blueprint(master_bp)

if __name__ == "__main__":
    # Run the application
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)







    
