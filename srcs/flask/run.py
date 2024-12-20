# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 17:45:12 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from config import DatabaseConfig, MailConfig, SecretConfig
from config import RunConfig as Config
from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Create tables if necessary
if DatabaseConfig.ACTIVE:
    from models.database import Database
    Database.create_tables()

# Configurate the application
if SecretConfig.ACTIVE:
    app.config.update(SecretConfig.config)

# Configurate the mail
mail = None
if MailConfig.ACTIVE:
    from flask_mail import Mail
    app.config.update(MailConfig.config)
    mail = Mail(app)

# Register the blueprints
from blueprints.register import register_to
register_to(app)

if __name__ == "__main__":
    # Run the application
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)







    
