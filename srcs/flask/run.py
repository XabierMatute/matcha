# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/27 12:59:37 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging
from config import DatabaseConfig, MailConfig, SecretConfig
from config import RunConfig as Config
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask application
try:
    logger.debug(f"Creating Flask application: {__name__}")
    app = Flask(__name__)
    logger.info("Flask application created successfully.")
except Exception as e:
    logger.exception(f"An error occurred while creating the Flask application: {e}")

# Create tables if necessary
if DatabaseConfig.ACTIVE:
    logger.debug("Creating database tables ")
    from models.database import Database
    Database.create_tables()
    logger.info("Database tables created.")

# Configurate the application
if SecretConfig.ACTIVE:
    logger.debug("Configuring application...")
    app.config.update(SecretConfig.config)
    logger.info("Application configuration updated with SecretConfig.")

# Configurate the mail
mail = None
if MailConfig.ACTIVE:
    logger.debug("Configuring mail...")
    from flask_mail import Mail
    app.config.update(MailConfig.config)
    mail = Mail(app)
    logger.info("Mail configuration updated and Mail instance created.")

# Register the blueprints
logger.debug("Registering blueprints...")
from blueprints.register import register_to
register_to(app)
logger.info("Blueprints registered to the application.")

if __name__ == "__main__":
    # Run the application
    logger.info(f"Starting the application on {Config.HOST}:{Config.PORT} with debug={Config.DEBUG}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
    logger.info("Application stopped.")