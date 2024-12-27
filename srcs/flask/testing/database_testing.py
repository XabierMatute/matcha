# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    database_testing.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/27 13:00:32 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/27 13:03:43 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint, request, jsonify
from models.database import Database

test_database_bp = Blueprint('test_database_bp', __name__, url_prefix='/test_database')

@test_database_bp.route('/hi', methods=['GET'])
def hi():
    return jsonify({"message": "Hi!"})

@test_database_bp.route('/create_tables', methods=['GET'])
def create_tables():
    Database.create_tables()
    return jsonify({"message": "Tables created."})

@test_database_bp.route('/drop_tables', methods=['GET'])
def drop_tables():
    Database.drop_tables()
    return jsonify({"message": "Tables dropped."})