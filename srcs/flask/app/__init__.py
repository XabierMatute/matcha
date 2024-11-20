# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:26:06 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 15:19:00 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#APP
from flask import Flask
from app.blueprints import main_bp

def create_app():
    app = Flask(__name__)

    # Aqui igual van cosas de configuración
    app.register_blueprint(main_bp)

    return app
