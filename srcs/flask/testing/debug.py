# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    debug.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/27 13:44:17 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/27 18:48:12 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging
from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app
from models.database import Database
from utils.list_routes import list_routes
from utils.render_content import render_content
from faker import Faker
from flask import jsonify

# Configurar el logger
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear una instancia de Faker
fake = Faker()
logging.getLogger('faker').setLevel(logging.WARNING)

debug_bp = Blueprint('debug', __name__, url_prefix='/debug')

@debug_bp.route('/hi', methods=['GET'])
def hi():
    logger.info("Accessed /hi route")
    return render_content("Hi there!")

@debug_bp.route('/create_tables', methods=['GET'])
def create_tables():
    logger.info("Accessed /create_tables route")
    Database.create_tables()
    logger.info("Tables created successfully")
    return render_content("Tables created.")

@debug_bp.route('/drop_tables', methods=['GET'])
def drop_tables():
    logger.info("Accessed /drop_tables route")
    Database.drop_tables()
    logger.info("Tables dropped successfully")
    return render_content("Tables dropped.")

@debug_bp.route("/list_routes")
def serve_list_routes():
    logger.info("Accessed /list_routes route")
    return render_content(list_routes(app))

@debug_bp.route('/generate_register_data', methods=['GET'])
def generate_example_data():
    example_data = {
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password()
    }
    return jsonify(example_data)

