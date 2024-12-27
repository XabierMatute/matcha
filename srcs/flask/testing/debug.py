# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    debug.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/27 13:44:17 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/27 14:32:45 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app
from models.database import Database
from utils.list_routes import list_routes


debug_bp = Blueprint('debug', __name__, url_prefix='/debug')

@debug_bp.route('/hi', methods=['GET'])
def hi():
    return render_template('content.html', content="hi")

@debug_bp.route('/create_tables', methods=['GET'])
def create_tables():
    Database.create_tables()
    return render_template('content.html', content="Tables created.")

@debug_bp.route('/drop_tables', methods=['GET'])
def drop_tables():
    Database.drop_tables()
    return render_template('content.html', content="Tables dropped.")

@debug_bp.route("/list_routes")
def serve_list_routes():
    return render_template('content.html', content=list_routes(app))
