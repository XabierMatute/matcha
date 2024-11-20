# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 12:13:05 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 15:19:16 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint

main_bp = Blueprint('main', __name__)

# from routes import routes_bp
# main_bp.register_blueprint(routes_bp)

from app.blueprints.root import bp as root_bp
main_bp.register_blueprint(root_bp)

from app.blueprints.hello import bp as hello_bp
main_bp.register_blueprint(hello_bp)

from app.blueprints.fake_users import bp as fake_users_bp
main_bp.register_blueprint(fake_users_bp)