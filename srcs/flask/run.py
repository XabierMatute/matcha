# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/21 14:37:06 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging
from config import DatabaseConfig, MailConfig, SecretConfig
from config import RunConfig as Config
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the Flask application
app = Flask(__name__)
logger.info("Flask application created.")

# Create tables if necessary
if DatabaseConfig.ACTIVE:
    from models.database import Database
    Database.create_tables()
    logger.info("Database tables created.")

# Configurate the application
if SecretConfig.ACTIVE:
    app.config.update(SecretConfig.config)
    logger.info("Application configuration updated with SecretConfig.")

# Configurate the mail
mail = None
if MailConfig.ACTIVE:
    from flask_mail import Mail
    app.config.update(MailConfig.config)
    mail = Mail(app)
    logger.info("Mail configuration updated and Mail instance created.")

# Register the blueprints
from blueprints.register import register_to
register_to(app)
logger.info("Blueprints registered to the application.")

if __name__ == "__main__":
    # Run the application
    logger.info(f"Starting the application on {Config.HOST}:{Config.PORT} with debug={Config.DEBUG}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)